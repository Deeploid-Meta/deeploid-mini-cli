<p align="center">
  <img src="https://www.genengnews.com/wp-content/uploads/2022/03/p32_TAY-685024919-1392x928.jpg" align="middle"  width="600" />
</p>


<h1 align="center">
 Deeploid mini

 Command Line Interface
</h1S>

<h4 align="center">

![1](https://img.shields.io/badge/python-3.8-aff.svg)
![2](https://img.shields.io/badge/os-linux%2C%20win%2C%20mac-pink.svg)
![3](https://img.shields.io/github/stars/Deeploid-Meta/deeploid-mini-cli?color=ccf)
![4](https://img.shields.io/github/v/release/Deeploid-Meta/deeploid-mini-cli?color=ffa)

</h4>

-----------------------------------------------

<h4 align="center">
  <a href=#features> Features </a> |
  <a href=#installation> Installation </a> |
  <a href=#quick-start> Quick Start </a> |
  <a href=#community> Community </a>
</h4>

-----------------------------------------------
## &#128204;Features

  Начиная процесс анализа метагеномных данных мы столкнулись с тем, что проблемы есть не только с данными, но и с инструментами. Существующие решения не только громоздкие, но и позволяют сделать ошибки неопытным пользователям. А эти ошибки приводят к неправильной интерпретации результатов, что недопустимо, когда это касается, например, здоровья человека.

  Все фишки и преимущества нашего приложения можно посмотреть на нашем сайте [DeepLoid](http://www.deeploid.tech/)

## &#128204;Installation

### Install, set and run (Linux/MacOS)

`Note that full installation is not possible from Windows`, because some of the dependencies are Unix (Linux/MacOS) only. `For Windows`, please use the minimal installation below.

Snakemake can be installed with all goodies needed to run in any environment and for creating interactive reports via

```sh
conda install -n base -c conda-forge mamba
conda activate base
mamba create -c conda-forge -c bioconda -n snakemake snakemake
```

from the Bioconda channel. This will install snakemake into an isolated software environment, that has to be activated with

```sh
conda activate snakemake
snakemake --help
```

Installing into isolated environments is best practice in order to avoid side effects with other packages.

### Minimal installation (Windows)

A minimal version of Snakemake which only depends on the bare necessities can be installed with

```sh
conda install -n base -c conda-forge mamba
conda activate base
mamba create -c bioconda -c conda-forge -n snakemake snakemake-minimal
```

In contrast to the full installation, which depends on some Unix (Linux/MacOS) only packages, this also works on Windows.

## &#128204; Quick Start

After snakemake env activate:

При запуске любого скрипта создается папка `path/output` и в ней появляются `ASV.csv, taxonomy.tsv и папка pipeline_artifacts`

- deblur_pipeline.py

      python3 deeploid_cli.py -t deblur -1 data/standart_dataset/mock_2_R1.fastq -2 data/standart_dataset/mock_2_R2.fastq -db databases/GG/85_otus_classifier.qza -tx databases/GG/85_otu_taxonomy.txt -o path/output

- qiime2_pipeline.py

      python3 deeploid_cli.py -t qiime2 -1 data/standart_dataset/mock_2_R1.fastq -2 data/standart_dataset/mock_2_R2.fastq -db databases/GG/85_otus.fasta -tx databases/GG/85_otu_taxonomy.txt -o path/output

- dada2_pipeline.R

      python3 deeploid_cli.py -t dada2 -1 mock_2_R1.fastq -2 mock_2_R2.fastq -db databases/dada/silva_nr99_v138.1_train_set.fa.gz -o path/output

- vsearch_pipeline.py

      python3 deeploid_cli.py -t vsearch -1 data/standart_dataset/mock_2_R1.fastq -2 data/standart_dataset/mock_2_R2.fastq -db databases/GG/85_otus_classifier.qza -o path/output

## &#128204;Community

### Your team!

* [Михаил](https://t.me/gurev)
* [Дарья](https://t.me/voronik1801)
* [Никита](https://t.me/space_apple)
* [Юрий](https://t.me/yubal42)
* [Данил](https://t.me/danil_zilov)
* [Маргарита](https://t.me/UnderPressureOf)
* [Валентина](https://t.me/Vale_612)

## Цитирование

Если вы используете CLI в своих исследованиях, рассмотрите возможность цитирования

```python
@misc{=Command Line Interface,
    title={High Performance CLI},
    author={Deeploid Contributors},
    howpublished = {\url{https://github.com/Deeploid-Meta/deeploid-mini-cli}},
    year={2023}
}
```

## Благодарность

- [AI Talent Hub](https://ai.itmo.ru/)
- [ПИШ](https://analytics.engineers2030.ru/schools/itmo/)
- [Updating the 97% identity threshold for 16S ribosomal RNA OTUs](https://www.biorxiv.org/content/10.1101/192211v1.full)
- [Comparing bioinformatic pipelines for microbial 16S rRNA amplicon sequencing](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0227434#pone.0227434.s002)


## Лицензия

 [The MIT License](https://opensource.org/licenses/mit-license.php)
