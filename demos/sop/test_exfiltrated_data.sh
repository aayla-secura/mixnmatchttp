#!/bin/bash

OUTDIR="exfiltrated_data"
[[ -d "$OUTDIR" ]] || mkdir "$OUTDIR"
rm "$OUTDIR"/* 2>/dev/null
cd "$OUTDIR"

entry=0
awk '
/POST \/demos/  { inpattern=1 }
/<----- Request End -----/ {
  inpattern=0;
}
/\{"data"/ {
  data=gensub(/^\{"data": *"([^"]+).*/, "\\1", "1")
  result[data][ua]=""
  # print data ": " ua
}
(inpattern && $0 ~ /^User-Agent/) { ua=gensub(/^User-Agent: */, "", "1") }
END {
  entry=0
  for (data in result) {
    entry++
    print data >> "data_" entry "_base64.txt"
    for (ua in result[data]) {
      print ua >> "UAs_" entry ".txt"
    }
  }
}
' ../logs/request_vary_host.log ../logs/request_vary_port_[ot]*.log

for f in data_*_base64.txt ; do
  decf="${f/_base64/}"
  base64 -D <"$f" > "$decf"
  rm "$f"
  if [[ $(file --mime-type --brief "$decf") == "image/png" ]] ; then
    mv "$decf" "${decf%txt}png"
  fi
done

cat <<EOF
Saved unique data contents to $OUTDIR/data_<entry>.<type>. Check that all of them are sane.
'UAs_<entry>.txt' contain a list of the User-Agent which submitted the corresponding entry."
EOF
