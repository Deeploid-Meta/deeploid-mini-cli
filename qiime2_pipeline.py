import gzip
import shutil
from pathlib import Path

import pandas as pd
import qiime2.plugins as plugins
from qiime2.sdk import PluginManager

import qiime2


def main():
    data = Path('data')
    sample_name = 'SRR22104214'

    qiime2_data = data / 'qiime2'
    qiime2_data.mkdir(exist_ok=True)

    qiime2_artifacts = data / 'qiime2_artifacts'
    qiime2_artifacts.mkdir(exist_ok=True)

    # Rename files
    for i in range(1, 3):
        with open(data / f'{sample_name}_{i}.fastq', 'rb') as f_in:
            with gzip.open(qiime2_data / f'{sample_name}_{i}_L001_R{i}_001.fastq.gz', 'wb') as f_out:
                f_out.writelines(f_in)
    paired_end_sequences = qiime2.Artifact.import_data('SampleData[PairedEndSequencesWithQuality]', 'data/qiime2')
    paired_end_sequences.save(str(qiime2_artifacts / 'paired-end-sequences.qza'))

    tmp_output = Path('data/qiime2_artifacts/test')
    paired_end_sequences.export_data(tmp_output)

    # Load plugins
    print(plugins.available_plugins())
    plugin_manager = PluginManager(True)
    

    # Use demux for visualization
    demux = plugin_manager.plugins['demux']
    # print(f'demux: {demux}')
    # print(f'demux actions: {demux.actions}')
    summarize = demux.actions['summarize']
    # print(f'summarize: {summarize}')
    # print(summarize.signature)
    # print(f'paired_end_sequences.type: {paired_end_sequences.type}')
    # print(f'type(paired_end_sequences): {type(paired_end_sequences)}')
    summary = summarize(data=paired_end_sequences)
    # print(f'summary: {summary}')
    # print(f'summary type: {type(summary)}')
    # print(summary.visualization)
    # print(type(summary.visualization))
    summary.visualization.save(str(qiime2_artifacts / 'demux.qzv'))


    # Use dada2 for denoising
    dada2 = plugin_manager.plugins['dada2']
    # print(f'dada2: {dada2}')
    # print(f'dada2 actions: {dada2.actions}')
    denoise_single = dada2.actions['denoise_single']
    # print(f'denoise_single: {denoise_single.signature}')
    result = denoise_single(
        demultiplexed_seqs=paired_end_sequences,
        trunc_len=150,
        trim_left=30,
        )
    print(result)
    result.table.save(str(qiime2_artifacts / 'table.qza'))
    result.representative_sequences.save(str(qiime2_artifacts / 'representative_sequences.qza'))
    result.denoising_stats.save(str(qiime2_artifacts / 'denoising_stats.qza'))

    # Use metadata plugin for visualization stats - tabulate
    metadata = plugin_manager.plugins['metadata']
    # print(f'metadata: {metadata}')
    # print(f'metadata actions: {metadata.actions}')
    tabulate = metadata.actions['tabulate']
    # print(f'tabulate: {tabulate}')
    # print(tabulate.signature)
    # print(result.denoising_stats)
    tab_denoising_stats = tabulate(result.denoising_stats.view(qiime2.Metadata))
    tab_denoising_stats.visualization.save(str(qiime2_artifacts / 'tab_denoising_stats.qzv'))
    # print(tab_denoising_stats.visualization)
    # print(type(tab_denoising_stats.visualization))
    # print(tab_denoising_stats.visualization._archiver.path)
    
    tab_denoising_stats.visualization.export_data(tmp_output)
    df_denoising_stats = pd.read_csv(tmp_output / 'metadata.tsv', sep='\t', skiprows=[1])
    print(df_denoising_stats)

    # Use feature-table plugin for visualization table - summarize
    feature_table = plugin_manager.plugins['feature-table']
    # print(f'feature_table: {feature_table}')
    # print(f'feature_table actions: {feature_table.actions}')
    summarize = feature_table.actions['summarize']
    # print(f'summarize: {summarize}')
    # print(summarize.signature)
    result_table_summary = summarize(table=result.table)
    # print(f'result_table_summary: {result_table_summary}')
    result_table_summary.visualization.export_data(tmp_output)
    feature_freqs = pd.read_csv(tmp_output / 'feature-frequency-detail.csv',
                                names=['feature_id', 'frequency'],
                                skiprows=1)
    print(feature_freqs.head(10))

    # Use feature-table plugin for visualization table - tabulate-seqs
    tabulate_sequences = feature_table.actions['tabulate_seqs']
    # print(f'tabulate_sequences: {tabulate_sequences}')
    # print(tabulate_sequences.signature)
    tab_seqs = tabulate_sequences(data=result.representative_sequences)
    # print(f'tab_seqs: {tab_seqs}')
    tab_seqs.visualization.export_data(tmp_output)
    # read fasta file and join it with feature_freqs
    with open(tmp_output / 'sequences.fasta', 'r') as f:
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
    print(df_seqs.head(10))
    df_seqs_freqs = pd.merge(df_seqs, feature_freqs, on='feature_id')
    print(df_seqs_freqs.head(10))
    

if __name__ == "__main__":
    main()
