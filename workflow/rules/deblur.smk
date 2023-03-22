rule deblur:
    input:
        fr = FORWARD_READS, 
        rr = REVERSE_READS,
        db = DATABASE,
        tx = TAXANOMY
    output:
        expand("{outdir}/deblur/taxonomy.tsv", outdir=OUTDIR)
    params:
        t = THREADS,
        outdir = directory(OUTDIR)
    conda:
        envs.qiime2
    shell:
        """
            python workflow/scripts/deblur_pipeline.py  -1 {input.fr} \
            -2 {input.rr} -db {input.db} -t {params.t} -o {params.outdir}
        """