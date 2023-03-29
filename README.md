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
  <a href=#features> Structure </a> |
  <a href=#installation> Installation </a> |
  <a href=#quick-start> Quick Start </a> |
  <a href=#community> Community </a>
</h4>

-----------------------------------------------
## &#128204;Features

  Начиная процесс анализа метагеномных данных мы столкнулись с тем, что проблемы есть не только с данными, но и с инструментами. Существующие решения не только громоздкие, но и позволяют сделать ошибки неопытным пользователям. А эти ошибки приводят к неправильной интерпретации результатов, что недопустимо, когда это касается, например, здоровья человека.

### Пайплайны 
  *Наглядное сравнение:*

- **deeploid_cli**

  ```sh
  #  If you have assembly and RNA-seq reads
   python3 deeploid_cli.py -t vsearch -1 data/standart_dataset/mock_2_R1.fastq -2 data/standart_dataset/mock_2_R2.fastq -db databases/GG/85_otus_classifier.qza -o path/output
  ```

- **qiime2 + deblur**

  ```sh
  qiime tools import \
   --type SampleData[PairedEndSequencesWithQuality] \
   --input-path seqs/ \
   --output-path q2/paired-end-demux.qza \
   --input-format CasavaOneEightSingleLanePerSampleDirFmt

  qiime demux summarize \
   --i-data q2/paired-end-demux.qza \
   --o-visualization q2/reports/paired-end-demux_summary.qzv

  qiime vsearch join-pairs \
  --i-demultiplexed-seqs paired-end-demux.qza \
  --o-joined-sequences demux-joined.qza \
  --p-minmergelen 240 \
  --p-maxmergelen 270 \
  --p-maxdiffs 10

  qiime quality-filter q-score-joined \
  --i-demux demux-joined.qza \
  --o-filtered-sequences demux-filtered.qza \
  --o-filter-stats demux-filter-stats.qza

  qiime deblur denoise-16S \
  --i-demultiplexed-seqs demux-filtered.qza \
  --p-trim-length 240 \
  --o-representative-sequences rep-seqs.qza \
  --o-table table.qza \
  --p-sample-stats \
  --p-jobs-to-start 10 \
  --o-stats deblur-stats.qza
  qiime deblur visualize-stats --i-deblur-stats deblur-stats.qza --o-visualization reports/deblur-stats.qzv
  qiime feature-table summarize --i-table table.qza --o-visualization reports/table.qzv
  qiime feature-table tabulate-seqs --i-data rep-seqs.qza --o-visualization reports/rep-seqs.qzv
  ```

Наш инструмент, лишен недостатков конкурентов и упрощает до одной строки получение нужных результатов. Но при этом, глубоко погруженные в тему, смогут добавить дополнительные аргументы и взять самое лучшее из других пайплайнов.

### Данные

Погрузившись в предметную область, поняли, что данные могут стать *плохими* в 4 случаях:

- Плохой забор проб, их транспортировка и хранение
- Дешевые методы секвенирования ДНК (ошибки делают)
- Ограничения по длине на исследование 16s (потеря инфы, если не полностью читать)
- Неправильная обработка сырых данных (тримминг, мержинг)

Сейчас мы способны решить только последний пункт, но впоследствии мы хотим обучить нейронку на отслеживание остальных проблем.

#### Под капотом сейчас

    1. Загрузка данных  в CLI
    2. Простейшая чистка данных с ошибками
    3. Удаление шума за счет математики (denoising)
    4. Кластеризация
    5. Химеринг
    6. Такосономия
    7. Визуализация

#### Под капотом с ML

    1. Загрузка данных в CLI
    2. Проверка качества данных и эксперимента (обученная нейронка)
    3. Отбраковка данных/учет выявленных зависимостей
    4. Удаление шума за счет математики (denoising)
    5. Кластеризация
    6. Химеринг
    7. Такосономия
    8. Визуализация

## Структура репозитория

-----------------------------------------------

```py
deeploid_mini_cli
├──data # input files (fasta/fastq)
│   ├── standart_dataset 
│   └── input_files
├──databases # database for pipelines
│   ├── GG
│   ├── vsearch
│   ├── silva
│   └── README.md 
├──markdown
├──workflow # SnakeMake workflow
│   ├── envs
│   ├── rules
│   ├── scripts
│   ├── snakefile
│   └── README.md
├──.gitignore 
├──README.md
└──deeploid_cli.py # main script 
```

### Визуализация **пути** продвинутого пользователя
![Текст с описанием картинки](/markdown/arch_full.jpg)


## Ну и как же проверять качество данных и полученных результатов?

---

### Сырые данные

 Для проверки сырых данных есть FastQC - это простой способ проверки качества необработанных данных, поступающих из высокопроизводительных систем секвенирования.

![Текст с описанием картинки](/markdown/fastQC.png)

### После таксономического анализа

Для анализа таксономии есть метрики филогенетического разнообразия

|  Филогенетическое разнообразие  | Альфа-разнообразие | Бета-разнообразие |
| ------------- | ------------- | ------------- |
|![Текст с описанием картинки](/markdown/philog_tree.png)  | ![Текст с описанием картинки](/markdown/alpha_chao.png)  | ![Текст с описанием картинки](/markdown/beta_kertice.png)  |


## &#128204;Installation

С использованием conda, mamba и bioconda

deeploid_cli is available in conda, to install and set is use following commands:
1) Download deeploid_cli in separate conda environment: `conda create -n deeploid_cli -c conda-forge -c bioconda -c deeploid_cli`
2) Activate the environment: `conda activate deeploid_cli`

## &#128204; Quick Start

deeploid_cli is available in conda, to install and set is use following commands:

1) To run deeploid_cli on your reads use one of the following commands:

   ```bash
   # If you have only assembly
   deeploid_cli -m fasta -a /path/to/assembly.fasta -t 32 -o /path/to/outdir

   # If you have assembly and closest reference proteins
   deeploid_cli -m fasta_faa -a /path/to/assembly.fasta -f /path/to/proteins.fasta -t 32 -o /path/to/outdir

   # If you have assembly and RNA-seq reads
   deeploid_cli -m fasta_rna -a /path/to/assembly.fasta -1 /path/to/forward_read_1.fastq -2 /path/to/reverse_read_2.fastq -t 32 -o /path/to/outdir

   # If you have assembly, closest reference proteins and RNA-seq data 
   deeploid_cli -m fasta_rna_faa -a /path/to/assembly.fasta -f /path/to/proteins.fasta -1 /path/to/forward_read_1.fastq -2 /path/to/reverse_read_2.fastq -t 32 -o /path/to/outdir
   ```

## &#128204;Community

### Расти вместе с AI Talent Hub!

На базе [AI Talent Hub](https://ai.itmo.ru/) Университет ИТМО совместно с компанией Napoleon IT запустил образовательную программу «Инженерия машинного обучения». Это не краткосрочные курсы без практического применения, а онлайн-магистратура нового формата, основанная на реальном рабочем процессе в компаниях.

Мы команда Deeploid:
* [Михаил](https://t.me/gurev)
* [Дарья](https://t.me/voronik1801)
* [Никита](https://t.me/space_apple)
* [Юрий](https://t.me/yubal42)
* [Данил](https://t.me/danil_zilov)
* [Маргарита](https://t.me/UnderPressureOf)
* [Валентина](https://t.me/Vale_612)

<details><summary> &#128516; Шутейка </summary>
<p>

![Jokes Card](https://readme-jokes.vercel.app/api)

</p>
</details>

## Цитирование

Если вы используете CLI в своих исследованиях, рассмотрите возможность цитирования

```python
@misc{=Command Line Interface,
    title={High Performance CLI},
    author={Deeploid Contributors},
    howpublished = {\url{https://github.com/Deeploid-Meta/deeploid-mini-cli}},
    year={2022}
}
```

## Благодарность

- [AI Talent Hub](https://ai.itmo.ru/)
- [ПИШ](https://analytics.engineers2030.ru/schools/itmo/)
- [Updating the 97% identity threshold for 16S ribosomal RNA OTUs](https://www.biorxiv.org/content/10.1101/192211v1.full)
- [Comparing bioinformatic pipelines for microbial 16S rRNA amplicon sequencing](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0227434#pone.0227434.s002)


## Лицензия

 [The MIT License](https://opensource.org/licenses/mit-license.php)
