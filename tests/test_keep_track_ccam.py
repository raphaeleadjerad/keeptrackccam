# Test file for keeptrackccam ---------------------------

# Modules ------------------------
import os
print(os.getcwd())
import pandas as pd
import glob
import csv
from keeptrack.keeptrackccam import clean_ccam, reduce_ccam, merge_version

# Parameters -----------------------
# CCAM available at https://www.ameli.fr/accueil-de-la-ccam/telechargement/index.php -> 3 last versions
# CCAM available at https://www.atih.sante.fr/les-versions-de-la-ccam?page=1, -> format NX


# test premiere fonction
nom = "./data/CCAM_V63.xls"
test = clean_ccam(nom, "63")
nom = "./data/CCAM_V62.xls"
clean_ccam(nom, "62")

# test deuxieme fonction
path2files = glob.glob("data/CCAM_V*")
dict_of_ccam = reduce_ccam(path2files)

# We add the 54 version already cleaned to the dict_of_ccam dictionary
first_nom = "./data/IR_CCAM_V54.csv"
second_nom = "./data/IR_CCAM_V56.csv"
nom = pd.read_csv(first_nom, sep=";")
# on lui ajoute les codes de regroupement de la version 56 car
# elle n'en disposait pas ce qui va fausser la comparaison des versions
temp = pd.read_csv(second_nom, sep=";")
nom = pd.merge(nom, temp, on = ["CAM_PRS_IDE_COD", "CAM_PRS_IDE_LIB"], how = "left")

dict_of_ccam.update({"54": nom})

# Test merge_version function -------------------------
version_ccam = merge_version(dict_of_ccam)

# Explore results -------------------------------------
version_ccam.version_disap.value_counts().sort_index()
version_ccam.version_ap.value_counts().sort_index()
len(version_ccam.CAM_PRS_IDE_COD.unique()) == version_ccam.shape[0]
version_ccam["dup"] = version_ccam["CAM_PRS_IDE_COD"].duplicated(keep=False)
# Inspect duplicates
test = version_ccam.loc[version_ccam["dup"] == 1, :]
# souvent precisions dans les labels -> deal with duplicates -> TODO

version_ccam.to_csv("data/version_ccam.csv", na_rep="NA",
          encoding="utf-8", sep=";", index=False, quoting=csv.QUOTE_NONNUMERIC, quotechar='"')

# appeared and disapeared codes --------------------------
disappeared_codes = version_ccam.loc[version_ccam["version_disap"] != "", :]
appeared_codes = version_ccam.loc[version_ccam["version_ap"] != "", :]
