# работа без багов V1 (MVP для qiime2)

При запуске qiime2_2020_8_py36.yaml и скрипта ниже **ВСЕ РАБОТАЕТ** папка `path/output` создается и в ней появляются `ASV.csv, taxonomy.tsv и папка qiime2_artifacts`

```
python3 deeploid_cli.py --tool qiime2 -1 data/standart_dataset/mock_2_R1.fastq -2 data/standart_dataset/mock_2_R2.fastq -db databases/GG/85_otus.fasta -tx databases/GG/85_otu_taxonomy.txt -o path/output
```

# Full instruction V1

## Install, set and run


Snakemake can be installed with all goodies needed to run in any environment and for creating interactive reports via

```shs
$ conda activate base
$ mamba create -c conda-forge -c bioconda -n snakemake snakemake
```

from the Bioconda channel. This will install snakemake into an isolated software environment, that has to be activated with

```sh
$ conda activate snakemake
$ snakemake --help
```

Installing into isolated environments is best practice in order to avoid side effects with other packages.

`Note that full installation is not possible from Windows`, because some of the dependencies are Unix (Linux/MacOS) only. `For Windows`, please use the minimal installation below.

## Minimal installation
A minimal version of Snakemake which only depends on the bare necessities can be installed with

```
$ conda activate base
$ mamba create -c bioconda -c conda-forge -n snakemake snakemake-minimal
```

In contrast to the full installation, which depends on some Unix (Linux/MacOS) only packages, this also works on Windows.

# Запуск скрипта dada2

#### Версия от Марго со снейком и ее пайплайном

```
python3 deeploid_cli.py --tool dada2  -1 data/standart_dataset/mock_2_R1.fastq -2 data/standart_dataset/mock_2_R2.fastq -db databases/silva_nr99_v138.1_train_set.fa.gz -o path/output
```

```bash
Rscript dada2_OTU_full.R -p <path/to/folder/with/fastq> -1 '*_R1.fastq.gz' -2 '*_R2.fastq.gz' -o <path/to/output/folder>
```

#### Версия от Никиты со снейком

```
python3 deeploid_cli.py --tool dada2 -1 data/standart_dataset/mock_2_R1.fastq -2 data/standart_dataset/mock_2_R2.fastq -db databases/GG/85_otus.fasta -o path/output
```

```bash
Rscript dada2_OTU_full.R -p <path/to/folder/with/fastq> -1 '*_R1.fastq.gz' -2 '*_R2.fastq.gz' -o <path/to/output/folder>
```

#### Версия от Даши

`pipeline/dada2_OTU_full.R` - скрипт для запуска дады до этапа OTU ТОЛЬКО с форвард и реверс ридами.
Пример запуска:
```bash
python3 deeploid_cli.py --tool dada2 -1 data/standart_dataset/mock_2_R1.fastq -2 data/standart_dataset/mock_2_R2.fastq -db databases/GG/85_otus.fasta -o path/output
```
`pipeline/dada2_taxa_full.R` - скрипт для запуска дады до этапа таксономии ТОЛЬКО с форвард и реверс ридами.
Пример запуска:
```bash
Rscript dada2_taxa_full.R -p <path/to/folder/with/fastq> -1 '*_R1.fastq.gz' -2 '*_R2.fastq.gz' -o <path/to/output/folder> -db <path/to/folder/database_training_set>
```

# Запуск скрипта deblur

#### Версия от Марго со снейком и ее пайплайном

```bash
python3 deeploid_cli.py --tool deblur -1 data/standart_dataset/mock_2_R1.fastq -2 data/standart_dataset/mock_2_R2.fastq /
-db databases/GG/85_otus.fasta -tx databases/GG/85_otu_taxonomy.txt -o path/output
```