## 1. Установка окружения

    conda env create -n qiime2-2022.8 --file qiime2-2022.8-py38-linux-conda.yml

## 2. Запуск

    conda activate qiime2-2022.8

Запустить можно вот такой командой (для удобства все необходимые файлы лежат в репозитории):

    python pipelines/qiime2_pipeline.py -1 data/standart_dataset/mock_2_R1.fastq -2 data/standart_dataset/mock_2_R2.fastq -db databases/GG/85_otus.fasta -tx databases/GG/85_otu_taxonomy.txt -t 8 --outdir output

## 3. Результат

<p> В папке output появятся файлы: </p>

    - OTU.csv
    - taxonomy.tsv

<p> В папке output/qiime2_artifacts - сохраняются артефакты qiime2, это потом можно будет убрать
