#!/bin/bash

REQFILE="${1:-requests.log}"
if [[ $(uname) == Darwin* ]] ; then
    AWK='gawk'
else
    AWK='awk'
fi

${AWK} '
BEGIN {
    IGNORECASE=1
    printf "| %-20s | %-20s | %-20s | %-20s |\n", "BROWSER", "METHOD", "ORIGIN", "CREDENTIALS"
    print "| -------------------- | -------------------- | -------------------- | -------------------- |"
}
/[^ ]/ {
    # look for first non-blank line after start
    if (newReq) {
        newReq=0
        requested=match($0, /^(GET|POST|OPTIONS|HEAD|DELETE|PUT) \/secret\.txt\?origin=([^&/]*)&creds=([01]) HTTP\/[0-9\.]+$/, mArr)
        if (requested) {
            method=mArr[1]
            origin=mArr[2]
            creds=mArr[3]
        }
    }
}
{
    if (requested) {
        # look for the Access-Control-Request-Method, or the Cookie and User-Agent after a request for /secret.txt
        if (match($0, /^Access-Control-Request-Method: *(.*)/, mArr)) {
            acMethod=mArr[1]
        }
        if (match($0, /^Cookie: *(.*)/, mArr)) {
            cookie=mArr[1]
        }
        if (match($0, /^User-Agent: *(.*)/, mArr)) {
            ua=mArr[1]
            numF=patsplit(ua, uaFields, /[A-Za-z]+\/[0-9\.]+/)
            # printf "DEBUG UA: numF=" numF ", uaFields=["
            # for (i in uaFields) { printf uaFields[i] ", " }
            # print "]"
            if (numF > 2) {
                if (uaFields[1] ~ /Opera\// || uaFields[1] ~ /Mozilla\// && uaFields[numF] ~ /OPR\//) {
                    ua="Opera " gensub(/.*\//, "", "1", uaFields[numF])
                }
                else if (uaFields[numF-1] ~ /Chrome\//) {
                    ua=gensub(/\//, " ", "1", uaFields[numF-1])
                }
                else if (uaFields[numF] ~ /(Safari|Firefox)\//) {
                    ua=gensub(/\//, " ", "1", uaFields[numF])
                }
                else {
                    ua=gensub(/\/.*/, "", "1", uaFields[1]) gensub(/\//, " ", "1", uaFields[numF])
                }
            }
        }
    }
}
/^----- Request Start ----->/ {
    newReq=1
    origin=""
    creds=""
    acMethod=""
    cookie=""
    ua=""
}
/^<----- Request End -----/ {
    if (requested) {
        # print method "\nOrigin: " origin "\nCredentials: " creds "\nCookie: " cookie "\nUser-Agent: " ua "\n\n===================="
        printf "| %-20s | %-20s | %-20s | %-20s |\n", ua, method " " acMethod, origin, creds
        requested=0
    }
}
' "${REQFILE}"
