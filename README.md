# Books Online

 Ce projet a été réalisé dans le cadre de la formation OpenClassrooms *Développeur d'application - Python*.

## Présentation de l'application :

**Books Online** est un projet de web scraping.

Le site web objet du scraping est [*books.toscrape.com*](http://books.toscrape.com/index.html), il s'agit d'une librairie en ligne fictive.

Pour chaque catégorie d'ouvrage, le script crée :
- un fichier csv contenant les principales informations des livres (titre, numéro d'identification, prix, etc.),
- un dossier contenant les images des couvertures.

## Lancement de l'application :
- créer un environnement virtuel : python -m venv [nom]
- activer l'environnement virtuel : [nom]\Scripts\activate
- installer les packages : pip install -r requirements.txt
- exécuter le script : python main.py

## Lancement de l'application (Anaconda) :
- créer un environnement virtuel : conda create --name [nom]
- activer l'environnement virtuel : conda activate [nom]
- installer pip : conda install pip
- installer les packages : pip install -r requirements.txt
- exécuter le script : python main.py