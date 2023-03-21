rule dada2:
    input:
        fr = FORWARD_READS, 
        rr = REVERSE_READS,
        db = DATABASE
    params:
        outdir = directory(OUTDIR)
    output:
        out = directory(OUTDIR)
    conda:
        envs.dada2
    shell:
        """
        Rscript workflow/scripts/dada2_pipeline.R -1 {input.fr} -2 {input.rr} -db {input.db} -o {params.outdir}
        """

# Дашин вариант
# Rscript scripts/dada2_pipeline.R -1 {input.fr} -2 {input.rr} -db {input.db} -o {params.outdir} cp {input} {output}