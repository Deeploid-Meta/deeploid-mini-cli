rule dada2:
    input:
        fr = FORWARD_READS, 
        rr = REVERSE_READS,
        db = DATABASE
    params:
        outdir = directory(OUTDIR) + '/TOOL'
    output:
        out = directory(OUTDIR)
    conda:
        envs.dada2
    shell:
        """
        Rscript workflow/scripts/dada2_taxa_full1.R -1 {input.fr} -2 {input.rr} -db {input.db} -o {params.outdir} -p data/standart_dataset/
        """