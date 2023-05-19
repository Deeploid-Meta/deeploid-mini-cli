#!/bin/bash

$usearch -fastq_mergepairs ../fq/SRR22104214_1.fastq \
        -fastq_maxdiffs 10 \
        -fastq_pctid 10 \
        -fastq_minmergelen 230 \
        -fastq_maxmergelen 270 \
        -fastqout ../out/merged.fq 

# Он сам находит lol_R2.fastq
