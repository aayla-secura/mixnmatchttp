#!/bin/bash
# to debug: uncomment the last line and do
# egrep 'DEBUG: ([A-Z]+ \/secret|POST \/demos|END: requested.*1)' $TMPFILE

REQFILE="${1:-logs/requests.log}"
OUTFILE="${2:-logs/requests_result.md}"
TMPFILE="${OUTFILE}.unsorted"
if [[ $(uname) == Darwin* ]] ; then
  AWK='gawk'
else
  AWK='awk'
fi

${AWK} '
BEGIN {
  IGNORECASE=1
  debug=0
  printf "| %-20s | %-20s | %-20s | %-20s | %-20s | %-20s | %-20s |\n", "BROWSER", "METHOD", "ORIGIN", "CREDENTIALS", "PREFLIGHT", "COOKIE", "READ BY JS"
  print "| :------------------: | :------------------: | :------------------: | :------------------: | :------------------: | :------------------: | :------------------: |"
}
/[^ ]/ {
  # look for first non-blank line after start
  if (newReq) {
    newReq=0 
    if (debug) { print "DEBUG: " $0 }
    requested=match($0,
      /^(GET|POST|OPTIONS|HEAD|DELETE|PUT) \/secret\/secret\.txt\?origin=(\*|%%ECHO%%)?&creds=([01])&via=([^&]*)[^ ]* HTTP\/[0-9\.]+$/,
      mArr)
    if (requested) {
      method=mArr[1]
      origin=mArr[2]
      creds=mArr[3]
      exfMethod=mArr[4]
    } else {
      exfiltrated=match($0,
        /^POST \/demos\/sop\/getData.html\?reqURL=[^&]+%2Fsecret%2Fsecret.txt%3Forigin%3D(\*|%25%25ECHO%25%25)?%26creds%3D([01])[^ ]*&post=([01])&via=([^&]*) HTTP\/[0-9\.]+$/,
        mArr)
      if (exfiltrated) {
        origin=gensub(/%25/, "%", "g", mArr[1])
        creds=mArr[2]
        if (mArr[3] == 1) { method="POST" }
        else { method="GET" }
        exfMethod=mArr[4]
      }
    }
    if (debug > 1) { print "DEBUG: requested: " requested ", exfiltrated: " exfiltrated }
  }
}
{
  if (requested || exfiltrated) {
    # look for the Access-Control-Request-Method, or the Cookie
    # and User-Agent after a request for /secret/secret.txt
    if (requested && match($0, /^Access-Control-Request-Method: *(.*)/, mArr)) {
      method=mArr[1]
      preflight="Y"
    }
    if (requested && match($0, /^Cookie: *SESSION=/)) {
      if (debug > 1) { print "DEBUG: Cookie: " $0 }
      cookie="Y"
    }
    if (match($0, /^User-Agent: *([^\(]*) *(\([^\)]*\))? *(.*)/, mArr)) {
      if (mArr[2]) {
        os=gensub(/^\(|\)$/, "", "g", mArr[2])
        uaFull=mArr[1] " " mArr[3]
      }
      else {
        os=""
        uaFull=mArr[1]
      }

      if (uaFull == "contype") {
        # IE being an idiot
        ua=uaOLD
      }
      else {
        numF=patsplit(uaFull, uaFields, /[A-Za-z]+\/[0-9\.]+/)
        # split(os, osFields, /; */)
        if (debug > 1) {
          printf "DEBUG: UA: os=" os ", numF=" numF ", uaFields=["
          for (i = 0; i <= numF ; i++) { printf uaFields[i] ", " }
          print "]"
        }
        ua=""
        if (numF > 2) {
          if (uaFields[1] ~ /Opera\// || uaFields[1] ~ /Mozilla\// && uaFields[numF] ~ /OPR\//) {
            # OPERA
            ua="Opera " gensub(/.*\//, "", "1", uaFields[numF])
          }
          else if (uaFields[numF-1] ~ /Chrome\//) {
            # CHROME
            ua=gensub(/\//, " ", "1", uaFields[numF-1])
          }
          else if (uaFields[numF] ~ /(Firefox)\//) {
            # FIREFOX
            ua=gensub(/\//, " ", "1", uaFields[numF])
          }
          else if (uaFields[numF] ~ /(Edge)\//) {
            # EDGE
            ua=gensub(/\//, " ", "1", uaFields[numF])
          }
          else if (uaFields[numF] ~ /(Safari)\//) {
            # SAFARI
            version=""
            for (i in uaFields) {
              if (uaFields[i] ~ /Version\// ) {
                version=gensub(/.*\//, "", "1", uaFields[i])
              }
            }
            if (! version) {
              version=gensub(/.*\//, "", "1", uaFields[numF]) # WebKit version
            }
            ua=gensub(/\//, " ", "1", uaFields[numF])
          }
        }
        if (! ua) {
          if (os ~ /MSIE|Trident/) {
            # INTERNET EXPLORER
            match(os, /(Windows NT *)([0-9\.]+)/, mArr)
            WinVersion=mArr[2]
            match(os, /(MSIE *|rv *: *)([0-9\.]+)/, mArr)
            IEVersion=mArr[2]
            if (! IEVersion) {
              IEVersion="(Unknown)"
            }
            ua="IE " IEVersion " (Win " WinVersion ")"
          }
          else {
            # UNKNOWN
            ua=uaFull
          }
        }
      }
    }
  }
}
/^----- Request Start ----->/ {
  newReq=1
  origin=""
  creds=""
  method=""
  preflight=""
  exfMethod=""
  cookie=""
  # keep it in case the next one is IE doing a HEAD with UA=contype
  uaOLD=ua
  ua=""
}
/^<----- Request End -----/ {

  if (requested || exfiltrated) {
    id=ua "@" origin "@" creds "@" method "@" exfMethod
    if (preflight) {
      result[id]["preflight"]=preflight (cookie ? " (with Cookie)" : "")
    } else if (requested) {
      result[id]["ua"]=ua
      result[id]["origin"]=origin
      result[id]["creds"]=creds
      result[id]["method"]=method " (via " exfMethod ")"
      result[id]["cookie"]=cookie
    } else if (exfiltrated) {
      result[id]["read"]="Y"
    }
    if (debug) {
      print "DEBUG: END: id: " id ", requested: " requested ", exfiltrated: " exfiltrated
      if (result[id]["ua"]) {
        printf "DEBUG: END: result[id]=["
        printf ua ": "
        for (f in result[id]) {
          printf f ": " result[id][f] "; "
        }
        print "]"
      }
    }
  }

  requested=0
  exfiltrated=0
}
END {
  for (id in result) {
    printf "| %-20s | %-20s | %-20s | %-20s | %-20s | %-20s | %-20s |\n", result[id]["ua"], result[id]["method"], result[id]["origin"], result[id]["creds"], result[id]["preflight"], result[id]["cookie"], result[id]["read"]
  }
}
' "${REQFILE}" > "${TMPFILE}"

# Sort the table
IFS=$'\n' read -d '' -a browsers < <(tail -n+3 "${TMPFILE}" | cut -d\| -f2 | sort -u)
# IFS=$'\n' read -d '' -a methods < <(tail -n+3 "${TMPFILE}" | cut -d\| -f3 | sort -u)
sep=$(sed -n '2p' "${TMPFILE}" | tr ':-' '~')

head -n2 "${TMPFILE}" > "${OUTFILE}"
for browser in "${browsers[@]}" ; do
  for c in '(' ')' '[' ']' '.' '^' '$' '+' '\?' '\*' '|' '\' '{' '}' ; do
    browser="${browser//${c}/\\${c}}"
  done
  for origin in '\*' '%%ECHO%%' '' ; do
    for creds in 1 0 ; do
      # don't sort them by method; keep the order in which requests were sent
      # for method in "${methods[@]}" ; do
      #  egrep '^\| *'"${browser}"' *\| *'"${method}"' *\| *'"${origin}"' *\| *'"${creds}"' *\|' "${TMPFILE}"
      # done
      egrep '^\| *'"${browser}"' *\| *'"[^\|]+"' *\| *'"${origin}"' *\| *'"${creds}"' *\|' "${TMPFILE}"
      echo "${sep}"
    done
  done
done | uniq >> "${OUTFILE}"

rm "${TMPFILE}"
