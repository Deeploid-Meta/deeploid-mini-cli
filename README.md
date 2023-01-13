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
```
Второй чекпоинт - до 13 января
    
    Что будет: Определено как представляете работу вовне, как будут собираться и храниться данные. Описаны критерии качества плохих данных. Есть понимание о том что можно визуализировать в рамках работы с данными (в идеале не только сырые данные и метрики над ними)
    
    Как проверять:
    
    - Есть описание и обоснование хранения данных, агрегации источников данных. 
    - Есть критерии качественных данных, и решения, что будем делать, если к нам текут не качественные данные
    - Прототип дашборда - визуализации, демонстрация влияния данных на целевые метрики, бенчмарки
    - Есть понятное популярное описание логики работы с данными в проекте, способы увеличения объема данных и/или их качества
```

Сейчас мы идем к тому, что вместо огромного количества команд проанализировать метаном можно всего одной командой, глубоко погруженные в тему смогут добавить дополнительные аргументы и из разных пайплайнов взять самое лучшее, а для менее погруженных мы предложим наилучшую базовую настройку 




## &#128204;Features

### Под капотом  (Мы предоставляем сценарий):

1. Обработка данных
2. Отсев признаков
3. Обучение модели
4. Прогноз



#### ⚡ Пример работы

```
чикпук
```

## &#128204;Structure

1. Структура папок:

- **data** - в эту папку кладем данные для скриптов, сейчас там для примера лежит пара файлов из стандартного датасета
- **databases** - в эту папку сохраняем базы данных, сейчас там для примера лежит урезанная база GreenGenes
- **pipelines** - сюда кладем наши пайплайны, который потом будут вызываться SnakeMake'ом, мой скрипт - qiime2_pipeline.py

2. Описания скриптов

Описание qiime2_pipeline.py - **QIIME2_pipeline.md**
В описании предлагаю всем добавить пример команды, которая запускает скрипт, например у меня это
    
    python pipelines/qiime2_pipeline.py -1 data/standart_dataset/mock_2_R1.fastq -2 data/standart_dataset/mock_2_R2.fastq -db databases/GG/85_otus.fasta -tx databases/GG/85_otu_taxonomy.txt -t 8 --outdir output

Если скачать репозиторий и активировать окружение с qiime из файла qiime2-2022.8-py38-linux-conda.yml, то эта команда запустит пайплайн без необходимости что-то еще скачивать. Если все так сделаем - то тому кто будет собириать snakemake будет сильно проще.


## &#128204;Installation

С использованием conda, mamba и bioconda
```
conda install -c conda-forge mamba
mamba create -n qiime2 -c qiime2 -c bioconda -c conda-forge -c defaults qiime2
conda deactivate base
conda activate qiime2
```

Вариант для любой платформы [ссылка на документацию qiime2](https://docs.qiime2.org/2022.8/install/native/)

```
conda update conda
conda install wget
wget https://data.qiime2.org/distro/core/qiime2-2022.8-py38-linux-conda.yml
conda env create -n qiime2 --file qiime2-2022.8-py38-linux-conda.yml
rm qiime2-2022.8-py38-linux-conda.yml
conda deactivate base
conda activate qiime2
```

## &#128204; Quick Start

В разработке

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