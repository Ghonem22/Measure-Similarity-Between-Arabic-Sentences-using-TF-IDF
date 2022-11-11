# Measure-Similarity-Between-Arabic-Sentences-using-TF-IDF

## Get the similarity between tweets against some keywords we write in yaml file

### How to use

1. git clone https://github.com/Ghonem22/Measure-Similarity-Between-Arabic-Sentences-using-TF-IDF.git

2. change directory to project folder 

3. Create virtual environment
        conda create -n similarity python=3.9
   
4. activate virtaul env
        conda activate similarity
   
5. install requirements
        pip install -r requirements.txt
   
6. edit the keywods in the yaml file

7. run in terminal
        python get_similarity.py
   
8. the code wil generate csv file with new columns (new column for each keyword)