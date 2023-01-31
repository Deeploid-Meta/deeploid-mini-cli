## Full installation

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

`Note that full installation is not possible from Windows`, because some of the dependencies are Unix (Linux/MacOS) only. For Windows, please use the minimal installation below.

## Minimal installation
A minimal version of Snakemake which only depends on the bare necessities can be installed with

```
$ conda activate base
$ mamba create -c bioconda -c conda-forge -n snakemake snakemake-minimal
```

In contrast to the full installation, which depends on some Unix (Linux/MacOS) only packages, this also works on Windows.

# ATTENTION

Из папки пайплайн убрал скрипты в scripts, но зависимости `не менял`

- [ ] Сначала обернуть пайплайн Миши 
  - [ ] выделить из мишиного скрипта аргументы (они есть в документации)

    **python pipelines/qiime2_pipeline.py `-1` data/standart_dataset/mock_2_R1.fastq `-2` data/standart_dataset/mock_2_R2.fastq `-db` databases/GG/85_otus.fasta `-tx` databases/GG/85_otu_taxonomy.txt `-t` 8 `--outdir` output**

- [ ] Прописать rules (это скрипт, который проверяет все ли файлы на месте и пихает аргументы в скрипт)

```m
    rule cutadapt_pe:
    input:
        get_cutadapt_input,
    output:
        fastq1="results/trimmed/{sample}-{unit}_R1.fastq.gz",
        fastq2="results/trimmed/{sample}-{unit}_R2.fastq.gz",
        qc="results/trimmed/{sample}-{unit}.paired.qc.txt",
    log:
        "logs/cutadapt/{sample}-{unit}.log",
    params:
        others=config["params"]["cutadapt-pe"],
        adapters=lambda w: str(units.loc[w.sample].loc[w.unit, "adapters"]),
    threads: 8
    wrapper:
        "v1.21.4/bio/cutadapt/pe"
```

```m
rule samtools_index:
    input:
        "sorted_reads/{sample}.bam"
    output:
        "sorted_reads/{sample}.bam.bai"
    shell:
        "samtools index {input}"
```


- [ ] Прописать envs ( установщик + версия)
  - [ ] channels: (conda-forge, bioconda) dependencies: (bioconductor-deseq2 =1.38)

- [ ] Snakefile заполняется параллельно, туда инициализация снэйка (вроде как). Там глобальные переменные прописываются (configfile: "config/config.yaml", report: "report/workflow.rst", container: "docker://continuumio/miniconda3", include: "rules/trim.smk") или как у Дани (OUTDIR = config["outdir"], MODE = config["mode"], rule envs: params: repeatmodeler = "../envs/repeatmodeler.yaml")

- [ ] [Логгирование](https://github.com/alperyilmaz/conda-snakemake/blob/master/index.ipynb)
тут и пайпланы можно рисовать автоматически и время отслеживать с помощью BAM-files

- [ ] Скорость выполнения функций (https://snakemake.readthedocs.io/en/stable/executing/monitoring.html)

## Все функции 

[All Options](https://snakemake.readthedocs.io/en/stable/executing/cli.html)~~~~