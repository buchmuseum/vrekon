import pandas as pd


def einlesen(bestand: str) -> pd.DataFrame:
    signatur = {"böm": "Bö", "böink": "Bö", "II": "II "}

    exemplare = get_exemplare(f"böm-exemplare.dat")
    exemplare = exemplare[
        (
            (exemplare.bibliothek == "009030115")
            | (pd.isna(exemplare.bibliothek))
            | (exemplare.bibliothek == "009033645")
        )
        & exemplare.signatur_a.str.startswith("Bö")
        & (exemplare.signatur_a.str.contains("angeb", na=False, case=False) == False)
        & (exemplare.standort != "DBSM/DA")
    ]
