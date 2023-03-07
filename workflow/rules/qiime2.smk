rule qiime2:
    input:
        fr = FORWARD_READS, 
        rr = REVERSE_READS,
        db = DATABASE,
        tx = TAXANOMY
    output:
        out = OUTDIR
    params:
        t = THREADS        
    conda:
        envs.qiime2
    shell:
        """
            python scripts/qiime2_pipeline.py  -1 {input.fr} 
            -2 {input.rr} -db {input.db}  -tx {input.tx} -t {params.t} --outdir {output.out}
        """