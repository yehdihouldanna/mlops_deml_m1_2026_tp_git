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


