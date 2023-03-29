rule vsearch:
    input:
        fr = FORWARD_READS, 
        rr = REVERSE_READS,
        db = DATABASE
    output:
        expand("{outdir}/vsearch/taxonomy.tsv", outdir=OUTDIR)
    params:
        t = THREADS,
        outdir = directory(OUTDIR)

    conda:
        envs.vsearch
    shell:
        """
            python workflow/scripts/vsearch_pipeline.py  -1 {input.fr} -2 {input.rr}  -o {params.outdir}  -db {input.db}
        """