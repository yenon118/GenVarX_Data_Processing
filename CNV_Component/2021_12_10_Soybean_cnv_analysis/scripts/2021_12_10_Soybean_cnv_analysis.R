#!/usr/bin/Rscript --vanilla
rm(list=ls())

set.seed(1)

library(jpeg)
library(dplyr)
library(tidyr)
library(tibble)
library(stringr)
library(ggplot2)
library(argparse)

library(cn.mops)


#######################################################################
# Constants/Variables
#######################################################################


##################################################
# Output folder
##################################################
output_path <- file.path("/scratch/yenc/projects/2021_12_10_Soybean_cnv_analysis/2021_12_10_Soybean_cnv_analysis/output")

if(!dir.exists(output_path)){
  dir.create(output_path, showWarnings=FALSE, recursive=TRUE)
  if(!dir.exists(output_path)){
    quit(status=1)
  }
}


##################################################
# Read in input file
##################################################

folder_path = file.path("/scratch/yenc/datasets/Soy1066")

bam_files <- Sys.glob(file.path(folder_path, "GATK_AddOrReplaceReadGroups", "*.bam"), dirmark = FALSE)
bam_file_prefixes <- gsub("(.*/)|(.bam)", "", bam_files)

soy1066_samples <- read.table(
  file = file.path(folder_path, "Soy1066_samples.txt"),
  header = FALSE,
  check.names = FALSE,
  stringsAsFactors = FALSE
)

idx <- (bam_file_prefixes %in% soy1066_samples[,1])
bam_files <- bam_files[idx]


print(length(bam_files))


##################################################
# Get read counts from BAM files
##################################################

bamDataRanges <- getReadCountsFromBAM(
  bam_files,
  refSeqName=c(
    "Chr01",
    "Chr02",
    "Chr03",
    "Chr04",
    "Chr05",
    "Chr06",
    "Chr07",
    "Chr08",
    "Chr09",
    "Chr10",
    "Chr11",
    "Chr12",
    "Chr13",
    "Chr14",
    "Chr15",
    "Chr16",
    "Chr17",
    "Chr18",
    "Chr19",
    "Chr20"
  ),
  parallel=4
)

res <- cn.mops(bamDataRanges)


##################################################
# Save to Rdata
##################################################

save(bam_files, bamDataRanges, res, file=file.path(output_path, "2021_12_10_soybean_cnv_analysis.RData"))
