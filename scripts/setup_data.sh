set -ex
mkdir -p ./data/raw

# Defacto
git clone https://github.com/microsoft/DeFacto.git --depth 1
mv DeFacto/data ./data/raw/defacto
rm -rf DeFacto

# Evidence
gdown https://drive.google.com/uc?id=1z63sisek--NxJABHpd28NGscPGcGgWCS
mkdir -p ./data/raw/evidence/ && mv dpr_50_3_test.jsonl ./data/raw/evidence/

# Fact Edit
git clone git@github.com:isomap/factedit.git --depth 1
tar -xjvf ./factedit/data/rotoedit.tar.bz2
mv rotoedit ./data/raw/factedit
rm -rf factedit

# Fruit  # Need to resolve dependencies
#mkdir -p fruit_dataset
#gsutil cp -R gs://gresearch/FRUIT/dataset fruit_dataset
#wget https://raw.githubusercontent.com/google-research/language/master/language/fruit/convert_task_to_jsonl.py -P fruit_dataset
#python fruit_dataset/convert_task_to_jsonl.py --task_name="wikidiff_diff_all_text_reference_gold_test" --split="test"
#mkdir -p ./data/raw/fruit && mv gold_test_inputlabels.jsonl ./data/raw/fruit
#rm -rf fruit_dataset

# StylePTB
git clone https://github.com/lvyiwei1/StylePTB.git --depth 1
mkdir -p ./data/raw/styleptb/ && mv StylePTB/Amazon\ Mechanical\ Turk\ Webpages\ and\ Results/InfoAdditionFullResult.csv ./data/raw/styleptb
rm -rf StylePTB

# WikiBias
mkdir -p ./data/raw/wikibias/
gdown https://drive.google.com/uc?id=11uJE9S3Dnj6AjS9CjIxDgS0V-Xrord4H
gdown https://drive.google.com/uc?id=1fsdE2Y4nOZXes-E04pgxkttjhCAlHE8_
mv test_source.tsv ./data/raw/wikibias/
mv test_target.tsv ./data/raw/wikibias/

# WNC
wget https://www.dropbox.com/s/qol3rmn0rq0dfhn/bias_data.zip
unzip bias_data.zip && rm bias_data.zip
mv bias_data/WNC ./data/raw/wnc
rm -rf bias_data