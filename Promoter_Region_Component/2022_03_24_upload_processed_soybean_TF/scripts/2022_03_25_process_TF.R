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
  file = file.path(folder_path, "Gma_TF_list.txt"),
  header = TRUE,
  sep = "\t",
  check.names = FALSE,
  stringsAsFactors = FALSE
)


##################################################
# Process the input file
##################################################

dat <- dat[,2:3]

colnames(dat) = c("TF", "TF_Family")


dat <- dat[stringr::str_starts(dat$TF, "Glyma...G"), ]

dat <- dat %>%
    distinct(TF, TF_Family, .keep_all = TRUE) %>%
    arrange(TF, TF_Family) %>%
    as.data.frame(stringsAsFactors = FALSE, check.names = FALSE)

print(head(dat))
print(tail(dat))
print(dim(dat))


##################################################
# Save processed data
##################################################
write.table(
  x = dat,
  file = file.path(output_path, "Gma_TF_list.txt"),
  sep = "\t",
  na = "",
  quote = FALSE,
  row.names = FALSE
)
