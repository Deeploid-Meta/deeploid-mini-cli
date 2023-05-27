## 1. Установка окружения

    conda env create -n qiime2-2022.8 --file qiime2-2022.8-py38-linux-conda.yml

## 2. Запуск

    conda activate qiime2-2022.8

Запустить можно вот такой командой (для удобства все необходимые файлы лежат в репозитории):

    python deblurFINAL_pipeline.py -1 data/SRR22104214_1.fastq -2 data/SRR22104214_2.fastq -db data/gg-13-8-99-515-806-nb-classifier.qza --outdir output

## 3. Результат

<p> В папке output появятся файлы: </p>

    - OTU.csv
    - taxonomy.tsv

<p> В папке output/qiime2_artifacts - сохраняются артефакты qiime2, это потом можно будет убрать
