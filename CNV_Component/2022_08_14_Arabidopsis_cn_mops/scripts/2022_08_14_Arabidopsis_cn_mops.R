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
output_path <- file.path("../output/")

if(!dir.exists(output_path)){
  dir.create(output_path, showWarnings=FALSE, recursive=TRUE)
  if(!dir.exists(output_path)){
    quit(status=1)
  }
}


##################################################
# Read in input file
##################################################

folder_path = file.path("/storage/htc/joshilab/yenc/datasets/Arabidopsis1135/output/GATK_AddOrReplaceReadGroups")

bam_files <- list.files(path = folder_path, pattern =".*\\.bam$", full.names = TRUE)

print(length(bam_files))


##################################################
# Get read counts from BAM files
##################################################

bamDataRanges <- getReadCountsFromBAM(
  bam_files,
  refSeqName=c(
    "Chr1",
    "Chr2",
    "Chr3",
    "Chr4",
    "Chr5"
  ),
  parallel=4
)

res <- cn.mops(bamDataRanges)

res <- calcIntegerCopyNumbers(res)


##################################################
# Save to Rdata
##################################################

save(bam_files, bamDataRanges, res, file=file.path(output_path, "arabidopsis_cnv.RData"))


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
