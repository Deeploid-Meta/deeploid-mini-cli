## Full instruction V1

### Install, set and run

Snakemake can be installed with all goodies needed to run in any environment and for creating interactive reports via

```sh
conda activate base
mamba create -c conda-forge -c bioconda -n snakemake snakemake
```

from the Bioconda channel. This will install snakemake into an isolated software environment, that has to be activated with

```sh
conda activate snakemake
snakemake --help
```

Installing into isolated environments is best practice in order to avoid side effects with other packages.

`Note that full installation is not possible from Windows`, because some of the dependencies are Unix (Linux/MacOS) only. `For Windows`, please use the minimal installation below.

### Minimal installation

A minimal version of Snakemake which only depends on the bare necessities can be installed with

```sh
conda activate base
mamba create -c bioconda -c conda-forge -n snakemake snakemake-minimal
```

In contrast to the full installation, which depends on some Unix (Linux/MacOS) only packages, this also works on Windows.

## MVP

При запуске любого скрипта создается папка `path/output` и в ней появляются `ASV.csv, taxonomy.tsv и папка pipeline_artifacts`

- deblur_pipeline.py

    python3 deeploid_cli.py -t deblur -1 data/standart_dataset/mock_2_R1.fastq -2 data/standart_dataset/mock_2_R2.fastq -db databases/GG/85_otus_classifier.qza -tx databases/GG/85_otu_taxonomy.txt -o path/output

- qiime2_pipeline.py

    python3 deeploid_cli.py -t qiime2 -1 data/standart_dataset/mock_2_R1.fastq -2 data/standart_dataset/mock_2_R2.fastq -db databases/GG/85_otus.fasta -tx databases/GG/85_otu_taxonomy.txt -o path/output

- dada2_pipeline.R

    python3 deeploid_cli.py -t dada2 -1 mock_2_R1.fastq -2 mock_2_R2.fastq -db databases/silva_nr99_v138.1_train_set.fa.gz -o path/output

- vsearch_pipeline.py

    python3 deeploid_cli.py -t vsearch -1 data/standart_dataset/mock_2_R1.fastq -2 data/standart_dataset/mock_2_R2.fastq -db databases/GG/85_otus_classifier.qza -o path/output

## Structure snakemake workflow

```py
workflow
├──envs # Combat environment dependencies for SnakeMake
│   ├── dada2.yaml 
│   ├── vsearch.yaml 
│   ├── deblur.yaml
│   ├── qiime2.yaml
│   ├── README.md
│   └── history # Test environment dependencies for SnakeMake
│       ├── qiime2_2020_8_py36.yaml
│       ├── qiime2_2022_8_py38.yaml
│       ├── qiime2_2022_11_py38.yaml
│       └── qiime2_2023_2_py38.yaml
├──rules # Pipeline`s rules for SnakeMake
│   ├── dada2.smk
│   ├── deblur.smk
│   ├── qiime2.smk
│   ├── vsearch.smk
│   └── README.md
├──scripts # Pipelines for taxonomy
│   ├── markdown # docs for pipelines
│   ├── qiime_pipleline.py
│   ├── dada_pipleline.py
│   ├── deblur_pipleline.py
│   ├── vsearch_pipleline.py
│   └── README.md
├──snakefile # main SnakeMake with architecture
└──README.md
```
