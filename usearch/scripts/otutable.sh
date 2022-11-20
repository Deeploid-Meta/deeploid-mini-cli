#!/bin/bash

$ usearch -usearch_global ../out/merged.fq \
        -db  ../out/otus.fa \
        -strand plus -id 0.97 \
        -otutabout ../out/otutable.txt
