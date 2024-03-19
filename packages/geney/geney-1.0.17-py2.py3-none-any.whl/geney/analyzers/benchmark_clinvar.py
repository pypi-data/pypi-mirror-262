import pandas as pd
from sklearn.metrics import roc_curve, precision_recall_curve
import matplotlib.pyplot as plt
from datetime import datetime
from geney import config_setup
import subprocess

def download_and_parse_clinvar():
    pass



def run_oncosplice_on_clinvar():
    now = datetime.now()
    benchmark_path = config_setup['ONCOSPLICE'] / f'clinvar_benchmark_{now.strftime("%m_%d_%Y")}'
    print(f"Saving benchmark results to {benchmark_path}")
    benchmark_path.mkdir(parents=True, exist_ok=True)
    subprocess.run(['python', '-m', 'geney.pipelines.dask_utils', '-i', '/tamir2/nicolaslynn/data/ClinVar', '-r', str(benchmark_path), '-n', '500', '-m', '5GB'])
    return benchmark_path



def benchmark_oncosplice_on_clinvar(benchmark_path):
    data = pd.concat([pd.read_csv(file) for file in benchmark_path.glob('*.csv')])
    # some way of aggregating the results
    data = pd.merge(data, pd.read_csv('/tamir2/nicolaslynn/data/ClinVar/clinvar_compact.csv'), on='mut_id')
    return data

def create_mut_id(row):
    return f"{row.Gene_name}:{row['Chromosome']}:{row['Start_Position']}:{row['Reference_Allele']}:{row['Tumor_Seq_Allele2']}"


def plot_performance(true_values, predictions):
    def map_clinsig(c):
        clinsig_map = {'Benign': 0, 'Pathogenic': 1}
        return clinsig_map[c]

    def scale_predictions(p):
        max_val = max(p)
        min_val = min(p)
        return (p - min_val) / (max_val - min_val)

    true_values = map(map_clinsig, true_values)
    predictions = scale_predictions(predictions)

    fpr, tpr, thresholds_roc = roc_curve(true_values, predictions)

    # Calculate Precision-Recall curve
    precision, recall, thresholds_pr = precision_recall_curve(true_values, predictions)

    # Plotting ROC curve
    plt.figure(figsize=(15, 5))

    plt.subplot(1, 3, 1)
    plt.plot(fpr, tpr)
    plt.title('ROC Curve')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')

    # Plotting Precision-Recall curve
    plt.subplot(1, 3, 2)
    plt.plot(recall, precision)
    plt.title('Precision-Recall Curve')
    plt.xlabel('Recall')
    plt.ylabel('Precision')

    # Plotting Precision vs. Thresholds
    plt.subplot(1, 3, 3)
    plt.plot(thresholds_pr, precision[:-1])  # Precision and thresholds have off-by-one lengths
    plt.title('Precision vs. Threshold')
    plt.xlabel('Threshold')
    plt.ylabel('Precision')

    plt.tight_layout()
    plt.show()
    return None

