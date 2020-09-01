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

Le fichier de configuration passé en paramètre doit être rédigé en yaml et être composé de trois listes. Il ne faut pas modifier le nom de ces listes ainsi que le nom des clés, seules les valeurs associées peuvent être modifiées si nécessaire. Le fichier "config_example.yaml" présent dans le dépôt peut être remplis et utilisé selon vos besoins.

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

_Installation du paquet_

Tout d'abord, il faut installer openssh server sur votre serveur distant. Ouvrir un terminal sur ce serveur, se connecter à un utilisateur ayant des droits sudo et exécuter la commande :
> sudo apt-get install openssh-server

Puis autoriser le service ssh :

> sudo systemctl enable ssh

> sudo systemctl start ssh

Une fois ces configurations faites, tester la connexion ssh depuis une machine vers le serveur avec la commande :

> ssh user@server_ip

_Echange de clé_

Pour l'envoi de la sauvegarde vers le serveur backup, il faut établir une connection SSH sécurisée. Pour ce faire, il faut établir un échange de clé RSA entre les deux machines et nous allons commencer par créer une paire de clé RSA avec la commande suivante, il ne faut pas lui attribuer de passphrase :

> ssh-keygen -t rsa

Ensuite il faut copier la clé sur le serveur distant avec la commande suivante :

> ssh-copy-id UserName@Server_IP

La connection avec échange de clé est maintenant établie, le transfert de fichier via ssh peut fonctionner sans demande de mot de passe.

**Login Mariadb**

La connection à la base de données MariaDB se fait avec un utilisateur ayant des droits admin sur la base de données. Pour pouvoir lancer le script sans demande de mot de passe, il suffit de créer le fichier _"~/.my.cnf"_ et d'y écrire le texte suivant, avec le nom d'utilisateur admin et son mot de passe : 

> [mysqldump]
> <br/>user=mysqluser
> <br/>password=secret

Le script peut maintenant être exécuté sans demande de mot de passe, faites bien attention à ce que le nom d'utilisateur défini dans ce fichier soit le même que celui indiqué dans le fichier de configuration yaml avec la clé "db_user".

## Code d'erreur retourné

En cas d'erreur lors de l'exécution du script, un code d'erreur spécifique est retourné et le script est arrêté. Leur signification est expliquée ci-dessous :

* 1 : Erreur lors de l'ouverture du fichier de configuration yaml, sa lecture a échouée ;
* 2 : Erreur lors de la création de l'archive, accès à un dossier ou fichier impossible ;
* 3 : CompressionError, la méthode de compression définie n'est pas supportée ;
* 4 : Erreur innatendue lors de la création de l'archive ;
* 5 : Erreur lors de la création du dump, voir le datacode retourné par mysqldump ;
* 6 : Erreur lors de l'export de l'archive vers le serveur distant, la commande _scp_ a échoué ;
* 7 : Timeout lors de l'export de l'archive, vérifier l'adresse ip indiquée et le nom d'utilisateur ;
* 8 : Aucun argument assigné en paramètre lors de l'exécution du script ;
* 9 : Le fichier de configuration passé en paramètre n'existe pas ;

## Exemple d'usage

Ouvrir un terminal et exécutez le script de la manière suivante avec value_it qui vaut 0 :

> python backup_website.py config_file.yaml 0
