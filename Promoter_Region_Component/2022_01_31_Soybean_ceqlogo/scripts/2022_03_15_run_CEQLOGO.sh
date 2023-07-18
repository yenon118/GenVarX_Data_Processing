for i in $(ls /scratch/yenc/projects/2022_01_31_Soybean_ceqlogo/data/*.meme | sed 's/.*\///g' | sed 's/.meme//g' | grep "Glyma\...G"); do \
echo ${i}; \
ceqlogo \
-i /scratch/yenc/projects/2022_01_31_Soybean_ceqlogo/data/${i}.meme \
-m ${i} \
-o /scratch/yenc/projects/2022_01_31_Soybean_ceqlogo/output/${i}.png \
-f PNG; \
done;
