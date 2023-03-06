rule dada2:
    input:
        FORWARD_READS, 
        REVERSE_READS
    output:
        OUTDIR,
        DATABASE
    conda:
        envs.dada2
    shell:
        """
        Rscript scripts/dada2_pipeline.R -1 {input[0]} -2 {input[1]} -db {output[1]} -o {output[0]}
        cp {input} {output}
        """