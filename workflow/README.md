## Full installation

Snakemake can be installed with all goodies needed to run in any environment and for creating interactive reports via

```shs
$ conda activate base
$ mamba create -c conda-forge -c bioconda -n snakemake snakemake
```

from the Bioconda channel. This will install snakemake into an isolated software environment, that has to be activated with

```sh
$ conda activate snakemake
$ snakemake --help
```

Installing into isolated environments is best practice in order to avoid side effects with other packages.

`Note that full installation is not possible from Windows`, because some of the dependencies are Unix (Linux/MacOS) only. For Windows, please use the minimal installation below.

## Minimal installation
A minimal version of Snakemake which only depends on the bare necessities can be installed with

```
$ conda activate base
$ mamba create -c bioconda -c conda-forge -n snakemake snakemake-minimal
```

In contrast to the full installation, which depends on some Unix (Linux/MacOS) only packages, this also works on Windows.