rule vsearch:
    input:
        db = DATABASE,
        tx = TAXANOMY
    output:
        expand("{outdir}/vsearch/taxonomy.tsv", outdir=OUTDIR)
    params:
        t = THREADS,
        outdir = directory(OUTDIR),
        fr = FORWARD_READS, 
        rr = REVERSE_READS
    conda:
        envs.vsearch
    shell:
        """
            python workflow/scripts/vsearch_pipeline.py  -r data/standart_dataset/ \
            -o {params.outdir} -t True
        """

# python vsearch_pipeline.py -r raw_reads -o output_folder_pe_trimmed -se False -t True

# python workflow/scripts/vsearch_pipeline.py  -1 {input.fr} \
#            -2 {input.rr} -db {input.db} -tx {input.tx} -t {params.t} -o {params.outdir}