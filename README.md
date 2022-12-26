# Dada2

Туториал на dada2

pipeline/dada2_OTU_full.R - скрипт для запуска дады до этапа OTU ТОЛЬКО с форвард и реверс ридами.
Пример запуска:
Rscript dada2_OTU_full.R -p /Users/d.voronkina/Desktop/Deeploid/deeploid-mini-cli/data -1 '*_R1.fastq.gz' -2 '*_R2.fastq.gz' -o /Users/d.voronkina/Desktop/Deeploid/deeploid-mini-cli/output

pipeline/dada2_taxa_full.R - скрипт для запуска дады до этапа таксономии ТОЛЬКО с форвард и реверс ридами.
Пример запуска:
Rscript dada2_taxa_full.R -p /Users/d.voronkina/Desktop/Deeploid/deeploid-mini-cli/data -1 '*_R1.fastq.gz' -2 '*_R2.fastq.gz' -o /Users/d.voronkina/Desktop/Deeploid/deeploid-mini-cli/output -db /Users/d.voronkina/Desktop/Deeploid/dada2_test/silva_nr_v132_train_set.fa