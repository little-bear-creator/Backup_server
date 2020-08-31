# Backup_server
## Présentation
Dans ce dépôt vous trouverez un script python, un fichier de configuration .yaml et un exemple d'usage. Le script "backup_website.py" réalise une sauvegarde d'un site web Wordpress et de sa base de donnée MariaDB associée. 

**Licence**
COncernant les droits de distribution, modification ou utilisation des fichiers de ce dépôt, se référencer au fichier "License.txt" présent dans le dépôt.

**Paramètres**
Le script python fonctionne avec deux paramètres :
1. _yaml_file_ : Ce premier paramètre est un fichier de configuration yaml possédant toutes les informations nécessaires à la réalisation de la sauvegarde du site web et de son exportation vers un serveur "backup". Il est obligatoire pour faire fonctionner le script.
1. *value_it* : Ce deuxième paramètre a pour valeur 0 ou 1 et il permet de déterminer la prise en compte d'erreurs lors de la création de l'archive contenant les dossiers de configurations du site web. En effet, certains dossiers peuvent être manquants ou l'utilisateur exécutant le script peut ne pas avoir suffisamment de droit pour effectuer des actions sur des dossiers/fichiers. Ainsi pour une valeur de *value_it* à 0, les erreurs seront ignorées pendant la création de l'archive alors que la valeur à 1 stoppe le script et affiche l'erreur rencontrée. **Important** : Si aucune valeur n'est assignée à *value_it* lors de l'exécution du scrpit, le paramètre aura pour valeur par défaut 1.

**Pré-requis**
Le script doit être exécuté sous Linux avec une distribution Debian/Ubuntu. A ce jour, le script a été testé sur une seule distribution, Debian Buster. Aussi, il faut avoir un compte administrateur avec des droits d'écriture concernant les dossiers et fichiers associés au site web wordpress ainsi qu'un compte administrateur sur sa base de donnée associée. Enfin, il faut avoir accès à un serveur distant où exporter la sauvegarde.

## Configuration du fichier yaml

Le fichier de configuration passé en paramètre doit être rédigé en yaml et être composé de trois dictionnaires. Il ne faut pas modifier le nom de ces listes ainsi que le nom des clés, seules les valeurs associées peuvent être modifiées si nécessaire. La première liste permet de renseigner le chemin vers le dossier contenant tous les sous-dossiers et fichiers du site web à sauvegarder. Sont aussi renseigné, le nom de l'archive, son extension et le mode d'archivage, exemple :
> web_configuration:
 > web_path: /var/www/path/to/website
 > tarfile: WebArchive_
 > web_ext: .tar.gz
 > mode: w|gz _(ne pas modifier)_

db_configuration:
  back_name: db_backup_
  db_name: database_name
  back_path: /path/to/your/backup/folder
  back_ext: .sql
  db_user: your_admin_user

transfert:
  backup_user: username_of_distant_server 
  server_ip: ip_adress_of_distant_server 
  port: 22
  directory: /path/to/your/distant/backup/folder
