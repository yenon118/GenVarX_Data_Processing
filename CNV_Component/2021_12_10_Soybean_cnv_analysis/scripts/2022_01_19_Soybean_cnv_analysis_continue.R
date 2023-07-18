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
output_path <- file.path("/scratch/yenc/projects/2021_12_10_Soybean_cnv_analysis/2021_12_10_Soybean_cnv_analysis/output/CNVRegionsPlots")

if(!dir.exists(output_path)){
  dir.create(output_path, showWarnings=FALSE, recursive=TRUE)
  if(!dir.exists(output_path)){
    quit(status=1)
  }
}

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

idx <- load(file.path(folder_path, "2022_01_18_soybean_cnv_analysis.RData"), verbose = TRUE)


ranges <- ranges(cnvr(res))

idx <- ranges(cnvr(res)) %over% ranges(bamDataRanges)

print(length(idx))
print(sum(idx, na.rm = TRUE))
print(sum(!idx, na.rm = TRUE))


segm <- as.data.frame(segmentation(res), check.names = FALSE, stringsAsFactors = FALSE)

CNVs <- as.data.frame(cnvs(res), check.names = FALSE, stringsAsFactors = FALSE)

CNVRegions <- as.data.frame(cnvr(res), check.names = FALSE, stringsAsFactors = FALSE)

ranges_df <- as.data.frame(ranges)


print(head(CNVRegions))
print(dim(CNVRegions))


##################################################
# Save outputs
##################################################

cat(rep("\n", 2))
for(i in 1:nrow(CNVRegions)){
  jpeg(
    filename = file.path(
      output_path, "CNVRegionsPlots",
      paste0(
        "detected_cnv_region_", 
        CNVRegions[i,1], "_", 
        CNVRegions[i,2], "_", 
        CNVRegions[i,3], "_", 
        CNVRegions[i,4], ".jpeg"
      )
    )
  )
  plot(res, which = i, toFile = TRUE)
  dev.off()
}



write.csv(
    segm, 
    file = file.path(output_path, "segmentation.csv"),
    na = "",
    quote = FALSE
)
write.csv(
    CNVs, 
    file = file.path(output_path, "cnvs.csv"),
    na = "",
    quote = FALSE
)
write.csv(
    CNVRegions, 
    file = file.path(output_path, "cnvr.csv"),
    na = "",
    quote = FALSE
)
write.csv(
    ranges_df, 
    file = file.path(output_path, "ranges_df.csv"),
    na = "",
    quote = FALSE
)
