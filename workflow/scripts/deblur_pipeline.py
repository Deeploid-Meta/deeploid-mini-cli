import gzip
import shutil
import argparse
from pathlib import Path

import pandas as pd
from qiime2.sdk import PluginManager

import qiime2

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description='deblur pipeline')
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
        '-db', '--database', help='Path to database (fasta/qza)',
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
    parser.add_argument(
        '--trim_length', help='deblur denoise-16S - trim_length',
        required=False, default=150, type=int)
    parser.add_argument(
        '--left_trim_len', help='deblur denoise-16S - left_trim_len',
        required=False, default=30, type=int)
    parser.add_argument(
        '--sample_stats', help='If true, gather stats per sample.',
        required=False, default=True, type=bool)
    return parser

def prepare_data_for_qiime_pipeline(forward_raw_reads: Path,
                                    reverse_raw_reads: Path,
                                    working_dir: Path) -> str:
    ''' Prepare files for qiime pipeline (should be gz files with _R1_001.fastq.gz
        and _R2_001.fastq.gz in filename)
    '''
    sample_name = forward_raw_reads.name.split('_')[0]
    with open(forward_raw_reads, 'rb') as f_in:
        with gzip.open(working_dir / f'{sample_name}_1_L001_R1_001.fastq.gz',
                       'wb') as f_out:
            f_out.writelines(f_in)
    with open(reverse_raw_reads, 'rb') as f_in:
        with gzip.open(working_dir / f'{sample_name}_2_L001_R2_001.fastq.gz',
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
    manifest.to_csv(working_dir / 'MANIFEST', index=False)

    # Prepare metadata file
    with open(working_dir / 'metadata.yml', 'w') as f:
        f.write('')
    return sample_name


def main():
    """
    Pipeline for metagenomics 16s data anlysis using vsearch
    """
    # Create parser
    parser = build_parser()
    args = vars(parser.parse_args())
    
    # Create raw_reads
    forward_raw_reads = Path(args['forward_reads'])
    reverse_raw_reads = Path(args['reverse_reads'])
    
    # Create output directory
    output_dir = Path(args['outdir'] + '/deblur')
    output_dir.mkdir(exist_ok=True)

    # Create working directory
    working_dir = output_dir / Path('working_dir')
    working_dir.mkdir(exist_ok=True)

    sample_name = prepare_data_for_qiime_pipeline(
        forward_raw_reads, reverse_raw_reads, working_dir)

    # Create qiime2 artifacts directory
    qiime2_artifacts = output_dir / 'qiime2_artifacts'
    qiime2_artifacts.mkdir(exist_ok=True)

    # Create temporary directory
    tmp_output = output_dir / Path('tmp')

    # Create working directory
    working_dir = output_dir / Path('working_dir')
    working_dir.mkdir(exist_ok=True)

    sample_name = prepare_data_for_qiime_pipeline(
        forward_raw_reads, reverse_raw_reads, working_dir)

    # Import data
    paired_end_sequences = qiime2.Artifact.import_data(
        'SampleData[PairedEndSequencesWithQuality]', str(working_dir))
    paired_end_sequences.save(
        str(qiime2_artifacts / 'paired-end-sequences.qza'))
    # paired_end_sequences.export_data(tmp_output)

    num_threads = args['threads']
    # Load plugins
    plugin_manager = PluginManager(True)

    # Use demux for visualization
    demux = plugin_manager.plugins['demux']
    summarize = demux.actions['summarize']
    summary = summarize(data=paired_end_sequences)
    summary.visualization.save(str(qiime2_artifacts / 'demux.qzv'))


    # Use denoise_16S for denoising
    deblur = plugin_manager.plugins['deblur']
#     Perform sequence quality control for Illumina data using the Deblur
# workflow with a 16S reference as a positive filter. Only forward reads are
# supported at this time.
# https://docs.qiime2.org/2022.8/plugins/available/deblur/denoise-16S/?highlight=deblur
    
    denoise_single = deblur.actions['denoise_16S']
    result = denoise_single(
        demultiplexed_seqs=paired_end_sequences,
        trim_length=args['trim_length'],
        jobs_to_start=args['threads'],
        left_trim_len=args['left_trim_len'],
        sample_stats=args['sample_stats']
        )
    
    # Use dada2 for denoising
    # dada2 = plugin_manager.plugins['dada2']

    # denoise_single = dada2.actions['denoise_single']
    # result = denoise_single(
    #     demultiplexed_seqs=paired_end_sequences,
    #     trunc_len=args['trunc_len'],
    #     trim_left=args['trim_left'],
    #     n_threads=num_threads
    #     )

    # denoise_paired = dada2.actions['denoise_paired']
    # print(f'denoise_paired: {denoise_paired.signature}')
    # result = denoise_paired(
    #     demultiplexed_seqs=paired_end_sequences,
    #     trunc_len_f=140,
    #     trunc_len_r=140,
    #     trim_left_f=10,
    #     trim_left_r=10,
    #     )
    result.table.save(str(qiime2_artifacts / 'deblur-stats.qza'))
    result.stats.save(str(qiime2_artifacts / 'table-deblur.qza'))
    result.representative_sequences.save(
        str(qiime2_artifacts / 'rep-seqs-deblur.qza'))
    
    # # Use metadata plugin for visualization stats - tabulate
    metadata = plugin_manager.plugins['metadata']
    tabulate = metadata.actions['tabulate']
    # tab_denoising_stats = tabulate(result.table)
    
    # tab_denoising_stats.visualization.save(
    #     str(qiime2_artifacts / 'tab_denoising_stats.qzv'))
    # tab_denoising_stats.visualization.export_data(tmp_output)

    # Use metadata plugin for visualization stats qiime deblur visualize-stats 
    tabulate_sequences = deblur.actions['visualize_stats']
    tab_seqs = tabulate_sequences(result.stats)
    tab_seqs.visualization.export_data(tmp_output / 'tab_seqs')
    # Use feature-table plugin for visualization table - summarize
    feature_table = plugin_manager.plugins['feature-table']
    summarize = feature_table.actions['summarize']
    result_table_summary = summarize(table=result.table)
    result_table_summary.visualization.export_data(
        tmp_output / 'table_summary')
    feature_freqs = pd.read_csv(
        tmp_output / 'table_summary' / 'feature-frequency-detail.csv',
        names=['feature_id', 'frequency'],
        skiprows=1)

    # Use feature-table plugin for visualization table - tabulate-seqs
    tabulate_sequences = feature_table.actions['tabulate_seqs']
    tab_seqs = tabulate_sequences(data=result.representative_sequences)
    tab_seqs.visualization.export_data(tmp_output / 'tab_seqs')

    # read fasta file and join it with feature_freqs
    with open(tmp_output / 'tab_seqs' / 'sequences.fasta', 'r') as f:
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
    df_seqs_freqs.drop('feature_id', axis=1).to_csv(output_dir / 'ASV.csv',
                                                    index=False)

    # Use feature-classifier plugin for taxonomy assignment
    classifier_path = Path(args['database'])
    feature_classifier = plugin_manager.plugins['feature-classifier']
    classify_sklearn = feature_classifier.actions['classify_sklearn']
    classifier = qiime2.Artifact.load(classifier_path)

    result_taxonomy = classify_sklearn(reads=result.representative_sequences,
                                       classifier=classifier,
                                       n_jobs=num_threads)
    result_taxonomy.classification.save(str(qiime2_artifacts / 'taxonomy.qza'))

    tab_taxonomy = tabulate(
        result_taxonomy.classification.view(qiime2.Metadata))
    tab_taxonomy.visualization.save(str(qiime2_artifacts / 'taxonomy.qzv'))
    tab_taxonomy.visualization.export_data(tmp_output / 'taxonomy')

    # Save taxonomy to tsv file
    taxanomy_metadata = pd.read_csv(
        tmp_output / 'taxonomy' / 'metadata.tsv',
        sep='\t',
        skiprows=2,
        names=['feature_id', 'taxonomy', 'confidence'])
    taxonomy = df_seqs_freqs.merge(
        taxanomy_metadata, on='feature_id', how='left')
    taxonomy.drop('feature_id', axis=1).to_csv(
        output_dir / 'taxonomy.tsv', index=False, sep='\t')

    # Use taxa plugin for visualization taxonomy - barplot
    taxa = plugin_manager.plugins['taxa']
    barplot = taxa.actions['barplot']
    result_barplot = barplot(table=result.table,
                             taxonomy=result_taxonomy.classification)
    result_barplot.visualization.save(str(qiime2_artifacts / 'barplot.qzv'))

    # Remove temporary files
    shutil.rmtree(working_dir)
    shutil.rmtree(tmp_output)


if __name__ == "__main__":
    main()
