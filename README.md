# mlops_deml_m1_2026_tp_git
Un repository pour le TP git pour les elèves SUPNUM DEML M1 2026

# LAB 2 : Git Seance interactive :

1. Crée un dossier pour le TP "TP Git"
2. Accepter l'invitation sur le repository
3. Allez dans votre dossier TP Git et cloner le repository du cours
`git clone git@github.com:yehdihouldanna/mlops_deml_m1_2026_tp_git.git`
4. Crée une branche avec votre nom :
    4.1 `git create branch BRANCHE_NAME`
    4.2 depuis le UI de github.
    4.3 aussi vous pouvez le faire avec `git checkout -b BRANCH_NAME`
4. Switcher la branche de travail local sur le votre
`git checkout VOTRE_BRANCH_NAME`
ex : `git checkout yehdih`



# LAB 3 : Serveur MLFlow sur EC2 
## 1.1. Mise de l'environement MLFLOW sur AWS : 

Le but de cet etape et des crée un serveur MLFlow, qui gère le registry de nos experiences MLs:

1. Allez dans votre compte AWS,
2. Crée un bucket s3, (rendre son accès public - pour minimiser les configuration nécessaire entre s3 et MLFLOW)
4. Crée un clé d'accès (Access Key) et  telecharger la, dans le fichier csv (vous trouvez votre Access_key_Id et Votre Secret_key).
5. Crée une machine Ec2 (type medium, OS:ubuntu), crée un key paire pour cette machine. donnez lui un accès Custom Port 5000 avec source 0.0.0.0/0 (tous le monde), 

- 5.1 Connecter sur cette machine avec ssh : 

```bash
    chmod 600 VOTRE_CLE.pem
    ssh -i VOTRE_CLE.pem ubuntu@ADRESSE_IP_PUBLIC_EC2
    
    # example 
    ssh -i /Users/yehdhihanna/Local-Documents/Teaching/MLOps_SupNum_DELM/2026/2026-m1-yehdih-lab3.pem ubuntu@51.44.165.217
    ssh -i /Users/yehdhihanna/Local-Documents/Teaching/MLOps_SupNum_DELM/2026/2026-m1-yehdih-lab3.pem ubuntu@15.237.119.156
```


- 5.2 OU connecter sur la machine depuis l'interface aws avec le boutton connect


6. sur cette machine on doit configurer notre MLFLOW avec les commandes suivantes (y inclut l'installation de quelques dependances) : 
```bash
sudo apt update
sudo apt install python3-pip
sudo apt install pipenv
sudo apt install virtualenv
mkdir mlflow
cd mlflow
pipenv install mlflow
pipenv install awscli
pipenv install boto3
pipenv shell
```
6. Maintenant configurer les accès à s3 pour MLflow depuis la machine (grace au clé que vous avez crée pour l'utilisateur dans l'etape 4)

```bash
# Set aws credentials
aws configure
```

7. Maintenant vous pouvez lancer mlflow dans cette machine en y précisant le nom de votre bucket (NB: le bucket sera utilisé pour stoker le cashe de MLFLOW : les runs, les experiments, les artefacts loggué, les models ...)

```bash
    # run mlflow server to be accessible globaly
    mlflow server --host 0.0.0.0 --port 5000 --default-artifact-root s3://YOUR_BUCKET_NAME --allowed-hosts "*" --cors-allowed-origins "*" 
```

    # run mlflow server to be accessible globaly
    mlflow server --host 0.0.0.0 --port 5000 --default-artifact-root s3://2026-m1-yehdih-lab3-mlflow-sur-ec2 --allowed-hosts "*" --cors-allowed-origins "*" 

6. [Conditionel] Si vous avez skipper le custom port 5000 accès vous pouvez allez dans la liste des instances EC2, clicker sur l'ID de votre instance, et dans l'onglet Security clicker sur le nom de votre security group,
et ajouter une nouvelle règle dans les inboud rules. 
_Custom - Port 5000 - 0.0.0.0/0_

8. Mlflow est running donc vous pouvez l'accéder depuis l'adresse le lien `http://ADDRESS_IP_EC2:5000`

9. Si vous avez stopper la machine et vous avez connecter à nouveau il faut reactiver l'environement pipenv et relancer votre mlflow.
> pipenv est un gestionaire d'environement python basé sur le dossier (dans ce cas "mlflow") ce n'est pas commes les autres packageurs d'environnement qui peuvent etre activé globalement avec un chemin absolue.
```bash
    cd mlflow
    pipenv shell
    mlflow server --host 0.0.0.0 --port 5000 --default-artifact-root s3://YOUR_BUCKET_NAME --allowed-hosts "*" --cors-allowed-origins "*" 
    cd mlflow
    pipenv shell
    mlflow server --host 0.0.0.0 --port 5000 --default-artifact-root s3://2026-m1-yehdih-lab3-mlflow-sur-ec2 --allowed-hosts "*" --cors-allowed-origins "*" 
    cd mlflow
    pipenv shell
    mlflow server --host 0.0.0.0 --port 5000 --default-artifact-root s3://lab1-s3-yana --allowed-hosts "*" --cors-allowed-origins "*" 



    # to keeps from stopping after closing the terminal you can use this command
    cd mlflow
    pipenv shell
    nohup mlflow server --host 0.0.0.0 --port 5000 --default-artifact-root s3://lab1-s3-yana --allowed-hosts "*" --cors-allowed-origins "*" > mlflow.log 2>&1 &
```

10. Maintenant vous pouvez exploiter MLFlow pour faire le suivi de vos modèles (en précisant le tracking uri dans votre code ) :

```python
import mlflow
mlflow.set_tracking_uri("http://ADDRESS_IP_EC2:5000")
```

> TRES BIEN VOUS AVEZ COMPLETE CETTE ETAPE.



# LAB 4 & 5 : dvc (Data version control)


## 4.1. Data Originale (Source de données) :
Pour similer une situation du monde réel avec une source de données externe dynamique nous allons crée sur notre bucket s3 un dossier dédié pour les données raw (ceci pourra venir de plusieurs sources).

Dans votre bucket S3 crée les dossier ``data/raw`` et uploader votre fichier ``data.csv``
en meme temps crée aussi le dossier ``data/processed``

Donc vous devrez avoir ce chemin dans votre bucket s3
`s3://YOUR_BUCKET_NAME/data/raw/data.csv`

> Dans le monde réel ceci pourra simuler le resultat d'un ETL lourd

## 4.2. Repository dvc sur s3 :

> Il existe des outils pour faire le repository dvc, cependant il faut comprendre que le dvc crée un fichier d'historique des metadata des données (elle ne stocke pas les données, mais chaque push de dvc correspond à un etat 'metadata' de données, elle peut contenir le path, sans contenir les données eux memes.)
> Cependant nous allons heberger notre repository dvc sur s3 c'est simple comme ça.
> Du coup on a deux chose à garder sur notre s3, nos données de base (n'a rien avoir avec dvc nécessairement, on peut avoir des données qui sont misees à jour journalierement)

1. initier dvc avec `dvc init`
2. crée une repository dvc  (attention : il faut crée cette dossier dans le meme dossier que votre git.)
(La ceci est le store c'est à dire il contient notre tree dvc)

configure local pc to communicate with aws:

```bash
conda install -c conda-forge awscli boto3
aws configure
```

```bash
    dvc init
    conda install dvc[s3]

    # 1. Define where DVC should store its actual "packages" (The Cache)
    dvc remote add -d dvcstore s3://YOUR_BUCKET_NAME

    # 2. Tell DVC to use your AWS credentials
    dvc remote modify dvcstore access_key_id   VOTRE_ACCESS_KEY_ID
    dvc remote modify dvcstore secret_access_key VOTRE_SECRET_ACCESS_KEY
```
3. Ajouter la source de données à tracker : 

```bash
    dvc import-url s3://YOUR_BUCKET_NAME/data/ .
    dvc import-url s3://lab1-s3-yana/data/ .
    #dvc import-url --to-remote s3://YOUR_BUCKET_NAME/data/ .


    dvc add data
    dvc push # now you can check on your s3 to see the result
```
> --to-remote permet de n'a pas avoir une copie local du fichier dans le dossier du code (la copie sera telechargé ailleur et son hash md5 sera claculé et sera supprimé après), si vous l'enlever le fichier sera dans votre dossier data

## 4.3. Adjuster votre fichier params :

ex:
```yaml
preprocess:
  input : s3://YOUR_BUCKET/data/raw/data.csv
  output : s3://YOUR_BUCKET/data//processed/data_processed.csv

train : 
  data: s3://YOUR_BUCKET/data/processed/data_processed.csv
  model_path : models/model.pkl

evaluate :
  model_path : models/model.pkl
  data_path : s3://YOUR_BUCKET/data/processed/data_processed.csv

aws :
  aws_access_key_id: *
  aws_secret_access_key: *
  region_name: eu-west-3

mlflow:
  MLFLOW_TRACKING_URI: "http://YOUR_IP_ADRESS:5000"
#   MLFLOW_TRACKING_URI: http://localhost:5050/
  EXPERIMENT_NAME: "Student_Experiment"
```
> Ce fichier assume que votre code preprocessing (utilise des données diabetes csv local [ou traked avec dvc et pulled]), applique le preprocessing pour sauvergarder une version preprocessed sur s3, et utlise la version sauvegardé sur s3 pour faire le training.
> EN suite le fichier evaluate utilise le mlflow running sur ec2 pour recuperer la version nommé dans le code de votre modèle pour l'appeler.

## 4.4 La commande qui automatise le lancement du pipeline dvc :
Maintenant avec la façon dont notre code est structuré en phases (preprocess et train)
nous pouvons lancer tous le flow quand on veut avec 

```bash
dvc repro
```
et vous devrais voir les sorties des données dans votre bucket s3
et les modèles dans l'interface de mlflow server.

---

