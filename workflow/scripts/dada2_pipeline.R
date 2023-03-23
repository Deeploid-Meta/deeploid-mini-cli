# argparse uploading only with mirror
if (!require(argparse)) {
  install.packages("argparse", repos = "https://mirror.truenetwork.ru/CRAN/")
  library(argparse)
}

#!/usr/bin/env Rscript
suppressPackageStartupMessages(library("argparse"))
library(dada2); packageVersion("dada2")

# create parser object
parser <- ArgumentParser()

parser$add_argument("-t", "--type", type = "character", default = "taxa",
    help = "Enter type for start: otu - create OTU, taxa - create taxonomy.")
parser$add_argument("-p", "--path", type = "character", default = "data/standart_dataset",
    help = "Enter path to  reads")
parser$add_argument("-1", "--forward", type = "character",
    help = "Enter forward reads pattern example: *_R1_001.fastq")
parser$add_argument("-2", "--reverse", type = "character",
    help = "Enter reverse reads pattern example: *_R2_001.fastq")
parser$add_argument("-db", "--database", type = "character",
    help = "Enter path to database in fasta format")
parser$add_argument("-o", "--output", type = "character", default = "/outupt",
    help = "Enter path to output result")

args <- parser$parse_args()

path <- args$path
output <- args$output

fnFs <- sort(list.files(path,
                        pattern = args$forward,
                        full.names = TRUE))
fnRs <- sort(list.files(path,
                        pattern = args$reverse,
                        full.names = TRUE))
sample.names <- sapply(strsplit(basename(fnFs), "\\."), `[`, 1)

filtFs <- file.path(output, "dada2/filtered", paste0(sample.names, "_F_filt.fastq"))
filtRs <- file.path(output, "dada2/filtered", paste0(sample.names, "_R_filt.fastq"))
names(filtFs) <- sample.names
names(filtRs) <- sample.names

out <- filterAndTrim(fnFs, filtFs, fnRs, filtRs, truncLen=c(240,160),
              maxN=0, maxEE=c(2,2), truncQ=2, rm.phix=TRUE,
              compress=TRUE, multithread=TRUE)

errF <- learnErrors(filtFs, multithread=TRUE)
errR <- learnErrors(filtRs, multithread=TRUE)


dadaFs <- dada(filtFs, err=errF, multithread=TRUE)
dadaRs <- dada(filtRs, err=errR, multithread=TRUE)


mergers <- mergePairs(dadaFs, filtFs, dadaRs, filtRs, verbose=TRUE)

seqtab <- makeSequenceTable(dadaFs)
write.table(seqtab, file=paste(args$output, "dada2", "OTU.tsv", sep = "/"), quote=FALSE, sep='\t', col.names = NA)

# nochim
table(nchar(getSequences(seqtab)))
seqtab.nochim <- removeBimeraDenovo(seqtab, method="consensus", multithread=TRUE, verbose=TRUE)

getN <- function(x) sum(getUniques(x))
track <- cbind(out, getN(dadaFs), getN(mergers), rowSums(seqtab), rowSums(seqtab.nochim))
colnames(track) <- c("input", "filtered", "denoisedF", "denoisedR", "merged", "nonchim")
rownames(track) <- sample.names

taxa <- assignTaxonomy(seqtab.nochim, args$database, multithread=TRUE)
taxa.print <- taxa
rownames(taxa.print) <- NULL
head(taxa.print)
write.table(taxa, file=paste(output, "dada2", "taxonomy.tsv", sep = "/"), quote=FALSE, sep='\t', col.names = NA)
