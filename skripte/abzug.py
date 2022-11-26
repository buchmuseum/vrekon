import os
import pandas as pd
from collections import defaultdict
import re
import numpy as np
from natsort import index_natsorted
from typing import List, Tuple
from datetime import datetime

filter_path = "filter"

# alle abzüge werden zusätzlich in einen datumspfad unterhalb des abzugs-pfade geschrieben, damit man ggf. eine historie der geschriebenen dateien rekonstruieren kann
heute = datetime.now().strftime("%y-%m-%d")

if not os.path.isdir(f"./abzug/{heute}"):
    os.mkdir(f"./abzug/{heute}")


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
    matchlist = (
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
    )
    # [('standort', 'DBSM/M/Klemm'), ('signatur_g', 'II 1,2a - Fragm.')]
    for match in matchlist:
        if (kategorie == "209A") and (re.match(r"\$a.+\$x0[1-8]", inhalt)):
            continue

        if kategorie != match[0]:
            continue

        unterfeldsuche = re.findall(f"\${match[1]}([^\$]+)", inhalt)
        if unterfeldsuche != None:
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

            # wenn Leerzeile ist Datensatz zu Ende und alle Exemplare dieses Titels werden zunächst in ein df umgewandelt und dann an das df mit allen Exemplaren angehängt
            if l == "\n":
                df = pd.concat([df, make_nested_frame(exemplare)])
                continue

            # Zeile wird getrennt in Kategorie und Inhalt, line[0] ist Kategorie, line[1] ist Inhalt
            line = l.split(" ", 1)

            # wenn beginn neuer titelsatz wird 3-fach verschachteltes dict exemplare neu angelegt und idn geschrieben
            if line[0] == "003@":
                exemplare = defaultdict(
                    lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(str)))
                )
                idn = line[1][2:].strip()
                continue

            # wenn neue Einrichtung wird das geschrieben
            if line[0] == "101@":
                einrichtung = line[1][2:].strip()
                continue

            # in allen anderen fällen werden die zeilen ausgelesen
            # kategorie und okkurrenz werden getrennt
            feld = line[0].split("/")
            # die unterfelder werden in klartext übersetzt
            feldergebnis = feldauswertung(feld[0], line[1].strip())
            for ergebnis in feldergebnis:
                # wenn feld und unterfeld gleich sind, werden die ergebnisse durch Semikolon getrennt aneinander gehängt; in der funktion feldauswertung wird ausgeschlossen dass 209A/*.a zurückgegeben wird, wenn $x01-08 ist (damit werden altsignaturen aus 7101 ausgeschlossen)
                exemplare[idn][einrichtung][feld[1]][ergebnis[0]] = "; ".join(
                    [ergebnis[1], exemplare[idn][einrichtung][feld[1]][ergebnis[0]]]
                )

        # wenn alle Zeilen der Exemplardaten ausgewertet wurden, wird das df mit sprechenden indizes versehen und zurückgegeben.
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
    """
    Funktion liest die Datei blacklist.txt und gibt ein tuple mit allen idns zurück, die ignoriert werden sollen. jede idn kann gegen dieses tuple, d.h. gegen diese funktion gecheckt werden mit 'if idn in blacklist()' Die Funktion filter alles aus, was mit # beginnt
    """
    liste = list()
    with open("blacklist.txt", "r") as f:
        for line in f:
            if line.startswith("#"):
                continue

            liste.append(line.split("#")[0].strip())

    return tuple(liste)


def einlesen(bestand: str) -> pd.DataFrame:
    bestand = bestand.lower()
    signatur = {
        "böm": "Bö",
        "böink": "Bö",
        "ii": "II ",
        "iii": "III",
        "iv": "IV",
    }

    # titeldaten des jeweiligen teilbestands einlesen
    titel = get_titel(f"{bestand}-titel.csv")
    # exemplardaten des jeweiligen bestands einlesen
    exemplare = get_exemplare(f"{bestand}-exemplare.dat")

    # exemplardaten reduzieren.
    # nur solche mit ISIL DNB oder DBSM bzw ohne ISIL (= unsere Daten außerhalb ZDB)
    # nur solche, deren signatur mit den entsprechenden zeichen beginnt, wie in match-dictionary signatur oben festgelegt
    # keine, deren signatur die zeichenkette "angeb" enthält (= angebundene Werke)
    # keine mit Standort DBSM/DA = Dauerausstellung
    # keine mit Ausleihcode e = Verlust oder Moskauer Bestand
    exemplare = exemplare[
        (
            (exemplare.bibliothek == "009030115")
            | (pd.isna(exemplare.bibliothek))
            | (exemplare.bibliothek == "009033645")
        )
        & exemplare.signatur_a.str.startswith(signatur[bestand])
        & (exemplare.signatur_a.str.contains("angeb", na=False, case=False) == False)
        & (exemplare.signatur_g.str.contains("angeb", na=False, case=False) == False)
        & (exemplare.standort != "DBSM/DA")
        & (exemplare["ausleihcode"].str.contains("e", na=False) == False)
    ]

    # merge von titeln und exemplardaten, es bleiben nur titel erhalten, die auch ein gültiges exemplar haben
    df = titel.merge(exemplare, on="idn", how="right")

    return df


def filtern(df: pd.DataFrame, bestand: str) -> pd.DataFrame:
    df = df.replace("", np.NaN)

    # jahresfilter für IV

    df = df.replace("", np.NaN)
    df.jahr = df.jahr.str.replace("X", "0")
    df.fillna({"jahr": "0"}, inplace=True)
    df = df.astype({"jahr": "int"})

    if bestand == "iv":
        df = df[df["jahr"] <= 1785]

    # idns aus der datei blacklist.txt im stammverzeichnis werden ausgefiltert
    df = df[~df.idn.isin(blacklist())]

    # Filtered f4241
    df = df[df["f4241"].isna()]

    # Filtered f4105_9
    df = df[df["f4105_9"].isna()]

    # Filtered f4243
    df = df[df["f4243"].isna()]

    # Filtered bbg
    df = df[df["bbg"] != "Hal"]

    # Filtered bbg
    df = df[df["bbg"] != "Hfl"]

    # Filtered bbg
    df = df[df["bbg"] != "Pa"]

    df = df[~df["bbg"].str.contains("Aaq", na=False)]

    df = df.sort_values(
        by="signatur_a",
        ascending=True,
        na_position="first",
        key=lambda X: np.argsort(index_natsorted(df["signatur_a"])),
    )
    return df


def schreiben(df: pd.DataFrame, bestand: str) -> None:
    spalten = (
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
        "jahr",
    )

    write_columns = [spalte for spalte in spalten if spalte in df.columns]

    df.to_excel(f"abzug/{bestand}.xlsx", index=False, columns=write_columns)
    df.to_csv(f"abzug/{bestand}.csv", index=False, columns=write_columns)
    df.to_excel(
        f"abzug/{heute}/{heute}-{bestand}.xlsx", index=False, columns=write_columns
    )
    df.to_csv(
        f"abzug/{heute}/{heute}-{bestand}.csv", index=False, columns=write_columns
    )


# main
# alle bestände aus dem Tuple bestaende werden geladen, gefiltert und die ergebnisse geschrieben
bestaende = ("böm", "böink", "ii", "iii", "iv")

for bestand in bestaende:
    df = einlesen(bestand)
    df = filtern(df, bestand)
    schreiben(df, bestand)

# schreibmeisterbücher können nicht nach dem allgemeinen system verarbeitet werden, weil es bei ihnen verschiedene besonderheiten gibt.

titel = get_titel("schreibmeister-titel.csv")
exemplare = get_exemplare("schreibmeister-exemplare.dat")

titel.jahr = titel.jahr.str.replace("[xX]", "0", regex=True)
titel.jahr = titel.jahr.str.replace("[\[\]]", "", regex=True)

titel.fillna({"jahr": "0"}, inplace=True)
titel = titel.astype({"jahr": "int"})

df = titel.merge(exemplare, on="idn", how="right")

df = df.replace("", np.NaN)
df = df[df["jahr"] <= 1830]
# idns aus der datei blacklist.txt im stammverzeichnis werden ausgefiltert
df = df[~df.idn.isin(blacklist())]

# Filtered f4105_9
df = df[df["f4105_9"].isna()]

df = df.sort_values(
    by="signatur_a",
    ascending=True,
    na_position="first",
    key=lambda x: np.argsort(index_natsorted(df["signatur_a"])),
)

schreiben(df, "schreibmeister")
