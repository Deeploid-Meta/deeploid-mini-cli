# Прохождение всего пайплайна от 2-х fastq файлов до таксономии в QIIME2

## 1. Данные
<p>

Использовать будем данные [отсюда](https://trace.ncbi.nlm.nih.gov/Traces/?view=run_browser&acc=SRR22104214&display=metadata). Скачаем их при помощи SRA tools.</p>

## 2. SRA tools

- Устанавливаем The SRA Toolkit (по инструкции) - https://github.com/ncbi/sra-tools
- Скачиваем данные с помощью команды:

    ```
    ./bin/prefetch SRR22104214
    ```
    у меня они сохраняются в папку **user_repo/sra**
- Разделяем на 2 fastq файла (forward и reverse):

    ```
    ./bin/fastq-dump --split-files ./user_repo/sra/SRR22104214.sra
    ```

## 3. QIIME 2

<p>

Я запускаю QIIME 2 из [докера](https://docs.qiime2.org/2022.8/install/virtual/docker/).</p>

1. **Импорт данных в QIIME 2** - [tutorial](https://docs.qiime2.org/2022.8/tutorials/importing/)
    - Для того, чтобы импортировать данные из 2 fastq файлов нужно создать manifest.tsv файл, мой файл можно посмотреть вот [тут](https://).
    - Сам импорт осуществляется командой:

    ```
    sudo docker run -t -i -v $(pwd):/data quay.io/qiime2/core:2022.8 qiime tools import \
        --type 'SampleData[PairedEndSequencesWithQuality]' \
        --input-path /data/manifest.tsv \
        --output-path /data/paired-end-demux.qza \
        --input-format PairedEndFastqManifestPhred33V2
    ```

    Результат выполнения команды:
    ```
    Imported /data/manifest.tsv as PairedEndFastqManifestPhred33V2 to /data/paired-end-demux.qza
    ```
    
    **Подготовим артефакт для визуализации:**

    ```
     sudo docker run -t -i -v $(pwd):/data quay.io/qiime2/core:2022.8 qiime demux summarize \
        --i-data /data/paired-end-demux.qza \
        --o-visualization /data/demux.qzv
    ```

    Результат выполнения команды:
    ```
    Saved Visualization to: /data/demux.qzv
    ```

    Его можно посмотреть, используя [онлайн тулзу](https://view.qiime2.org/)

    ![Quality](https://raw.githubusercontent.com/Deeploid-Meta/Deeploid-mini/qiime_tutorial/qiime2/img/quality.png)

    Видим, что медианы качества на позициях 151 и в forward reads и в reverse reads больше 30, поэтому используем 151 в следующей команде

1. **Denoising и построение таблиц OTU**
    ```
    sudo docker run -t -i -v $(pwd):/data quay.io/qiime2/core:2022.8 qiime dada2 denoise-paired \
        --i-demultiplexed-seqs /data/paired-end-demux.qza \
        --p-trunc-len-f 151 \
        --p-trunc-len-r 151 \
        --p-trim-left-f 0 \
        --p-trim-left-r 0 \
        --o-representative-sequences /data/rep-seqs.qza \
        --o-table /data/table.qza \
        --o-denoising-stats /data/stats.qza
    ```

    Результат выполнения команды:
    ```
    Saved FeatureTable[Frequency] to: /data/table.qza
    Saved FeatureData[Sequence] to: /data/req-seqs.qza
    Saved SampleData[DADA2Stats] to: /data/stats.qza
    ```

1. **Подготовим артефакт для визуализации:**

    ```
    sudo docker run -t -i -v $(pwd):/data quay.io/qiime2/core:2022.8 qiime metadata tabulate \
       --m-input-file /data/stats.qza \
       --o-visualization /data/stats.qzv
    ```

    Результат выполнения команды:
    ```
    Saved Visualization to: /data/stats.qzv
    ```

    ```
    sudo docker run -t -i -v $(pwd):/data quay.io/qiime2/core:2022.8 qiime feature-table summarize \
        --i-table /data/table.qza \
        --o-visualization /data/table.qzv
    ```

    Результат выполнения команды:
    ```
    Saved Visualization to: /data/table.qzv
    ```

    ```
    sudo docker run -t -i -v $(pwd):/data quay.io/qiime2/core:2022.8 qiime feature-table tabulate-seqs \
        --i-data /data/rep-seqs.qza \
        --o-visualization /data/rep-seqs.qzv
    ```

    Результат выполнения команды:
    ```
    Saved Visualization to: /data/rep-seqs.qzv
    ```


    Все артефакты для визуализации можно посмотреть, используя [онлайн тулзу](https://view.qiime2.org/)

1. **Классификация**
    - Скачиваем [классификатор](https://data.qiime2.org/2022.8/common/gg-13-8-99-515-806-nb-classifier.qza)

    ```
    sudo docker run -t -i -v $(pwd):/data quay.io/qiime2/core:2022.8 qiime feature-classifier classify-sklearn \
        --i-classifier /data/gg-13-8-99-515-806-nb-classifier.qza \
        --i-reads /data/rep-seqs.qza \
        --o-classification /data/taxonomy.qza
    ```

    Результат выполнения команды:
    ```
    Saved FeatureData[Taxonomy] to: /data/taxonomy.qza
    ```

1. **Подготовим артефакт для визуализации:**

    ```
    sudo docker run -t -i -v $(pwd):/data quay.io/qiime2/core:2022.8 qiime metadata tabulate \
        --m-input-file /data/taxonomy.qza \
        --o-visualization /data/taxonomy.qzv
    ```

    Результат выполнения команды:
    ```
    Saved Visualization to: /data/taxonomy.qzv
    ```

    Его можно посмотреть, используя [онлайн тулзу](https://view.qiime2.org/)

1. **Построим гистограмму**

    ```
    sudo docker run -t -i -v $(pwd):/data quay.io/qiime2/core:2022.8 qiime taxa barplot \
        --i-table /data/table.qza \
        --i-taxonomy /data/taxonomy.qza \
        --o-visualization /data/taxa-bar-plots.qzv
    ```

    Результат выполнения команды:
    ```
    Saved Visualization to: /data/taxa-bar-plots.qzv
    ```

    Ее можно посмотреть, используя [онлайн тулзу](https://view.qiime2.org/)