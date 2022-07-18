# Suchbefehle zum Abziehen der Daten aus dem Gesamtdump mit pica-rs

## Bö M

ACHTUNG: das ö innerhalb des Filterausdrucks muss NFD sein

### Titeldaten Bö M

```bash
pica filter "209A/*.a =^ 'Bö M' || 209A/*.g =^ 'Bö M' || 209A/*.a =^ 'Boe M' || 209A/*.g =^ 'Boe M'" dbsm-titel-exemplare-22-03.dat | pica select --translit nfc "003@.0,002@.0,021A{a,d},021A{Y?,Y},021B{l,a},039D.9,039I.9,039B.9,036H{9,g}" -H "idn,bbg,tit_a, tit_d, tit_Y,stuecktitel_l,stuecktitel_a, f4243,f4256,f4241,f4105_9,f4105_g" -o böm-titel.csv
```

### Exemplardaten Bö M

```bash
pica filter --reduce "003@,209A,209C,247C,237A,101@" "209A/*.a =^ 'Bö M' || 209A/*.g =^ 'Bö M' || 209A/*.a =^ 'Boe M' || 209A/*.g =^ 'Boe M'" dbsm-titel-exemplare-22-03.dat | pica print --translit nfc -o böm-exemplare.dat
```

003@.0,idn
002@.0,bbg
021A{a,d},tit_a, tit_d, tit_8
021A{Y?,Y},tit_Y
021B{l,a},stuecktitel_l,stuecktitel_a, stuecktitel_r
039D.9,4243
039I.9, 4256
039B.9,4241
036H{9,g} 4105_9,_g

## Bö Ink #TODO

### Titeldaten Bö Ink

```bash
pica filter "209A/*.a =^ 'Bö Ink' || 209A/*.g =^ 'Bö Ink'" dbsm-titel-exemplare-22-03.dat | pica select --translit nfc "003@.0,002@.0,021A{a,d},021A{Y?,Y},021B{l,a},039D.9,039I.9,039B.9,036H{9,g}" -H "idn,bbg,tit_a, tit_d, tit_Y,stuecktitel_l,stuecktitel_a, f4243,f4256,f4241,f4105_9,f4105_g" -o böink-titel.csv
```

### Exemplardaten

```bash
pica filter --reduce "003@,209A,209C,247C,237A,101@" "209A/*.a =^ 'Bö Ink' || 209A/*.g =^ 'Bö Ink'" dbsm-titel-exemplare-22-03.dat | pica print --translit nfc -o böink-exemplare.dat
```

## II Inkunabeln

f sig II* und sw Inkunabel und bbg a*

### Titeldaten II

```bash
pica filter "209A/*.a =^ 'II' && 044P/*.9 == '040270416'" dbsm-titel-exemplare-22-03.dat | pica select --translit nfc "003@.0,002@.0,021A{a,d},021A{Y?,Y},021B{l,a},039D.9,039I.9,039B.9,036H{9,g}" -H "idn,bbg,tit_a, tit_d, tit_Y,stuecktitel_l,stuecktitel_a, f4243,f4256,f4241,f4105_9,f4105_g" -o ii-titel.csv
```

### Exemplardaten II

```bash
pica filter --reduce "003@,209A,209C,247C,237A,101@" "209A/*.a =^ 'II' && 044P/*.9 == '040270416'" dbsm-titel-exemplare-22-03.dat | pica print --translit nfc -o ii-exemplare.dat
```

## III (Drucke 1501-1560)

f sig III* und bbg a*

### Titeldaten III

```bash
pica filter "209A/*.a =^ 'III'" dbsm-titel-exemplare-22-03.dat | pica select --translit nfc "003@.0,002@.0,021A{a,d},021A{Y?,Y},021B{l,a},039D.9,039I.9,039B.9,036H{9,g}" -H "idn,bbg,tit_a, tit_d, tit_Y,stuecktitel_l,stuecktitel_a, f4243,f4256,f4241,f4105_9,f4105_g" -o iii-titel.csv
```

### Exemplardaten III

```bash
pica filter --reduce "003@,209A,209C,247C,237A,101@" "209A/*.a =^ 'III'" dbsm-titel-exemplare-22-03.dat | pica print --translit nfc -o iii-exemplare.dat
```

## IV (Drucke 1561-1800)

f sig IV* und bbg a* und std dbsmm* und jhr <1831

### Titeldaten III

```bash
pica filter "209A/*.a =^ 'IV'" dbsm-titel-exemplare-22-03.dat | pica select --translit nfc "003@.0,002@.0,011@.a,021A{a,d},021A{Y?,Y},021B{l,a},039D.9,039I.9,039B.9,036H{9,g}" -H "idn,bbg,jahr,tit_a, tit_d, tit_Y,stuecktitel_l,stuecktitel_a, f4243,f4256,f4241,f4105_9,f4105_g" -o iv-titel.csv
```

### Exemplardaten III

```bash
pica filter --reduce "003@,209A,209C,247C,237A,101@" "209A/*.a =^ 'IV'" dbsm-titel-exemplare-22-03.dat | pica print --translit nfc -o iv-exemplare.dat
```

## I (Handschriften, nur vor 1831)

f sig {I* und nicht IV*} und {I* und nicht III*} und {I* und nicht II*} und bbg h* und jhr <1831

### Titeldaten I
```bash
pica filter "209A/*.a =^ 'I,' " dbsm-titel-exemplare-22-03.dat | pica select --translit nfc "003@.0,002@.0,011@.a,021A{a,d},021A{Y?,Y},021B{l,a},039D.9,039I.9,039B.9,036H{9,g}" -H "idn,bbg,jahr,tit_a, tit_d, tit_Y,stuecktitel_l,stuecktitel_a, f4243,f4256,f4241,f4105_9,f4105_g" -o i-titel.csv
```

### Exemplardaten I
```bash
pica filter --reduce "003@,209A,209C,247C,237A,101@" "209A/*.a =^ 'I,'" dbsm-titel-exemplare-22-03.dat | pica print --translit nfc -o i-exemplare.dat
```

## V (nur bis EJ 1830)

f sig {V* und nicht VIII*} und bbg ungleich X* und std dbsmm* und jhr <1831

### Titeldaten V

```bash
pica filter "209A/*.a =~ '^V[a-z]+.*' && 011@.a =~ '^([01xX][0-7x][0-9xX][0-9xX])|([01xX][8][12][0-9xX])|([01xX][8][3][0])'" dbsm-titel-exemplare-22-03.dat | pica select --translit nfc "003@.0,002@.0,011@.a,021A{a,d},021A{Y?,Y},021B{l,a},039D.9,039I.9,039B.9,036H{9,g}" -H "idn,bbg,jahr,tit_a, tit_d, tit_Y,stuecktitel_l,stuecktitel_a, f4243,f4256,f4241,f4105_9,f4105_g" -o v-titel.csv
```

### Exemplardaten V

```bash
pica filter --reduce "003@,209A,209C,247C,237A,101@" "209A/*.a =~ '^V[a-z]+.*' && 011@.a =~ '^([01xX][0-7x][0-9xX][0-9xX])|([01xX][8][12][0-9xX])|([01xX][8][3][0])'" dbsm-titel-exemplare-22-03.dat | pica print --translit nfc -o v-exemplare.dat
```

## VIII (nur bis EJ 1830)

f sig VIII* und bbg nicht x* und bbg nicht q* und bbg nicht p* und std dbsmm* und jhr <1831

### Titeldaten VIII

```bash
pica filter "209A/*.a =^ 'VIII' && 011@.a =~ '^([01xX][0-7x][0-9xX][0-9xX])|([01xX][8][12][0-9xX])|([01xX][8][3][0])'" dbsm-titel-exemplare-22-03.dat | pica select --translit nfc "003@.0,002@.0,011@.a,021A{a,d},021A{Y?,Y},021B{l,a},039D.9,039I.9,039B.9,036H{9,g}" -H "idn,bbg,jahr,tit_a, tit_d, tit_Y,stuecktitel_l,stuecktitel_a, f4243,f4256,f4241,f4105_9,f4105_g" -o viii-titel.csv
```

### Exemplardaten VIII
```bash
pica filter --reduce "003@,209A,209C,247C,237A,101@" "209A/*.a =^ 'VIII' && 011@.a =~ '^([01xX][0-7x][0-9xX][0-9xX])|([01xX][8][12][0-9xX])|([01xX][8][3][0])'" dbsm-titel-exemplare-22-03.dat | pica print --translit nfc -o viii-exemplare.dat
```

## Bö Fachbibliothek

f sig bö* und std dbsmfbö und bbg nicht q* und jhr <1831

### Titeldaten Bö F

```bash
pica filter "209A/*.a =^ 'Bö' || 209A/*.a =^ 'Boe'" --and "011@.a =~ '^([01xX][0-7x][0-9xX][0-9xX])|([01xX][8][12][0-9xX])|([01xX][8][3][0])'" --and "209A/*.f == 'DBSM/F/Bö' || 209A/*.f == 'DBSM/F/Boe'" dbsm-titel-exemplare-22-03.dat | pica select --translit nfc "003@.0,002@.0,011@.a,021A{a,d},021A{Y?,Y},021B{l,a},039D.9,039I.9,039B.9,036H{9,g}" -H "idn,bbg,jahr,tit_a, tit_d, tit_Y,stuecktitel_l,stuecktitel_a, f4243,f4256,f4241,f4105_9,f4105_g" -o böf-titel.csv
```

### Exemplardaten Bö F

```bash
pica filter --reduce "003@,209A,209C,247C,237A,101@" "209A/*.a =^ 'Bö' || 209A/*.a =^ 'Boe'" --and "011@.a =~ '^([01xX][0-7x][0-9xX][0-9xX])|([01xX][8][12][0-9xX])|([01xX][8][3][0])'" --and "209A/*.f == 'DBSM/F/Bö' || 209A/*.f == 'DBSM/F/Boe'" dbsm-titel-exemplare-22-03.dat | pica print --translit nfc -o böf-exemplare.dat
```
## Klemm Fachbibliothek

f std dbsmfklemm und bbg nicht q* und jhr <1831 und nicht bbg "Ac*"

### Titeldaten Klemm Fachbibliothek

```bash
pica filter "209A/*.f == 'DBSM/F/Klemm' && 011@.a =~ '^([01xX][0-7x][0-9xX][0-9xX])|([01xX][8][12][0-9xX])|([01xX][8][3][0])'" dbsm-titel-exemplare-22-03.dat | pica select --translit nfc "003@.0,002@.0,011@.a,021A{a,d},021A{Y?,Y},021B{l,a},039D.9,039I.9,039B.9,036H{9,g}" -H "idn,bbg,jahr,tit_a, tit_d, tit_Y,stuecktitel_l,stuecktitel_a, f4243,f4256,f4241,f4105_9,f4105_g" -o klemmf-titel.csv
```

### Exemplardaten Klemm Fachbibliothek

```bash
pica filter --reduce "003@,209A,209C,247C,237A,101@" "209A/*.f == 'DBSM/F/Klemm' && 011@.a =~ '^([01xX][0-7x][0-9xX][0-9xX])|([01xX][8][12][0-9xX])|([01xX][8][3][0])'" dbsm-titel-exemplare-22-03.dat | pica print --translit nfc -o klemmf-exemplare.dat
```