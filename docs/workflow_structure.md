## Structure snakemake workflow

```py
workflow
├──envs # Combat environment dependencies for SnakeMake
│   ├── dada2.yaml 
│   ├── vsearch.yaml 
│   ├── deblur.yaml
│   ├── qiime2.yaml
│   ├── README.md
│   └── history # Test environment dependencies for SnakeMake
│       ├── qiime2_2020_8_py36.yaml
│       ├── qiime2_2022_8_py38.yaml
│       ├── qiime2_2022_11_py38.yaml
│       └── qiime2_2023_2_py38.yaml
├──rules # Pipeline`s rules for SnakeMake
│   ├── dada2.smk
│   ├── deblur.smk
│   ├── qiime2.smk
│   ├── vsearch.smk
│   └── README.md
├──scripts # Pipelines for taxonomy
│   ├── markdown # docs for pipelines
│   ├── qiime_pipleline.py
│   ├── dada_pipleline.py
│   ├── deblur_pipleline.py
│   ├── vsearch_pipleline.py
│   └── README.md
├──snakefile # main SnakeMake with architecture
└──README.md
```
