rule dada:
    input:
        TODO
    output:
        TODO
    params:
        TODO
        
        forward = ,
        reverse = , 
        database = , 
        output = ,
    shell:
        """
        Rscript dada2_pipeline.R -1 {params.forward} -2 {params.revrse} -db {params.database} -o {params.output}
        cp {input} {output}
        """