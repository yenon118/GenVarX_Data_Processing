#!/usr/bin/Rscript --vanilla
rm(list=ls())

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

folder_path = file.path("../data")

dat = read.table(
  file = file.path(folder_path, "RAP-MSU_2022-03-11.txt"),
  header = TRUE,
  sep = "\t",
  check.names = FALSE,
  stringsAsFactors = FALSE
)

print(head(dat))
print(tail(dat))
print(dim(dat))


##################################################
# Process the input file
##################################################

colnames(dat) = c("New_ID", "Old_ID")


dat <- dat %>%
    separate_rows(Old_ID, sep = ",", convert = TRUE) %>%
    filter(Old_ID != "None") %>%
    filter(New_ID != "None") %>%
    mutate(Old_ID = gsub("(LOC_)|(\\..*)", "", Old_ID)) %>%
    distinct() %>%
    as.data.frame(stringsAsFactors = FALSE, check.names = FALSE)

print(head(dat))
print(tail(dat))
print(dim(dat))


##################################################
# Save processed data
##################################################
write.table(
  x = dat,
  file = file.path(output_path, "RAP_MSU_2022_03_11.txt"),
  sep = "\t",
  na = "",
  quote = FALSE,
  row.names = FALSE
)
