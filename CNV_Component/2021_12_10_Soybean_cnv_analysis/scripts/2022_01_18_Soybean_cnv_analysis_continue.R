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

folder_path = file.path("/scratch/yenc/projects/2021_12_10_Soybean_cnv_analysis/2021_12_10_Soybean_cnv_analysis/output")

idx <- load(file.path(folder_path, "2021_12_10_soybean_cnv_analysis.RData"), verbose = TRUE)


res <- calcIntegerCopyNumbers(res)


##################################################
# Save to Rdata
##################################################

save(bam_files, bamDataRanges, res, file=file.path(output_path, "2022_01_18_soybean_cnv_analysis.RData"))
