#deseq2.r                        20.01.15
#hur.benjamin@mayo.edu
#
#run deseq2 for rawcounts
#
#[input data] and [input meta data] can be attained by using "prepare_DESeq2.py"
#
#cmd : deseq2.r [input data] [input meta data] [output name]


library(DESeq2)

#example data
#input_data <- read.csv('/Users/m221138/Scarisbrick_Project/RNAseq/deseq2/overall.tsv', sep="\t", row.names=1, header=TRUE)
#input_meta_data <- read.csv('/Users/m221138/Scarisbrick_Project/RNAseq/deseq2/overall.meta.tsv', sep="\t", header=TRUE, row.names=1)

args <- commandArgs(trailingOnly=TRUE)

input_data <- read.csv(args[1], sep="\t", row.names=1, header=TRUE)
input_meta_data <- read.csv(args[2], sep="\t", row.names=1, header=TRUE)
output_file <- args[3]
#output_ncount_file <- args[4]

cts <- as.matrix(input_data)
coldata <- input_meta_data

dds <- DESeqDataSetFromMatrix(countData = cts,
                              colData = coldata,
                              design = ~ condition)

dds <- estimateSizeFactors(dds)
norm.counts <- counts(dds, normalized=TRUE)
deseq_result <- DESeq(dds)

#res <- results(deseq_result)
#controlling the comparision order of conditions
#by default, it will compare conditions in alphabatic order. i.e. control vs case
#but I want case vs control for log2FC
res <- results(deseq_result, contrast=c("condition", "case","control"))


pvalue_orded_results <- res[order(res$pvalue),]
write.csv(as.data.frame(pvalue_orded_results), file=output_file, quote=FALSE)

#write.csv(as.data.frame(norm.counts), file=output_ncount_file, quote=FALSE)

