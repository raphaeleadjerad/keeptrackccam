# *Keep track of CCAM* nomenclature

[WIP]

This project aims at following **changes in CCAM nomenclatures** in a simplified manner.
For instance, you would want to know from one version of the CCAM to the other if
they are new codes, if some of the new codes are children to codes in the previous
version of the nomenclature.

This project imports all versions of the CCAM available (made available by
CNAM, at [url](https://www.ameli.fr/accueil-de-la-ccam/telechargement/index.php)), exports them
to csv with only the codes, labels and regrouping codes. It cleans each version of the nomenclature.
Modifiers are not part of the nomenclature.

Then, it compares all versions of ccam and adds three additional variables: `version`,
`version_ap` and `version_disap`. The last two respectively indicate the version in which the
code appeared and the version in which it disappeared. The variable `version` is a 
list of all the version in which the CCAM code appeared.

An alternative would be to use VC (for instance Git) but it will only give you
the history (you would see new codes and disappeared codes) whereas you would want to link a parent with a children
in a unified nomenclature. For instance if you analyze longitudinal data
with evolving nomenclature names. You would use this unified nomenclature.