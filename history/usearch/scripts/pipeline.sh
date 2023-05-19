
# biblio
export usearch=~/Deeploid/usearch11.0.667_i86linux32
# Pipline to choose scripts
    ./merge.sh \
    ./filter.sh \
    ./uniques.sh \
    ./otus.sh \
    ./otutable.sh

less -S ../out/otutable.txt

# merge
$usearch -fastq_mergepairs ../fq/SRR22104214_R1.fastq \
        -fastq_maxdiffs 10 \
        -fastq_pctid 10 \
        -fastqout ../out/merged.fq 
        #-fastq_minmergelen 230 \
        #-fastq_maxmergelen 270 \
# filter
$usearch -fastq_filter ../out/merged.fq \
        -fastq_maxee 1.0 \
        -fastaout ../out/filtered.fa

# uniques
$usearch -fastx_uniques ../out/filtered.fa \
	    -fastaout ../out/uniques.fa \
	    -relabel Uniq -sizeout

# otus
$usearch -cluster_otus ../out/uniques.fa \
        -minsize 2 \
        -otus ../out/otus.fa \
        -relabel Otu   #(будет номера по порядку давать Otu1, Otu2, Otu3)

# otutable
$usearch -usearch_global ../out/merged.fq \
        -db  ../out/otus.fa \
        -strand plus -id 0.97 \
        -otutabout ../out/otutable.txt