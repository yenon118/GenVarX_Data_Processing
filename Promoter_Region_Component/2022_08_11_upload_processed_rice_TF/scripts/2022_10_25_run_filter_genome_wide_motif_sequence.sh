source /data/yenc/tools/my_environment/bin/activate

python3 2022_10_25_filter_genome_wide_motif_sequence.py \
-i ../output/Oryza_sativa_Japonica_Group_TFBS_from_motif_genome-wide_Osj.gff \
-r ../../2022_08_11_upload_rice_gff/output/mViz_Rice_Nipponbare_GFF.txt \
-c ${1} \
-o ../output/Oryza_sativa_Japonica_Group_TFBS_from_motif_genome-wide_Osj_${1}.txt

deactivate
