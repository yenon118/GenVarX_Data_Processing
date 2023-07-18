#!/usr/bin/Rscript --vanilla
rm(list=ls())

set.seed(1)

library(dplyr)
library(tidyr)
library(tibble)
library(stringr)

library(cn.mops)


##################################################
# Constants/Variables
##################################################


##################################################
# Output folder
##################################################
output_path <- file.path("../output")

if(!dir.exists(output_path)){
  dir.create(output_path, showWarnings=FALSE, recursive=TRUE)
  if(!dir.exists(output_path)){
    quit(status=1)
  }
}


##################################################
# Read in input file
##################################################

folder_path = file.path("/90daydata/bilyeu_soybean_genomic_merge/yenc/datasets/Maize1210/renamed_BAM_files")

bam_files <- list.files(path = folder_path, pattern =".*\\.bam$", full.names = FALSE)

print(head(bam_files))
print(length(bam_files))

bam_files_prefixes <- gsub(".bam", "", bam_files)

bam_files <- file.path(folder_path, bam_files)

print(head(bam_files))
print(length(bam_files))


##################################################
# Get read counts from BAM files
##################################################

bamDataRanges <- getReadCountsFromBAM(
  bam_files,
  refSeqName=c(
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "10"
  ),
  parallel=4
)

res <- cn.mops(bamDataRanges)

res <- calcIntegerCopyNumbers(res)


##################################################
# Save to Rdata
##################################################

save(bam_files, bamDataRanges, res, file=file.path(output_path, "maize_cnv.RData"))


##################################################
# Validations and data processing
##################################################

ranges_obj <- ranges(cnvr(res))

idx <- ranges(cnvr(res)) %over% ranges(bamDataRanges)

print(length(idx))
print(sum(idx, na.rm = TRUE))
print(sum(!idx, na.rm = TRUE))


segm <- as.data.frame(segmentation(res), check.names = FALSE, stringsAsFactors = FALSE, optional = TRUE)

CNVs <- as.data.frame(cnvs(res), check.names = FALSE, stringsAsFactors = FALSE, optional = TRUE)

print(head(CNVs))

CNVRegions <- as.data.frame(cnvr(res), check.names = FALSE, stringsAsFactors = FALSE, optional = TRUE)

ranges_df <- as.data.frame(ranges_obj)


print(head(CNVRegions))
print(dim(CNVRegions))


##################################################
# Save outputs
##################################################

write.csv(
    segm, 
    file = file.path(output_path, "segmentation.csv"),
    na = "",
    quote = FALSE,
    row.names = FALSE
)
write.csv(
    CNVs, 
    file = file.path(output_path, "cnvs.csv"),
    na = "",
    quote = FALSE,
    row.names = FALSE
)
write.csv(
    CNVRegions, 
    file = file.path(output_path, "cnvr.csv"),
    na = "",
    quote = FALSE,
    row.names = FALSE
)
write.csv(
    ranges_df, 
    file = file.path(output_path, "ranges_df.csv"),
    na = "",
    quote = FALSE,
    row.names = FALSE
)
