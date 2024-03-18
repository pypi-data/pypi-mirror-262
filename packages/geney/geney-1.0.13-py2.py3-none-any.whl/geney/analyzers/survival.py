import pandas as pd
from lifelines import KaplanMeierFitter
from lifelines.statistics import logrank_test
from geney import unload_pickle, unload_json, access_conservation_data
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Rectangle
from oncosplice.oncosplice import transform_conservation_vector
from geney import contains
pd.set_option('display.max_columns', None)

# CLINICAL_DATA_FILE = Path('/tamir2/nicolaslynn/data/TCGA/cancer_reports/new_df_p_proc.pkl')
# CLINICAL_DATA_FILE = Path('/tamir2/yoramzar/Projects/Cancer_mut/Explore_data/reports/df_p_all.pkl')
# CANCER_DATA_PATH = Path('/tamir2/cancer_proj/gdc_db/data/filtered_feb_2021/AllGenes')
# MAF_FILE_NAME = 'GeneMutTble.txt'
# CASE_TRACKER = pd.read_csv('/tamir2/nicolaslynn/projects/TCGAParsed/case2proj.csv', index_col=0)
# PROJ_COUNTS = CASE_TRACKER.proj.value_counts()
# OKGP_DATA_FILE = Path('/tamir2/nicolaslynn/projects/1000GenomesProjMutations/parsed_1kgp_mutations_in_target_genes.csv')
# MUTATION_FREQ_DF = pd.read_csv(OKGP_DATA_FILE, index_col=0)
# PROTEIN_ANNOTATIONS = pd.read_csv('/tamir2/nicolaslynn/data/BioMart/protein_annotations.csv').rename(columns={'Interpro start': 'start', 'Interpro end': 'end', 'Interpro Short Description': 'name'})[['Gene stable ID', 'Transcript stable ID', 'start', 'end', 'name']]
# PROTEIN_ANNOTATIONS['length'] = PROTEIN_ANNOTATIONS.apply(lambda row: abs(row.start - row.end), axis=1)

def prepare_clinical_data():
    df = unload_pickle(CLINICAL_DATA_FILE)
    df.rename(columns={'patient_uuid': 'case_id'}, inplace=True)
    cols = list(df.columns)
    cols_days_to_followup = [col for col in cols if 'days_to_followup' in col] + [col for col in cols if 'days_to_last_followup' in col]
    cols_days_to_know_alive = [col for col in cols if 'days_to_know_alive' in col] + [col for col in cols if 'days_to_last_known_alive' in col]
    cols_days_to_death = [col for col in cols if 'days_to_death' in col]
    cols_duration = cols_days_to_followup + cols_days_to_know_alive + cols_days_to_death
    col_vital_status = 'days_to_death'
    event_col_label = 'event'
    duration_col_label = 'duration'
    df.insert(1, event_col_label, df.apply(lambda x: int(not np.isnan(x[col_vital_status])), axis=1))
    df.insert(1, duration_col_label, df.apply(lambda x: max([x[col] for col in cols_duration if not np.isnan(x[col])], default=-1), axis=1))
    df[duration_col_label] /= 365
    df = df.query(f"{duration_col_label}>=0.0")
    return df

def prepare_gene_sets():
    # gene_annotations_file = Path('/tamir2/nicolaslynn/data/COSMIC/cancer_gene_roles.csv')
    # GENE_DF = pd.read_csv(gene_annotations_file, index_col=0)
    # all_oncogenes = GENE_DF[GENE_DF.OG==True].index.tolist()
    # all_oncogenes = list(set(all_oncogenes))
    return [], [], []

CLIN_DF = prepare_clinical_data()
TSGS, ONCOGENES, CANCER_GENES = prepare_gene_sets()


def generate_survival_quantitative(affected_df, nonaffected_df):
    if affected_df.empty or nonaffected_df.empty:
        return np.nan, np.nan, np.nan
    results = logrank_test(affected_df['duration'], nonaffected_df['duration'],
                           event_observed_A=affected_df['event'],
                           event_observed_B=nonaffected_df['event'])
    p_value = results.p_value
    kmf = KaplanMeierFitter()
    kmf.fit(affected_df['duration'], affected_df['event'], label=f'With Epistasis ({len(affected_df)})')
    times, surv_probs = kmf.survival_function_.index.values, kmf.survival_function_.values.flatten()
    auc1 = np.trapz(surv_probs, times)
    kmf.fit(nonaffected_df['duration'], nonaffected_df['event'], label=f'Without Epistasis ({len(nonaffected_df)})')
    times, surv_probs = kmf.survival_function_.index.values, kmf.survival_function_.values.flatten()
    auc2 = np.trapz(surv_probs, times)
    return p_value, auc1, auc2

def generate_survival_pvalue(affected_df, unaffected_df):
    results = logrank_test(affected_df['duration'], unaffected_df['duration'],
                           event_observed_A=affected_df['event'],
                           event_observed_B=unaffected_df['event'])

    p_value = results.p_value
    kmf = KaplanMeierFitter()
    # Fit data
    kmf.fit(affected_df['duration'], affected_df['event'], label=f'Without Epistasis ({len(affected_df)})')
    ax = kmf.plot()

    kmf.fit(unaffected_df['duration'], unaffected_df['event'], label=f'With Epistasis ({len(unaffected_df)})')
    kmf.plot(ax=ax)
    plt.text(5, 0.95, f'pval: {p_value:.3e}')
    plt.show()
    return p_value

def get_project_prevalence(cases_affected):
    ca = [c for c in cases_affected if c in CASE_TRACKER.index]
    prevalences = CASE_TRACKER.loc[ca].proj.value_counts() / PROJ_COUNTS
    prevalences.fillna(0, inplace=True)
    prevalences = prevalences[[i for i in prevalences.index if 'TCGA' in i]]
    prevalences.index = [s.replace('TCGA', 'prev') for s in prevalences.index]
    return prevalences

def get_project_counts(cases_affected):
    ca = [c for c in cases_affected if c in CASE_TRACKER.index]
    prevalences = CASE_TRACKER.loc[ca].proj.value_counts()
    prevalences = prevalences[[i for i in prevalences.index if 'TCGA' in i]]
    prevalences.index = [s.replace('TCGA_', '') for s in prevalences.index]
    return prevalences

def get_event_consequence(df):
    assert df.Transcript_ID.nunique() == 1, 'Too many transcripts to return a single consequenc.'
    return df.iloc[0].Consequence

def get_dbSNP_id(df):
    return df.iloc[0].dbSNP_RS

def load_variant_file(gene):
    df = pd.read_csv(CANCER_DATA_PATH / gene / MAF_FILE_NAME, low_memory=False)
    df['mut_id'] = df.apply(lambda row: f"{row.Gene_name}:{row.Chromosome.replace('chr', '')}:{row.Start_Position}:{row.Reference_Allele}:{row.Tumor_Seq_Allele2}", axis=1)
    return df

def find_event_data(event):
    df = load_variant_file(event.gene)
    if df.empty:
        return None

    df = df.query \
        ('Chromosome == @event.chromosome & Start_Position == @event.start & Reference_Allele == @event.ref & Tumor_Seq_Allele2 == @event.alt')

    if df.empty:
        return None

    if event.transcript_id is not None:
        df = df[df.Transcript_ID == event.transcript_id]
    df['mut_id'] = event.event_id
    return df


class GEvent:
    def __init__(self, event_id, transcript_id=None):
        self.gene, self.chromosome, self.start, self.ref, self.alt = event_id.split(':')
        self.transcript_id = transcript_id
        self.chromosome = f'chr{self.chromosome}'
        self.start = int(self.start)
        self.event_id = event_id



def get_okgp_mutation_frequency(mut_id):
    if mut_id in MUTATION_FREQ_DF.index:
        return MUTATION_FREQ_DF.loc[mut_id].cases_affected
    else:
        return 0

def get_df_filter_info(df):
    filter_artifact_values: list = ["oxog", "bPcr", "bSeq"]
    MuTect2_filters: list = ['Germline risk', 't_lod_fstar', 'alt_allele_in_normal', 'panel_of_normals', 'clustered_events',
                             'str_contraction', 'multi_event_alt_allele_in_normal', 'homologous_mapping_event', 'triallelic_site']
    filter_col_name: str = "FILTER_info"  # column name to add to the dataframe
    filter_info_list: list = []
    f_cnr_info = {}

    for j, (prj, df_prj) in enumerate(df.groupby('Proj_name')):
        filter_vals = list(df_prj['FILTER'])
        num_pass, num_artifacts, num_mutect2_filters = 0, 0, 0
        for filter_val in filter_vals:
            num_pass += ('PASS' in filter_val)
            num_artifacts += any([x in filter_val for x in filter_artifact_values])
            num_mutect2_filters += any([x in filter_val for x in MuTect2_filters])
        num_rest = max(0, (len(filter_vals) - num_pass - num_artifacts - num_mutect2_filters))
        f_cnr_info[str(prj)[5:]] = (num_pass, num_mutect2_filters, num_artifacts, num_rest)
    return f_cnr_info

def yoram_mutid(row):
    return f'{row.Gene_name}:{row.Chromosome}:{row.Consequence}:{row.Start_Position}:{row.Reference_Allele}:{row.Tumor_Seq_Allele2}'


def annotate_level_two(mut_id, tid):
    mut = GEvent(mut_id, tid)
    df = find_event_data(mut)

    if df.empty or df is None:
        return None

    patients_affected = df.cases_affected.unique().tolist()
    p_val, auc_a, auc_n = generate_survival_quantitative(CLIN_DF[CLIN_DF.case_id.isin(patients_affected)], CLIN_DF[~CLIN_DF.case_id.isin(patients_affected)])
    project_prevalences = get_project_prevalence(patients_affected)
    prev_dict = project_prevalences.to_dict().sort()
    project_counts = get_project_counts(patients_affected)

    s = pd.Series({
        'mut_id': mut_id,
        'yoram_mut_id': yoram_mutid(df.iloc[0]),
        'transcript_id': tid,
        'affected_cases': len(patients_affected),
        'dbSNP_id': get_dbSNP_id(df),
        'consequence': get_event_consequence(df),
        'survival_p_value': p_val,
        'auc_affected': auc_a,
        'auc_nonaffected': auc_n,
        'TSG': contains(TSGS, mut.gene),
        'oncogene': contains(ONCOGENES, mut.gene),
        'cases_1kgp': get_okgp_mutation_frequency(mut.event_id),
        'filter_inf': get_df_filter_info(df),
        'strand': df.Strand.unique().tolist()[0],
        'prevalences': prev_dict
    })

    s['max_prev'] = project_prevalences.max()
    s['rel_proj'] = ','.join([c.split('_')[-1] for c in project_prevalences[project_prevalences == project_prevalences.max()].index.tolist()])
    s = pd.concat([s, project_prevalences, project_counts])
    del df
    return s

def get_mut_counts():
    cases = unload_json('/tamir2/nicolaslynn/projects/TCGAParsed/recurring_single_muts_tcga.json')
    cases = pd.Series(cases)
    cases.name = 'num_cases'
    cases.index.name = 'mut_id'
    cases = cases.to_frame()
    cases.reset_index(inplace=True)
    return cases


def plot_conservation(tid, gene='', mutation_loc=None, target_region=None, mut_name='Mutation', domain_annotations=[]):
    _, cons_vec = access_conservation_data(tid)

    sns.set_theme(style="white")
    fig, ax = plt.subplots(figsize=(15, 3))  # Adjusted figure size for better layout

    # Plotting the conservation vectors in the main plot
    temp = transform_conservation_vector(cons_vec, 76)
    temp /= max(temp)
    ax.plot(list(range(len(temp))), temp, c='b', label='Estimated Functional Residues')
    temp = transform_conservation_vector(cons_vec, 7)
    temp /= max(temp)
    ax.plot(list(range(len(temp))), temp, c='k', label='Estimated Functional Domains')

    # Setting up primary axis for the main plot
    ax.set_xlabel(f'AA Position - {gene}', weight='bold')
    ax.set_xlim(0, len(cons_vec))
    ax.set_ylim(0, 1)  # Set y-limit to end at 1
    ax.set_ylabel('Relative Importance', weight='bold')
    ax.tick_params(axis='y')
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    # Create a separate axes for protein domain visualization above the main plot
    domain_ax_height = 0.06  # Adjust for thinner protein diagram
    domain_ax = fig.add_axes([0.125, 0.95, 0.775, domain_ax_height])  # Position higher above the main plot
    domain_ax.set_xlim(0, len(cons_vec))
    domain_ax.set_xticks([])
    domain_ax.set_yticks([])
    domain_ax.spines['top'].set_visible(False)
    domain_ax.spines['right'].set_visible(False)
    domain_ax.spines['left'].set_visible(False)
    domain_ax.spines['bottom'].set_visible(False)

    # Draw the full-length protein as a base rectangle
    domain_ax.add_patch(Rectangle((0, 0), len(cons_vec), 0.9, facecolor='lightgray', edgecolor='none'))

    # Overlay domain annotations
    for domain in domain_annotations:
        start, end, label = domain
        domain_ax.add_patch(Rectangle((start, 0), end - start, 0.9, facecolor='orange', edgecolor='none', alpha=0.5))
        domain_ax.text((start + end) / 2, 2.1, label, ha='center', va='center', color='black', size=8)

    # Plotting Rate4Site scores on secondary y-axis
    ax2 = ax.twinx()
    c = np.array(cons_vec)
    c = c + abs(min(c))
    c = c/max(c)
    ax2.set_ylim(min(c), max(c)*1.1)
    ax2.scatter(list(range(len(c))), c, color='green', label='Rate4Site Scores', alpha=0.4)
    ax2.set_ylabel('Rate4Site Normalized', color='green', weight='bold')
    ax2.tick_params(axis='y', labelcolor='green')
    ax2.spines['right'].set_visible(True)
    ax2.spines['top'].set_visible(False)

    # Plotting mutation location and target region
    if mutation_loc is not None:
        ax.axvline(x=mutation_loc, ymax=1,color='r', linestyle='--', alpha=0.7)
        ax.text(mutation_loc, 1.01, mut_name, color='r', weight='bold', ha='center')

    if target_region is not None:
        ax.add_patch(Rectangle((target_region[0], 0.85), target_region[1] - target_region[0], 0.05, alpha=0.3, facecolor='blue'))
        center_loc = target_region[0] + 0.5 * (target_region[1] - target_region[0])
        ax.text(center_loc, 0.875, 'Target Region', ha='center', va='center', color='blue', weight='bold')

    plt.show()


def merge_overlapping_regions(df):
    # Sort the DataFrame by the 'start' column
    df = df.sort_values(by='start')

    merged_regions = []  # List to store merged regions as tuples (start, end, combined_name)

    current_start = None
    current_end = None
    combined_names = []  # List to store names of overlapping regions

    for index, row in df.iterrows():
        start = row['start']
        end = row['end']
        name = row['name'].replace('_', ' ')

        if current_start is None:
            # Initialize the current region
            current_start = start
            current_end = end
            combined_names.append(name)
        else:
            if start <= current_end:
                # Regions overlap, update the current region and add the name to combined_names
                current_end = max(current_end, end)
                combined_names.append(name)
            else:
                # Regions don't overlap, add the current region to the result with combined names
                combined_name = ', '.join(combined_names)
                merged_regions.append((current_start, current_end, combined_name))
                # Start a new current region with the current row
                current_start = start
                current_end = end
                combined_names = [name]

    # Add the last current region to the result
    if current_start is not None:
        combined_name = ', '.join(combined_names)
        merged_regions.append((current_start, current_end, combined_name))

    merged_regions = [(a, b, split_text(c, 35)) for a, b, c in merged_regions]
    return merged_regions

def split_text(text, width):
    lines = []
    while text:
        # Find the index to split at or take the whole text if it's shorter than the width
        split_index = min(len(text), width)
        # Append the substring up to the split index to the lines list
        lines.append(text[:split_index])
        # Remove the processed substring from the original text
        text = text[split_index:]
    return '\n'.join(lines)

def get_annotations(target_gene, w=500):
    temp = PROTEIN_ANNOTATIONS[(PROTEIN_ANNOTATIONS['Transcript stable ID'] == PROTEIN_ANNOTATIONS[target_gene]) & (PROTEIN_ANNOTATIONS.length < w)].drop_duplicates(subset=['Interpro Short Description'], keep='first')
    return merge_overlapping_regions(temp)


