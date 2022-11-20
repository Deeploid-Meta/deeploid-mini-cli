# Никитос разобрался

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

Мы используем ползовательские переменные в которой хранится путь до скрипта с [сайта](https://drive5.com/usearch/download.html) USEARCH

```bash
mkdir gq out scripts
export usearch=~/usearch11.0.667_i86linux32.gz
$usearch # значение переменной
```

Структура:
пользовательская переменная -функция файлы

```bash
$usearch -fastx_info lol.fastq
```

Пример исполнения в терминале линукса. Видно, что при запуске линускоидного файла выделяются разные ресурсы ПК

```bash
nikivene@DESKTOP-78NOBF0:~/Deeploid$ export usearch=~/Deeploid/usearch11.0.667_win32.exe
nikivene@DESKTOP-78NOBF0:~/Deeploid$ cd fq/
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
(C) Copyright 2013-18 Robert C. Edgar, all rights reserved.
https://drive5.com/usearch

License: personal use only

00:00 38Mb    100.0% Processing
File size 4.4M, 7793 seqs, 2.0M letters and quals
Lengths min 249, lo_quartile 251, median 251, hi_quartile 251, max 251
Letter freqs G 34.9%, A 25.5%, C 19.9%, T 19.8%, N 0.004%
0% masked (lower-case)
ASCII_BASE=33
EE mean 0.6; min 0.0, lo_quartile 0.1, median 0.2, hi_quartile 0.7, max 17.2
```
