for i in $(ls /scratch/yenc/projects/2022_08_12_Rice_Japonica_ceqlogo/data/*.meme | sed 's/.*\///g' | sed 's/.meme//g'); do \
echo ${i}; \
ceqlogo \
-i /scratch/yenc/projects/2022_08_12_Rice_Japonica_ceqlogo/data/${i}.meme \
-m ${i} \
-o /scratch/yenc/projects/2022_08_12_Rice_Japonica_ceqlogo/output/original/${i}.png \
-f PNG; \
done;
