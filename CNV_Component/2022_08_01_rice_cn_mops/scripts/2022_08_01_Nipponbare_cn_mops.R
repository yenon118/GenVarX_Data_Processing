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
output_path <- file.path("../output/Nipponbare/")

if(!dir.exists(output_path)){
  dir.create(output_path, showWarnings=FALSE, recursive=TRUE)
  if(!dir.exists(output_path)){
    quit(status=1)
  }
}


##################################################
# Read in input file
##################################################

folder_path = file.path("../data/Nipponbare/output")

bam_files <- list.files(path = folder_path, pattern =".*\\.bam$", full.names = TRUE)

print(length(bam_files))

# Remove this line when run all
# bam_files <- bam_files[str_detect(bam_files, pattern = "(CX357)|(CX358)|(IRIS_313-12082)|(IRIS_313-12066)")]


##################################################
# Get read counts from BAM files
##################################################

bamDataRanges <- getReadCountsFromBAM(
  bam_files,
  refSeqName=c(
    "chr01",
    "chr02",
    "chr03",
    "chr04",
    "chr05",
    "chr06",
    "chr07",
    "chr08",
    "chr09",
    "chr10",
    "chr11",
    "chr12"
  ),
  parallel=4
)

res <- cn.mops(bamDataRanges)

res <- calcIntegerCopyNumbers(res)


##################################################
# Save to Rdata
##################################################

save(bam_files, bamDataRanges, res, file=file.path(output_path, "rice_cnv.RData"))


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
