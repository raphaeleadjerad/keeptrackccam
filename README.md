# *Keep track of CCAM* nomenclature

[WIP]

This project aims at following **changes in CCAM nomenclatures** in a simplified manner.
For instance, you would want to know from one version of the CCAM to the other if
they are new codes, if some of the new codes are children to codes in the previous
version of the nomenclature.

This project imports all versions of the CCAM available (made available by
CNAM, at [url](https://www.ameli.fr/accueil-de-la-ccam/telechargement/index.php), exports them
to csv with only the codes, labels and regrouping codes. It cleans each version of the dataset.
Then, it compares all versions of ccam and adds two additional variables:
`version_ap` and `version_disap`, respectively indicating the version in which the
code appeared and the version in which it disappeared.

An alternative would be to use VC (for instance Git) but it will only give you
the history (you would see new codes and disappeared codes) whereas you would want to link a parent with a children
in a unified nomenclature. For instance if you analyze longitudinal data
with evolving nomenclature names. You would use this unified nomenclature.
Once again you could also download all versions of the nomenclature and
link your longitudinal data with all these nomenclatures and then pick the right one for each time period.
This is just a simplification, and a quick way to check evolution in nomenclature.
This is especially useful if as for the CCAM the evolution from
one version to the next is well documented but not necessarily from one version at time `t-n` and
one version at time `t`.


