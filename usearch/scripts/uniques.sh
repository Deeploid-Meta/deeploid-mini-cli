#!/bin/bash

$ usearch -fastx_uniques ../out/filtered.fa
-fastaout ../out/uniques.fa
-relabel Uniq -sizeout
