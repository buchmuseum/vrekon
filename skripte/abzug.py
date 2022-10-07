import pandas as pd
from collections import defaultdict
import re
import numpy as np
from natsort import index_natsorted
from typing import List, Tuple

filter_path = "filter"


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


def feldauswertung(kategorie: str, inhalt: str) -> List[Tuple[str, str]]:
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
        ("220C", "w", "wert"),
    ]
    # [('standort', 'DBSM/M/Klemm'), ('signatur_g', 'II 1,2a - Fragm.')]
    for match in matchlist:
        if kategorie == match[0]:
            if len(unterfeldsuche := re.findall(r"\${match[1]}([^\$]+)", inhalt)) > 0:
                if (kategorie == "209A") and (re.findall(r"\$a.+\$x0[1-8]", inhalt)):
                    pass
                else:
                    unterfeld = (match[2], "; ".join(unterfeldsuche))
                    ergebnisse.append(unterfeld)

    return ergebnisse


def get_exemplare(datei: str) -> pd.DataFrame:
    """
    Auf IDN und Exemplardatenfelder reduzierter Dump, dessen Dateiname als Argument übergeben wird, wird in df mit gewünschten Feldern umgewandelt
    """
    with open(f"{filter_path}/{datei}", "r") as f:
        df = pd.DataFrame(dtype="string")
        for l in f:
            # Zeile wird getrennt in Kategorie und Inhalt, line[0] ist Kategorie, line[1] ist Inhalt
            line = l.split(" ", 1)
            # wenn Leerzeile ist Datensatz zu Ende und alle Exemplare dieses Titels werden zunächst in ein df umgewandelt und dann an das df mit allen Exemplaren angehängt
            if l == "\n":
                df = pd.concat([df, make_nested_frame(exemplare)])

            # wenn beginn neuer titelsatz wird 3-fach verschachteltes dict exemplare neu angelegt und idn geschrieben
            elif line[0] == "003@":
                exemplare = defaultdict(
                    lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(str)))
                )
                idn = line[1][2:].strip()
            # wenn neue Einrichtung wird das geschrieben
            elif line[0] == "101@":
                einrichtung = line[1][2:].strip()

            # in allen anderen fällen werden die zeilen ausgelesen
            else:
                # kategorie und okkurrenz werden getrennt
                feld = line[0].split("/")
                # die unterfelder werden in klartext übersetzt
                feldergebnis = feldauswertung(feld[0], line[1].strip())
                for ergebnis in feldergebnis:
                    # wenn feld und unterfeld gleich sind, werden die ergebnisse durch Semikolon getrennt aneinander gehängt; in der funktion feldauswertung wird ausgeschlossen dass 209A/*.a zurückgegeben wird, wenn $x01-08 ist (damit werden altsignaturen aus 7101 ausgeschlossen)
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
    df = pd.read_csv(f"{filter_path}/{datei}", low_memory=False, dtype="string")
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


def blacklist() -> Tuple:
    liste = list()
    with open("blacklist.txt", "r") as f:
        while True:
            line = f.readline()
            if line.startswith("#"):
                pass
            elif line:
                liste.append(line.split("#")[0].strip())
            elif not line:
                break
    return tuple(liste)


# Bö M

titel = get_titel("böm-titel.csv")
exemplare = get_exemplare("böm-exemplare.dat")
exemplare = exemplare[
    (
        (exemplare.bibliothek == "009030115")
        | (pd.isna(exemplare.bibliothek))
        | (exemplare.bibliothek == "009033645")
    )
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
        "umfang",
        "f4243",
        "f4256",
        "f4241",
        "f4105_9",
        "f4105_g",
        "ausleihcode",
        "sig_komm",
        "f4801_a",
        "bibliothek",
        "einrichtung",
        "exemplar",
        "wert",
    ]
]

df = df.replace(r"", np.NaN)

# Filtered signatur_a
df = df[~df["signatur_a"].str.contains("angeb", na=False, case=False)]

# idns aus der datei blacklist.txt im stammverzeichnis werden ausgefiltert
df = df[~df.idn.isin(blacklist())]

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

df = df.sort_values(
    by="signatur_a",
    ascending=True,
    na_position="first",
    key=lambda X: np.argsort(index_natsorted(df["signatur_a"])),
)

df.to_excel("abzug/böm.xlsx", index=False)
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
        "umfang",
        "f4243",
        "f4256",
        "f4241",
        "f4105_9",
        "f4105_g",
        "ausleihcode",
        "f4801_a",
        "f4801_k",
        "einrichtung",
        "exemplar",
        "wert",
    ]
]

df = df.replace(r"", np.NaN)

# Filtered f4105_9
df = df[df["f4105_9"].isna()]

# idns aus der datei blacklist.txt im stammverzeichnis werden ausgefiltert
df = df[~df.idn.isin(blacklist())]

# Filtered f4243
df = df[df["f4243"].isna()]

# Filtered signatur_g
df = df[~df["signatur_g"].str.contains("angeb", na=False, case=False)]

# Filtered signatur_a
df = df[~df["signatur_a"].str.contains("angeb", na=False, case=False)]

# Filtered bbg
df = df[~df["bbg"].str.contains("Aaq", na=False)]

# Filtered standort
df = df[df["standort"] != "DBSM/DA"]

df = df.sort_values(
    by="signatur_a",
    ascending=True,
    na_position="first",
    key=lambda x: np.argsort(index_natsorted(df["signatur_a"])),
)

df.to_excel("abzug/böink.xlsx", index=False)
df.to_csv("abzug/böink.csv", index=False)

# II Inkunabeln
titel = get_titel("ii-titel.csv")

exemplare = get_exemplare("ii-exemplare.dat")
exemplare = exemplare[
    (
        (exemplare.bibliothek == "009030115")
        | (exemplare.bibliothek == "009033645")
        | (pd.isna(exemplare.bibliothek))
    )
    & exemplare.signatur_a.str.startswith("II ")
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
        "umfang",
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
        "wert",
    ]
]

df = df.replace(r"", np.NaN)

# idns aus der datei blacklist.txt im stammverzeichnis werden ausgefiltert
df = df[~df.idn.isin(blacklist())]

# Filtered f4105_9
df = df[df["f4105_9"].isna()]

# Filtered f4241
df = df[df["f4241"].isna()]

# Filtered signatur_g
df = df[~df["signatur_g"].str.contains("angeb", na=False, case=False)]

# Filtered signatur_a
df = df[~df["signatur_a"].str.contains("angeb", na=False, case=False)]

# Filtered standort
df = df[df["standort"] != "DBSM/DA"]

# Ausleihcode nicht e (= Moskauer Bestand)
# Filtered ausleihcode
df = df[~df["ausleihcode"].str.contains("e", na=False)]

df = df.sort_values(
    by="signatur_a",
    ascending=True,
    na_position="first",
    key=lambda x: np.argsort(index_natsorted(df["signatur_a"])),
)
df.to_excel("abzug/ii.xlsx", index=False)

df.to_csv("abzug/ii.csv", index=False)


# III (Drucke 1501-1560)
titel = get_titel("iii-titel.csv")

exemplare = get_exemplare("iii-exemplare.dat")
exemplare = exemplare[
    (
        (exemplare.bibliothek == "009030115")
        | (exemplare.bibliothek == "009033645")
        | (pd.isna(exemplare.bibliothek))
    )
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
        "umfang",
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

df = df.replace(r"", np.NaN)

# Filtered signatur_g
df = df[~df["signatur_g"].str.contains("angeb", na=False, case=False)]

# Filtered signatur_a
df = df[~df["signatur_a"].str.contains("angeb", na=False, case=False)]

# idns aus der datei blacklist.txt im stammverzeichnis werden ausgefiltert
df = df[~df.idn.isin(blacklist())]

# Filtered f4241
df = df[df["f4241"].isna()]

# Filtered f4105_9
df = df[df["f4105_9"].isna()]

# Filtered standort
df = df[df["standort"] != "DBSM/DA"]

# Ausleihcode nicht e (= Moskauer Bestand)
# Filtered ausleihcode
df = df[~df["ausleihcode"].str.contains("e", na=False)]

# Filtered bbg
df = df[df["bbg"] != "Hal"]

# Filtered bbg
df = df[~df["bbg"].str.contains("Aaq", na=False)]

# Filtered signatur_g
df = df[~df["signatur_a"].str.contains("II 30,13", na=False)]

df = df.sort_values(
    by="signatur_a",
    ascending=True,
    na_position="first",
    key=lambda x: np.argsort(index_natsorted(df["signatur_a"])),
)
df.to_excel("abzug/iii.xlsx", index=False)
df.to_csv("abzug/iii.csv", index=False)

# IV (Drucke 1561-1800)
titel = get_titel("iv-titel.csv")

exemplare = get_exemplare("iv-exemplare.dat")
exemplare = exemplare[
    (
        (exemplare.bibliothek == "009030115")
        | (exemplare.bibliothek == "009033645")
        | (pd.isna(exemplare.bibliothek))
    )
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
        "umfang",
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

df = df.replace(r"", np.NaN)

df.jahr = df.jahr.str.replace("X", "0")
df.fillna({"jahr": "0"}, inplace=True)
df = df.astype({"jahr": "int"})

# Filtered signatur_g
df = df[~df["signatur_g"].str.contains("angeb", na=False, case=False)]

# Filtered signatur_a
df = df[~df["signatur_a"].str.contains("angeb", na=False, case=False)]

# idns aus der datei blacklist.txt im stammverzeichnis werden ausgefiltert
df = df[~df.idn.isin(blacklist())]

# Filtered f4241
df = df[df["f4241"].isna()]

# Filtered f4105_9
df = df[df["f4105_9"].isna()]

# Filtered jahr
df = df[df["jahr"] <= 1785]

# Filtered standort
df = df[df["standort"] != "DBSM/DA"]

# Ausleihcode nicht e (= Moskauer Bestand)
# Filtered ausleihcode
df = df[~df["ausleihcode"].str.contains("e", na=False)]

# Filtered signatur_g
df = df[~df["signatur_a"].str.contains("IV 205, 76", na=False)]

# Filtered signatur_a
df = df[~df["signatur_a"].str.contains("IV 205,76", na=False)]

# Filtered signatur_g
df = df[~df["signatur_a"].str.contains("IV 114, 15", na=False)]

# Filtered signatur_g
df = df[~df["signatur_a"].str.contains("IV 114, 13a", na=False)]

df = df.sort_values(
    by="signatur_a",
    ascending=True,
    na_position="first",
    key=lambda x: np.argsort(index_natsorted(df["signatur_a"])),
)

df.to_csv("abzug/iv.csv", index=False)
df.to_excel("abzug/iv.xlsx", index=False)

# Schreibmeisterbücher

titel = get_titel("schreibmeister-titel.csv")
exemplare = get_exemplare("schreibmeister-exemplare.dat")

titel.jahr = titel.jahr.str.replace(r"[xX]", "0", regex=True)
titel.jahr = titel.jahr.str.replace(r"[\[\]]", "", regex=True)

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
        "umfang",
        "f4243",
        "f4256",
        "f4241",
        "f4105_9",
        "f4105_g",
        "ausleihcode",
        "f4801_a",
        "einrichtung",
        "exemplar",
    ]
]

df = df.replace(r"", np.NaN)

# idns aus der datei blacklist.txt im stammverzeichnis werden ausgefiltert
df = df[~df.idn.isin(blacklist())]

df = df.sort_values(
    by="signatur_a",
    ascending=True,
    na_position="first",
    key=lambda x: np.argsort(index_natsorted(df["signatur_a"])),
)

df.to_csv("abzug/schreibmeister.csv", index=False)
df.to_excel("abzug/schreibmeister.xlsx", index=False)
