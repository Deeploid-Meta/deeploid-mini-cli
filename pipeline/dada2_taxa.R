# !/usr/bin/env Rscript
suppressPackageStartupMessages(library("argparse"))
library(dada2); packageVersion("dada2")

# create parser object
parser <- ArgumentParser()

parser$add_argument("-t", "--type", type = "character", default = "otu",
    help = "Enter type for start: otu - create OTU, taxa - create taxonomy.")
parser$add_argument("-1", "--forward", type = "character",
    help = "Enter path to forward reads")
parser$add_argument("-2", "--reverse", type = "character",
    help = "Enter path to forward reads")
parser$add_argument("-db", "--database", type = "character",
    help = "Enter path to database for taxanomy, file extension fa.gz")
parser$add_argument("-o", "--output", type = "character", default = "outupt",
    help = "Enter path to output result")
parser$add_argument("-p", "--pattern", type = "character", default = "fastq",
    help = "Enter pattern for reads example: *.fastq or *_R1_001.fastq")

args <- parser$parse_args()

filts_forward <- list.files(args$forward, 
                            pattern = args$pattern, 
                            full.names = TRUE)
## list of sample prefixes
filtFs <- sapply(strsplit(basename(filts_forward), "\\."), `[`, 1)
## name all reads with prefix
names(filtFs) <- sample.names

set.seed(100)

errF <- learnErrors(filtFs, multithread=TRUE)
dadaFs <- dada(filtFs, err=errF, multithread=TRUE)


if (args$reverse) {
    filts_reverse <- list.files(args$reverse, 
                                pattern = args$pattern, 
                                full.names = TRUE)
    filtRs <- sapply(strsplit(basename(filts_reverse), "\\."), `[`, 1)
    names(filtRs) <- sample.names

    out <- filterAndTrim(filts_forward, filtFs, filts_reverse, filtRs, truncLen=c(240,160),
              maxN=0, maxEE=c(2,2), truncQ=2, rm.phix=TRUE,
              compress=TRUE, multithread=TRUE)
    errR <- learnErrors(filtRs, multithread=TRUE)

    dadaRs <- dada(filtRs, err=errR, multithread=TRUE)
    mergers <- mergePairs(dadaFs, filtFs, dadaRs, filtRs, verbose=TRUE)
    seqtab <- makeSequenceTable(mergers)
} else {
    dds <- vector("list", length(sample.names))
    names(dds) <- sample.names
    for(sam in sample.names) {
    cat("Processing:", sam, "\n")
    derep <- derepFastq(filts[[sam]])
    dds[[sam]] <- dada(derep, err=err, multithread=TRUE)
    }
    seqtab <- makeSequenceTable(dds)
}

saveRDS(seqtab, paste(args$reverse, "otu.rds", sep = "/")) 


if (args$type == "taxa"){
    if (args$database){
        taxanomy <- assignTaxonomy(seqtab, args$database, multithread=TRUE)
        saveRDS(taxanomy, paste(args$reverse, "taxa.rds", sep = "/"))
    } else {
        cat("Add database for analyse")
    }
}