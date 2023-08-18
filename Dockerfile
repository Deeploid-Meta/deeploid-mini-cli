FROM python:3.10-slim-buster
FROM continuumio/miniconda3

RUN apt-get update && \
    pip install --upgrade pip

RUN conda install -n base -c conda-forge mamba
RUN conda install libarchive -n base -c conda-forge
RUN mamba create -c conda-forge -c bioconda -n snakemake snakemake -y

# RUN conda env create -n snakemake --file ./environment.yml
# conda activate snakemake
RUN echo "source activate snakemake" > ~/.bashrc
ENV PATH /opt/conda/envs/snakemake/bin:$PATH

RUN mkdir -p /usr/src/app/
WORKDIR /usr/src/app/

COPY . /usr/src/app/
