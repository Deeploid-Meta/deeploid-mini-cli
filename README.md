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

Сейчас мы идем к тому, что вместо огромного количества команд проанализировать метаном можно всего одной командой, глубоко погруженные в тему смогут добавить дополнительные аргументы и из разных пайплайнов взять самое лучшее, а для менее погруженных мы предложим наилучшую базовую настройку.

Tasklist 

- [X] Определено как представляете работу вовне, как будут собираться и храниться данные.

Мы планируем, что пользователь скачивает CLI себе на машину. Также пользователь сам полностью выбирает данные и загружет их, согдасно пайплайну

- [X] Описаны критерии качества плохих данных

Для нас данные могут стать *плохими* в 3 случаях:

- плохой забор проб их транспортировка и хранение
- Дешевый секвенатор ДНК
- Неправильная обработка сырых данных

Критерии - QC, филогения, альфа/бета разнообразие

- [X] Есть понимание о том что можно визуализировать в рамках работы с данными (в идеале не только сырые данные и метрики над ними) -да, прошлый пункт

Как проверять:

- [X] Есть описание и обоснование хранения данных, агрегации источников данных.

В рамках CLI пользователь сам над этим думает. В рамка API у нас есть собсьвенный сервер.

- [X] Есть критерии качественных данных, и решения, что будем делать, если к нам текут не качественные данные

Есть понимание некачественных данных. Есть проверки данных. Пользователя предупреждаем о точности конечнойю

- [ ] Прототип дашборда - визуализации, демонстрация влияния данных на целевые метрики, бенчмарки

`ДАША и НИКИТА ЭТОТ ПУНКТ НЕ ЗАБЫТЬ!`

- [X] Есть понятное популярное описание логики работы с данными в проекте, способы увеличения объема данных и/или их качества

Да, все есть все дальнейших пункты про это

## &#128204;Features


### Под капотом сейчас

  1. Загрузка данных  в CLI
  2. Простейшая чистка данных с ошибками
  3. Удаление шума за счет математики (denoising)
  4. Кластеризация
  5. Такосономия

### Под капотом с ML

  1. Загрузка данных в CLI
  2. Проверка качества данных и эксперимента
  3. Отбраковка данных/Учет выявленных зависимостей
  4. Удаление шума за счет математики (denoising)
  5. Кластеризация
  6. Такосономия

Визуализация **пути** пользователя

<img src='https://g.gravizo.com/svg?
 digraph G {
   "Загрузка данных  в CLI" -> "Простейшая чистка данных (merging, trimming)";
   "Простейшая чистка данных (merging, trimming)" -> "Кластеризация OTU (vsearch)";
   "Простейшая чистка данных (merging, trimming)" -> "Удаление шума (DADA2, deblur)" ->  "Кластеризация OTU (vsearch)";
   "Кластеризация OTU (vsearch)" -> "Таксономия" -> "Визуализация результатов";
   "Этап 1" -> "Этап 2" -> "Этап 2.1" -> "Этап 3" -> "Этап 4"-> "Этап 5";
 }
'/>

### Возможный скрипт

Описание qiime2_pipeline.py - **QIIME2_pipeline.md**
В описании предлагаю всем добавить пример команды, которая запускает скрипт, например у меня это
    
    python pipelines/qiime2_pipeline.py -1 data/standart_dataset/mock_2_R1.fastq -2 data/standart_dataset/mock_2_R2.fastq -db databases/GG/85_otus.fasta -tx databases/GG/85_otu_taxonomy.txt -t 8 --outdir output

Если скачать репозиторий и активировать окружение с qiime из файла qiime2-2022.8-py38-linux-conda.yml, то эта команда запустит пайплайн без необходимости что-то еще скачивать. Если все так сделаем - то тому кто будет собириать snakemake будет сильно проще.

#### ⚡ Пример работы

```
чикпук
```

## &#128204;Structure

### Структура папок

По аналогии с Проектом [Дани](https://github.com/aglabx/paniman)

```bash
├──envs # Зависимости окружений для SnakeMake
│   ├── dada.yaml
│   ├── deblur.yaml
│   └── vsearch.yaml
├──markdown # Хранение файлов для README.md 
│   ├── photo.png
│   └── lol.gif
├──rules # Правила для SnakeMake
│   ├── dada.smk
│   ├── deblur.smk
│   └── vsearch.smk
├──scripts # Правила для SnakeMake
│   ├── qiime_pipleline.py
│   ├── dada_pipleline.py
│   ├── deblur_pipleline.py
│   └── vsearch_pipleline.py
├──workflow # Зависимости SnakeMake ( тут его архитектура)
│   └── snakefile
├──databases 
├──README.md
└──deeploid_cli.py
```

## &#128204;Installation

С использованием conda, mamba и bioconda

PANIMAN is available in conda, to install and set is use following commands:
1) Download PANIMAN in separate conda environment: `conda create -n paniman -c conda-forge -c bioconda -c aglab paniman`
2) Activate the environment: `conda activate paniman`

## &#128204; Quick Start

PANIMAN is available in conda, to install and set is use following commands:

1) EggNOG-mapper database (~50GB) is required to run PANIMAN.
   You can download it or set your own one if you have it already. Use `paniman_download_db` tool to set or download databases. Examples:

   ```bash
   # Download EggNOG db
   paniman_download_db -o /path/to/database/directory
   
   # Set your EggNOG db
   paniman_download_db -e /path/to/eggnog/database
   ```

2) To run PANIMAN on your reads use one of the following commands:

   ```bash
   # If you have only assembly
   paniman -m fasta -a /path/to/assembly.fasta -t 32 -o /path/to/outdir

   # If you have assembly and closest reference proteins
   paniman -m fasta_faa -a /path/to/assembly.fasta -f /path/to/proteins.fasta -t 32 -o /path/to/outdir

   # If you have assembly and RNA-seq reads
   paniman -m fasta_rna -a /path/to/assembly.fasta -1 /path/to/forward_read_1.fastq -2 /path/to/reverse_read_2.fastq -t 32 -o /path/to/outdir

   # If you have assembly, closest reference proteins and RNA-seq data 
   paniman -m fasta_rna_faa -a /path/to/assembly.fasta -f /path/to/proteins.fasta -1 /path/to/forward_read_1.fastq -2 /path/to/reverse_read_2.fastq -t 32 -o /path/to/outdir
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
## Лицензия

 [The MIT License](https://opensource.org/licenses/mit-license.php)