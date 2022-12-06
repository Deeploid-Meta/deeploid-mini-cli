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
    
    qiime2_data = Path('vsearch_data')
    qiime2_data.mkdir(exist_ok=True)
    
    qiime2_artifacts = Path('vsearch_artifacts')
    qiime2_artifacts.mkdir(exist_ok=True)
    
    
    
    for i in range(1, 3):
        with open(data / f'{sample_name}_{i}.fastq', 'rb') as f_in:
            with gzip.open(qiime2_data / f'{sample_name}_{i}_L001_R{i}_001.fastq.gz', 'wb') as f_out:
                f_out.writelines(f_in)
    
    #importing data to qiime2
    paired_end_sequences = qiime2.Artifact.import_data('SampleData[PairedEndSequencesWithQuality]', 'vsearch_data')
    paired_end_sequences.save(str(qiime2_artifacts / 'paired-end-sequences.qza'))
    
    
    #merging
    plugin_manager = PluginManager(True)
    vsearch = plugin_manager.plugins["vsearch"]
    
    join_pairs = vsearch.actions["join_pairs"]
    result = join_pairs(demultiplexed_seqs=paired_end_sequences)
    print(result)
    
    joined_sequences = result.joined_sequences
    joined_sequences.save(str(qiime2_artifacts / 'joined-sequences.qza'))
    
    
    #dereplication
    dereplicate_sequences = vsearch.actions["dereplicate_sequences"]
    result = dereplicate_sequences(sequences = joined_sequences)
    print(result)
    
    
    dereplicated_table = result.dereplicated_table
    dereplicated_sequences = result.dereplicated_sequences
    
    dereplicated_sequences.save(str(qiime2_artifacts / 'dereplicated_sequences.qza'))
    dereplicated_table.save(str(qiime2_artifacts / 'dereplicated_table.qza'))
    
    
    #OTUs (clustering)
    
    cluster_features_de_novo = vsearch.actions["cluster_features_de_novo"]
    result = cluster_features_de_novo(sequences = dereplicated_sequences, table = dereplicated_table, perc_identity = 0.97)
    print(result)
    
    clustered_table = result.clustered_table
    clustered_sequences = result.clustered_sequences
    
    clustered_table.save(str(qiime2_artifacts / 'clustered_table.qza'))
    clustered_sequences.save(str(qiime2_artifacts / 'clustered_sequences.qza'))



if __name__ == "__main__":
    main()
