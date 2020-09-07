# Projet 2 : Analyser des données de systèmes éducatifs
*Pierre-Eloi Ragetly*

Ce projet fait parti du parcours DataScientist.  

L'objectif principal est de réaliser une analyse exploratoire sur des données d'éducation afin d'établir un score. Ce score servira à determiner quels sont les pays les plus prometteurs pour une compagnie spécialisée dans la formation en ligne à destination des lycées et des étudiants en étude supérieure. Les données à ma disposition étaient les données de la banque mondiale.
https://datacatalog.worldbank.org/dataset/education-statistics

Vous trouverez l'ensemble de l'analyse dans le notebook nommé *Project_2*.  
Cette analyse peut être décomposée en trois grandes parties :

Une première consacrée au nettoyage des données et à la sélection des variables. Le jeu de données était très exhaustif et comportaient de nombreuses variables non significatives. Cette étape de sélection a permis de réduire drastiquement le nombre de variables de 3665 à 5.

La deuxième est consacrée à l'exploration des données. Un *bubble plot* a été utilisé afin de visualiser un maximum de variables sur un seul graphique.

![Bubble_Plot](/charts.bubble_plot.png "Bubble Plot")

Ce graphique montre l'existence de corrélations entre les variables. Une ANOVA a été effectuée pour confirmer ces corrélations, malheureusement le test n'a pas pu être conclusif en raison du non respect des hypothèses de normalité et d'homoscédasticité. Une analyse des pair plots a montré qu'il était préférable de prendre le log pour certaines variables. Enfin les résultats de cette analyse des corrélations ont été utilisés afin de créer un modèle d'imputation des données manquantes basé sur l'algorithme du **kNN**.

La dernière est dédiée à la création du score. Pour cela une note a été attribuée pour chacune des cinq variables, le score est égale à la moyenne de ces cinqs notes. Chaque pays a été représenté sous forme de *radar chart* afin de visualiser les atouts (et les faiblesses) de chaque pays. À noter qu'il aurait été possible de prendre comme score non pas la moyenne mais la surface délimitée par le diagramme radar.

Les librairies python nécessaires pour pouvoir lancer le notebook sont regroupées dans le fichier *requirements.txt*

Toutes les fonctions créées afin de mener à bien le projet ont été regroupées dans le dossier **analysis**.
- les fonctions permettant de charger les données ont été regroupées dans le fichier *dataload*
- les fonctions de visualisation dans *datavisu*
- les fonctions d'analyse statistique dans *datastats*
