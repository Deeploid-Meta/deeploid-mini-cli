#!/bin/bash

$usearch -cluster_otus ../out/uniques.fa \
        -minsize 2 \
        -otus ../out/otus.fa \
        -relabel Otu   #(будет номера по порядку давать Otu1, Otu2, Otu3)
 
    
