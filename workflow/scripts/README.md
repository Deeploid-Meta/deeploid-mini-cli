# Про скрипты НА ТЕСТЕ


## Про скрипты РАБОЧИЕ

- deblur_pipeline.py - последняя Никиты

    python3 deeploid_cli.py -t deblur -1 data/standart_dataset/mock_2_R1.fastq -2 data/standart_dataset/mock_2_R2.fastq -db databases/GG/85_otus_classifier.qza -tx databases/GG/85_otu_taxonomy.txt -o path/output

- qiime2_pipeline.py - последний Миши

    python3 deeploid_cli.py -t qiime2 -1 data/standart_dataset/mock_2_R1.fastq -2 data/standart_dataset/mock_2_R2.fastq -db databases/GG/85_otus.fasta -tx databases/GG/85_otu_taxonomy.txt -o path/output

- dada2_pipeline.R - последняя Марго

    python3 deeploid_cli.py -t dada2 -1 mock_2_R1.fastq -2 mock_2_R2.fastq -db databases/silva_nr99_v138.1_train_set.fa.gz -o path/output
