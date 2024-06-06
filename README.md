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
  

  L'application est déployer sur azure via machine virtuel et docker.
  L'apllication intègres des test de non régrétion et de build.


## détaille des modèles :

### modèle de détection de langue et d'analyse de sentiments

### modèle de  prévision de réussite

le modele est intégré à MLFlow

![image](https://github.com/data-IA-2023/projetmoocDataSentinels/assets/43037380/c44dbd32-ca66-4f5b-9c67-c1e73f7c23c8)

![image2](https://github.com/data-IA-2023/projetmoocDataSentinels/assets/43037380/769db225-d02a-41ad-bb5e-0669572b5952)


### topic modeling et FAQ :

## Base de données :

Les fichier json sont ouvert et annalyser sur mangoDB. Nous avons, par la suite migré les informations utiles dans une base de Donnée SQL postgres pour plus de facilité.

![diagram_bd](https://github.com/data-IA-2023/projetmoocDataSentinels/assets/43037380/0f121aa8-97d1-48b5-aa22-c14624790b90)


## visuel de l'application :

![Capture3](https://github.com/data-IA-2023/projetmoocDataSentinels/assets/43037380/07c58f43-5a6e-41f0-9755-274d1c5424a1)


