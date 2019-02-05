#!/bin/bash
# Download Chromium builds from the official archives

OUTFILE="chromium-builds.txt"
REPO="snapshots"
TO_FECTH=() # fetch list of builds in that prefix
TO_DOWNLOAD=() # download prefix/build/chrome-<platform>.zip

function usage {
  cat <<EOF
Usage:
  ${BASH_SOURCE[0]} [<prefix> [<prefix> ...]] [<prefix>/<build> [<prefix>/<build> ...]] [-o <outfile>] [-r <repo>]

Will save to <outfile> a list of all builds under each <prefix> and download chrome-<platform>.zip for each <prefix>/<build>.
For versions <= 51 use -r continuous.
EOF
exit 1
}

[[ $# -eq 0 ]] && usage

while [[ $# -gt 0 ]] ; do
  case ${1} in
    -o)
      OUTFILE="${2}"
      shift
      ;;
    -r)
      REPO="${2}"
      shift
      ;;
    -*)
      echo "Unknown command '${1}'" 1>&2
      usage
      ;;
    *)
      IFS=/ read pref build <<<"${1}"
      if [[ ${pref//\//} != ${pref} || ${build//\//} != ${build} ]] ; then
        echo "Only one level of recursion suppored, give <prefix>/<build>" 1>&2
        exit 2
      fi
      if [[ -z ${build} ]] ; then
        TO_FETCH[${#TO_FETCH[@]}]="${pref}"
      else
        TO_DOWNLOAD[${#TO_DOWNLOAD[@]}]="${1}"
      fi
  esac
  shift
done

function fetch_builds {
  local prefix="${1}" page=1
  echo "Fetching builds under ${prefix}/"
  while true ; do
    echo "  Page ${page}"
    nextPageToken=$(http --ignore-stdin --print=b GET \
        "https://www.googleapis.com/storage/v1/b/chromium-browser-${REPO}/o" \
        delimiter==/ prefix==${prefix}/ fields==prefixes,nextPageToken \
        ${nextPageToken:+pageToken==${nextPageToken}} | \
          awk -v prefix="${prefix}" -v outfile="${OUTFILE}.tmp" '
    BEGIN { pref_regex="^ *\"(" prefix "/[0-9]+)/\",? *$" }
    /nextPageToken/ { print gensub(/^ *"nextPageToken": *"([^"]+)".*/, "\\1", "1") }
    /^ *\]/ { in_prefixes=0 }
    (in_prefixes) { print gensub(pref_regex, "\\1", "1") >> outfile }
    /^ *"prefixes": \[/ { in_prefixes=1 }'
    )
    [[ -z "${nextPageToken}" ]] && break
    page=$((page+1))
  done

  # append to OUTFILE
  cat "${OUTFILE}" >> "${OUTFILE}.tmp" 2>/dev/null
  sort -t/ -k2 -n "${OUTFILE}.tmp" > "${OUTFILE}"
  rm "${OUTFILE}.tmp"
}

function download_build {
  local prefix="${1}"
  mediaLink=$(http --ignore-stdin --print=b GET \
      "https://www.googleapis.com/storage/v1/b/chromium-browser-${REPO}/o" \
      delimiter==/ prefix==${prefix}/ fields=='items(mediaLink)' | \
        egrep -o 'https?://[^"]+chrome-[a-zA-Z0-9]+\.zip[^"]*')
  wget --continue "${mediaLink}" -O "${prefix//\//_}.zip"
}

for pref in "${TO_FETCH[@]}" ; do
  fetch_builds "${pref}"
done

for pref in "${TO_DOWNLOAD[@]}" ; do
  download_build "${pref}"
done
