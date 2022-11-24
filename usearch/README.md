# Никитос разобрался

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
    На выходе имеем 2 файла в папке: 
```
./user_repo/sra/SRR22104214_1.fastq  SRR22104214_2.fastq
```

## 3. Usearch

## Как устроены bash-скрипты

Создайте пустой файл с использованием команды touch. В его первой строке нужно указать, какую именно оболочку мы собираемся использовать. Нас интересует bash, поэтому первая строка файла будет такой:

```bash
#!/bin/bash
```

Сделаем файл исполняемым и потом попытаемся его выполнить:

```bash
chmod +x ./myscript
./myscript
```

>Существуют два типа переменных, которые можно использовать в bash-скриптах:\
Переменные среды\
Пользовательские переменные

Мы используем ползовательские переменные в которой хранится путь до скрипта

## Начнем работать
Создаем папку
./user_repo/Deeploid/
в ней выполняем

```bash
mkdir gq out scripts
```

Скачиваем и распаковываем в ./user_repo/Deeploid/ файлик с [сайта](https://drive5.com/usearch/download.html) USEARCH \

"Активируем" usearch для использования

```bash
export usearch=~/Deeploid/usearch11.0.667_i86linux32
$usearch -fastx_info lol.fastq #test
```

## Добавляем файлы
Переименовываем их, чтобы содержалось _R1 и _R2 в названии fastq файлов это нужно, чтобы функция $usearch -fastq_mergepairs смогла отработать:

```bash
cp ./user_repo/sra/SRR22104214_1.fastq  ./user_repo/Deeplod/fq/SRR22104214_R1.fastq
cp ./user_repo/sra/SRR22104214_2.fastq  ./user_repo/Deeplod/fq/SRR22104214_R2.fastq 
```

## Работа со сткриптами

Вообще функций у USEARCH [миллион](https://drive5.com/usearch/manual10/cmds_by_category.html) \
Мы с вами выполним пайплан до токсономии, с минимальными настройками огромного функционала

Можно просто в консоли бахать или через скрипты открывать (они на гитхабе есть)

[-fastq_mergepairs](https://drive5.com/usearch/manual10/cmd_fastq_mergepairs.html)

```bash
# merge
$usearch -fastq_mergepairs ../fq/SRR22104214_R1.fastq \
        -fastq_maxdiffs 10 \
        -fastq_pctid 10 \
        -fastqout ../out/merged.fq 
        #-fastq_minmergelen 230 \
        #-fastq_maxmergelen 270 \

Merging
  Fwd ../fq/SRR22104214_R1.fastq
  Rev ../fq/SRR22104214_R2.fastq
  Keep read labels

00:00 72Mb   FASTQ base 33 for file ../fq/SRR22104214_R1.fastq
00:00 72Mb   CPU has 16 cores, defaulting to 10 threads
00:01 158Mb   100.0% 1.3% merged

Totals:
    101437  Pairs (101.4k)
      1329  Merged (1329, 1.31%)
       627  Alignments with zero diffs (0.62%)
        35  Too many diffs (> 10) (0.03%)
         2  Fwd tails Q <= 2 trimmed (0.00%)
         0  Rev tails Q <= 2 trimmed (0.00%)
        73  Fwd too short (< 64) after tail trimming (0.07%)
         2  Rev too short (< 64) after tail trimming (0.00%)
     99998  No alignment found (98.58%)
         0  Alignment too short (< 16) (0.00%)
        22  Staggered pairs (0.02%) merged & trimmed
    104.00  Mean alignment length
    182.28  Mean merged length
      0.34  Mean fwd expected errors
      0.20  Mean rev expected errors
      0.22  Mean merged expected errors
```

[=fastq_filter](https://drive5.com/usearch/manual10/cmd_fastq_filter.html)

```bash
# filter
$usearch -fastq_filter ../out/merged.fq \
        -fastq_maxee 1.0 \
        -fastaout ../out/filtered.fa

00:00 4.2Mb  FASTQ base 33 for file ../out/merged.fq
00:00 38Mb   CPU has 16 cores, defaulting to 10 threads
00:00 90Mb    100.0% Filtering, 96.7% passed
      1329  Reads (1329)                    
        44  Discarded reads with expected errs > 1.00
      1285  Filtered reads (1285, 96.7%)
```

[-fastx_uniques](https://drive5.com/usearch/manual10/cmd_fastx_uniques.html)

```bash
# uniques
$usearch -fastx_uniques ../out/filtered.fa \
	    -fastaout ../out/uniques.fa \
	    -relabel Uniq -sizeout

00:00 41Mb    100.0% Reading ../out/filtered.fa
00:00 7.4Mb  CPU has 16 cores, defaulting to 10 threads
00:00 90Mb    100.0% DF
00:00 92Mb   1285 seqs, 914 uniques, 801 singletons (87.6%)
00:00 92Mb   Min size 1, median 1, max 16, avg 1.41
00:00 92Mb    100.0% Writing ../out/uniques.fa
```

[-cluster_otus](https://drive5.com/usearch/manual10/cmd_cluster_otus.html)

```bash
# otus
$usearch -cluster_otus ../out/uniques.fa \
        -minsize 2 \
        -otus ../out/otus.fa \
        -relabel Otu   #(будет номера по порядку давать Otu1, Otu2, Otu3)

00:00 47Mb    100.0% 16 OTUs, 0 chimeras
```

[-usearch_global](https://drive5.com/usearch/manual10/cmd_usearch_global.html)

```bash
# otutable
$usearch -usearch_global ../out/merged.fq \
        -db  ../out/otus.fa \
        -strand plus -id 0.97 \
        -otutabout ../out/otutable.txt

00:00 41Mb    100.0% Reading ../out/otus.fa
00:00 7.1Mb   100.0% Masking (fastnucleo)  
00:00 7.9Mb   100.0% Word stats          
00:00 7.9Mb   100.0% Alloc rows
00:00 7.9Mb   100.0% Build index
00:00 41Mb   CPU has 16 cores, defaulting to 10 threads
00:00 137Mb   100.0% Searching merged.fq, 61.7% matched
820 / 1329 mapped to OTUs (61.7%)                      
00:00 137Mb  Writing ../out/otutable.txt
00:00 137Mb  Writing ../out/otutable.txt ...done.
```

### Итог
```bash 
less -S ../out/otutable.txt
```
















Пример исполнения в терминале линукса. Видно, что при запуске линускоидного файла выделяются разные ресурсы ПК

```bash
nikivene@DESKTOP-78NOBF0:~/Deeploid/fq$ $usearch -fastx_info F3D0_S188_L001_R1_001.fastq
usearch v11.0.667_win32, 2.0Gb RAM (17.0Gb total), 16 cores
(C) Copyright 2013-18 Robert C. Edgar, all rights reserved.
https://drive5.com/usearch

License: personal use only

00:01 9.5Mb   100.0% Processing
File size 4.4M, 7793 seqs, 2.0M letters and quals
Lengths min 249, lo_quartile 251, median 251, hi_quartile 251, max 251
Letter freqs G 34.9%, A 25.5%, C 19.9%, T 19.8%, N 0.004%
0% masked (lower-case)
ASCII_BASE=33
EE mean 0.6; min 0.0, lo_quartile 0.1, median 0.2, hi_quartile 0.7, max 17.2
```

```bash
nikivene@DESKTOP-78NOBF0:~/Deeploid/fq$ export usearch=~/Deeploid/usearch11.0.667_i86linux32
nikivene@DESKTOP-78NOBF0:~/Deeploid/fq$ $usearch -fastx_info F3D0_S188_L001_R1_001.fastq
usearch v11.0.667_i86linux32, 4.0Gb RAM (8.1Gb total), 16 cores
```
