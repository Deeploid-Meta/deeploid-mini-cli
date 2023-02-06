Deblur
======

Deblur is a greedy deconvolution algorithm for amplicon sequencing based on Illumina Miseq/Hiseq error profiles.

ЧЕрез windows не запускается

```
conda install -c conda-forge mamba
mamba create -n qiime2 -c qiime2 -c bioconda -c conda-forge -c defaults qiime2
conda deactivate base
conda activate qiime2
```

Install
=======
- Deblur requires Python 3.8. If Python 3.8 is not installed, you can create a [conda](http://conda.pydata.org/docs/install/quick.html) environment for Deblur using:

для WSL [ссылка](https://docs.qiime2.org/2022.8/install/native/)

```
conda update conda
conda install wget
wget https://data.qiime2.org/distro/core/qiime2-2022.8-py38-linux-conda.yml
conda env create -n qiime2 --file qiime2-2022.8-py38-linux-conda.yml
rm qiime2-2022.8-py38-linux-conda.yml
conda deactivate base
conda activate qiime2

```

## С сайта [1](https://www.nicholas-ollberding.com/post/denoising-amplicon-sequence-variants-using-dada2-deblur-and-unoise3-with-qiime2/)

Возможный пайплайн

```
#BSUB -W 10:00
#BSUB -M 64000
#BSUB -n 10
#BSUB -e /data/MMAC-Shared-Drive/scratch/%J.err
#BSUB -o /data/MMAC-Shared-Drive/scratch/%J.out


#Script to run DeBlur workflow for 16S V4 reads via QIIME2
# - Denoising: DeBlur (merge F and R reads using vsearch)
# - Taxonomic classification: GG13_8 Naive Bayesian classifier
# - Phylogenetic tree: SEPP


#Program Assumes:
# - demultiplexed F and R fastq files are placed in "seqs" folder within project folder
# - files are compressed (.gz)
# - primers and all non-biologic sequences have been removed
# - sequence files are in Casava 1.8 format (if not need to generate QIIME2 sample manifest and place in folder; see example code at bottom)
# - example format for manifest_file.tsv provided below
# - do not generate manifest file in excel due to incompatible line endings
# - DeBlur will not accept underscores in the sample-id field


#Sample Manifest Format:
#sample-id  forward-absolute-filepath   reverse-absolute-filepath
#F3D0.S188  /scratch/olljt2/project/seqs/F3D0_S188_L001_R1_001.fastq    /scratch/olljt2/project/seqs/F3D0_S188_L001_R2_001.fastq
#F3D141.S207    /scratch/olljt2/project/seqs/F3D141_S207_L001_R1_001.fastq  /scratch/olljt2/project/seqs/F3D141_S207_L001_R2_001.fastq
#F3D142.S208    /scratch/olljt2/project/seqs/F3D142_S208_L001_R1_001.fastq  /scratch/olljt2/project/seqs/F3D142_S208_L001_R2_001.fastq


#To run the script 
# - create a new folder for the project
# - change first line of code below to navigate to the project folder
# - navigate to the project folder
# - enter bsub at command line to run: bsub < deblur_v4_qiime2.bat
# - may need to modify wall time etc. given size of project (above should be overkill for single MiSeq run)



#Navigate to project folder (change me)
cd /data/MMAC-Shared-Drive/example_data/example_runs/amplicon/deblur_v4_q2


#Load qiime2
module load qiime/2.2020.2


#Convert fastq files to q2 artifact
mkdir q2
mkdir q2/reports

qiime tools import \
   --type SampleData[PairedEndSequencesWithQuality] \
   --input-path seqs/ \
   --output-path q2/paired-end-demux.qza \
   --input-format CasavaOneEightSingleLanePerSampleDirFmt

qiime demux summarize \
   --i-data q2/paired-end-demux.qza \
   --o-visualization q2/reports/paired-end-demux_summary.qzv


#Denoise reads with DeBlur
cd q2

qiime vsearch join-pairs \
  --i-demultiplexed-seqs paired-end-demux.qza \
  --o-joined-sequences demux-joined.qza \
  --p-minmergelen 240 \
  --p-maxmergelen 270 \
  --p-maxdiffs 10

qiime demux summarize --i-data demux-joined.qza --o-visualization reports/demux-joined.qzv

qiime quality-filter q-score-joined \
  --i-demux demux-joined.qza \
  --o-filtered-sequences demux-filtered.qza \
  --o-filter-stats demux-filter-stats.qza

qiime metadata tabulate --m-input-file demux-filter-stats.qza --o-visualization reports/demux-filter-stats.qzv

qiime deblur denoise-16S \
  --i-demultiplexed-seqs demux-filtered.qza \
  --p-trim-length 240 \
  --o-representative-sequences rep-seqs.qza \
  --o-table table.qza \
  --p-sample-stats \
  --p-jobs-to-start 10 \
  --o-stats deblur-stats.qza
#notes: - trim-length is a tuning parameter and the length should be based on visual examination of the q-score distribution over the read length

qiime deblur visualize-stats --i-deblur-stats deblur-stats.qza --o-visualization reports/deblur-stats.qzv
qiime feature-table summarize --i-table table.qza --o-visualization reports/table.qzv
qiime feature-table tabulate-seqs --i-data rep-seqs.qza --o-visualization reports/rep-seqs.qzv


#Assign taxonomy using pre-trained (515F-806R) GG ref db
qiime feature-classifier classify-sklearn \
  --i-classifier /data/MMAC-Shared-Drive/ref_databases/qiime2/gg-13-8-99-515-806-nb-classifier.qza \
  --i-reads rep-seqs.qza \
  --o-classification taxonomy.qza \
  --p-confidence .8 \
  --p-n-jobs -10

qiime metadata tabulate --m-input-file taxonomy.qza --o-visualization reports/taxonomy.qzv


#Fragment insertion via SEPP for phylogenetic tree
qiime fragment-insertion sepp \
  --i-representative-sequences rep-seqs.qza \
  --i-reference-database /data/MMAC-Shared-Drive/ref_databases/qiime2/sepp-refs-gg-13-8.qza \
  --o-tree tree.qza \
  --o-placements insertion-placements.qza \
  --p-threads 10


#Cleaning up files
mkdir other
mv deblur.log other/.; mv demux-filter-stats.qza other/.; mv paired-end-demux.qza other/.  
mv deblur-stats.qza other/.; mv demux-joined.qza other/.; mv demux-filtered.qza other/. 
mv insertion-placements.qza other/.



#Can drop in code if fastq files are not in Casava 1.8 format (will need to provide manifest_file.tsv)
#qiime tools import \
#  --type 'SampleData[PairedEndSequencesWithQuality]' \
#  --input-path manifest_file.tsv \
#  --output-path q2/paired-end-demux.qza \
#  --input-format PairedEndFastqManifestPhred33V2
```

## С сайта [2](https://telatin.github.io/microbiome-bioinformatics/Metabarcoding-deblur/)

Возможный пайплайн

*Denoising with Deblur*
Deblur is an alternative method to produce a set of denoised sequences. While DADA2 can natively support paired-end reads, Deblur can only manage single-end reads.

We can merge the paired end reads using VSEARCH, that is available as a Qiime2 plugin

*Merge reads with VSEARCH*
The complete documentation of the q2-vsearch plugin contains all the available parameters.

This subprogram merge the overlapping pairs to produce a set of single-end FASTQ file, and will work only when the amplicon are designed with the overlap.

```
qiime vsearch join-pairs \
     --i-demultiplexed-seqs raw-reads.qza \
     --o-joined-sequences joined-reads.qza \
     --p-threads 8
```

*Sequence quality control and feature table construction*
This method filters sequence based on quality scores and the presence of ambiguous base calls.

```
qiime quality-filter q-score \
      --i-demux joined-reads.qza \
      --o-filtered-sequences joined-filtered.qza \
      --o-filter-stats joined-filter-stats.qza
```

*Denoising with deblur*
Deblur requires to process a set of single end reads truncated at the same length (which now should be decided after)

```
qiime deblur denoise-16S \
      --i-demultiplexed-seqs joined-filtered.qza \
      --p-trim-length 245 \
      --p-sample-stats \
      --p-jobs-to-start 32 \
      --o-stats deblur-stats.qza \
      --o-representative-sequences rep-seqs-deblur.qza \
      --o-table table-deblur.qza
```
As usual, we can produce visualization artifacts to summarize the content of:

- representative sequences
- denoising statistics
- feature table

```
qiime deblur visualize-stats \
       --i-deblur-stats deblur-stats.qza \
       --o-visualization deblur-stats.qzv

qiime feature-table tabulate-seqs \
       --i-data rep-seqs-deblur.qza \
       --o-visualization rep-seqs-deblur.qzv

qiime feature-table summarize \
       --i-table table-deblur.qza \
       --m-sample-metadata-file metadata.tsv \
       --o-visualization table-deblur.qzv
```

## Из документации (Qiime2)[https://docs.qiime2.org/2022.8/plugins/available/deblur/denoise-16S/]

Docstring:

```
Usage: qiime deblur denoise-16S [OPTIONS]

  Perform sequence quality control for Illumina data using the Deblur workflow
  with a 16S reference as a positive filter. Only forward reads are supported
  at this time. The specific reference used is the 88% OTUs from Greengenes
  13_8. This mode of operation should only be used when data were generated
  from a 16S amplicon protocol on an Illumina platform. The reference is only
  used to assess whether each sequence is likely to be 16S by a local
  alignment using SortMeRNA with a permissive e-value; the reference is not
  used to characterize the sequences.

Inputs:
  --i-demultiplexed-seqs ARTIFACT SampleData[SequencesWithQuality |
    PairedEndSequencesWithQuality | JoinedSequencesWithQuality]
                         The demultiplexed sequences to be denoised.
                                                                    [required]
Parameters:
  --p-trim-length INTEGER
                         Sequence trim length, specify -1 to disable
                         trimming.                                  [required]
  --p-left-trim-len INTEGER
    Range(0, None)       Sequence trimming from the 5' end. A value of 0 will
                         disable this trim.                       [default: 0]
  --p-sample-stats / --p-no-sample-stats
                         If true, gather stats per sample.    [default: False]
  --p-mean-error NUMBER  The mean per nucleotide error, used for original
                         sequence estimate.                   [default: 0.005]
  --p-indel-prob NUMBER  Insertion/deletion (indel) probability (same for N
                         indels).                              [default: 0.01]
  --p-indel-max INTEGER  Maximum number of insertion/deletions.   [default: 3]
  --p-min-reads INTEGER  Retain only features appearing at least min-reads
                         times across all samples in the resulting feature
                         table.                                  [default: 10]
  --p-min-size INTEGER   In each sample, discard all features with an
                         abundance less than min-size.            [default: 2]
  --p-jobs-to-start INTEGER
                         Number of jobs to start (if to run in parallel).
                                                                  [default: 1]
  --p-hashed-feature-ids / --p-no-hashed-feature-ids
                         If true, hash the feature IDs.        [default: True]
Outputs:
  --o-table ARTIFACT FeatureTable[Frequency]
                         The resulting denoised feature table.      [required]
  --o-representative-sequences ARTIFACT FeatureData[Sequence]
                         The resulting feature sequences.           [required]
  --o-stats ARTIFACT     Per-sample stats if requested.
    DeblurStats                                                     [required]
Miscellaneous:
  --output-dir PATH      Output unspecified results to a directory
  --verbose / --quiet    Display verbose output to stdout and/or stderr
                         during execution of this action. Or silence output if
                         execution is successful (silence is golden).
  --example-data PATH    Write example data and exit.
  --citations            Show citations and exit.
  --help                 Show this message and exit.
```

Display Deblur statistics per sample

```
Docstring:
Usage: qiime deblur visualize-stats [OPTIONS]

  Display Deblur statistics per sample

Inputs:
  --i-deblur-stats ARTIFACT
    DeblurStats        Summary statistics of the Deblur process.    [required]
Outputs:
  --o-visualization VISUALIZATION
                                                                    [required]
Miscellaneous:
  --output-dir PATH    Output unspecified results to a directory
  --verbose / --quiet  Display verbose output to stdout and/or stderr during
                       execution of this action. Or silence output if
                       execution is successful (silence is golden).
  --example-data PATH  Write example data and exit.
  --citations          Show citations and exit.
  --help               Show this message and exit.
```