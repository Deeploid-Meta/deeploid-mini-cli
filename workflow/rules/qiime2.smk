rule qiime2:
    input:
        "FORWARD_READS"
        "REVERSE_READS"
    output:
        "OUTDIR"
    conda:
        envs.qiime2
    threads: 
        "THREADS"
    params:
        
    shell:
        """
            python scripts/qiime2_pipeline.py  -1 {input[0]} 
            -2 {input[1]} -db {output[0]}  -tx {output[0]}
            -t {threads[0]}
        """



