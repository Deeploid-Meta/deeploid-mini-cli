# rules


## Удачно про rule all

https://www.embl.org/groups/bioinformatics-rome/blog/2022/04/snakemake-profile-4-defining-resources-and-threads/

rule all:
  input:
    expand("results/{sampleName}.txt", sampleName=SAMPLENAMES),
    expand("results/{sampleName}-bowtie2.txt", sampleName=SAMPLENAMES)
rule printContent:
  input:
    "inputs/{sampleName}.txt"
  output:
    "results/{sampleName}.txt"
  shell:
    """
    cat {input} > {output}
    """
rule bowtie2:
  input:
    "inputs/{sampleName}.txt"
  output:
    "results/{sampleName}-bowtie2.txt"
  shell:
    """
    cat {input} > {output}
    """