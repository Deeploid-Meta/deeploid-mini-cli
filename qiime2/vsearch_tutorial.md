# VSEARCH
Будем использовать vsearch, который есть в виде плагина в qiime. Запускал из докера.

## Подготовка данных
Загрузить данные с помощью SRA-tools. Их можно установить в докере с помощью конды.


**Установка sra-tools на линукс с помощью конды**

conda config --add channels bioconda
conda config --add channels conda-forge

conda create -n sratool sra-tools
conda activate sratools

**Загрузка данных**

prefetch SRR22104214
cd SRR22104214
fastq-dump --split-files SRR22104214.sra

Затем создаем manifest.tsv (apt-get udate && apt install nano && nano manifest.tsv):
```
sample-id       forward-absolute-filepath       reverse-absolute-filepath
sample-1        /data/SRR22104214/SRR22104214_1.fastq   /data/SRR22104214/SRR22104214_2.fastq
```
conda deactivate

**Импорт данных в qiime**

qiime tools import --type 'SampleData[PairedEndSequencesWithQuality]' --input-path manifest.tsv --output-path paired-end-demux.qza --input-format PairedEndFastqManifestPhred33V2


Для dada нужны два файла, vsearch требуется один. Делаем его с помощью данной команды из сырых данных:

qiime vsearch join-pairs --i-demultiplexed-seqs paired-end-demux.qza --o-joined-sequences joined.qza

Результат: 
Saved SampleData[JoinedSequencesWithQuality] to: joined.qza

## Дерепликация

qiime vsearch dereplicate-sequences \
  --i-sequences joined.qza \
  --o-dereplicated-table table-vs.qza \
  --o-dereplicated-sequences rep-seqs-vs.qza
  
Результат:
Saved FeatureTable[Frequency] to: table-vs.qza
Saved FeatureData[Sequence] to: rep-seqs-vs.qza
 
## Clustering
de-novo clustering

qiime vsearch cluster-features-de-novo \
  --i-table table-vs.qza \
  --i-sequences rep-seqs-vs.qza \
  --p-perc-identity 0.99 \
  --o-clustered-table table-dn-99-vs.qza \
  --o-clustered-sequences rep-seqs-dn-99-vs.qza


## Визуализация 
qiime vsearch fastq-stats --i-sequences paired-end-demux.qza --o-visualization vsearch_stats.qzv

Результат:
Saved Visualization to: vsearch_stats.qzv

