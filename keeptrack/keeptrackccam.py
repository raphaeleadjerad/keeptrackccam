# ---------------------------------------------
# CODE ACTUALISATION CCAM
# ---------------------------------------------


# Modules ------------------------
import pandas as pd
import numpy as np
import csv
import re
import functools

# Clean and transform into csv ---------------------------------------


def clean_ccam(nom, version):
    """
    Function that imports CNAM xls CCAM nomenclature and exports a csv for this version of
    the CCAM, and also returns the pandas Dataframe of this version of the ccam
    It is always structured in the same way with ccam code, label and regrouping code
    The primary key is ccam code
    :param nom: Str, filename for nomenclature
    :param version: Str, containing name for the imported version of the nomenclature
    :return: Pandas DataFrame of CCAM version
    """
    df = pd.read_excel(nom, header=None)
    df.columns = df.iloc[1, :].str.lower()
    err = [itm for itm in ['code', 'texte', 'regroupement'] if itm not in df.columns]
    if len(err) > 0:
        print("ERROR Le format du fichier a changé")
    df = (df.drop([0, 1])
          .dropna(axis=0, subset=['code'])
          .loc[df["code"].str.contains('^[a-zA-Z]+') == True, ['code', 'texte', 'regroupement']])
    df.columns = ["CAM_PRS_IDE_COD", "CAM_PRS_IDE_LIB", "CAM_PRS_RGT"]

    # Isolate modifiers
    modifiers = df.loc[df["CAM_PRS_IDE_COD"].str.strip().str.match(r'^[a-zA-Z]{1}$'), :]
    df = df.loc[~df["CAM_PRS_IDE_COD"].isin(modifiers["CAM_PRS_IDE_COD"]), :]
    df = df.reset_index().drop(columns="index")
    # also strip whitespace from codes
    df["CAM_PRS_IDE_COD"] = df["CAM_PRS_IDE_COD"].str.strip()
    # Drop duplicates based on values of all the columns
    df = df.drop_duplicates()
    # verify primary key unique after this
    if not (len(df["CAM_PRS_IDE_COD"].unique()) == df.shape[0]):
        print(50 * "*")
        print("ERROR Primary Key for version {} not unique".format(version))
        print("Number of duplicates : {}".format(df["CAM_PRS_IDE_COD"].duplicated().sum()))
        print("List of duplicates : {}".format(
            [itm for itm in df.loc[df["CAM_PRS_IDE_COD"].duplicated(), 'CAM_PRS_IDE_COD']]))

    df.to_csv("data/IR_CCAM_V" + version + ".csv", na_rep="NA",
              encoding="utf-8", sep=";", index=False, quoting=csv.QUOTE_NONNUMERIC, quotechar='"')
    return df


# Reduce CCAM files to dictionary of DataFrames --------------------------

def reduce_ccam(path2files):
    """
    Function that applies clean_ccam to a list of files and then
    stores each cleaned ccam version as pandas DataFrame as values of
    a dictionary
    :param path2files: List containing file names for CCAM
    :return: dictionary, its keys are the different versions and its values
    are the pandas DataFrame containing the ccam corresponding to the version in the key
    """
    r = re.compile(r"[0-9]{2,}")
    versions = pd.Series([r.search(f).group() for f in path2files])
    versions.index = path2files
    dfs = dict.fromkeys(versions)
    for f in path2files:
        version = versions[f]
        dfs[version] = clean_ccam(f, version)
    return dfs

# Output comparison of versions -----------------------------------------------------


def merge_version(dfs):
    """
    Function that merges pandas DataFrames that are values of a dictionary.
    It performs outer join for each pair of DF and adds a variable "version_ap"
    indicating the version for appeared rows throughout versions and
    a variable "version_disap" indicating the version for disappeared rows
    :return: A pandas DataFrame with the same columns as the DataFrames in dfs, with
    additional, "version", "version_ap"  and "version_disap" columns
    The "version" column is a list of all the versions in which the codes appeared
    """
    for k in dfs.keys():
        dfs[k] = dfs[k].assign(version=k)
    dfs = list(dfs.values())
    df_merged = functools.reduce(lambda left, right: pd.merge(left, right, how='outer'), dfs)
    df_merged_g = \
        df_merged.groupby(['CAM_PRS_IDE_COD', 'CAM_PRS_IDE_LIB', 'CAM_PRS_RGT'])['version'].apply(list)
    df_merged_g = df_merged_g.reset_index()
    max_version = df_merged.version.max()
    min_version = df_merged.version.min()
    # we use apply by row here because there is not really an efficiency pb but could be improved
    df_merged_g["version_disap"] = df_merged_g.apply(lambda df: np.where(max_version not in df["version"],
                                                                         max(df["version"]), ""), axis=1)
    df_merged_g["version_ap"] = df_merged_g.apply(lambda df:
                                                  np.where(min_version not in df["version"], min(df["version"]), ""),
                                                  axis=1)

    return df_merged_g
