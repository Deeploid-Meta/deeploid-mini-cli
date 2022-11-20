#!/bin/bash

$ usearch -fastq_filter ../out/merged.fq \
        -fastq_maxee 1.0 \
        -fastaout ../out/filtered.fa
