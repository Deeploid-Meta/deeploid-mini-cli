import gzip
import shutil
import argparse
from pathlib import Path

import os

import pandas as pd
import qiime2.plugins as plugins
from qiime2.sdk import PluginManager
from qiime2 import Artifact
from urllib import request
from qiime2 import Metadata
import qiime2.plugins.metadata.actions as metadata_actions
import qiime2.plugins.feature_classifier.actions as feature_classifier_actions

import qiime2

plugin_manager = PluginManager(True)
vsearch = plugin_manager.plugins["vsearch"]


def build_parser() -> argparse.ArgumentParser:

    parser = argparse.ArgumentParser(description='vsearch pipeline for 16s rrna data analysis')
    parser.add_argument('-r', '--raw_reads_dir', help='Forward reads file (or single-end) in fastq|fq|gz|tar.gz format', required=True)
    parser.add_argument('-o', '--outdir', help='Output folder with artifacts and data', required=True)
    parser.add_argument('-se', '--is_single_ended', help='Analyse as single ended', required=False, default=False)
    parser.add_argument('-t', '--trimming', help='Trim raw reads before analysis', required=False, default=False)

    return parser


def prepare_data_se(raw_reads_path, working_dir):
    ''' Prepare sindle ended files for qiime pipeline (should be gz files with _R1_001.fastq.gz
        and _R2_001.fastq.gz in filename)
    '''
    prepared_for_qiime2_reads_dir = working_dir / Path('prepared_data')
    prepared_for_qiime2_reads_dir.mkdir(exist_ok=True)


    reads_names = os.listdir(raw_reads_path)
    reads_names = [x for x in reads_names if '.fastq' in x or '.fq' in x]
    sample_names  = list(set([x.split('_')[0] for x in reads_names]))


    for sample_name in sample_names:
        with open(raw_reads_path / f'{sample_name}_1.fastq', 'rb') as f_in:
            with gzip.open(prepared_for_qiime2_reads_dir / f'{sample_name}_1_L001_R1_001.fastq.gz', 'wb') as f_out:
                f_out.writelines(f_in)

    # Prepare MANIFEST file
    manifest_data = []
    for sample_name in sample_names:
        manifest_data.append([sample_name, str(f'{sample_name}_1_L001_R1_001.fastq.gz') ,'forward',])

    manifest = pd.DataFrame(manifest_data, columns=['sample-id', 'filename', 'direction'])
    manifest.to_csv(prepared_for_qiime2_reads_dir / 'MANIFEST', index=False)

    # Prepare metadata file
    with open(prepared_for_qiime2_reads_dir / 'metadata.yml', 'w') as f:
        f.write('phred-offset: 33')

    return prepared_for_qiime2_reads_dir


def prepare_data_pe(raw_reads_path,
                    working_dir):
    ''' Prepare pair ended files for qiime pipeline (should be gz files with _R1_001.fastq.gz
        and _R2_001.fastq.gz in filename)
    '''
    prepared_for_qiime2_reads_dir = working_dir / Path('prepared_data')
    prepared_for_qiime2_reads_dir.mkdir(exist_ok=True)


    reads_names = os.listdir(raw_reads_path)
    reads_names = [x for x in reads_names if '.fastq' in x or '.fq' in x]
    sample_names  = list(set([x.split('_')[0] for x in reads_names]))


    for sample_name in sample_names:
        for i in range(1, 3):
            with open(raw_reads_path / f'{sample_name}_{i}.fastq', 'rb') as f_in:
                with gzip.open(prepared_for_qiime2_reads_dir / f'{sample_name}_{i}_L001_R{i}_001.fastq.gz', 'wb') as f_out:
                    f_out.writelines(f_in)

    # Prepare MANIFEST file
    manifest_data = []
    for sample_name in sample_names:
        manifest_data.append([sample_name, str(f'{sample_name}_1_L001_R1_001.fastq.gz') ,'forward',])
        manifest_data.append([sample_name, str(f'{sample_name}_2_L001_R2_001.fastq.gz') ,'reverse',])

    manifest = pd.DataFrame(manifest_data, columns=['sample-id', 'filename', 'direction'])
    manifest.to_csv(prepared_for_qiime2_reads_dir / 'MANIFEST', index=False)

    # Prepare metadata file
    with open(prepared_for_qiime2_reads_dir / 'metadata.yml', 'w') as f:
        f.write('phred-offset: 33')

    return prepared_for_qiime2_reads_dir


def load_sequences_to_qiime2(is_single_ended, prepared_for_qiime2_reads_dir, output_dir):
    """
    Imports data to qiime2
    """
    if is_single_ended:
        single_end_sequences = qiime2.Artifact.import_data('SampleData[SequencesWithQuality]', prepared_for_qiime2_reads_dir)
        single_end_sequences.save(str(output_dir / 'single-end-sequences.qza'))
        os.system(f'rm -rf {prepared_for_qiime2_reads_dir}')

        return single_end_sequences

    else:
        paired_end_sequences = qiime2.Artifact.import_data('SampleData[PairedEndSequencesWithQuality]', prepared_for_qiime2_reads_dir)
        paired_end_sequences.save(str(output_dir / 'paired-end-sequences.qza'))
        os.system(f'rm -rf {prepared_for_qiime2_reads_dir}')

        return paired_end_sequences



def trimming(is_single_ended, raw_reads_path, working_dir):
    """Trims raw data"""
    reads_names = os.listdir(raw_reads_path)
    reads_names = [x for x in reads_names if '.fastq' in x or '.fq' in x]
    sample_names  = list(set([x.split('_')[0] for x in reads_names]))

    new_path = working_dir / Path("raw_data_dir_trimmed")
    new_path.mkdir(exist_ok=True)

    if is_single_ended:
        for sample_name in sample_names:
            os.system(f"""trimmomatic SE {raw_reads_path}/{sample_name}_1.fastq {new_path}/{sample_name}_1.fastq ILLUMINACLIP:TruSeq3-PE.fa:2:30:10:2:True""")

    else:
        for sample_name in sample_names:
            os.system(f"""trimmomatic PE {raw_reads_path}/{sample_name}_1.fastq {raw_reads_path}/{sample_name}_2.fastq {new_path}/{sample_name}_1.fastq {new_path}/output_forward_unpaired {new_path}/{sample_name}_2.fastq {new_path}/output_reverse_unpaired ILLUMINACLIP:TruSeq3-PE.fa:2:30:10:2:True""")


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

    parser = build_parser()
    args = vars(parser.parse_args())

    raw_reads_dir = Path(args['raw_reads_dir'])
    is_single_ended = args["is_single_ended"] == 'True'
    to_trim = args["trimming"] == 'True'

    # Create output directory
    output_dir = Path(args['outdir'])
    output_dir.mkdir(exist_ok=True)

    # Create working directory
    working_dir = output_dir / Path('working_dir')
    working_dir.mkdir(exist_ok=True)

    #trimming
    if to_trim:
        trimming(is_single_ended, raw_reads_dir, working_dir)
        raw_reads_dir = working_dir / Path("raw_data_dir_trimmed")

    #preprocessing and importing data
    if is_single_ended:
        prepared_for_qiime2_reads_dir = prepare_data_se(raw_reads_dir, working_dir)
        sequences = load_sequences_to_qiime2(True, prepared_for_qiime2_reads_dir, output_dir)
    else:
        prepared_for_qiime2_reads_dir = prepare_data_pe(raw_reads_dir, working_dir)
        paired_end_sequences = load_sequences_to_qiime2(False, prepared_for_qiime2_reads_dir, output_dir)
        sequences = merging(paired_end_sequences, output_dir)

    #dereplication
    dereplicated_table, dereplicated_sequences = dereplication(sequences, output_dir)

    #OTUs (clustering)
    clustered_table, clustered_sequences = otu_clustering(dereplicated_table, dereplicated_sequences, output_dir)

    # taxonomy classification
    taxonomy = taxonomy_classification(clustered_table, clustered_sequences, output_dir)


if __name__ == "__main__":
    main()
