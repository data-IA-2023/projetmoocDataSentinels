# projetmoocDataSentinels

lien du trello : https://trello.com/invite/b/97gStloa/ATTI77219a83e9f886a5c986948c763e47c46A4CD3BB/mooc

lien du google doc : https://docs.google.com/document/d/1RpKTF53EDqeXQOWVQJqJz2Hf-2vFspMKKSNg8GAF2oM/edit?usp=sharing


## rôle :
gestion de gitHub : Jonathan

gestion de trello et chef de projet : Sandy

gestion de machine virtuel et de base de données : Mohammed


## détaille de l'application :

L'application est codé avec streamlit. Elle permet de remplir un formulaire et d'ans faire l'analise grâce à plusieur modele de machine learning :

    . modèle de détection de langue
  
    . modèle d'analyse de sentiments
  
    . modèle de  prévision de réussite
  
    . topic modeling
    
    . FAQ
  

L'application est déployer sur docker mais pas sur azure via machine virtuel.
  
L'apllication intègres des test de non régrétion et de build.


## détaille des modèles :

### modèle de détection de langue et d'analyse de sentiments

Après comparaison des différents modèles pré-entraînés, nous avons choisi RoBERTa pour l'analyse de sentiment.

RoBERTa : BERT (Bidirectional Encoder Representations from Transformers) est un modèle de langage profond développé par Google. Bien qu'il soit principalement utilisé pour des tâches de compréhension de texte, il peut également être adapté à l'analyse de sentiment en fine-tunant le modèle sur des données d'analyse de sentiment. Implémentations disponibles en Python : Hugging Face Transformers, TensorFlow, PyTorch.

Pour détecter la langue, nous avons choisi langdetect, un module Python.

### modèle de  prévision de réussite

Pour le modèle de prévition nous avons crée et entrainner un modele personnelle de RandomForestRegressor.


Le modele est intégré à MLFlow.

![image](https://github.com/data-IA-2023/projetmoocDataSentinels/assets/43037380/c44dbd32-ca66-4f5b-9c67-c1e73f7c23c8)

![image2](https://github.com/data-IA-2023/projetmoocDataSentinels/assets/43037380/769db225-d02a-41ad-bb5e-0669572b5952)


### topic modeling et FAQ :

Pour le modèle de recherche de topics et FAQ, nous avons créé et entraîné un modèle personnel.

Le modèle est basé sur le modèle CamemBERT, nous faisons l'embedding du texte du message à analyser. Ensuite, nous effectuons une similarité cosinus sur les messages de la base de données. Pour plus d'efficacité et de rapidité, la similarité cosinus est calculée directement dans la base de données, pendant la requête. Les 7 messages les plus similaires sont affichés. Le topic est le cours et la session des messages.



## Base de données :

Les fichier json sont ouvert et annalyser sur mangoDB. Nous avons, par la suite migré les informations utiles dans une base de Donnée SQL postgres pour plus de facilité.

![diagram_bd](https://github.com/data-IA-2023/projetmoocDataSentinels/assets/43037380/0f121aa8-97d1-48b5-aa22-c14624790b90)


## Visuel de l'application :

![Capture3](https://github.com/data-IA-2023/projetmoocDataSentinels/assets/43037380/748f9f98-b00d-48b4-a96e-0f96c431f766)
