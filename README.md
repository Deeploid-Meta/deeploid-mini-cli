# Deeploid-mini

1. Структура папок:

- **data** - в эту папку кладем данные для скриптов, сейчас там для примера лежит пара файлов из стандартного датасета
- **databases** - в эту папку сохраняем базы данных, сейчас там для примера лежит урезанная база GreenGenes
- **pipelines** - сюда кладем наши пайплайны, который потом будут вызываться SnakeMake'ом, мой скрипт - qiime2_pipeline.py

2. Описания скриптов

Описание qiime2_pipeline.py - **QIIME2_pipeline.md**
В описании предлагаю всем добавить пример команды, которая запускает скрипт, например у меня это
    
    python pipelines/qiime2_pipeline.py -1 data/standart_dataset/mock_2_R1.fastq -2 data/standart_dataset/mock_2_R2.fastq -db databases/GG/85_otus.fasta -tx databases/GG/85_otu_taxonomy.txt -t 8 --outdir output

Если скачать репозиторий и активировать окружение с qiime из файла qiime2-2022.8-py38-linux-conda.yml, то эта команда запустит пайплайн без необходимости что-то еще скачивать. Если все так сделаем - то тому кто будет собириать snakemake будет сильно проще.

