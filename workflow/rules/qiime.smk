rule qiime:
    input:
        "data/standart_dataset/mock_2_R1.fastq"
        "data/standart_dataset/mock_2_R2.fastq"
    output:
        "databases/GG/85_otus.fasta"
        "databases/GG/85_otu_taxonomy.txt"
    conda:
        "../envs/qiime2.yaml"
    threads: 
        "8"
    params:
        
    shell:
        """
            python scripts/qiime2_pipeline.py  -1 {input[0]} 
            -2 {input[1]} -db {output[0]}  -tx {output[1]}
            -t {threads[0]}
        """