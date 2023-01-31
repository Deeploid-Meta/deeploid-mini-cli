rule qiime:
    input:
        TODO
    output:
        TODO
    conda:
        "../envs/qiime2.yaml"
    params:
        TODO

        forward = ,
        reverse = ,
        database = ,
        output = ,
    shell:
        """
            conda activate qiime2-2022.8
            python ../pipelines/qiime2_pipeline.py -1 {params.forward} -2 {params.revrse} -db {params.database} -o {params.output} -tx ../databases/GG/85_otu_taxonomy.txt
        """