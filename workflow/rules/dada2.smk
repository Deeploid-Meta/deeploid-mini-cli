rule dada2:
    input:
        db = DATABASE
    output:
        expand("{outdir}/dada2/taxonomy.tsv", outdir=OUTDIR)
    params:
        outdir = directory(OUTDIR),
        rr = REVERSE_READS,
        fr = FORWARD_READS 
    conda:
        envs.dada2
    shell:
        """
        Rscript workflow/scripts/dada2_pipeline.R -1 {params.fr} -2 {params.rr} -o {params.outdir} -db {input.db} -p data/standart_dataset/
        """