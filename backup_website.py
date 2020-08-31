import argparse
import subprocess
from subprocess import STDOUT, check_output
import sys
import string
import os
import tarfile 
import yaml
from datetime import date


#-----------------------------------------------------------------------------#
# CONFIGURATION YAML
# Fonction pour récupérer la configuration du serveur depuis un fichier yaml
# Retourne un dictionnaire "name_list"
def open_config_file(yaml_file):

  print("Récupération des informations de "+yaml_file+"...")
  
  try:
    with open(yaml_file) as file :
      name_list = yaml.load(file, Loader=yaml.FullLoader)
  except OSError:
    print("cannot open ", yaml_file)
    sys.exit(1)
  except:
    print("YAML file: Unexpected error: ", sys.exc_info()[0])
    sys.exit(2) 

  return name_list

# Fonction pour récupérer les erreurs de os.walk() lors de l'itération dans 
# les dossiers du wordpress pour réaliser l'archive
def walk_error_handler(exception_instance):

  print("Error : "+str(exception_instance))
  if int(value_it) == 1:
    print("Arrêt de la sauvegarde")
    sys.exit(3)
  else:
    print("Erreur ignorée, la création continue.")

#-----------------------------------------------------------------------------#
# ARCHIVE
# Création de l"archive avec un nom, une date et un type de fichier depuis un 
# dictionnaire "name_list"
# Retourne un objet tar
def create_archive(name_list):
 
  # Variables nécessaires à la création de l"archive tar 
  ext = name_list["web_configuration"]["web_ext"]
  arch_mode = name_list["web_configuration"]["mode"]

  # Création de l'archive tar
  print("Création de l'archive...")
  
  try:
    tar = tarfile.open((name_list["web_configuration"]["tarfile"])+d1+ext, arch_mode)
  except tarfile.CompressionError:
    print("Compression method is not supported or data cannot be decoded properly, script is stoped.")
    sys.exit(4)
  except:
    print("ARCHIVE CREATION : Unexpected error: ", sys.exc_info()[0])
    sys.exit(5) 

  # Boucle pour ajouter les fichiers et sous-dossiers du wordpress à l"archive
  print("Archive créée ! Récupération des données...")
  for dirname, subdirs, files in os.walk(name_list["web_configuration"]["web_path"], onerror=walk_error_handler):
    tar.add(dirname)
    for filename in files:
      tar.add(os.path.join(dirname,filename))

  print("Récupération terminée.")
  return tar



#-----------------------------------------------------------------------------#
# CREATION DUMP 
# Fonction qui créée un dump de la base de donnée depuis le dictionnaire 
# "name_list"
# Retourne le nom de la base de donnée avec son chemin
def create_dump(name_list):
  
  # Récupération des informations sur le dump depuis name_list 
  dataBase = name_list["db_configuration"]["db_name"]
  back_path = name_list["db_configuration"]["back_path"]
  back_ext = name_list["db_configuration"]["back_ext"]
  back_name = str(name_list["db_configuration"]["back_name"])+d1+back_ext
  user = name_list["db_configuration"]["db_user"]

  # Nom et chemin du dump qui va être créé 
  final_dump = open(back_path+back_name, "w")

  # Commande de création du dump
  print("Création du dump de la base de donnée "+back_name+"...")
  datacode = subprocess.run(["mysqldump","-u", user, dataBase], stdout=final_dump)

  if (datacode.returncode != 0):
    print("Erreur lors de la création du dump, datacode error : %d" % datacode.returncode)
    sys.exit(6)

  final_dump.close()
  print("Dump Créé.") 

  return str(final_dump.name)


#-----------------------------------------------------------------------------#
# EXPORT DU BACKUP
# Fonction qui exporte le backup sur un serveur dont les caractéristiques 
# sont définies dans le dictionnaire "name_list" 
def export_backup(name_list, tar):

  user = name_list["transfert"]["backup_user"]
  ip_addr = name_list["transfert"]["server_ip"]
  directory = name_list["transfert"]["directory"]
  fichier = tar.name 

  print("Exportation en cours...") 

  # Exécution de la commande scp avec un timeout de 30 secondes 
  try:
    output = check_output(["scp", fichier, user+"@"+ip_addr+":"+directory], stderr=STDOUT, timeout=30)
  except subprocess.CalledProcessError:
    print("Erreur lors de l'export du backup vers "+ip_addr)
    sys.exit(7)
  except subprocess.TimeoutExpired:
    print("Erreur : Timeout lors de l'export du backup vers "+ip_addr)
    sys.exit(8)
  except:
    print("Failure")
    sys.exit(9)


#-----------------------------------------------------------------------------#
#-----------------------------------------------------------------------------#
# MAIN
if __name__ == "__main__":

  print("")

  # Récupération de l'argument avec un parser
  parser = argparse.ArgumentParser(description="Sauvegarde d'un wordpress et de sa base de données.")

  # ------------------------------------------------------------------#
  # Test si il n'y a pas d'arguments ou pas assez
  if len(sys.argv) == 1:
    print("Il manque les arguments (fichier yaml et value_it), voir README.")
    sys.exit(10)
  # Valeur de value_it par défaut si jamais l'argument n'est pas définie
  elif len(sys.argv) == 2:
    print("Valeur par défaut pour value_it")
    value_it = 1
  # Test si value_it a bien pour valeur 0 ou 1
  elif len(sys.argv) > 2:
    value_it = sys.argv[2]
    if (int(value_it) < 0 or int(value_it) > 1):
      print("Erreur : valeur incorrecte pour value_it, value_it définie par défaut")
      value_it = 1

  # Initialisation de la variable yaml_file 
  # Test si le fichier de configuraiton existe
  if not(os.path.isfile(sys.argv[1])):
    print("Erreur : le fichier de configuration n'existe pas") 
    sys.exit(11)
  yaml_file = sys.argv[1]

  
  # ------------------------------------------------------------------#
  # Script démarre
  print("Début du script de sauvegarde de wordpress et de sa base de données")

  # Définitions des variables de date et de temps 
  today = date.today()
  d1 = today.strftime("%b-%d-%Y")

  # Récupération de la configuration via un fichier yaml
  name_list = open_config_file(yaml_file)

  # Création de l"archive depuis les informations du fichier yaml
  tar = create_archive(name_list)

  # Ajout du dump mariaDB à l'archive
  tar.add(create_dump(name_list))
  print("Dump ajouté à l'archive.")

  # Fermeture de l'archive
  tar.close()

  # Export du backup vers un serveur via ssh et avec échange de clées RSA 
  export_backup(name_list, tar)
