# !/usr/bin/env Rscript
suppressPackageStartupMessages(library("argparse"))
library(dada2); packageVersion("dada2")
# create parser object
parser <- ArgumentParser()

parser$add_argument("-1", "--forward", type = "character",
    help = "Enter forward reads pattern example: *_R1_001.fastq")
parser$add_argument("-2", "--reverse", type = "character",
    help = "Enter reverse reads pattern example: *_R2_001.fastq")
parser$add_argument("-db", "--database", type = "character",
    help = "Enter path to database in fasta format")
parser$add_argument("-o", "--output", type = "character", default = "/output",
    help = "Enter path to output result")

args <- parser$parse_args()

path <- args$path

nF1 <- system.file("extdata", args$forward, package="dada2")
fnR1 <- system.file("extdata", args$forward, package="dada2")
filtF1 <- tempfile(fileext=".fastq.gz")
filtR1 <- tempfile(fileext=".fastq.gz")



out <- filterAndTrim(fwd=fnF1, filt=filtF1, rev=fnR1, filt.rev=filtR1,
                  trimLeft=10, truncLen=c(240, 200), 
                  maxN=0, maxEE=2,
                  compress=TRUE, verbose=TRUE)

derepF1 <- derepFastq(filtF1, verbose=TRUE)
derepR1 <- derepFastq(filtR1, verbose=TRUE)

errF <- learnErrors(derepF1, multithread=FALSE) 
errR <- learnErrors(derepR1, multithread=FALSE)


dadaF1 <- dada(derepF1, err=errF, multithread=FALSE)
dadaR1 <- dada(derepR1, err=errR, multithread=FALSE)


merger1 <- mergePairs(dadaF1, derepF1, dadaR1, derepR1, verbose=TRUE)
merger1.nochim <- removeBimeraDenovo(merger1, multithread=FALSE, verbose=TRUE)

seqtab <- makeSequenceTable(list(merger1))
write.table(seqtab, file=paste(args$output, "OTU.tsv", sep = "/"), quote=FALSE, sep='\t', col.names = NA)

# nochim
seqtab.nochim <- removeBimeraDenovo(seqtab, verbose=TRUE)

getN <- function(x) sum(getUniques(x))
track <- cbind(out, sapply(dadaFs, getN), sapply(dadaRs, getN), sapply(mergers, getN), rowSums(seqtab.nochim))
colnames(track) <- c("input", "filtered", "denoisedF", "denoisedR", "merged", "nonchim")
rownames(track) <- sample.names

taxa <- assignTaxonomy(seqtab.nochim, args$database, multithread=TRUE)
taxa.print <- taxa
rownames(taxa.print) <- NULL
head(taxa.print)
write.table(taxa, file=paste(args$output, "TAXA.tsv", sep = "/"), quote=FALSE, sep='\t', col.names = NA)