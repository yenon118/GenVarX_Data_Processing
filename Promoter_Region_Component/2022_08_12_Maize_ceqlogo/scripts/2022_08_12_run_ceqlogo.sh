for i in $(ls /scratch/yenc/projects/2022_08_12_Maize_ceqlogo/data/*.meme | sed 's/.*\///g' | sed 's/.meme//g'); do \
echo ${i}; \
ceqlogo \
-i /scratch/yenc/projects/2022_08_12_Maize_ceqlogo/data/${i}.meme \
-m ${i} \
-o /scratch/yenc/projects/2022_08_12_Maize_ceqlogo/output/${i}.png \
-f PNG; \
done;
