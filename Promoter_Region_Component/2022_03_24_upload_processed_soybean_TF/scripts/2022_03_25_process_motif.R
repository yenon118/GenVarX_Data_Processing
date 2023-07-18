#!/usr/bin/Rscript --vanilla
rm(list=ls())

library(jpeg)
library(dplyr)
library(tidyr)
library(tibble)
library(stringr)
library(ggplot2)

set.seed(1)


##################################################
# Constants/Variables
##################################################


##################################################
# Output folder
##################################################
output_path <- file.path("/data/yenc/projects/2022_03_24_mViz/2022_03_24_upload_processed_soybean_TF/output")

if(!dir.exists(output_path)){
  dir.create(output_path, showWarnings=FALSE, recursive=TRUE)
  if(!dir.exists(output_path)){
    quit(status=1)
  }
}


##################################################
# Read in input file
##################################################

folder_path = file.path("/data/yenc/projects/2022_03_24_mViz/2022_03_24_upload_processed_soybean_TF/data")

dat = read.table(
  file = file.path(folder_path, "Glycine_max_binding_regulation_merged_Gma.txt"),
  header = FALSE,
  sep = "\t",
  check.names = FALSE,
  stringsAsFactors = FALSE
)


##################################################
# Process the input file
##################################################

dat <- dat[,c(1,3)]

colnames(dat) = c("Motif", "Gene")

dat <- dat[stringr::str_starts(dat$Motif, "Glyma...G"), ]
dat <- dat[stringr::str_starts(dat$Gene, "Glyma...G"), ]

dat <- dat %>%
    distinct(Motif, Gene, .keep_all = TRUE) %>%
    arrange(Motif, Gene) %>%
    as.data.frame(stringsAsFactors = FALSE, check.names = FALSE)


print(head(dat))
print(tail(dat))
print(dim(dat))


##################################################
# Save processed data
##################################################
write.table(
  x = dat,
  file = file.path(output_path, "Glycine_max_binding_regulation_merged_Gma.txt"),
  sep = "\t",
  na = "",
  quote = FALSE,
  row.names = FALSE
)
