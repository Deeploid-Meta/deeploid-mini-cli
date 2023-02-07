# Dada2

Туториал на dada2

## 1. Создание окружение из .yml файла
Деактивировать текущую среду
```bash
conda deactivate
```
Установить среду из файла
```bash
conda env create -f ./env_dada2/environment.yml
```
## 2. Запустить скрипт по установке argparse
```bash
Rscript pipeline/upl_libraries
```
## 3. Запуск скрипта dada2
`pipeline/dada2_OTU_full.R` - скрипт для запуска дады до этапа OTU ТОЛЬКО с форвард и реверс ридами.
Пример запуска:
```bash
Rscript dada2_OTU_full.R -p <path/to/folder/with/fastq> -1 '*_R1.fastq.gz' -2 '*_R2.fastq.gz' -o <path/to/output/folder>
```
`pipeline/dada2_taxa_full.R` - скрипт для запуска дады до этапа таксономии ТОЛЬКО с форвард и реверс ридами.
Пример запуска:
```bash
Rscript dada2_taxa_full.R -p <path/to/folder/with/fastq> -1 '*_R1.fastq.gz' -2 '*_R2.fastq.gz' -o <path/to/output/folder -db <path/to/folder/database_training_set>
```
