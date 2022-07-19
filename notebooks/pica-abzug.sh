RAWPATH="../raw/"
DATFILE="dbsm-titel-exemplare.dat"

pica filter "209A/*.a =^ 'Bö M' || 209A/*.g =^ 'Bö M' || 209A/*.a =^ 'Boe M' || 209A/*.g =^ 'Boe M'" "$RAWPATH$DATFILE" | pica select --translit nfc "003@.0,002@.0,021A{a,d},021A{Y?,Y},021B{l,a},039D.9,039I.9,039B.9,036H{9,g}" -H "idn,bbg,tit_a, tit_d, tit_Y,stuecktitel_l,stuecktitel_a, f4243,f4256,f4241,f4105_9,f4105_g" -o "$RAWPATH"böm-titel.csv
pica filter --reduce "003@,209A,209C,247C,237A,101@" "209A/*.a =^ 'Bö M' || 209A/*.g =^ 'Bö M' || 209A/*.a =^ 'Boe M' || 209A/*.g =^ 'Boe M'" "$RAWPATH$DATFILE" | pica print --translit nfc -o "$RAWPATH"böm-exemplare.dat

pica filter "209A/*.a =^ 'Bö Ink' || 209A/*.g =^ 'Bö Ink'" "$RAWPATH$DATFILE" | pica select --translit nfc "003@.0,002@.0,021A{a,d},021A{Y?,Y},021B{l,a},039D.9,039I.9,039B.9,036H{9,g}" -H "idn,bbg,tit_a, tit_d, tit_Y,stuecktitel_l,stuecktitel_a, f4243,f4256,f4241,f4105_9,f4105_g" -o "$RAWPATH"böink-titel.csv
pica filter --reduce "003@,209A,209C,247C,237A,101@" "209A/*.a =^ 'Bö Ink' || 209A/*.g =^ 'Bö Ink'" "$RAWPATH$DATFILE" | pica print --translit nfc -o "$RAWPATH"böink-exemplare.dat

pica filter "209A/*.a =^ 'II' && 044P/*.9 == '040270416'" "$RAWPATH$DATFILE" | pica select --translit nfc "003@.0,002@.0,021A{a,d},021A{Y?,Y},021B{l,a},039D.9,039I.9,039B.9,036H{9,g}" -H "idn,bbg,tit_a, tit_d, tit_Y,stuecktitel_l,stuecktitel_a, f4243,f4256,f4241,f4105_9,f4105_g" -o "$RAWPATH"ii-titel.csv
pica filter --reduce "003@,209A,209C,247C,237A,101@" "209A/*.a =^ 'II' && 044P/*.9 == '040270416'" "$RAWPATH$DATFILE" | pica print --translit nfc -o "$RAWPATH"ii-exemplare.dat

pica filter "209A/*.a =^ 'III'" "$RAWPATH$DATFILE" | pica select --translit nfc "003@.0,002@.0,021A{a,d},021A{Y?,Y},021B{l,a},039D.9,039I.9,039B.9,036H{9,g}" -H "idn,bbg,tit_a, tit_d, tit_Y,stuecktitel_l,stuecktitel_a, f4243,f4256,f4241,f4105_9,f4105_g" -o "$RAWPATH"iii-titel.csv
pica filter --reduce "003@,209A,209C,247C,237A,101@" "209A/*.a =^ 'III'" "$RAWPATH$DATFILE" | pica print --translit nfc -o "$RAWPATH"iii-exemplare.dat

pica filter "209A/*.a =^ 'IV'" "$RAWPATH$DATFILE" | pica select --translit nfc "003@.0,002@.0,011@.a,021A{a,d},021A{Y?,Y},021B{l,a},039D.9,039I.9,039B.9,036H{9,g}" -H "idn,bbg,jahr,tit_a, tit_d, tit_Y,stuecktitel_l,stuecktitel_a, f4243,f4256,f4241,f4105_9,f4105_g" -o "$RAWPATH"iv-titel.csv
pica filter --reduce "003@,209A,209C,247C,237A,101@" "209A/*.a =^ 'IV'" "$RAWPATH$DATFILE" | pica print --translit nfc -o "$RAWPATH"iv-exemplare.dat

# pica filter "209A/*.a =^ 'I,' " "$RAWPATH$DATFILE" | pica select --translit nfc "003@.0,002@.0,011@.a,021A{a,d},021A{Y?,Y},021B{l,a},039D.9,039I.9,039B.9,036H{9,g}" -H "idn,bbg,jahr,tit_a, tit_d, tit_Y,stuecktitel_l,stuecktitel_a, f4243,f4256,f4241,f4105_9,f4105_g" -o "$RAWPATH"i-titel.csv
# pica filter --reduce "003@,209A,209C,247C,237A,101@" "209A/*.a =^ 'I,'" "$RAWPATH$DATFILE" | pica print --translit nfc -o "$RAWPATH"i-exemplare.dat

# pica filter "209A/*.a =~ '^V[a-z]+.*' && 011@.a =~ '^([01xX][0-7x][0-9xX][0-9xX])|([01xX][8][12][0-9xX])|([01xX][8][3][0])'" "$RAWPATH$DATFILE" | pica select --translit nfc "003@.0,002@.0,011@.a,021A{a,d},021A{Y?,Y},021B{l,a},039D.9,039I.9,039B.9,036H{9,g}" -H "idn,bbg,jahr,tit_a, tit_d, tit_Y,stuecktitel_l,stuecktitel_a, f4243,f4256,f4241,f4105_9,f4105_g" -o "$RAWPATH"v-titel.csv
# pica filter --reduce "003@,209A,209C,247C,237A,101@" "209A/*.a =~ '^V[a-z]+.*' && 011@.a =~ '^([01xX][0-7x][0-9xX][0-9xX])|([01xX][8][12][0-9xX])|([01xX][8][3][0])'" "$RAWPATH$DATFILE" | pica print --translit nfc -o "$RAWPATH"v-exemplare.dat

# pica filter "209A/*.a =^ 'VIII' && 011@.a =~ '^([01xX][0-7x][0-9xX][0-9xX])|([01xX][8][12][0-9xX])|([01xX][8][3][0])'" "$RAWPATH$DATFILE" | pica select --translit nfc "003@.0,002@.0,011@.a,021A{a,d},021A{Y?,Y},021B{l,a},039D.9,039I.9,039B.9,036H{9,g}" -H "idn,bbg,jahr,tit_a, tit_d, tit_Y,stuecktitel_l,stuecktitel_a, f4243,f4256,f4241,f4105_9,f4105_g" -o "$RAWPATH"viii-titel.csv
# pica filter --reduce "003@,209A,209C,247C,237A,101@" "209A/*.a =^ 'VIII' && 011@.a =~ '^([01xX][0-7x][0-9xX][0-9xX])|([01xX][8][12][0-9xX])|([01xX][8][3][0])'" "$RAWPATH$DATFILE" | pica print --translit nfc -o "$RAWPATH"viii-exemplare.dat

# pica filter "209A/*.a =^ 'Bö' || 209A/*.a =^ 'Boe'" --and "011@.a =~ '^([01xX][0-7x][0-9xX][0-9xX])|([01xX][8][12][0-9xX])|([01xX][8][3][0])'" --and "209A/*.f == 'DBSM/F/Bö' || 209A/*.f == 'DBSM/F/Boe'" "$RAWPATH$DATFILE" | pica select --translit nfc "003@.0,002@.0,011@.a,021A{a,d},021A{Y?,Y},021B{l,a},039D.9,039I.9,039B.9,036H{9,g}" -H "idn,bbg,jahr,tit_a, tit_d, tit_Y,stuecktitel_l,stuecktitel_a, f4243,f4256,f4241,f4105_9,f4105_g" -o "$RAWPATH"böf-titel.csv
# pica filter --reduce "003@,209A,209C,247C,237A,101@" "209A/*.a =^ 'Bö' || 209A/*.a =^ 'Boe'" --and "011@.a =~ '^([01xX][0-7x][0-9xX][0-9xX])|([01xX][8][12][0-9xX])|([01xX][8][3][0])'" --and "209A/*.f == 'DBSM/F/Bö' || 209A/*.f == 'DBSM/F/Boe'" "$RAWPATH$DATFILE" | pica print --translit nfc -o "$RAWPATH"böf-exemplare.dat

# pica filter "209A/*.f == 'DBSM/F/Klemm' && 011@.a =~ '^([01xX][0-7x][0-9xX][0-9xX])|([01xX][8][12][0-9xX])|([01xX][8][3][0])'" "$RAWPATH$DATFILE" | pica select --translit nfc "003@.0,002@.0,011@.a,021A{a,d},021A{Y?,Y},021B{l,a},039D.9,039I.9,039B.9,036H{9,g}" -H "idn,bbg,jahr,tit_a, tit_d, tit_Y,stuecktitel_l,stuecktitel_a, f4243,f4256,f4241,f4105_9,f4105_g" -o "$RAWPATH"klemmf-titel.csv
# pica filter --reduce "003@,209A,209C,247C,237A,101@" "209A/*.f == 'DBSM/F/Klemm' && 011@.a =~ '^([01xX][0-7x][0-9xX][0-9xX])|([01xX][8][12][0-9xX])|([01xX][8][3][0])'" "$RAWPATH$DATFILE" | pica print --translit nfc -o "$RAWPATH"klemmf-exemplare.dat

pica filter "037A.a =^ 'in:' && 002@.0 == 'Aal'" dbsm-titel-exemplare-22-7.dat | pica select --translit nfc "003@.0,002@.0,011@.a,021A{a,d},021A{Y?,Y},021B{l,a},039D.9,039I.9,039B.9,036H{9,g},037A.a" -H "idn,bbg,jahr,tit_a, tit_d, tit_Y,stuecktitel_l,stuecktitel_a, f4243,f4256,f4241,f4105_9,f4105_g, 4201" -o Aal-4201.csv

pica filter "044P/*.9 == '041799844'" dbsm-titel-exemplare-22-7.dat | pica select --translit nfc "003@.0,002@.0,011@.a,021A{a,d},021A{Y?,Y},021B{l,a},039D.9,039I.9,039B.9,036H{9,g}" -H "idn,bbg,jahr,tit_a, tit_d, tit_Y,stuecktitel_l,stuecktitel_a, f4243,f4256,f4241,f4105_9,f4105_g" -o schreibmeister-titel.csv

pica filter --reduce "003@,209A,209C,247C,237A,101@" "044P/*.9 == '041799844' && 011@.a =~ '^([01xX][0-7x][0-9xX][0-9xX])|([01xX][8][12][0-9xX])|([01xX][8][3][0])'" "$RAWPATH$DATFILE" | pica print --translit nfc -o "$RAWPATH"schreibmeister-exemplare.dat