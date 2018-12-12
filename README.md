# Description

This is a simple wrapper around python's simple http server for CORS testing purposes. It can add custom headers including Access-Control-Allow-Origin: `<request origin>`. It can serve over SSL too.

# Usage

```
simple.py [-h] [-a IP] [-p PORT] [-o "Allowed origins" | -O] [-c]
          [-H [Header: Value [Header: Value ...]]] [-C FILE] [-K FILE]
          [-S]

Serve the current working directory over HTTPS and with custom headers.

optional arguments:
  -h, --help            show this help message and exit
  -a IP, --address IP   Address of interface to bind to. (default: 0.0.0.0)
  -p PORT, --port PORT  HTTP port to listen on. (default: 58081)
  -o "Allowed origins", --origins "Allowed origins"
                        "*" or a coma-separated whitelist of origins.
                        (default: None)
  -O, --all-origins     Allow all origins, i.e. echo the Origin in the
                        request. (default: None)
  -c, --cors-credentials
                        Allow sending credentials with CORS requests, i.e. add
                        Access-Control-Allow-Credentials. Using this only
                        makes sense if you are providing some list of origins
                        (see -o and -O options), otherwise this option is
                        ignored. (default: False)
  -H [Header: Value [Header: Value ...]], --headers [Header: Value [Header: Value ...]]
                        Additional headers. (default: [])
  -C FILE, --cert FILE  PEM file containing the server certificate. (default:
                        ./cert.pem)
  -K FILE, --key FILE   PEM file containing the private key for the server
                        certificate. (default: ./key.pem)
  -S, --no-ssl          Don't use SSL. (default: True)
```

# CORS test

The html pages should work with older browser (not tested all yet).

  * login.html: sets the auth cookie and redirects to a URL given as the goto GET parameter or index.html
  * secret.txt: a dummy secret
  * getSecret.html: fetches secret.txt with withCredentials set to True from the hostname given as the host GET parameter

Start the server on all interfaces (default) and then visit

```
http://<ip 1>:58081/login.html?goto=http%3A%2F%2F<ip 2>%3A58081%2FgetSecret.html%3Fhost%3D<ip 1>
```

replacing `<ip 1>` and `<ip 2>` with two different interfaces, e.g. `127.0.0.1` and `192.168.0.1`.

Alternatively, start it only on one interface and use a DNS name which resolves to the interface's IP address.

You can omit the host parameter the goto URL if listening on `localhost` and `localhost` has the `127.0.0.1` address. `getSecret.html` will detect that and use `localhost` and `127.0.0.1` as `<ip 1>` and `<ip 2>` or the other way around.
