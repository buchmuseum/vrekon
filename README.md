# vrekon

## Requirements

Versionen siehe `pyproject.toml`

- Python
- pandas
- dvc
- pica-rs (muss manuell auf dem Rechner installiert werden, so dass es über den Befehl `pica` aufgerufen werden kann.)
- DNBtitelundexemplare.dat.gz

Praktisch für die Notebooks aber nicht unbedingt notwendig:

- mitosheet (benötigt neben dem Python Package binaries, die manuell über das pip-Packet `mitoinstaller` installiert werden können.)

## Datapipeline

Mit diesem Repository werden aus dem monatlichen Gesamtabzug der DNB-Daten `DNBtitelundexemplare.dat.gz` pro Bestandsgruppe .csv & .xlsx-Dateien gebildet, welche die zu digitalisierenden Bestände im Projekt Virtuelle Rekonstruktion der DNB-Buchsammlungen enthalten.

Die Data-Pipeline wird mit dem Tool `dvc` erstellt. Dieses Tool ruft in mehreren voneinander abhängigen Stages verschiedene Skripte auf, die die finalen Dateien produzieren.

Mit `dvc repro` wird die Pipeline gestartet. Es werden nur solche Schritte neu gerechnet, für die sich entweder der Programmcode oder die abhängigen Daten geändert haben.

Die Rohdaten (Gesamtabzug und Teilabzug mit DBSM-Daten) werden nicht nach Github commitet. Der Pfad zum Gesamtabzug wird in der Datei `dvc.yaml` konfiguriert.

## Stages

prepare: Aus dem Gesamtabzug werden mit `pica-rs` nur die DBSM-Daten gefiltert und im Verzeichnis `dump` abgelegt.

filter: Aus dem Teilabzug der DBSM-Daten werden mit `pica-rs` für jeden Teilbestand des Projektes die Titeldaten und die Exemplardaten separat im Verzeichnis `filter` abgelegt.

abzug: Die Titel- und Exemplardaten werden mit Python zu einer .csv pro Teilbestand synthetisiert.

## Jupyter Notebook & sonstige Dateien

Die Notebooks in `notebooks` werden mit `dvc repro` nicht ausgeführt. Sie dienen nur dem einfacheren Experimentieren mit den Daten. Änderungen an den Filtern müssen händisch nach `skripte/abzug.py` übertragen werden.

## einzelne IDNs vom Projekt ausschließen

Im Stammverzeichnis des Projektes liegt die Datei `blacklist.txt` Alle dort enthaltenen IDNs werden automatisch aus dem Projekt entfernt.
