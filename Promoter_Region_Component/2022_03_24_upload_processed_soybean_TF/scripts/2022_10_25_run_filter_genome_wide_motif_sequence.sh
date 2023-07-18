source /data/yenc/tools/my_environment/bin/activate

python3 2022_10_25_filter_genome_wide_motif_sequence.py \
-i ../data/Glycine_max_binding_TFBS_from_motif_genome-wide_Gma.gff \
-r ../../2022_03_24_upload_processed_soybean_gff/output/gene_region.txt \
-c ${1} \
-o ../output/Glycine_max_binding_TFBS_from_motif_genome-wide_Gma_${1}.txt

deactivate
