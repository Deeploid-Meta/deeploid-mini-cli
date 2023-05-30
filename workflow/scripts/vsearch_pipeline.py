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
import os
import argparse

plugin_manager = PluginManager(True)
vsearch = plugin_manager.plugins["vsearch"]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='vsearch pipeline for 16s rrna data analysis')
    parser.add_argument(
        '-1', '--forward_reads',
        help='Forward reads file (or single-end) in fastq|fq|gz|tar.gz format',
        required=True)
    parser.add_argument(
        '-2', '--reverse_reads',
        help='Reverse reads file in fastq|fq|gz|tar.gz format', required=False,
        default=False)
    parser.add_argument(
        '-o', '--outdir', help='Output folder (default = reads folder)',
        required=False, default=False)
    parser.add_argument(
        '-p', '--prefix',
        help='Output file prefix (default = prefix of original file)',
        required=False, default=False)
    parser.add_argument(
        '-db', '--database', help='Path to database (fasta)',
        required=False, default=False)
    parser.add_argument(
        '-tx', '--taxonomy', help='Path to database taxonomy (txt)',
        required=False, default=False)
    parser.add_argument(
        '-t', '--threads', help='Number of threads (default = 8)',
        required=False, default=8, type=int)
    parser.add_argument(
        '--trunc_len', help='dada2 denoise_single - trunc length',
        required=False, default=150, type=int)
    parser.add_argument(
        '--trim_left', help='dada2 denoise_single - trim left',
        required=False, default=30, type=int)
    return parser

def prepare_data_pe(forward_raw_reads: Path,
                    reverse_raw_reads: Path,
                    working_dir: Path) -> str:
    ''' Prepare files for vsearch pipeline (should be gz files with _R1_001.fastq.gz
        and _R2_001.fastq.gz in filename)
    '''

    prepared_for_qiime2_reads_dir = working_dir / Path('prepared_data')
    prepared_for_qiime2_reads_dir.mkdir(exist_ok=True)

    sample_name = forward_raw_reads.name.split('_')[0]
    with open(forward_raw_reads, 'rb') as f_in:
        with gzip.open(prepared_for_qiime2_reads_dir / f'{sample_name}_1_L001_R1_001.fastq.gz',
                       'wb') as f_out:
            f_out.writelines(f_in)
    with open(reverse_raw_reads, 'rb') as f_in:
        with gzip.open(prepared_for_qiime2_reads_dir / f'{sample_name}_2_L001_R2_001.fastq.gz',
                       'wb') as f_out:
            f_out.writelines(f_in)

    # Prepare MANIFEST file
    manifest_data = []
    manifest_data.append(
        [sample_name, str(f'{sample_name}_1_L001_R1_001.fastq.gz'), 'forward'])
    manifest_data.append(
        [sample_name, str(f'{sample_name}_2_L001_R2_001.fastq.gz'), 'reverse'])
    manifest = pd.DataFrame(
        manifest_data, columns=['sample-id', 'filename', 'direction'])
    manifest.to_csv(prepared_for_qiime2_reads_dir / 'MANIFEST', index=False)

    # Prepare metadata file
    with open(prepared_for_qiime2_reads_dir / 'metadata.yml', 'w') as f:
        f.write('phred-offset: 33')

    return prepared_for_qiime2_reads_dir, sample_name



def prepare_data_se(forward_raw_reads,
                    working_dir):
    ''' Prepare sindle ended files for qiime pipeline
    (should be gz files with _R1_001.fastq.gz
    and _R2_001.fastq.gz in filename)
    '''
    prepared_for_qiime2_reads_dir = working_dir / Path('prepared_data')
    prepared_for_qiime2_reads_dir.mkdir(exist_ok=True)

    sample_name = forward_raw_reads.name.split('_')[0]

    with open(forward_raw_reads, 'rb') as f_in:
        with gzip.open(prepared_for_qiime2_reads_dir / f'{sample_name}_1_L001_R1_001.fastq.gz',
                       'wb') as f_out:
            f_out.writelines(f_in)

    # Prepare MANIFEST file
    manifest_data = []
    manifest_data.append(
        [sample_name, str(f'{sample_name}_1_L001_R1_001.fastq.gz'), 'forward'])
    manifest = pd.DataFrame(
        manifest_data, columns=['sample-id', 'filename', 'direction'])
    manifest.to_csv(prepared_for_qiime2_reads_dir / 'MANIFEST', index=False)


    # Prepare metadata file
    with open(prepared_for_qiime2_reads_dir / 'metadata.yml', 'w') as f:
        f.write('phred-offset: 33')

    return prepared_for_qiime2_reads_dir, sample_name


def load_sequences_to_qiime2(prepared_for_qiime2_reads_dir, output_dir):
    """
    Imports data to qiime2
    """

    paired_end_sequences = qiime2.Artifact.import_data('SampleData[PairedEndSequencesWithQuality]', prepared_for_qiime2_reads_dir)
    paired_end_sequences.save(str(output_dir / 'paired-end-sequences.qza'))
    os.system(f'rm -rf {prepared_for_qiime2_reads_dir}')

    return paired_end_sequences



def trimming(is_single_ended, raw_reads_path, working_dir):
    """Trims raw data"""
    reads_names = os.listdir(raw_reads_path)
    reads_names = [x for x in reads_names if '.fastq' in x or '.fq' in x]
    sample_names = list(set([x.split('_')[0] for x in reads_names]))

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

    join_pairs = vsearch.actions["merge_pairs"]
    result = join_pairs(demultiplexed_seqs=paired_end_sequences)

    print(result)

    joined_sequences = result.merged_sequences
    joined_sequences.save(str(vsearch_artifacts / 'joined-sequences.qza'))

    return joined_sequences

def dereplication(joined_sequences, vsearch_artifacts):
    """
    Dereplication of joined sequences
    """

    dereplicate_sequences = vsearch.actions["dereplicate_sequences"]
    result = dereplicate_sequences(sequences=joined_sequences)

    print(result)

    dereplicated_table = result.dereplicated_table
    dereplicated_sequences = result.dereplicated_sequences

    dereplicated_sequences.save(str(vsearch_artifacts / 'dereplicated_sequences.qza'))
    dereplicated_table.save(str(vsearch_artifacts / 'dereplicated_table.qza'))


    return dereplicated_table, dereplicated_sequences

def otu_clustering(dereplicated_table, dereplicated_sequences, vsearch_artifacts, sample_name):
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

    feature_table = plugin_manager.plugins['feature-table']
    summarize = feature_table.actions['summarize']
    result_table_summary = summarize(table=clustered_table)
    result_table_summary.visualization.export_data(
        vsearch_artifacts / 'table_summary')

    feature_freqs = pd.read_csv(
        vsearch_artifacts / 'table_summary' / 'feature-frequency-detail.csv',
        names=['feature_id', 'frequency'],
        skiprows=1)

    print(feature_freqs.head())

    tabulate_sequences = feature_table.actions['tabulate_seqs']
    tab_seqs = tabulate_sequences(data=clustered_sequences)
    tab_seqs.visualization.export_data(vsearch_artifacts / 'tab_seqs')

    # read fasta file and join it with feature_freqs
    with open(vsearch_artifacts / 'tab_seqs' / 'sequences.fasta', 'r') as f:
        seq_ids = []
        seqs = []
        for i, line in enumerate(f.readlines()):
            if i % 2 == 0:
                seq_id = line[1:].rstrip()
                seq_ids.append(seq_id)
            else:
                sequence = line.rstrip()
                seqs.append(sequence)

    df_seqs = pd.DataFrame({'feature_id': seq_ids, 'sequence': seqs})
    df_seqs_freqs = pd.merge(df_seqs, feature_freqs, on='feature_id')

    # Save OTU table
    df_seqs_freqs['frequency'] = df_seqs_freqs['frequency'].astype(int)
    df_seqs_freqs.rename(columns={'frequency': sample_name}, inplace=True)
    df_seqs_freqs.drop('feature_id', axis=1).to_csv(vsearch_artifacts / 'ASV.csv',
                                                    index=False)


    return clustered_table, clustered_sequences, df_seqs_freqs


def taxonomy_classification(clustered_table, clustered_sequences,
                            vsearch_artifacts, df_seqs_freqs, classifier_qza):
    """
    Does taxonomy classification, saves visualizations for taxonomy
    """

    fn = classifier_qza
    # 'databases/GG/85_otus_classifier.qza'
    # fn = 'gg-13-8-99-515-806-nb-classifier.qza'

    try:
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

    metadata = plugin_manager.plugins['metadata']
    tabulate = metadata.actions['tabulate']
    tab_taxonomy = tabulate(taxonomy.view(qiime2.Metadata))
    tab_taxonomy.visualization.export_data(vsearch_artifacts / 'taxonomy')

    # Use taxa plugin for visualization taxonomy - barplot
    taxa = plugin_manager.plugins['taxa']
    barplot = taxa.actions['barplot']
    result_barplot = barplot(table=clustered_table,
                             taxonomy=taxonomy)
    print(f'result_barplot: {result_barplot}')

    result_barplot.visualization.save(str(vsearch_artifacts / 'barplot.qzv'))

    # Save taxonomy to tsv file
    taxanomy_metadata = pd.read_csv(
        vsearch_artifacts / 'taxonomy' / 'metadata.tsv',
        sep='\t',
        skiprows=2,
        names=['feature_id', 'taxonomy', 'confidence'])
    taxonomy_table = df_seqs_freqs.merge(
        taxanomy_metadata, on='feature_id', how='left')
    taxonomy_table.drop('feature_id', axis=1).to_csv(
        vsearch_artifacts / 'taxonomy.tsv', index=False, sep='\t')

    return taxonomy


def main():
    """
    Pipeline for metagenomics 16s data anlysis using vsearch
    """
    # Create raw_reads
    parser = build_parser()
    args = vars(parser.parse_args())

    # Create raw_reads
    forward_raw_reads = Path(args['forward_reads'])
    reverse_raw_reads = Path(args['reverse_reads'])

    # Create output directory
    output_dir = Path(args['outdir'] + '/vsearch')
    output_dir.mkdir(exist_ok=True)

    # Create working directory
    working_dir = output_dir / Path('working_dir')
    working_dir.mkdir(exist_ok=True)

    # preprocessing and importing data

    prepared_for_qiime2_reads_dir, sample_name = prepare_data_pe(forward_raw_reads, reverse_raw_reads, working_dir)
    paired_end_sequences = load_sequences_to_qiime2(prepared_for_qiime2_reads_dir, output_dir)
    sequences = merging(paired_end_sequences, output_dir)

    # dereplication
    dereplicated_table, dereplicated_sequences = dereplication(sequences, output_dir)

    # OTUs (clustering)
    clustered_table, clustered_sequences, df_seqs_freqs = otu_clustering(dereplicated_table, dereplicated_sequences, output_dir, sample_name)

    # taxonomy classification
    classifier_qza = Path(args['database'])
    taxonomy = taxonomy_classification(clustered_table, clustered_sequences, output_dir, df_seqs_freqs, classifier_qza)

    # delete dirs:
    # to_delete = [i for i in os.listdir(output_dir) if not i.endswith(('.csv', '.tsv', '.qza', '.qzv'))]
    # for k in to_delete:
    #     print(f'{str(output_dir) + "/" + k} will be removed')
    #     #os.system(f'rm -r {str(output_dir) + "/" + k}')
    #     path_temp = output_dir / Path(k)
    #     shutil.rmtree(path_temp)

if __name__ == "__main__":
    main()
