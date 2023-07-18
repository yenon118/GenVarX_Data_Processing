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
output_path <- file.path("/data/yenc/projects/2022_03_24_mViz/2022_05_01_upload_processed_arabidopsis_TF/output")

if(!dir.exists(output_path)){
  dir.create(output_path, showWarnings=FALSE, recursive=TRUE)
  if(!dir.exists(output_path)){
    quit(status=1)
  }
}


##################################################
# Read in input file
##################################################

folder_path = file.path("/data/yenc/projects/2022_03_24_mViz/2022_05_01_upload_processed_arabidopsis_TF/data")

dat = read.table(
  file = file.path(folder_path, "Arabidopsis_thaliana_binding_TFBS_from_motif_genome-wide_Ath.gff"),
  header = FALSE,
  sep = "\t",
  check.names = FALSE,
  stringsAsFactors = FALSE
)


##################################################
# Process the input file
##################################################

colnames(dat) = c("Chromosome", "Source", "Feature", "Start", "End", "Score", "Strand", "Frame", "V9")


dat$ID = dat$V9
dat$Name = dat$V9
dat$Sequence = dat$V9

dat = dat %>%
    mutate(
        ID = gsub("(.*ID=)|(;.*)", "", ID),
        Name = gsub("(.*Name=)|(;.*)", "", Name),
        Sequence = gsub("(.*equence=)|(;.*)", "", Sequence)
    ) %>%
    as.data.frame(stringsAsFactors = FALSE, check.names = FALSE)

dat <- dat[,-9]

dat <- dat[startsWith(dat$Chromosome, "Chr"), ]

dat <- dat %>%
    arrange(desc(Score)) %>%
    distinct(Chromosome, Source, Feature, Start, End, Strand, Name, Sequence, .keep_all = TRUE) %>%
    arrange(Chromosome, Start, End) %>%
    as.data.frame(stringsAsFactors = FALSE, check.names = FALSE)

print(head(dat))
print(tail(dat))
print(dim(dat))


##################################################
# Save processed data
##################################################
write.table(
  x = dat,
  file = file.path(output_path, "Arabidopsis_thaliana_binding_TFBS_from_motif_genome-wide_Ath.txt"),
  sep = "\t",
  na = "",
  quote = FALSE,
  row.names = FALSE
)
