# Про скрипты НА ТЕСТЕ

- dada2_pipeline.R - версия Даши
- dada2_taxa_full.R - первая версия от Марго
- dada2_taxa_full1.R - последняя версия от Марго

# Про скрипты РАБОЧИЕ

- deblur_pipeline.py - последняя Никиты

    python3 deeploid_cli.py -t deblur -1 data/standart_dataset/mock_2_R1.fastq -2 data/standart_dataset/mock_2_R2.fastq -db databases/GG/85_otus_classifier.qza -tx databases/GG/85_otu_taxonomy.txt -o path/output

- qiime2_pipeline.py - последний Миши

    python3 deeploid_cli.py -t qiime2 -1 data/standart_dataset/mock_2_R1.fastq -2 data/standart_dataset/mock_2_R2.fastq -db databases/GG/85_otus.fasta -tx databases/GG/85_otu_taxonomy.txt -o path/output