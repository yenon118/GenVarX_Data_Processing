source /data/yenc/tools/my_environment/bin/activate

python3 2022_10_25_filter_genome_wide_motif_sequence.py \
-i ../data/Arabidopsis_thaliana_binding_TFBS_from_motif_genome-wide_Ath.gff \
-r ../../2022_08_11_upload_processed_arabidopsis_gff/output/gene_region.txt \
-c ${1} \
-o ../output/Arabidopsis_thaliana_binding_TFBS_from_motif_genome-wide_Ath_${1}.txt

deactivate
