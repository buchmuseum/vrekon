import pandas as pd
from collections import defaultdict
import re
import numpy as np

def make_nested_frame(dict) -> pd.DataFrame:
    """
    Die Funktion nimmt ein dreifach verschachteltes Dict und generiert daraus ein DataFrame mit dreifachem index
    """
    return pd.DataFrame.from_dict(
        {
            (k1, k2, k3): v3
            for k1, v1 in dict.items()
            for k2, v2 in v1.items()
            for k3, v3 in v2.items()
        },
        orient="index",
        dtype="string",
    )


def feldauswertung(kategorie: str, inhalt: str) -> list[tuple[str, str]]:
    """
    Die Funktion hat zwei Argumente: die Pica-Kategorie und den Feldinhalt.
    Per regex wird das gewünschte Unterfeld gesucht und in einem tuple mit der Klarfeldbezeichnung ausgegeben.
    Weil auch Unterfelder wiederholbar sind, kommt eine Liste von Tupeln zurück.
    """
    ergebnisse = list()
    matchlist = [
        ("209A", "f", "standort"),
        ("209A", "g", "signatur_g"),
        ("209A", "d", "ausleihcode"),
        ("209A", "a", "signatur_a"),
        ("209A", "c", "sig_komm"),
        ("209C", "a", "akz"),
        ("237A", "a", "f4801_a"),
        ("237A", "k", "f4801_k"),
        ("247C", "9", "bibliothek"),
    ]

    for match in matchlist:
        if kategorie == match[0]:
            ergebnisse.append(
                (match[2], "; ".join(re.findall(f"\${match[1]}([^\$]+)", inhalt)))
            )

    return ergebnisse


def get_exemplare(datei: str) -> pd.DataFrame:
    """
    Auf IDN und Exemplardatenfelder reduzierter Dump, dessen Dateiname als Argument übergeben wird, wird in df mit gewünschten Feldern umgewandelt
    """
    with open(f"filter/{datei}", "r") as f:
        df = pd.DataFrame(dtype="string")
        for l in f:
            # print(l)
            line = l.split(" ", 1)
            if l == "\n":
                df = pd.concat([df, make_nested_frame(exemplare)])

            elif line[0] == "003@":
                exemplare = defaultdict(
                    lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(str)))
                )
                idn = line[1][2:].strip()
            elif line[0] == "101@":
                einrichtung = line[1][2:].strip()

            else:
                feld = line[0].split("/")
                feldergebnis = feldauswertung(feld[0], line[1].strip())
                for ergebnis in feldergebnis:
                    # der seltsame join deshalb, weil Felder auch wiederholt werden können und die Ergebnisse dann zusammengezogen und durch Semikolon getrennt werden. wahrscheinlich nicht die beste lösung.
                    exemplare[idn][einrichtung][feld[1]][ergebnis[0]] = "; ".join(
                        [ergebnis[1], exemplare[idn][einrichtung][feld[1]][ergebnis[0]]]
                    )

        df.index.set_names(["idn", "einrichtung", "exemplar"], inplace=True)
        return (
            df.reset_index()
            .apply(lambda x: x.str.strip("; ") if x.dtype == "string" else x)
            .astype("string")
        )


def get_titel(datei: str) -> pd.DataFrame:
    df = pd.read_csv(f"filter/{datei}", low_memory=False, dtype="string")
    df["titel"] = df.tit_a.str.cat(df.tit_d, sep=" : ", na_rep="")
    df.loc[pd.notna(df.tit_Y), "titel"] = df.tit_Y
    df.titel = df.titel.str.slice(0, 150)

    df = df.merge(
        df.fillna("").groupby(["idn"])["f4243"].apply(", ".join).reset_index(),
        on="idn",
        how="right",
    ).drop(["f4243_x"], axis=1)
    df = df.merge(
        df.fillna("").groupby(["idn"])["stuecktitel_l"].apply(", ".join).reset_index(),
        on="idn",
        how="right",
    ).drop(["stuecktitel_l_x"], axis=1)
    df = df.merge(
        df.fillna("").groupby(["idn"])["stuecktitel_a"].apply(", ".join).reset_index(),
        on="idn",
        how="right",
    ).drop(["stuecktitel_a_x"], axis=1)

    df["stuecktitel"] = df.stuecktitel_l_y.str.cat(
        df.stuecktitel_a_y, sep=" : ", na_rep=""
    )
    df.drop(
        ["stuecktitel_l_y", "stuecktitel_a_y", "tit_a", "tit_d", "tit_Y"],
        axis=1,
        inplace=True,
    )
    df.rename({"f4243_y": "f4243"}, axis=1, inplace=True)
    df.drop_duplicates(subset=["idn"], inplace=True)

    return df.astype("string")


# Bö M

titel = get_titel("böm-titel.csv")
exemplare = get_exemplare("böm-exemplare.dat")
exemplare = exemplare[
    ((exemplare.bibliothek == "009030115") | (pd.isna(exemplare.bibliothek)))
    & exemplare.signatur_a.str.startswith("Bö")
]

df = titel.merge(exemplare, on="idn", how="right")
df = df[
    [
        "idn",
        "akz",
        "bbg",
        "standort",
        "signatur_g",
        "signatur_a",
        "titel",
        "stuecktitel",
        "f4243",
        "f4256",
        "f4241",
        "f4105_9",
        "f4105_g",
        "ausleihcode",
        "sig_komm",
        "f4801_a",
        "f4801_k",
        "bibliothek",
        "einrichtung",
        "exemplar",
    ]
]

df = df.replace(r'', np.NaN)

# Filtered signatur_a
df = df[~df["signatur_a"].str.contains("angeb", na=False)]

# Filtered f4243
df = df[df["f4243"].isna()]

# Filtered f4256
df = df[df["f4256"].isna()]

# Filtered f4241
df = df[df["f4241"].isna()]

# Filtered f4105_9
df = df[df["f4105_9"].isna()]

# Filtered standort
df = df[df["standort"] != "DBSM/DA"]

# Filtered bbg
df = df[df["bbg"] != "Hal"]

# Filtered bbg
df = df[df["bbg"] != "Hfl"]

# Filtered bbg
df = df[df["bbg"] != "Pa"]

df.to_csv("abzug/böm.csv", index=False)

# Bö Ink
titel = get_titel("böink-titel.csv")
exemplare = get_exemplare("böink-exemplare.dat")
exemplare = exemplare[exemplare.signatur_a.str.startswith("Bö")]

df = titel.merge(exemplare, on="idn", how="right")

df = df[
    [
        "idn",
        "akz",
        "bbg",
        "standort",
        "signatur_g",
        "signatur_a",
        "titel",
        "stuecktitel",
        "f4243",
        "f4256",
        "f4241",
        "f4105_9",
        "f4105_g",
        "ausleihcode",
        "sig_komm",
        "f4801_a",
        "f4801_k",
        "einrichtung",
        "exemplar",
    ]
]

df = df.replace(r'', np.NaN)

# Filtered f4105_9
df = df[df["f4105_9"].isna()]

# Filtered f4241
df = df[df["f4241"].isna()]

# Filtered f4256
df = df[df["f4256"].isna()]

# Filtered f4243
df = df[df["f4243"].isna()]

# Filtered signatur_g
df = df[~df["signatur_g"].str.contains("angeb", na=False)]

# Filtered signatur_a
df = df[~df["signatur_a"].str.contains("angeb", na=False)]

# Filtered bbg
df = df[~df["bbg"].str.contains("Aaq", na=False)]

# Filtered standort
df = df[df["standort"] != "DBSM/DA"]

df.to_csv("abzug/böink.csv", index=False)

# II Inkunabeln
titel = get_titel("ii-titel.csv")

exemplare = get_exemplare("ii-exemplare.dat")
exemplare = exemplare[exemplare.signatur_a.str.startswith("II")]

df = titel.merge(exemplare, on="idn", how="right")
df = df[
    [
        "idn",
        "akz",
        "bbg",
        "standort",
        "signatur_g",
        "signatur_a",
        "titel",
        "stuecktitel",
        "f4243",
        "f4256",
        "f4241",
        "f4105_9",
        "f4105_g",
        "ausleihcode",
        "sig_komm",
        "f4801_a",
        "f4801_k",
        "einrichtung",
        "exemplar",
    ]
]

df = df.replace(r'', np.NaN)

# Filtered f4256
df = df[df["f4256"].isna()]

# Filtered f4105_9
df = df[df["f4105_9"].isna()]

# Filtered f4241
df = df[df["f4241"].isna()]

# Filtered f4243
df = df[df["f4243"].isna()]

# Filtered signatur_g
df = df[~df["signatur_g"].str.contains("angeb", na=False)]

# Filtered signatur_a
df = df[~df["signatur_a"].str.contains("angeb", na=False)]

# Filtered standort
df = df[df["standort"] != "DBSM/DA"]

df.to_csv("abzug/ii.csv", index=False)


# III (Drucke 1501-1560)
titel = get_titel("iii-titel.csv")

exemplare = get_exemplare("iii-exemplare.dat")
exemplare = exemplare[
    ((exemplare.bibliothek == "009030115") | (pd.isna(exemplare.bibliothek)))
    & exemplare.signatur_a.str.startswith("III")
]

df = titel.merge(exemplare, on="idn", how="right")
df = df[
    [
        "idn",
        "akz",
        "bbg",
        "standort",
        "signatur_g",
        "signatur_a",
        "titel",
        "stuecktitel",
        "f4243",
        "f4256",
        "f4241",
        "f4105_9",
        "f4105_g",
        "ausleihcode",
        "sig_komm",
        "f4801_a",
        "f4801_k",
        "einrichtung",
        "exemplar",
    ]
]

df = df.replace(r'', np.NaN)

# Filtered signatur_g
df = df[~df["signatur_g"].str.contains("angeb", na=False)]

# Filtered signatur_a
df = df[~df["signatur_a"].str.contains("angeb", na=False)]

# Filtered f4243
df = df[df["f4243"].isna()]

# Filtered f4256
df = df[df["f4256"].isna()]

# Filtered f4241
df = df[df["f4241"].isna()]

# Filtered f4105_9
df = df[df["f4105_9"].isna()]

# Filtered standort
df = df[df["standort"] != "DBSM/DA"]

# Filtered bbg
df = df[df["bbg"] != "Hal"]

# Filtered bbg
df = df[~df["bbg"].str.contains("Aaq", na=False)]

# Filtered signatur_g
df = df[~df["signatur_g"].str.contains("II 30,13", na=False)]

df.to_csv("abzug/iii.csv", index=False)

# IV (Drucke 1561-1800)
titel = get_titel("iv-titel.csv")

exemplare = get_exemplare("iv-exemplare.dat")
exemplare = exemplare[
    ((exemplare.bibliothek == "009030115") | (pd.isna(exemplare.bibliothek)))
    & exemplare.signatur_a.str.startswith("IV")
]

df = titel.merge(exemplare, on="idn", how="right")
df = df[
    [
        "idn",
        "akz",
        "bbg",
        "standort",
        "signatur_g",
        "signatur_a",
        "jahr",
        "titel",
        "stuecktitel",
        "f4243",
        "f4256",
        "f4241",
        "f4105_9",
        "f4105_g",
        "ausleihcode",
        "sig_komm",
        "f4801_a",
        "f4801_k",
        "bibliothek",
        "einrichtung",
        "exemplar",
    ]
]

df = df.replace(r'', np.NaN)

df.jahr = df.jahr.str.replace("X", "0")
df.fillna({"jahr": "0"}, inplace=True)
df = df.astype({"jahr": "int"})

# Filtered signatur_g
df = df[~df["signatur_g"].str.contains("angeb", na=False)]

# Filtered signatur_a
df = df[~df["signatur_a"].str.contains("angeb", na=False)]

# Filtered f4243
df = df[df["f4243"].isna()]

# Filtered f4256
df = df[df["f4256"].isna()]

# Filtered f4241
df = df[df["f4241"].isna()]

# Filtered f4105_9
df = df[df["f4105_9"].isna()]

# Filtered jahr
df = df[df["jahr"] <= 1785]

# Filtered standort
df = df[df["standort"] != "DBSM/DA"]

# Filtered signatur_g
df = df[~df["signatur_g"].str.contains("IV 205, 76", na=False)]

# Filtered signatur_a
df = df[~df["signatur_a"].str.contains("IV 205,76", na=False)]

# Filtered signatur_g
df = df[~df["signatur_g"].str.contains("IV 114, 15", na=False)]

# Filtered signatur_g
df = df[~df["signatur_g"].str.contains("IV 114, 13a", na=False)]

df.to_csv("abzug/iv.csv", index=False)

# Schreibmeisterbücher

titel = get_titel("schreibmeister-titel.csv")
exemplare = get_exemplare("schreibmeister-exemplare.dat")

# exemplare = exemplare[
#    ((exemplare.bibliothek == "009030115") | (pd.isna(exemplare.bibliothek)))
# ]

titel.jahr = titel.jahr.str.replace("[xX]", "0", regex=True)
titel.jahr = titel.jahr.str.replace("[\[\]]", "", regex=True)

titel.fillna({"jahr": "0"}, inplace=True)
titel = titel.astype({"jahr": "int"})

df = titel.merge(exemplare, on="idn", how="right")
df = df[
    [
        "idn",
        "akz",
        "bbg",
        "standort",
        "signatur_g",
        "signatur_a",
        "jahr",
        "titel",
        "stuecktitel",
        "f4243",
        "f4256",
        "f4241",
        "f4105_9",
        "f4105_g",
        "ausleihcode",
        "sig_komm",
        "f4801_a",
        "f4801_k",
        "einrichtung",
        "exemplar",
    ]
]

df = df.replace(r'', np.NaN)

df.to_csv("abzug/schreibmeister.csv", index=False)