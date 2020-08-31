# Backup_server
## Présentation

Dans ce dépôt vous trouverez un script python, un fichier de configuration .yaml et un exemple d'usage. Le script "backup_website.py" réalise une sauvegarde d'un site web Wordpress et de sa base de donnée MariaDB associée. Le script se comporte de la manière suivante : Il commence par ouvrir et lire le fichier de configuration yaml, puis, en utilisant toutes les informations de ce fichier, il créé une archive et y ajoute les dossiers, sous-dossiers et fichiers du site web. Ensuite, il réalise une sauvegarde de la base de données définie dans le fichier yaml, l'ajoute à l'archive et clos cette archive. Enfin dans un dernier temps, le script envoie l'archive générée via ssh au serveur distant stockant les backups du site web visé.

**Licence**

Concernant les droits de distribution, modification ou utilisation des fichiers de ce dépôt, se référencer au fichier "License.txt" présent dans le dépôt.

**Paramètres**

Le script python fonctionne avec deux paramètres :
1. _yaml_file_ : Ce premier paramètre est un fichier de configuration yaml possédant toutes les informations nécessaires à la réalisation de la sauvegarde du site web et de son exportation vers un serveur "backup". Il est obligatoire pour faire fonctionner le script.
1. *value_it* : Ce deuxième paramètre a pour valeur 0 ou 1 et il permet de déterminer la prise en compte d'erreurs lors de la création de l'archive contenant les dossiers de configurations du site web. En effet, certains dossiers peuvent être manquants ou l'utilisateur exécutant le script peut ne pas avoir suffisamment de droit pour effectuer des actions sur des dossiers/fichiers. Ainsi pour une valeur de *value_it* à 0, les erreurs seront ignorées pendant la création de l'archive alors que la valeur à 1 stoppe le script et affiche l'erreur rencontrée. **Important** : Si aucune valeur n'est assignée à *value_it* lors de l'exécution du scrpit, le paramètre aura pour valeur par défaut 1.

**Pré-requis**

Le script doit être exécuté sous Linux avec une distribution Debian/Ubuntu. A ce jour, le script a été testé sur une seule distribution, Debian Buster. Aussi, il faut avoir un compte administrateur avec des droits d'écriture concernant les dossiers et fichiers associés au site web wordpress ainsi qu'un compte administrateur sur sa base de donnée associée. Enfin, il faut avoir accès à un serveur distant où exporter la sauvegarde.

## Configuration du fichier yaml

Le fichier de configuration passé en paramètre doit être rédigé en yaml et être composé de trois listes. Il ne faut pas modifier le nom de ces listes ainsi que le nom des clés, seules les valeurs associées peuvent être modifiées si nécessaire. Le fichier "config_example.yaml" présent dans le dépôt peut être remplis et utilisés selon vos besoins.

**La première liste** permet de renseigner le chemin vers le dossier contenant tous les sous-dossiers et fichiers du site web à sauvegarder. Sont aussi renseigné, le nom de l'archive, son extension et le mode d'archivage, exemple :

> web_configuration:
 > <br/>web_path: /var/www/path/to/website
 > <br/>tarfile: WebArchive_
 > <br/>web_ext: .tar.gz
 > <br/>mode: w|gz _(ne pas modifier)_

**Dans la deuxième liste** vous pouvez définir le nom du fichier backup de la base de donnée, le nom de cette dernière, le chemin où enregistrer le fichier backup, son extension ainsi que l'utilisateur ayant des droits admin sur cette base de donnée.

> db_configuration:
 > <br/>back_name: db_backup_
 > <br/>db_name: database_name
 > <br/>back_path: /path/to/your/backup/folder
 > <br/>back_ext: .sql
 > <br/>db_user: your_admin_user

**La troisième liste** concerne l'export de la sauvegarde, il faut donc renseigner le nom de l'utilisateur distant, présent sur le serveur distant où l'on envoie la sauvegarde, afin d'envoyer le fichier via ssh. Il faut aussi renseigner l'adresse ip du serveur, le port ssh et le dossier où enregistrer la sauvegarde.

>transfert:
 > <br/>backup_user: username_of_distant_server 
 > <br/>server_ip: ip_adress_of_distant_server 
 > <br/>port: 22
 > <br/>directory: /path/to/your/distant/backup/folder

## Configurations à réaliser avant de lancer le script

Avant de lancer le script, il faut établir une connexion ssh sécurisée vers le serveur distant ainsi que la création d'un fichier permettant l'accès à la base de données sans demande de mot de passe. Cette dernière configuration n'est pas obligatoire mais si vous souhaitez réaliser une série de tests automatisés ou exécuter le script régulièrement avec un tâche programmée, cette dernière configuration va être nécessaire.

**Connexion SSH sécurisée**



**Login Mariadb**
