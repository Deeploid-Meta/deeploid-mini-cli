import gzip
import shutil
from pathlib import Path
import pandas as pd
import qiime2.plugins as plugins
from qiime2.sdk import PluginManager
import qiime2
from qiime2 import Artifact
from urllib import request
from qiime2 import Metadata
import qiime2.plugins.metadata.actions as metadata_actions
import qiime2.plugins.feature_classifier.actions as feature_classifier_actions


raw_data = Path('data')
sample_name = 'SRR22104214'

vsearch_data = Path('vsearch_data')
vsearch_data.mkdir(exist_ok=True)

vsearch_artifacts = Path('vsearch_artifacts')
vsearch_artifacts.mkdir(exist_ok=True)

plugin_manager = PluginManager(True)
vsearch = plugin_manager.plugins["vsearch"]


def preprocess_import_data(raw_data, sample_name, vsearch_data, vsearch_artifacts):
    """
    Parse data from folder with raw reads and transform them to qiime2 format.
    Then imports data to qiime2.
    """
    #data to qiime2 format
    for i in range(1, 3):
        with open(raw_data / f'{sample_name}_{i}.fastq', 'rb') as f_in:
            with gzip.open(vsearch_data / f'{sample_name}_{i}_L001_R{i}_001.fastq.gz', 'wb') as f_out:
                f_out.writelines(f_in)

    #importing data to qiime2
    paired_end_sequences = qiime2.Artifact.import_data('SampleData[PairedEndSequencesWithQuality]', 'vsearch_data')
    paired_end_sequences.save(str(vsearch_artifacts / 'paired-end-sequences.qza'))

    return paired_end_sequences

def merging(paired_end_sequences, vsearch_artifacts):
    """
    Merges raw sequences into one file for vsearch usage
    """

    join_pairs = vsearch.actions["join_pairs"]
    result = join_pairs(demultiplexed_seqs=paired_end_sequences)

    print(result)

    joined_sequences = result.joined_sequences
    joined_sequences.save(str(vsearch_artifacts / 'joined-sequences.qza'))

    return joined_sequences

def dereplication(joined_sequences, vsearch_artifacts):
    """
    Dereplication of joined sequences
    """

    dereplicate_sequences = vsearch.actions["dereplicate_sequences"]
    result = dereplicate_sequences(sequences = joined_sequences)

    print(result)

    dereplicated_table = result.dereplicated_table
    dereplicated_sequences = result.dereplicated_sequences

    dereplicated_sequences.save(str(vsearch_artifacts / 'dereplicated_sequences.qza'))
    dereplicated_table.save(str(vsearch_artifacts / 'dereplicated_table.qza'))

    return dereplicated_table, dereplicated_sequences

def otu_clustering(dereplicated_table, dereplicated_sequences, vsearch_artifacts):
    """
    Creates OTUs feature table and sequences
    """

    cluster_features_de_novo = vsearch.actions["cluster_features_de_novo"]
    result = cluster_features_de_novo(sequences = dereplicated_sequences, table = dereplicated_table, perc_identity = 0.97)

    print(result)

    clustered_table = result.clustered_table
    clustered_sequences = result.clustered_sequences

    clustered_table.save(str(vsearch_artifacts / 'clustered_table.qza'))
    clustered_sequences.save(str(vsearch_artifacts / 'clustered_sequences.qza'))

    return clustered_table, clustered_sequences

def taxonomy_classification(clustered_table, clustered_sequences, vsearch_artifacts):
    """
    Does taxonomy classification, saves visualizations for taxonomy
    """

    fn = 'gg-13-8-99-515-806-nb-classifier.qza'

    try :
        gg_13_8_99_515_806_nb_classifier = Artifact.load(fn)
    except:
        url = 'https://docs.qiime2.org/jupyterbooks/cancer-microbiome-intervention-tutorial/data/030-tutorial-downstream/020-taxonomy/gg-13-8-99-515-806-nb-classifier.qza'
        request.urlretrieve(url, fn)
        gg_13_8_99_515_806_nb_classifier = Artifact.load(fn)


    taxonomy, = feature_classifier_actions.classify_sklearn(
        classifier=gg_13_8_99_515_806_nb_classifier,
        reads=clustered_sequences,
    )
    taxonomy.save(str(vsearch_artifacts / 'taxonomy.qza'))

    # visualization
    taxonomy_as_md_md = taxonomy.view(Metadata)
    taxonomy_viz, = metadata_actions.tabulate(
        input=taxonomy_as_md_md,
    )
    taxonomy_viz.save(str(vsearch_artifacts / 'taxonomy_viz.qzv'))

    # Use taxa plugin for visualization taxonomy - barplot
    taxa = plugin_manager.plugins['taxa']
    barplot = taxa.actions['barplot']
    result_barplot = barplot(table=clustered_table,
                             taxonomy=taxonomy)
    print(f'result_barplot: {result_barplot}')

    result_barplot.visualization.save(str(vsearch_artifacts / 'barplot.qzv'))

    return taxonomy

def main():
    """
    Pipeline for metagenomics 16s data anlysis using vsearch
    """
    #import data
    paired_end_sequences = preprocess_import_data(raw_data, sample_name, vsearch_data, vsearch_artifacts)

    #merging
    joined_sequences = merging(paired_end_sequences, vsearch_artifacts)

    #dereplication
    dereplicated_table, dereplicated_sequences = dereplication(joined_sequences, vsearch_artifacts)

    #OTUs (clustering)
    clustered_table, clustered_sequences = otu_clustering(dereplicated_table, dereplicated_sequences, vsearch_artifacts)

    # taxonomy classification
    taxonomy = taxonomy_classification(clustered_table, clustered_sequences, vsearch_artifacts)





if __name__ == "__main__":
    main()
