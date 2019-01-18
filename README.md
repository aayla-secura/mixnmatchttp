# Description

This is a simple multi-threaded wrapper around python's simple http server for CORS testing purposes. It can add custom headers including Access-Control-Allow-Origin: `<request origin>`. It can serve over SSL too.

CORS headers (Allow-Origins and Allow-Credentials) can also be controlled per request with the `origin` and `creds` URL parameters. If origin is `%%ECHO%%` it is taken from the Origin header in the request.

# CORS test

The html pages should work with older browser (not tested all yet).

  * `login.html`: sets the auth cookie and redirects to a URL given as the goto GET parameter or index.html
  * `secret.txt`: a dummy secret, accessible only if an 'auth=1' cookie is present
  * `getData.html`: fetches the requested resource (given in the `goto` URL parameter) with `withCredentials` set to True; it does GET unless the `post` URL parameter is true
  * `getSecret.html`: fetches `secret.txt` from the target host (given by the `host`, `hostname` or `port` URL parameters, see below) by loading `getData.html` in multiple iframes (see below for description)

### Running the server

`getSecret.html` will determine the target host using one of the following URL parameters, in this order of precedence:
  * `host`: gives the full hostname/IP address:port of the target
  * `hostname`: gives only the hostname/IP address of the target; the port number is the same as the origin
  * `port`: gives only the port number of the target; the hostname/IP address is the same as the origin

You therefore have these options for CORS testing:

1. Start the server on all interfaces (default):


```
python3 simple.py -S -l logs/requests.log
```

then visit:

```
https://<IP_1>:58081/getSecret.html?hostname=<IP_2>
```

replacing `<IP_1>` and `<IP_2>` with two different interfaces, e.g. `127.0.0.1` and `192.168.0.1`.

2. Alternatively, start it only on one interface:

```
python3 simple.py -S -a <IP> -l logs/requests.log
```

and use a DNS name which resolves to the interface's IP address:

```
https://<IP>:58081/getSecret.html?hostname=<hostname>
```

or:

```
https://<hostname>:58081/getSecret.html?hostname=<IP>
```

You can omit the hostname URL parameter if listening on `localhost` and `localhost` has the `127.0.0.1` address. `getSecret.html` will detect that and use `localhost` or `127.0.0.1` as the target domain (if the origin is `127.0.0.1` or `localhost` respectively).

3. Alternatively, run two different instances on one interface but different ports:

```
python3 simple.py -S -a <IP> -p 58081 -l logs/requests_58081.log
python3 simple.py -S -a <IP> -p 58082 -l logs/requests_58082.log
```

then visit:

```
https://<IP>:58081/getSecret.html?port=58082
```

### Viewing results, logging to file and parsing it

`getSecret.html` will log in to the target host (e.g. `<IP_2>` if running as described in option 1. and load 10 iframes, each of which will fetch `https://<target_host>/secret.txt?origin=...&creds=...` requesting one of the following 5 CORS combinations from the server, once using GET and once using POST methods:
  * Origin: `*` , Credentials: true
  * Origin: `*` , Credentials: false
  * Origin: `<as request origin>` , Credentials: true
  * Origin: `<as request origin>` , Credentials: false
  * no CORS headers

Results from the Ajax calls will be logged to the page; check the JS console for CORS security errors. Full requests from the browser will be logged to the logfile given by the `-l` option. To parse the script and print the results in a table do:

```
/parse_request_log.sh logs/requests.log logs/requests_result.md
```

# Usage

```
usage: simple.py [-h] [-a IP] [-p PORT] [-o [Origin [Origin ...]] | -O]
                 [-x [Header: Value [Header: Value ...]]]
                 [-m [Header: Value [Header: Value ...]]] [-c] [-C FILE]
                 [-K FILE] [-S] [-H [Header: Value [Header: Value ...]]]
                 [-l FILE] [-d]

Serve the current working directory over HTTPS and with custom headers. The
CORS related options (-o and -c) define the default behaviour. It can be
overriden on a per-request basis using the origin and creds URL parameters.
creds should be 0 or 1. origin is taken literally unless it is `%%ECHO%%`,
then it is taken from the Origin header in the request.

optional arguments:
  -h, --help            show this help message and exit

Listen options:
  -a IP, --address IP   Address of interface to bind to. (default: 0.0.0.0)
  -p PORT, --port PORT  HTTP port to listen on. (default: 58081)

CORS options (requires -o or -O):
  -o [Origin [Origin ...]], --allowed-origins [Origin [Origin ...]]
                        Allowed origins for CORS requests. Can be "*"
                        (default: [])
  -O, --allow-all-origins
                        Allow all origins, i.e. echo the Origin in the
                        request. (default: None)
  -x [Header: Value [Header: Value ...]], --allowed-headers [Header: Value [Header: Value ...]]
                        Additional headers allowed for CORS requests.
                        (default: [])
  -m [Header: Value [Header: Value ...]], --allowed-methods [Header: Value [Header: Value ...]]
                        Additional methods allowed for CORS requests.
                        (default: [])
  -c, --allow-credentials
                        Allow sending credentials with CORS requests, i.e. add
                        Access-Control-Allow-Credentials. Using this only
                        makes sense if you are providing some list of origins
                        (see -o and -O options), otherwise this option is
                        ignored. (default: False)

SSL options:
  -C FILE, --cert FILE  PEM file containing the server certificate. (default:
                        ./cert.pem)
  -K FILE, --key FILE   PEM file containing the private key for the server
                        certificate. (default: ./key.pem)
  -S, --no-ssl          Don't use SSL. (default: True)

Misc options:
  -H [Header: Value [Header: Value ...]], --headers [Header: Value [Header: Value ...]]
                        Additional headers to include in the response.
                        (default: [])
  -l FILE, --logfile FILE
                        File to write requests to. Will write to stdout if not
                        given. (default: None)
  -d, --debug           Enable debugging output. (default: 20)
```
