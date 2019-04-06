#!/bin/bash

which xxd >/dev/null && which http >/dev/null || exit 1

ANSI_RED=$'\e[31m'
ANSI_GREEN=$'\e[32m'
ANSI_YELLOW=$'\e[33m'
ANSI_BLUE=$'\e[34m'
ANSI_MAGENTA=$'\e[35m'
ANSI_CYAN=$'\e[36m'
ANSI_WHITE=$'\e[37m'
ANSI_BOLD=$'\e[1m'
ANSI_RESET=$'\e[0m'

ANSI_DEBUG="${ANSI_BLUE}"
ANSI_INFO="${ANSI_WHITE}"
ANSI_WARNING="${ANSI_YELLOW}${ANSI_BOLD}"
ANSI_ERROR="${ANSI_RED}${ANSI_BOLD}"
ANSI_PROMPT="${ANSI_CYAN}"

DEBUG=3
INFO=2
WARNING=1
ERROR=0
PROMPT=-1   # always print
VERBOSITY=2 # max level printed
PYVER=2     # default guess is server runs python2

SESSION=$(xxd -p -l 10 </dev/urandom)
HOST='http://localhost:58080'
TESTS_ALL=(auth proxy cache endpoints templates misc)

############################################################
######################### TESTS ############################
############################################################
function test_auth {
  log INFO "-------------------- AUTHENTICATION TESTS --------------------"
  req -eh "^HTTP/1\.[01] 401" GET /secret/ # no cookie
  req -eh "^HTTP/1\.[01] 401" GET /topsecret/
  req -eh "^HTTP/1\.[01] 401" GET /foo/secret/
  req -eh "^HTTP/1\.[01] 200" GET /foo/topsecret/ # /topsecret is not relative

  req -i -w -eh "^Set-Cookie: *SESSION=[a-f0-9]" GET /dummylogin
  req -eb "This is do_GET for  @  \(\)" GET /secret/

  req -i -eh "^Set-Cookie: *SESSION=[^\w]" \
    GET /logout # should clear the session on the server, but not in client,
                # since session is read-only here
  req -eh "^HTTP/1\.[01] 401" GET /secret/ # old cookie, should be invalid

  req -i -w -eh "^Set-Cookie: *SESSION=[a-f0-9]" GET /dummylogin # re-login
  req -eb "This is do_GET for  @  \(\)" GET /secret/
  req -i -eh "^Set-Cookie: *SESSION=[a-f0-9]" \
    GET /dummylogin # re-login should clear the old cookie (set above) do not
                    # remember the new one
  req -eh "^HTTP/1\.[01] 401" \
    GET /secret/ # request secret with the old cookie, should fail
  req -i -w -eh "^Set-Cookie: *SESSION=[^\w]" GET /logout

  req -eh "^HTTP/1\.[01] 401" POST /login # no credentials
  req -eh "^HTTP/1\.[01] 401" GET /secret/ # old cookie, should be invalid
  req -w -eh "^HTTP/1\.[01] 401" POST /login
  req -eh "^HTTP/1\.[01] 401" GET /secret/
  req -w -eh "^HTTP/1\.[01] 401" POST /login username=foo # no password
  req -eh "^HTTP/1\.[01] 401" GET /secret/
  req -w -eh "^HTTP/1\.[01] 401" \
    POST /login username=bla password= # user has no password,
                                       # should not have been created
  req -w -eh "^HTTP/1\.[01] 401" POST /login username=baz password= # as above
  req -w -eh "^HTTP/1\.[01] 401" \
    POST /login username=foobar # user has weak password,
                                # should not have been created

  req -i -w -eh "^Set-Cookie: *SESSION=[a-f0-9]" \
    POST /login username=foo password=bar
  req -eb "This is do_GET for  @  \(\)" GET /secret/
  req -i -w -eh "^Set-Cookie: *SESSION=[a-f0-9]" -f \
    POST /login username=foo password=bar
  req -eb "This is do_GET for  @  \(\)" GET /secret/

  req -w -eh "^HTTP/1\.[01] 401" \
    POST /changepwd username=foo new_password=barbaz
  req -i -w -eh "^Set-Cookie: *SESSION=[a-f0-9]" \
    POST /changepwd username=foo password=bar new_password=barbaz
  req -i -w -eh "^Set-Cookie: *SESSION=[a-f0-9]" -f \
    POST /changepwd username=foo password=barbaz new_password=foobar
  req -i -w -eh "^Set-Cookie: *SESSION=[a-f0-9]" \
    POST /changepwd username=foo password=foobar new_password=foobaz
  req -w -eh "^HTTP/1\.[01] 401" \
    POST /login username=foo password=bar # old password
  req POST /changepwd username=foo password=foobaz new_password=bar
}

############################################################
function test_proxy {
  log INFO "-------------------- PROXY TESTS --------------------"
  req -eh "^HTTP/1\.[01] 200" GET /goto/foo # no host given
  req -eh "^HTTP/1\.[01] 200" GET /goto//foo # no host given
  req -i -eh "^Location: *//foo" GET /goto///foo
  req -eh "^HTTP/1\.[01] 200" GET /goto/foo # no host given
  req -eh "^HTTP/1\.[01] 200" GET /goto/foo 'Referer: foobar' # invalid Referer
  req -i -eh "^Location: *//foobar/foo" GET /goto/foo 'Referer: //foobar'
  req -i -eh "^Location: *//foobar/bar/foo" GET /goto/foo 'Referer: //foobar/bar'
  req -i -eh "^Location: *//foobar/foo" GET /goto//foo 'Referer: //foobar/bar'
  req -i -eh "^Location: *http://foobar/foo" GET /goto//foo 'Referer: http://foobar/bar'
  req -i -eh "^Location: *http://foobar/foo" GET /goto/foo 'Origin: http://foobar'
  req -i -eh "^Location: *//foobar/foo" GET /goto/foo 'Origin: //foobar'
  req -i -eh "^Location: *//foobar/foo" GET /goto/foo 'X-Forwarded-Host: foobar'
  req -i -eh "^Location: *//foobar/foo" GET /goto/foo 'X-Forwarded-For: foobar'
  req -i -eh "^Location: *//foobar/../foo" GET /goto/../foo 'Referer: //foobar'
}

############################################################
function test_cache {
  log INFO "-------------------- CACHE TESTS --------------------"
  req -eh "^HTTP/1\.[01] 500" \
    -3eb "Error code explanation: 500 - This page has not been cached yet" \
    GET /cache/"${SESSION}" # SESSION will do as it's re-generated each time the script is run
  req -eh "^HTTP/1\.[01] 400" \
    -3eb "Error code explanation: 400 - Cannot load parameters from request" \
    -f POST /cache/"${SESSION}"
  req -eh "^HTTP/1\.[01] 400" \
    -3eb "Error code explanation: 400 - Cannot load parameters from request" \
    -f POST /echo
  req -eh "^HTTP/1\.[01] 400" \
    -3eb "Error code explanation: 400 - No \"data\" parameter present" \
    -f POST /cache/"${SESSION}" type="text/plain"
  req -eh "^HTTP/1\.[01] 400" \
    -3eb "Error code explanation: 400 - No \"data\" parameter present" \
    -f POST /echo type="text/plain"

  req -eh "^HTTP/1\.[01] 204" \
    -f POST /cache/"${SESSION}" data=foo type="text/foo" # invalid type should default to text/plain
  req -i -eh "^HTTP/1\.[01] 200" -eh "Content-Type: *text/plain" -eb "foo" \
    GET /cache/"${SESSION}"
  req -i -eh "^HTTP/1\.[01] 200" -eh "Content-Type: *text/plain" -eb "foo" \
    -f POST /echo data=foo type="text/foo"

  req -eh "^HTTP/1\.[01] 500" \
    -3eb "Error code explanation: 500 - Cannot overwrite page, choose a different name" \
    -f POST /cache/"${SESSION}" data=bar type="text/foo"
  req -eb "foo" \
    GET /cache/"${SESSION}" # data should not have been overwritten

  req -eh "^HTTP/1\.[01] 204" \
    -f POST /cache/"${SESSION}.2" data=foo type="text/html"
  req -i -eh "^Content-Type: *text/html" \
    GET /cache/"${SESSION}.2"
  req -i -eh "^Content-Type: *text/html" \
    -f POST /echo data=foo type="text/html"
  req -eh "^HTTP/1\.[01] 400" \
    -3eb "Error code explanation: 400 - Cannot Base64 decode request data" \
    POST /echo data=foo type="text/html" # send it as JSON, but not encoded
}

############################################################
function test_endpoints {
  log INFO "-------------------- MISC ENDPOINTS TESTS --------------------"
  req -eh "^HTTP/1\.[01] 404" \
    -3eb "Error code explanation: 404 - Extra arguments: foo" \
    GET /test/foo
  req -eh "^HTTP/1\.[01] 404" \
    -3eb "Error code explanation: 404 - Missing required argument" \
    POST /test/post_one
  req -eh "^HTTP/1\.[01] 404" \
    -3eb "Error code explanation: 404 - Extra arguments: bar" \
    POST /test/post_one/foo/bar
  req -eh "^HTTP/1\.[01] 404" \
    -3eb "Error code explanation: 404 - Missing required argument" \
    GET /test/get_req
  req -eh "^HTTP/1\.[01] 404" \
    -3eb "Error code explanation: 404 - Missing required argument" \
    GET /test/get_req/
  req -eh "^HTTP/1\.[01] 404" \
    -3eb "Error code explanation: 404 - Extra arguments: bar" \
    GET /test/get_opt/foo/bar

  req -i -eh "^HTTP/1\.[01] 405" -eh "^Allow:" \
    -3eb "Error code explanation: 405 - Specified method is invalid for this resource" \
    GET /test/post_one/foo
  req -i -eh "^HTTP/1\.[01] 405" -eh "^Allow:" \
    -3eb "Error code explanation: 405 - Specified method is invalid for this resource" \
    POST /test/get_opt/foo
  req -i -eh "^HTTP/1\.[01] 200" -eh "^Content-Length: *0" -eh "^Allow:" \
    OPTIONS /test/post_one/foo

  req -eb "This is do_GET for  @  \(\)" GET /
  req -eb "This is do_deep for /deep @  \(\)" GET /deep/
  req -eb "This is do_deep for /deep @ 1 \(\)" GET /deep/1
  req -eb "This is do_deep for /deep @ 1/2 \(\)" GET /deep/1/2
  req -eb "This is do_deep for /deep @ 1/2/3 \(\)" GET /deep/1/2/3
  req -eb "This is do_deep_1_2_4 for /deep/1/2/4 @  \(\)" GET /deep/1/2/4
  req -eb "This is do_default for  @ test \(\)" GET /test/
  req -eb "This is do_default for  @ test \(\)" GET /a/../test/
  req -eb "This is do_default for  @ test \(\)" GET /test/a/../
  req -eb "This is do_default for  @ test/post_one \(foo\)" POST /test/post_one/foo
  req -eb "This is do_default for  @ test/post_one \(foo\)" POST /test/post_one/a/../foo
  req -eb "This is do_default for  @ test/get_opt \(\)" GET /test/get_opt
  req -eb "This is do_default for  @ test/get_opt \(\)" GET /test/get_opt/
  req -eb "This is do_default for  @ test/get_opt \(foo\)" GET /test/get_opt/foo
  req -eb "This is do_default for  @ test/get_any \(\)" GET /test/get_any/
  req -eb "This is do_default for  @ test/get_any \(foo/bar/baz\)" GET /test/get_any/foo/bar/baz
  req -eb "This is do_default for  @ test/get_req \(foo/bar/baz\)" GET /test/get_req/foo/bar/baz

  req -i -eh "^X-Mod: *Test" \
    GET /modtest # modifies the default subpoint for /test to require 1 arg
  req -eh "^HTTP/1\.[01] 404" \
    -3eb "Error code explanation: 404 - Extra arguments: foo" \
    GET /test/foo # should not take effect, i.e. it should still accept no args as before
}

############################################################
function test_templates {
  log INFO "-------------------- TEMPLATES TESTS --------------------"
  req -eb "This is do_default for  @ test \(\)" GET /test/
  req -eb "This is do_GET for  @  \(\)" GET /foo/
}

############################################################
function test_misc {
  log INFO "-------------------- MISC TESTS --------------------"
  req -eh "^HTTP/1\.[01] 403" -eh "^X-Foo: Foo" GET /forbidden/
  req -i -eh "^Cache-Control: *no-cache, *no-store, *must-revalidate" GET /foo
  req -i -uh "^Cache-Control: *no-cache, *no-store, *must-revalidate" GET /foo.js

  req -eb "This is do_default for  @ test \(\)" GET //test/
  req -eb "This is do_default for  @ test \(\)" GET /foo/../test/
  req -eb "This is do_default for  @ test \(\)" GET /foo%2f../test/
  req -i -eh "^Location: *//foo\?bar" GET /foo%2f%2e.%2fgoto%2f//foo%3fbar?baz
}

############################################################
######################## HELPERS ###########################
############################################################
function print {
  local level="${1}" msg="${2}" color="ANSI_${level}"
  [[ "${!level}" -le "${VERBOSITY}" ]] || return
  echo -ne "${!color}${msg}${ANSI_RESET}"
}

function log {
  local level="${1}" msg="${2}" spaces="     "
  print "${level}" "${level}: ${spaces:0:$((7 - ${#level}))}${msg}\n"
}

function req {
  local ignorecase=0 expected_hb="" expected_h="" expected_b="" \
    unexpected_hb="" unexpected_h="" unexpected_b="" \
    httpargs=() pathset=0 sesstype="--session-read-only" printtype
  while [[ $# -gt 0 ]] ; do
    case "$1" in
      -e|-eh|-eb|-u|-uh|-ub|-2e|-2eh|-2eb|-2u|-2uh|-2ub|-3e|-3eh|-3eb|-3u|-3uh|-3ub)
        # match regex $2 in whole response (-e), headers only (-eh) or body only (-eb)
        # must not match regex $2 in whole response (-u), headers only (-uh) or body only (-ub)
        # if preceded by 2 or 3 only match if the server is running this python version
        opt="${1:1}"
        ver="${PYVER}"
        if [[ "${opt:0:1}" =~ ^[23] ]] ; then
          ver="${opt:0:1}"
          opt="${opt:1}"
        fi
        if [[ "${ver}" -eq "${PYVER}" ]] ; then
          matchtype="${opt:0:1}"
          [[ "${matchtype}" == "e" ]] && matchtype="" || matchtype="un"
          currprinttype="${opt:1}"
          [[ -z "${currprinttype}" ]] && currprinttype="hb"
          currvar_n="${matchtype}expected_${currprinttype}"
          log DEBUG "Adding '$2' to ${currvar_n}"
          typeset "${currvar_n}=${!currvar_n:+${!currvar_n}\n}$2"
          printtype="${printtype/${currprinttype}/}${currprinttype}"
        else
          log DEBUG "Skipping '$2' for python${PYVER}"
        fi
        shift
        ;;
      -i)
        ignorecase=1
        ;;
      -w)
        # save cookies and request headers
        sesstype="--session"
        ;;
      -*)
        httpargs=("${httpargs[@]}" "$1")
        ;;
      *)
        arg="$1"
        if [[ ! "${arg}" =~ ^(GET|HEAD|POST|PUT|PATCH|DELETE|OPTIONS|TRACE)$ && ${pathset} -eq 0 ]] ; then
          arg="${HOST}${arg}" # prepend HOST to path
          pathset=1
        fi
        httpargs=("${httpargs[@]}" "${arg}")
        ;;
    esac
    shift
  done
  log DEBUG "----------"
  log INFO "http --print="${printtype}" "${sesstype}" '${SESSION}' ${httpargs[*]}"
  log DEBUG "Looking for the following lines in the response:\nHEADERS:\n${expected_h}\nBODY:\n${expected_b}\nANY:\n${expected_hb}"
  resp=$(http --print=hb "${sesstype}" "${SESSION}" "${httpargs[@]}")
  log DEBUG "${resp}"
  matchres=$(echo -n "${resp}" | awk \
    -v IGNORECASE="${ignorecase}" \
    -v exp_hb="${expected_hb//\\/\\\\}" \
    -v exp_h="${expected_h//\\/\\\\}" \
    -v exp_b="${expected_b//\\/\\\\}" \
    -v unexp_hb="${unexpected_hb//\\/\\\\}" \
    -v unexp_h="${unexpected_h//\\/\\\\}" \
    -v unexp_b="${unexpected_b//\\/\\\\}" \
    '
BEGIN {
  split(exp_hb, exp_hb_arr, "\\\\n")
  split(exp_h, exp_h_arr, "\\\\n")
  split(exp_b, exp_b_arr, "\\\\n")
  split(unexp_hb, unexp_hb_arr, "\\\\n")
  split(unexp_h, unexp_h_arr, "\\\\n")
  split(unexp_b, unexp_b_arr, "\\\\n")
  # for (e in exp_hb_arr) { print "XXX " e " " exp_hb_arr[e] }
  # for (e in exp_h_arr) { print "XXX " e " " exp_h_arr[e] }
  # for (e in exp_b_arr) { print "XXX " e " " exp_b_arr[e] }
  # for (e in unexp_hb_arr) { print "XXX un" e " " unexp_hb_arr[e] }
  # for (e in unexp_h_arr) { print "XXX un" e " " unexp_h_arr[e] }
  # for (e in unexp_b_arr) { print "XXX un" e " " unexp_b_arr[e] }
  delete unexp[0] # declare unexp as an array
}
/^\r$/ { inside_body=1 }
{
  for (e in exp_hb_arr) {
    # print "XXX matching " $0 " against " exp_hb_arr[e]
    if ($0 ~ exp_hb_arr[e]) {
      # print "XXX match!"
      delete exp_hb_arr[e]
    }
  }
  for (e in unexp_hb_arr) {
    # print "XXX neg matching " $0 " against " unexp_hb_arr[e]
    if ($0 ~ unexp_hb_arr[e]) {
      # print "XXX match!"
      unexp[length(unexp)+1]=unexp_hb_arr[e]
    }
  }
  if (inside_body) {
    for (e in exp_b_arr) {
      # print "XXX matching " $0 " against " exp_b_arr[e]
      if ($0 ~ exp_b_arr[e]) {
        # print "XXX match!"
        delete exp_b_arr[e]
      }
    }
    for (e in unexp_b_arr) {
      # print "XXX neg matching " $0 " against " unexp_b_arr[e]
      if ($0 ~ unexp_b_arr[e]) {
        # print "XXX match!"
        unexp[length(unexp)+1]=unexp_b_arr[e]
      }
    }
  } else {
    for (e in exp_h_arr) {
      # print "XXX matching " $0 " against " exp_h_arr[e]
      if ($0 ~ exp_h_arr[e]) {
        # print "XXX match!"
        delete exp_h_arr[e]
      }
    }
    for (e in unexp_h_arr) {
      # print "XXX neg matching " $0 " against " unexp_h_arr[e]
      if ($0 ~ unexp_h_arr[e]) {
        # print "XXX match!"
        unexp[length(unexp)+1]=unexp_h_arr[e]
      }
    }
  }
}
END {
  for (e in exp_hb_arr) { print "Did not match: " exp_hb_arr[e] }
  for (e in exp_h_arr) { print "Did not match: " exp_h_arr[e] }
  for (e in exp_b_arr) { print "Did not match: " exp_b_arr[e] }
  for (e in unexp) { print "Matched: " unexp[e] }
  if ( length(exp_hb_arr) || length(exp_h_arr) || length(exp_b_arr) || length(unexp) ) { exit 1 }
}')

  if [[ $? -ne 0 ]] ; then
    log WARNING "Unexpected response to '${httpargs[*]}':\n${matchres}"
    # exit 2
  fi
  # log DEBUG "XXX ${matchres}"
}

function join {
  local IFS="$1"
  shift
  echo -n "$*"
}

function is_valid_test {
  local t="$1" re=$(join "|" "${TESTS_ALL[@]}")
  [[ "$t" =~ ^($re)$ ]] && return 0 || return 1
}

############################################################
########################## MAIN ############################
############################################################
while [[ $# -gt 0 ]] ; do
  case "$1" in
    -d)
      VERBOSITY="${DEBUG}"
      ;;
    -H)
      HOST="$2"
      shift
      ;;
    -t)
      [[ "${TESTS-x}" == "x" ]] && TESTS=()
      TESTS=("${TESTS[@]}" "$2")
      shift
      ;;
    -2|-3)
      PYVER="${1:1:1}"
      ;;
    -*)
      log ERROR "Unknown option '$1'"
      exit 1
      ;;
    *)
      log ERROR "Unknown argument '$1'"
      exit 1
      ;;
  esac
  shift
done

if [[ "${TESTS-x}" == "x" ]] ; then
  TESTS=("${TESTS_ALL[@]}")
fi

log INFO "Assuming server runs python${PYVER}"
for t in "${TESTS[@]}" ; do
  if ! is_valid_test "$t"; then
    log ERROR "Invalid test '$t'"
    continue
  fi
  test_"$t"
done
