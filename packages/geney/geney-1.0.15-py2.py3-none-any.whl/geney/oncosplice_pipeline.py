import numpy as np
import pandas as pd
from Bio import pairwise2
import re
from copy import deepcopy
from geney.splicing import PredictSpliceAI
from .Gene import Gene, Transcript
from geney.mutations.variant_utils import Variations, develop_aberrant_splicing
import matplotlib.pyplot as plt

sample_mut_id = 'KRAS:12:25227343:G:T'
sample_epistasis_id = 'KRAS:12:25227343:G:T|KRAS:13:25227344:T:A'

def oncosplice(mutation: str, sai_threshold=0.25, prevalence_threshold=0.25, annotate=False, plot_term=False) -> pd.DataFrame:
    '''
        :param mutation: str
                        the genomic variation
        :param sai_threshold: float
                        the threshold for including missplicing predictions in gene builds
        :param prevalence_threshold: float
                        the minimum threshold needed to consider a predicted isoform as valid
        :param target_directory: pathlib.Path
                        the directory on the machine where the mrna annotation files are stored
        :return: a dataframe object
                will contain columns pertinant to assessing mutation pathogenicity including pipelines score, GOF score, legacy pipelines score, missplicing,
    '''

    print(f'>> Processing: {mutation}')
    mutation = Variations(mutation)                                             # Generate mutation object
    # Gene annotations should be available in the target directory under the file name mrna_gene.json
    gene = Gene(mutation.gene)                                                      # We obtain the annotation file and convert it into a Gene object
    aberrant_splicing = PredictSpliceAI(mutation, gene, threshold=sai_threshold)      # SpliceAI predictions are processed and obtained for each mutation
    # Oncosplice obtains predictions for each transcript in the annotation file
    results = pd.concat([oncosplice_transcript(reference_transcript.generate_protein(), mutation, aberrant_splicing, prevalence_threshold, annotate, plot_term) for
                         reference_transcript in gene if reference_transcript.transcript_biotype == 'protein_coding'])

    # Append some additional, uniform information to the results dataframe
    results['mut_id'] = mutation.mut_id
    results['missplicing'] = aberrant_splicing.get_max_missplicing_delta()
    results['gene'] = mutation.gene
    return results

def oncosplice_transcript(reference_transcript: Transcript, mutation: Variations, aberrant_splicing:PredictSpliceAI, prevalence_threshold=0.0, annotate=False, plot_term=False) -> pd.DataFrame:
    '''
    :param reference_transcript:
    :param mutation:
    :param aberrant_splicing:
    :param prevalence_threshold:
    :param full_output:
    :return:
    '''
    reports = []
    if reference_transcript.cons_available and reference_transcript.cons_seq.replace('*', '') == reference_transcript.protein:
        if len(reference_transcript.cons_vector) == len(reference_transcript.protein) + 1:
            reference_transcript.cons_vector = reference_transcript.cons_vector[:-1]

        if len(reference_transcript.cons_vector) != len(reference_transcript.protein):
            raise ValueError(f"Length of conservation ({len(reference_transcript.cons_vector)})is not equal to the length of the protein ({len(reference_transcript.protein)}).")

        cons_available, cons_vector = True, reference_transcript.cons_vector
        cons_available = True

    else:
        cons_available, cons_vector = False, np.ones(len(reference_transcript.protein), dtype=float)

    # For each transcript, we generate a series of isoforms based on the splice site predictions; each isoform is assigned a prevalence score
    # obtained using simple graph theory where the probability of the edges taken to generate the isoform are multiplied together
    for i, new_boundaries in enumerate(develop_aberrant_splicing(reference_transcript, aberrant_splicing.aberrant_splicing)):

        # The variant transcript is duplicated from the reference transcript and all needed modifications are performed
        variant_transcript = Transcript(deepcopy(reference_transcript).__dict__).set_exons(new_boundaries).generate_mature_mrna(mutations=mutation.mut_id.split('|'), inplace=True).generate_translational_boundaries().generate_protein()

        # The optimal alignment that minimizes gaps between the trnascripts is obtained
        alignment = get_logical_alignment(reference_transcript.protein, variant_transcript.protein)

        # Based on the optimal alignment, we can generate the relative locations of insertions and deletions
        deleted, inserted = find_indels_with_mismatches_as_deletions(alignment.seqA, alignment.seqB)

        report = {
            'log': variant_transcript.log,
            'isoform': i,
            'isoform_prevalence': new_boundaries['path_weight'],
            'legacy_oncosplice_score': calculate_legacy_oncosplice_score(deleted, inserted, cons_vector,
                                                      min(76, len(reference_transcript.protein))),
            'variant_length': len(variant_transcript.protein.replace('*', '')),
        }

        oncosplice_output = oncosplice_report(deleted, inserted, cons_vector,10, tplot=plot_term)
        report.update(oncosplice_output)

        # unmodified_positions = find_unmodified_positions(len(cons_vector), deleted, inserted)
        # report.update(calculate_oncosplice_scores(deleted, inserted, cons_vector))
        # report.update(calculate_oncosplice_scores(deleted, inserted, cons_vector, 10))

        if annotate:
            report.update(OncospliceAnnotator(reference_transcript, variant_transcript, mutation))
            report['insertions'] = inserted
            report['deletions'] = deleted
            report['full_missplicing'] = aberrant_splicing.missplicing

        reports.append(report)

    reports = pd.DataFrame(reports)
    reports['cons_available'] = int(cons_available)
    reports['transcript_id'] = reference_transcript.transcript_id
    reports['cons_sum'] = np.sum(np.exp(np.negative(cons_vector)))
    reports['transcript_length'] = len(reference_transcript.protein)
    reports['primary_transcript'] = reference_transcript.primary_transcript

    return reports[reports.isoform_prevalence >= prevalence_threshold]


def oncosplice_per_mut(df):
    target_columns = [c for c in df.columns if 'oncosplice' in c]
    if len(target_columns) == 0:
        print("No oncosplice scores to reduce.")
        return None

    scores = []
    for score in target_columns:
        scores.append(df.groupby(['mut_id', 'transcript_id'])[score].mean().groupby('mut_id').max())

    return pd.concat(scores)


def find_continuous_gaps(sequence):
    """Find continuous gap sequences in an alignment."""
    return [(m.start(), m.end()) for m in re.finditer(r'-+', sequence)]


def get_logical_alignment(ref_prot, var_prot):
    """
    Aligns two protein sequences and finds the optimal alignment with the least number of gaps.

    Parameters:
    ref_prot (str): Reference protein sequence.
    var_prot (str): Variant protein sequence.

    Returns:
    tuple: Optimal alignment, number of insertions, and number of deletions.
    """

    # Perform global alignment
    alignments = pairwise2.align.globalms(ref_prot, var_prot, 1, -1, -3, 0, penalize_end_gaps=(True, False))

    # Selecting the optimal alignment
    if len(alignments) > 1:
        # Calculate continuous gaps for each alignment and sum their lengths
        gap_lengths = [sum(end - start for start, end in find_continuous_gaps(al.seqA) + find_continuous_gaps(al.seqB)) for al in alignments]
        optimal_alignment = alignments[gap_lengths.index(min(gap_lengths))]
    else:
        optimal_alignment = alignments[0]

    return optimal_alignment


def find_indels_with_mismatches_as_deletions(seqA, seqB):
    """
    Identify insertions and deletions in aligned sequences, treating mismatches as deletions.

    Parameters:
    seqA, seqB (str): Aligned sequences.

    Returns:
    tuple: Two dictionaries containing deletions and insertions.
    """
    if len(seqA) != len(seqB):
        raise ValueError("Sequences must be of the same length")

    seqA_array, seqB_array = np.array(list(seqA)), np.array(list(seqB))

    # Find and mark mismatch positions in seqB
    mismatches = (seqA_array != seqB_array) & (seqA_array != '-') & (seqB_array != '-')
    seqB_array[mismatches] = '-'
    modified_seqB = ''.join(seqB_array)

    gaps_in_A = find_continuous_gaps(seqA)
    gaps_in_B = find_continuous_gaps(modified_seqB)

    insertions = {start: modified_seqB[start:end].replace('-', '') for start, end in gaps_in_A if seqB[start:end].strip('-')}
    deletions = {start: seqA[start:end].replace('-', '') for start, end in gaps_in_B if seqA[start:end].strip('-')}
    return deletions, insertions



def parabolic_window(window_size):
    """Create a parabolic window function with a peak at the center."""
    x = np.linspace(-1, 1, window_size)
    return 0.9 * (1 - x**2) + 0.1


def calculate_window_size(conservation_vector_length):
    return int(9 + (51 - 9) * (1 - np.exp(-0.0005 * conservation_vector_length)))



def transform_conservation_vector(conservation_vector, plot=False, tplot=False, tid=''):
    # Calculate dynamic window size
    window_size = calculate_window_size(len(conservation_vector))

    if window_size > len(conservation_vector):
        window_size = int(len(conservation_vector) / 2)

    # Create convolution window and transform vector
    convolving_window = parabolic_window(window_size)
    factor = int(100 / window_size)
    transformed_vector = np.convolve(conservation_vector, convolving_window, mode='same') / sum(convolving_window)
    transformed_vector = np.exp(-transformed_vector * factor)

    transformed_vector -= np.percentile(transformed_vector, 75)
    max_val = max(transformed_vector)
    transformed_vector /= max_val

    # Balancing negative values
    negative_values = transformed_vector[transformed_vector < 0]
    if negative_values.size > 0:
        balance_factor = -np.sum(transformed_vector[transformed_vector >= 0]) / np.sum(negative_values)
        transformed_vector[transformed_vector < 0] *= balance_factor


    if plot:
        # Plotting the two vectors
        fig, ax1 = plt.subplots(figsize=(8, 4))
        color = 'tab:blue'
        ax1.set_xlabel('Position')
        ax1.set_ylabel('Conservation Vector', color=color, alpha=0.5)
        ax1.plot(conservation_vector, color=color)
        ax1.tick_params(axis='y', labelcolor=color)

        ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
        color = 'tab:red'
        ax2.set_ylabel('Transformed Vector', color=color)  # we already handled the x-label with ax1
        ax2.plot(transformed_vector, color=color)
        ax2.tick_params(axis='y', labelcolor=color)
        plt.axhline(0)
        plt.title(tid)
        fig.tight_layout()  # otherwise the right y-label is slightly clipped
        plt.show()

    if tplot:
        import termplotlib as tpl
        fig = tpl.figure()
        fig.plot(list(range(len(conservation_vector))), conservation_vector, width=100, height=15)
        fig.plot(list(range(len(transformed_vector))), transformed_vector, width=100, height=15)
        fig.show()

    return transformed_vector



def find_modified_positions(sequence_length, deletions, insertions, reach_limit=16):
    """
    Identify unmodified positions in a sequence given deletions and insertions.

    :param sequence_length: Length of the sequence.
    :param deletions: Dictionary of deletions.
    :param insertions: Dictionary of insertions.
    :param reach_limit: Limit for considering the effect of insertions/deletions.
    :return: Array indicating unmodified positions.
    """
    unmodified_positions = np.ones(sequence_length, dtype=float)

    for pos, insertion in insertions.items():
        if pos >= sequence_length:
            pos = sequence_length - 1

        reach = min(len(insertion) // 2, reach_limit)
        front_end, back_end = max(0, pos - reach), min(sequence_length-1, pos + reach)
        len_start, len_end = pos - front_end, back_end - pos

        try:
            gradient_front = np.linspace(0, 1, len_start, endpoint=False)[::-1]
            gradient_back = np.linspace(0, 1, len_end, endpoint=False)
            combined_gradient = np.concatenate([gradient_front, gradient_back])
            unmodified_positions[front_end:back_end] = combined_gradient

        except ValueError as e:
            print(
                f"Error: {e} | Lengths: unmodified_positions_slice={back_end - front_end}, combined_gradient={len(combined_gradient)}")
            unmodified_positions[front_end:back_end] = np.zeros(back_end - front_end)

    for pos, deletion in deletions.items():
        deletion_length = len(deletion)
        unmodified_positions[pos:pos + deletion_length] = 0

    return 1 - unmodified_positions


def oncosplice_report(deletions, insertions, cons_vector, window_size=4, tplot=False):
    """
    Calculate pipelines scores based on conservation vectors and detected sequence modifications.

    :param deletions: Dictionary of deletions in the sequence.
    :param insertions: Dictionary of insertions in the sequence.
    :param cons_vector: Conservation vector.
    :param window_size: Window size for calculations.
    :return: Dictionary of pipelines scores.
    """
    modified_positions = find_modified_positions(len(cons_vector), deletions, insertions)
    cons_vec = transform_conservation_vector(cons_vector, tplot=tplot)
    affected_cons_scores = cons_vec * modified_positions
    affected_sum = np.sum(affected_cons_scores)
    modified_cons_vector = np.convolve(affected_cons_scores, np.ones(window_size), mode='same') / window_size

    # obtaining scores
    max_score = np.max(modified_cons_vector)
    max_score_indices = np.where(modified_cons_vector == max_score)[0]

    # Exclude windows within one window_size of the max scoring window
    exclusion_zone = set().union(*(range(max(i - window_size, 0), min(i + window_size, len(modified_cons_vector))) for i in max_score_indices))
    viable_secondary_scores = [score for i, score in enumerate(modified_cons_vector) if i not in exclusion_zone]

    if len(viable_secondary_scores) == 0:
        gof_prob = 0

    else:
        second_highest_score = np.max(viable_secondary_scores)
        gof_prob = (max_score - second_highest_score) / max_score


    return {f'gof': gof_prob, f'oncosplice_score': max_score, 'affected_cons_sum': affected_sum, 'cons_vector': cons_vector, 'affected_positions': modified_positions}


def calculate_penalty(domains, cons_scores, W, is_insertion=False):
    """
    Calculate the penalty for mutations (either insertions or deletions) on conservation scores.

    :param domains: Dictionary of mutations (inserted or deleted domains).
    :param cons_scores: Conservation scores.
    :param W: Window size.
    :param is_insertion: Boolean flag to indicate if the mutation is an insertion.
    :return: Penalty array.
    """
    penalty = np.zeros(len(cons_scores))
    for pos, seq in domains.items():
        mutation_length = len(seq)
        weight = max(1.0, mutation_length / W)

        if is_insertion:
            reach = min(W // 2, mutation_length // 2)
            penalty[pos - reach:pos + reach] = weight * cons_scores[pos - reach:pos + reach]
        else:  # For deletion
            penalty[pos:pos + mutation_length] = cons_scores[pos:pos + mutation_length] * weight

    return penalty


def calculate_legacy_oncosplice_score(deletions, insertions, cons_vec, W):
    """
    Calculate the legacy Oncosplice score based on deletions, insertions, and conservation vector.

    :param deletions: Dictionary of deletions.
    :param insertions: Dictionary of insertions.
    :param cons_vec: Conservation vector.
    :param W: Window size.
    :return: Legacy Oncosplice score.
    """
    smoothed_conservation_vector = np.exp(np.negative(moving_average_conv(cons_vec, W, 2)))
    del_penalty = calculate_penalty(deletions, smoothed_conservation_vector, W, is_insertion=False)
    ins_penalty = calculate_penalty(insertions, smoothed_conservation_vector, W, is_insertion=True)
    combined_scores = del_penalty + ins_penalty
    return np.max(np.convolve(combined_scores, np.ones(W), mode='same'))



def OncospliceAnnotator(reference_transcript, variant_transcript, mut):
    affected_exon, affected_intron, distance_from_5, distance_from_3 = find_splice_site_proximity(mut, reference_transcript)

    report = {}
    report['reference_mRNA'] = reference_transcript.transcript_seq
    report['reference_CDS_start'] = reference_transcript.TIS
    report['reference_pre_mrna'] = reference_transcript.pre_mrna
    report['reference_ORF'] = reference_transcript.pre_mrna[reference_transcript.transcript_indices.index(reference_transcript.TIS):reference_transcript.transcript_indices.index(reference_transcript.TTS)]
    report['reference_protein'] = reference_transcript.protein

    report['variant_mRNA'] = variant_transcript.transcript_seq
    report['variant_CDS_start'] = variant_transcript.TIS
    report['variant_pre_mrna'] = variant_transcript.pre_mrna[variant_transcript.transcript_indices.index(variant_transcript.TIS):variant_transcript.transcript_indices.index(variant_transcript.TTS)]
    report['variant_ORF'] = variant_transcript.pre_mrna
    report['variant_protein'] = variant_transcript.protein

    descriptions = define_missplicing_events(reference_transcript.exons, variant_transcript.exons,
                              reference_transcript.rev)
    report['exon_changes'] = '|'.join([v for v in descriptions if v])
    report['splicing_codes'] = summarize_missplicing_event(*descriptions)
    report['affected_exon'] = affected_exon
    report['affected_intron'] = affected_intron
    report['mutation_distance_from_5'] = distance_from_5
    report['mutation_distance_from_3'] = distance_from_3
    return report


def find_splice_site_proximity(mut, transcript):
    affected_exon, affected_intron, distance_from_5, distance_from_3 = None, None, None, None
    for i, (ex_start, ex_end) in enumerate(transcript.exons):
        if min(ex_start, ex_end) <= mut.start <= max(ex_start, ex_end):
            affected_exon = i + 1
            distance_from_5 = abs(mut.start - ex_start)
            distance_from_3 = abs(mut.start - ex_end)

    for i, (in_start, in_end) in enumerate(transcript.introns):
        if min(in_start, in_end) <= mut.start <= max(in_start, in_end):
            affected_intron = i + 1
            distance_from_5 = abs(mut.start - in_end)
            distance_from_3 = abs(mut.start - in_start)

    return affected_exon, affected_intron, distance_from_5, distance_from_3

def define_missplicing_events(ref_exons, var_exons, rev):
    ref_introns = [(ref_exons[i][1], ref_exons[i + 1][0]) for i in range(len(ref_exons) - 1)]
    var_introns = [(var_exons[i][1], var_exons[i + 1][0]) for i in range(len(var_exons) - 1)]
    num_ref_exons = len(ref_exons)
    num_ref_introns = len(ref_introns)
    if not rev:
        partial_exon_skipping = ','.join(
            [f'Exon {exon_count + 1}/{num_ref_exons} truncated: {(t1, t2)} --> {(s1, s2)}' for (s1, s2) in var_exons for
             exon_count, (t1, t2) in enumerate(ref_exons) if (s1 == t1 and s2 < t2) or (s1 > t1 and s2 == t2)])
        partial_intron_retention = ','.join(
            [f'Intron {intron_count + 1}/{num_ref_introns} partially retained: {(t1, t2)} --> {(s1, s2)}' for (s1, s2)
             in var_introns for intron_count, (t1, t2) in enumerate(ref_introns) if
             (s1 == t1 and s2 < t2) or (s1 > t1 and s2 == t2)])

    else:
        partial_exon_skipping = ','.join(
            [f'Exon {exon_count + 1}/{num_ref_exons} truncated: {(t1, t2)} --> {(s1, s2)}' for (s1, s2) in var_exons for
             exon_count, (t1, t2) in enumerate(ref_exons) if (s1 == t1 and s2 > t2) or (s1 < t1 and s2 == t2)])
        partial_intron_retention = ','.join(
            [f'Intron {intron_count + 1}/{num_ref_introns} partially retained: {(t1, t2)} --> {(s1, s2)}' for (s1, s2)
             in var_introns for intron_count, (t1, t2) in enumerate(ref_introns) if
             (s1 == t1 and s2 > t2) or (s1 < t1 and s2 == t2)])

    exon_skipping = ','.join(
        [f'Exon {exon_count + 1}/{num_ref_exons} skipped: {(t1, t2)}' for exon_count, (t1, t2) in enumerate(ref_exons)
         if
         t1 not in [s1 for s1, s2 in var_exons] and t2 not in [s2 for s1, s2 in var_exons]])
    novel_exons = ','.join([f'Novel Exon: {(t1, t2)}' for (t1, t2) in var_exons if
                            t1 not in [s1 for s1, s2 in ref_exons] and t2 not in [s2 for s1, s2 in ref_exons]])
    intron_retention = ','.join(
        [f'Intron {intron_count + 1}/{num_ref_introns} retained: {(t1, t2)}' for intron_count, (t1, t2) in
         enumerate(ref_introns) if
         t1 not in [s1 for s1, s2 in var_introns] and t2 not in [s2 for s1, s2 in var_introns]])

    return partial_exon_skipping, partial_intron_retention, exon_skipping, novel_exons, intron_retention


def summarize_missplicing_event(pes, pir, es, ne, ir):
    event = []
    if pes:
        event.append('PES')
    if es:
        event.append('ES')
    if pir:
        event.append('PIR')
    if ir:
        event.append('IR')
    if ne:
        event.append('NE')
    if len(event) > 1:
        return event
    elif len(event) == 1:
        return event[0]
    else:
        return '-'




# def find_indels_with_mismatches_as_deletions(seqA, seqB):
#     # Convert sequences to numpy arrays for element-wise comparison
#     ta, tb = np.array(list(seqA)), np.array(list(seqB))
#
#     # Find mismatch positions
#     mismatch_positions = (ta != tb) & (ta != '-') & (tb != '-')
#
#     # Replace mismatch positions in seqB with '-'
#     tb[mismatch_positions] = '-'
#     modified_seqB = ''.join(tb)
#
#     # Function to find continuous gaps using regex
#     def find_continuous_gaps(sequence):
#         return [(m.start(), m.end()) for m in re.finditer(r'-+', sequence)]
#
#     # Find gaps in both sequences
#     gaps_in_A = find_continuous_gaps(seqA)
#     gaps_in_B = find_continuous_gaps(modified_seqB)
#
#     # Identify insertions and deletions
#     insertions = {start: modified_seqB[start:end].replace('-', '') for start, end in gaps_in_A if
#                   seqB[start:end].strip('-')}
#     deletions = {start: seqA[start:end].replace('-', '') for start, end in gaps_in_B if seqA[start:end].strip('-')}
#
#     return deletions, insertions



# def moving_average_conv(vector, window_size, factor=1):
#     """
#     Calculate the moving average convolution of a vector.
#
#     :param vector: Input vector.
#     :param window_size: Size of the convolution window.
#     :return: Convolved vector as a numpy array.
#     """
#     convolving_length = np.array([min(len(vector) + window_size - i, window_size, i)
#                                   for i in range(window_size // 2, len(vector) + window_size // 2)], dtype=float)
#
#     return np.convolve(vector, np.ones(window_size), mode='same') / (convolving_length / factor)
#


# def get_logical_alignment(ref_prot, var_prot):
#     '''
#     :param ref_prot:
#     :param var_prot:
#     :return:
#     '''
#
#     alignments = pairwise2.align.globalms(ref_prot, var_prot, 1, -1, -3, 0, penalize_end_gaps=(True, False))
#     if len(alignments) == 1:
#         optimal_alignment = alignments[0]
#     else:
#         # This calculates the number of gaps in each alignment.
#         number_of_gaps = [re.sub('-+', '-', al.seqA).count('-') + re.sub('-+', '-', al.seqB).count('-') for al in
#                           alignments]
#
#         optimal_alignment = alignments[number_of_gaps.index(min(number_of_gaps))]
#
#     num_insertions = re.sub('-+', '-', optimal_alignment.seqA).count('-')
#     num_deletions = re.sub('-+', '-', optimal_alignment.seqB).count('-')
#     return optimal_alignment
#


# def transform_conservation_vector(conservation_vector, window_size=10, verbose=False):
#     """
#     Transforms a conservation vector by applying a moving average convolution and scaling.
#
#     :param conservation_vector: Array of conservation scores.
#     :param window_size: Window size for the moving average convolution. Defaults to 10, the average binding site length.
#     :return: Transformed conservation vector.
#     """
#     factor = 100 / window_size
#     conservation_vector = moving_average_conv(conservation_vector, window_size)
#     transformed_vector = np.exp(-conservation_vector*factor)
#     transformed_vector = transformed_vector / max(transformed_vector)
#
#     if verbose:
#         import asciiplotlib as apl
#         fig = apl.figure()
#         fig.plot(list(range(len(transformed_vector))), transformed_vector, width=50, height=15, title="Conservation Vector")
#         fig.plot(list(range(len(conservation_vector))), transformed_vector, width=50, height=15, title="Entropy Vector")
#         fig.show()
#
#     return transformed_vector




def moving_average_conv(vector, window_size, factor=1):
    """
    Calculate the moving average convolution of a vector.

    Parameters:
    vector (iterable): Input vector (list, tuple, numpy array).
    window_size (int): Size of the convolution window. Must be a positive integer.
    factor (float): Scaling factor for the average. Default is 1.

    Returns:
    numpy.ndarray: Convolved vector as a numpy array.
    """
    if not isinstance(vector, (list, tuple, np.ndarray)):
        raise TypeError("vector must be a list, tuple, or numpy array")
    if not isinstance(window_size, int) or window_size <= 0:
        raise ValueError("window_size must be a positive integer")
    if len(vector) < window_size:
        raise ValueError("window_size must not be greater than the length of vector")
    if factor == 0:
        raise ValueError("factor must not be zero")

    return np.convolve(vector, np.ones(window_size), mode='same') / window_size