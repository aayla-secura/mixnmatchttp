| BROWSER              | METHOD                 | ORIGIN      | CREDENTIALS | PREFLIGHT       | COOKIE      | READ BY JS  |
| :------------------: | :--------------------: | :---------: | :---------: | :-------------: | :---------: | :---------: |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 0.2.150.0     | GET (via 2DCanvas)     |             | 0           |                 | Y           |             |
| Chrome 0.2.150.0     | GET (via BitmapCanvas) |             | 0           |                 | Y           |             |
| Chrome 0.2.150.0     | GET (via Iframe)       |             | 0           |                 | Y           |             |
| Chrome 0.2.150.0     | GET (via Object)       |             | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 0.2.150.0     | GET (via 2DCanvas)     | *           | 1           |                 | Y           |             |
| Chrome 0.2.150.0     | GET (via BitmapCanvas) | *           | 1           |                 | Y           |             |
| Chrome 0.2.150.0     | GET (via Iframe)       | *           | 1           |                 | Y           |             |
| Chrome 0.2.150.0     | GET (via Object)       | *           | 1           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 0.2.150.0     | GET (via 2DCanvas)     | *           | 0           |                 | Y           |             |
| Chrome 0.2.150.0     | GET (via BitmapCanvas) | *           | 0           |                 | Y           |             |
| Chrome 0.2.150.0     | GET (via Iframe)       | *           | 0           |                 | Y           |             |
| Chrome 0.2.150.0     | GET (via Object)       | *           | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 0.2.150.0     | GET (via 2DCanvas)     | {ECHO}      | 1           |                 | Y           |             |
| Chrome 0.2.150.0     | GET (via BitmapCanvas) | {ECHO}      | 1           |                 | Y           |             |
| Chrome 0.2.150.0     | GET (via Iframe)       | {ECHO}      | 1           |                 | Y           |             |
| Chrome 0.2.150.0     | GET (via Object)       | {ECHO}      | 1           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 0.2.150.0     | GET (via 2DCanvas)     | {ECHO}      | 0           |                 | Y           |             |
| Chrome 0.2.150.0     | GET (via BitmapCanvas) | {ECHO}      | 0           |                 | Y           |             |
| Chrome 0.2.150.0     | GET (via Iframe)       | {ECHO}      | 0           |                 | Y           |             |
| Chrome 0.2.150.0     | GET (via Object)       | {ECHO}      | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 0.3.155.0     | GET (via 2DCanvas)     |             | 0           |                 | Y           |             |
| Chrome 0.3.155.0     | GET (via BitmapCanvas) |             | 0           |                 | Y           |             |
| Chrome 0.3.155.0     | GET (via Iframe)       |             | 0           |                 | Y           |             |
| Chrome 0.3.155.0     | GET (via Object)       |             | 0           |                 | Y           |             |
| Chrome 0.3.155.0     | GET (via XHR)          |             | 0           |                 | Y           |             |
| Chrome 0.3.155.0     | POST (via XHR)         |             | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 0.3.155.0     | GET (via 2DCanvas)     | *           | 1           |                 | Y           |             |
| Chrome 0.3.155.0     | GET (via BitmapCanvas) | *           | 1           |                 | Y           |             |
| Chrome 0.3.155.0     | GET (via Iframe)       | *           | 1           |                 | Y           |             |
| Chrome 0.3.155.0     | GET (via Object)       | *           | 1           |                 | Y           |             |
| Chrome 0.3.155.0     | GET (via XHR)          | *           | 1           |                 | Y           |             |
| Chrome 0.3.155.0     | POST (via XHR)         | *           | 1           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 0.3.155.0     | GET (via 2DCanvas)     | *           | 0           |                 | Y           |             |
| Chrome 0.3.155.0     | GET (via BitmapCanvas) | *           | 0           |                 | Y           |             |
| Chrome 0.3.155.0     | GET (via Iframe)       | *           | 0           |                 | Y           |             |
| Chrome 0.3.155.0     | GET (via Object)       | *           | 0           |                 | Y           |             |
| Chrome 0.3.155.0     | GET (via XHR)          | *           | 0           |                 | Y           |             |
| Chrome 0.3.155.0     | POST (via XHR)         | *           | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 0.3.155.0     | GET (via 2DCanvas)     | {ECHO}      | 1           |                 | Y           |             |
| Chrome 0.3.155.0     | GET (via BitmapCanvas) | {ECHO}      | 1           |                 | Y           |             |
| Chrome 0.3.155.0     | GET (via Iframe)       | {ECHO}      | 1           |                 | Y           |             |
| Chrome 0.3.155.0     | GET (via Object)       | {ECHO}      | 1           |                 | Y           |             |
| Chrome 0.3.155.0     | GET (via XHR)          | {ECHO}      | 1           |                 | Y           |             |
| Chrome 0.3.155.0     | POST (via XHR)         | {ECHO}      | 1           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 0.3.155.0     | GET (via 2DCanvas)     | {ECHO}      | 0           |                 | Y           |             |
| Chrome 0.3.155.0     | GET (via BitmapCanvas) | {ECHO}      | 0           |                 | Y           |             |
| Chrome 0.3.155.0     | GET (via Iframe)       | {ECHO}      | 0           |                 | Y           |             |
| Chrome 0.3.155.0     | GET (via Object)       | {ECHO}      | 0           |                 | Y           |             |
| Chrome 0.3.155.0     | GET (via XHR)          | {ECHO}      | 0           |                 | Y           |             |
| Chrome 0.3.155.0     | POST (via XHR)         | {ECHO}      | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 0.5.155.0     | GET (via 2DCanvas)     |             | 0           |                 | Y           |             |
| Chrome 0.5.155.0     | GET (via BitmapCanvas) |             | 0           |                 | Y           |             |
| Chrome 0.5.155.0     | GET (via Iframe)       |             | 0           |                 | Y           |             |
| Chrome 0.5.155.0     | GET (via Object)       |             | 0           |                 | Y           |             |
| Chrome 0.5.155.0     | POST (via XHR)         |             | 0           |                 | Y           |             |
| Chrome 0.5.155.0     | GET (via XHR)          |             | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 0.5.155.0     | GET (via 2DCanvas)     | *           | 1           |                 | Y           |             |
| Chrome 0.5.155.0     | GET (via BitmapCanvas) | *           | 1           |                 | Y           |             |
| Chrome 0.5.155.0     | GET (via Iframe)       | *           | 1           |                 | Y           |             |
| Chrome 0.5.155.0     | GET (via Object)       | *           | 1           |                 | Y           |             |
| Chrome 0.5.155.0     | GET (via XHR)          | *           | 1           |                 | Y           |             |
| Chrome 0.5.155.0     | POST (via XHR)         | *           | 1           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 0.5.155.0     | GET (via 2DCanvas)     | *           | 0           |                 | Y           |             |
| Chrome 0.5.155.0     | GET (via BitmapCanvas) | *           | 0           |                 | Y           |             |
| Chrome 0.5.155.0     | GET (via Iframe)       | *           | 0           |                 | Y           |             |
| Chrome 0.5.155.0     | GET (via Object)       | *           | 0           |                 | Y           |             |
| Chrome 0.5.155.0     | GET (via XHR)          | *           | 0           |                 | Y           |             |
| Chrome 0.5.155.0     | POST (via XHR)         | *           | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 0.5.155.0     | GET (via 2DCanvas)     | {ECHO}      | 1           |                 | Y           |             |
| Chrome 0.5.155.0     | GET (via BitmapCanvas) | {ECHO}      | 1           |                 | Y           |             |
| Chrome 0.5.155.0     | GET (via Iframe)       | {ECHO}      | 1           |                 | Y           |             |
| Chrome 0.5.155.0     | GET (via Object)       | {ECHO}      | 1           |                 | Y           |             |
| Chrome 0.5.155.0     | POST (via XHR)         | {ECHO}      | 1           |                 | Y           |             |
| Chrome 0.5.155.0     | GET (via XHR)          | {ECHO}      | 1           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 0.5.155.0     | GET (via 2DCanvas)     | {ECHO}      | 0           |                 | Y           |             |
| Chrome 0.5.155.0     | GET (via BitmapCanvas) | {ECHO}      | 0           |                 | Y           |             |
| Chrome 0.5.155.0     | GET (via Iframe)       | {ECHO}      | 0           |                 | Y           |             |
| Chrome 0.5.155.0     | GET (via Object)       | {ECHO}      | 0           |                 | Y           |             |
| Chrome 0.5.155.0     | POST (via XHR)         | {ECHO}      | 0           |                 | Y           |             |
| Chrome 0.5.155.0     | GET (via XHR)          | {ECHO}      | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 13.0.772.0    | GET (via 2DCanvas)     |             | 0           |                 | Y           |             |
| Chrome 13.0.772.0    | GET (via BitmapCanvas) |             | 0           |                 | Y           |             |
| Chrome 13.0.772.0    | GET (via Iframe)       |             | 0           |                 | Y           |             |
| Chrome 13.0.772.0    | GET (via Object)       |             | 0           |                 | Y           |             |
| Chrome 13.0.772.0    | GET (via XHR)          |             | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 13.0.772.0    | GET (via 2DCanvas)     | *           | 1           |                 | Y           |             |
| Chrome 13.0.772.0    | GET (via BitmapCanvas) | *           | 1           |                 | Y           |             |
| Chrome 13.0.772.0    | GET (via Iframe)       | *           | 1           |                 | Y           |             |
| Chrome 13.0.772.0    | GET (via Object)       | *           | 1           |                 | Y           |             |
| Chrome 13.0.772.0    | GET (via XHR)          | *           | 1           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 13.0.772.0    | GET (via 2DCanvas)     | *           | 0           |                 | Y           |             |
| Chrome 13.0.772.0    | GET (via BitmapCanvas) | *           | 0           |                 | Y           |             |
| Chrome 13.0.772.0    | GET (via Iframe)       | *           | 0           |                 | Y           |             |
| Chrome 13.0.772.0    | GET (via Object)       | *           | 0           |                 | Y           |             |
| Chrome 13.0.772.0    | GET (via XHR)          | *           | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 13.0.772.0    | GET (via 2DCanvas)     | {ECHO}      | 1           |                 | Y           |             |
| Chrome 13.0.772.0    | GET (via BitmapCanvas) | {ECHO}      | 1           |                 | Y           |             |
| Chrome 13.0.772.0    | GET (via Iframe)       | {ECHO}      | 1           |                 | Y           |             |
| Chrome 13.0.772.0    | GET (via Object)       | {ECHO}      | 1           |                 | Y           |             |
| Chrome 13.0.772.0    | GET (via XHR)          | {ECHO}      | 1           |                 | Y           | Y           |
| Chrome 13.0.772.0    | POST (via XHR)         | {ECHO}      | 1           | Y (with Cookie) | Y           | Y           |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 13.0.772.0    | GET (via 2DCanvas)     | {ECHO}      | 0           |                 | Y           |             |
| Chrome 13.0.772.0    | GET (via BitmapCanvas) | {ECHO}      | 0           |                 | Y           |             |
| Chrome 13.0.772.0    | GET (via Iframe)       | {ECHO}      | 0           |                 | Y           |             |
| Chrome 13.0.772.0    | GET (via Object)       | {ECHO}      | 0           |                 | Y           |             |
| Chrome 13.0.772.0    | GET (via XHR)          | {ECHO}      | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 16.0.906.0    | GET (via 2DCanvas)     |             | 0           |                 | Y           |             |
| Chrome 16.0.906.0    | GET (via BitmapCanvas) |             | 0           |                 | Y           |             |
| Chrome 16.0.906.0    | GET (via Iframe)       |             | 0           |                 | Y           |             |
| Chrome 16.0.906.0    | GET (via Object)       |             | 0           |                 | Y           |             |
| Chrome 16.0.906.0    | GET (via XHR)          |             | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 16.0.906.0    | GET (via 2DCanvas)     | *           | 1           |                 | Y           |             |
| Chrome 16.0.906.0    | GET (via BitmapCanvas) | *           | 1           |                 | Y           |             |
| Chrome 16.0.906.0    | GET (via Iframe)       | *           | 1           |                 | Y           |             |
| Chrome 16.0.906.0    | GET (via Object)       | *           | 1           |                 | Y           |             |
| Chrome 16.0.906.0    | GET (via XHR)          | *           | 1           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 16.0.906.0    | GET (via 2DCanvas)     | *           | 0           |                 | Y           |             |
| Chrome 16.0.906.0    | GET (via BitmapCanvas) | *           | 0           |                 | Y           |             |
| Chrome 16.0.906.0    | GET (via Iframe)       | *           | 0           |                 | Y           |             |
| Chrome 16.0.906.0    | GET (via Object)       | *           | 0           |                 | Y           |             |
| Chrome 16.0.906.0    | GET (via XHR)          | *           | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 16.0.906.0    | GET (via 2DCanvas)     | {ECHO}      | 1           |                 | Y           | Y           |
| Chrome 16.0.906.0    | GET (via BitmapCanvas) | {ECHO}      | 1           |                 | Y           |             |
| Chrome 16.0.906.0    | GET (via Iframe)       | {ECHO}      | 1           |                 | Y           |             |
| Chrome 16.0.906.0    | GET (via Object)       | {ECHO}      | 1           |                 | Y           |             |
| Chrome 16.0.906.0    | GET (via XHR)          | {ECHO}      | 1           |                 | Y           | Y           |
| Chrome 16.0.906.0    | POST (via XHR)         | {ECHO}      | 1           | Y (with Cookie) | Y           | Y           |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 16.0.906.0    | GET (via 2DCanvas)     | {ECHO}      | 0           |                 | Y           |             |
| Chrome 16.0.906.0    | GET (via BitmapCanvas) | {ECHO}      | 0           |                 | Y           |             |
| Chrome 16.0.906.0    | GET (via Iframe)       | {ECHO}      | 0           |                 | Y           |             |
| Chrome 16.0.906.0    | GET (via Object)       | {ECHO}      | 0           |                 | Y           |             |
| Chrome 16.0.906.0    | GET (via XHR)          | {ECHO}      | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 18.0.998.0    | GET (via 2DCanvas)     |             | 0           |                 | Y           |             |
| Chrome 18.0.998.0    | GET (via BitmapCanvas) |             | 0           |                 | Y           |             |
| Chrome 18.0.998.0    | GET (via Iframe)       |             | 0           |                 | Y           |             |
| Chrome 18.0.998.0    | GET (via Object)       |             | 0           |                 | Y           |             |
| Chrome 18.0.998.0    | GET (via XHR)          |             | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 18.0.998.0    | GET (via 2DCanvas)     | *           | 1           |                 | Y           |             |
| Chrome 18.0.998.0    | GET (via BitmapCanvas) | *           | 1           |                 | Y           |             |
| Chrome 18.0.998.0    | GET (via Iframe)       | *           | 1           |                 | Y           |             |
| Chrome 18.0.998.0    | GET (via Object)       | *           | 1           |                 | Y           |             |
| Chrome 18.0.998.0    | GET (via XHR)          | *           | 1           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 18.0.998.0    | GET (via 2DCanvas)     | *           | 0           |                 | Y           |             |
| Chrome 18.0.998.0    | GET (via BitmapCanvas) | *           | 0           |                 | Y           |             |
| Chrome 18.0.998.0    | GET (via Iframe)       | *           | 0           |                 | Y           |             |
| Chrome 18.0.998.0    | GET (via Object)       | *           | 0           |                 | Y           |             |
| Chrome 18.0.998.0    | GET (via XHR)          | *           | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 18.0.998.0    | GET (via 2DCanvas)     | {ECHO}      | 1           |                 | Y           | Y           |
| Chrome 18.0.998.0    | GET (via BitmapCanvas) | {ECHO}      | 1           |                 | Y           |             |
| Chrome 18.0.998.0    | GET (via Iframe)       | {ECHO}      | 1           |                 | Y           |             |
| Chrome 18.0.998.0    | GET (via Object)       | {ECHO}      | 1           |                 | Y           |             |
| Chrome 18.0.998.0    | POST (via XHR)         | {ECHO}      | 1           | Y (with Cookie) | Y           | Y           |
| Chrome 18.0.998.0    | GET (via XHR)          | {ECHO}      | 1           |                 | Y           | Y           |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 18.0.998.0    | GET (via 2DCanvas)     | {ECHO}      | 0           |                 | Y           |             |
| Chrome 18.0.998.0    | GET (via BitmapCanvas) | {ECHO}      | 0           |                 | Y           |             |
| Chrome 18.0.998.0    | GET (via Iframe)       | {ECHO}      | 0           |                 | Y           |             |
| Chrome 18.0.998.0    | GET (via Object)       | {ECHO}      | 0           |                 | Y           |             |
| Chrome 18.0.998.0    | GET (via XHR)          | {ECHO}      | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 18.0.999.0    | GET (via 2DCanvas)     |             | 0           |                 | Y           |             |
| Chrome 18.0.999.0    | GET (via BitmapCanvas) |             | 0           |                 | Y           |             |
| Chrome 18.0.999.0    | GET (via Iframe)       |             | 0           |                 | Y           |             |
| Chrome 18.0.999.0    | GET (via Object)       |             | 0           |                 | Y           |             |
| Chrome 18.0.999.0    | GET (via XHR)          |             | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 18.0.999.0    | GET (via 2DCanvas)     | *           | 1           |                 | Y           |             |
| Chrome 18.0.999.0    | GET (via BitmapCanvas) | *           | 1           |                 | Y           |             |
| Chrome 18.0.999.0    | GET (via Iframe)       | *           | 1           |                 | Y           |             |
| Chrome 18.0.999.0    | GET (via Object)       | *           | 1           |                 | Y           |             |
| Chrome 18.0.999.0    | GET (via XHR)          | *           | 1           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 18.0.999.0    | GET (via 2DCanvas)     | *           | 0           |                 | Y           |             |
| Chrome 18.0.999.0    | GET (via BitmapCanvas) | *           | 0           |                 | Y           |             |
| Chrome 18.0.999.0    | GET (via Iframe)       | *           | 0           |                 | Y           |             |
| Chrome 18.0.999.0    | GET (via Object)       | *           | 0           |                 | Y           |             |
| Chrome 18.0.999.0    | GET (via XHR)          | *           | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 18.0.999.0    | GET (via 2DCanvas)     | {ECHO}      | 1           |                 | Y           | Y           |
| Chrome 18.0.999.0    | GET (via BitmapCanvas) | {ECHO}      | 1           |                 | Y           |             |
| Chrome 18.0.999.0    | GET (via Iframe)       | {ECHO}      | 1           |                 | Y           |             |
| Chrome 18.0.999.0    | GET (via Object)       | {ECHO}      | 1           |                 | Y           |             |
| Chrome 18.0.999.0    | GET (via XHR)          | {ECHO}      | 1           |                 | Y           | Y           |
| Chrome 18.0.999.0    | POST (via XHR)         | {ECHO}      | 1           | Y (with Cookie) | Y           | Y           |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 18.0.999.0    | GET (via 2DCanvas)     | {ECHO}      | 0           |                 | Y           |             |
| Chrome 18.0.999.0    | GET (via BitmapCanvas) | {ECHO}      | 0           |                 | Y           |             |
| Chrome 18.0.999.0    | GET (via Iframe)       | {ECHO}      | 0           |                 | Y           |             |
| Chrome 18.0.999.0    | GET (via Object)       | {ECHO}      | 0           |                 | Y           |             |
| Chrome 18.0.999.0    | GET (via XHR)          | {ECHO}      | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 2.0.157.0     | GET (via 2DCanvas)     |             | 0           |                 | Y           |             |
| Chrome 2.0.157.0     | GET (via BitmapCanvas) |             | 0           |                 | Y           |             |
| Chrome 2.0.157.0     | GET (via Iframe)       |             | 0           |                 | Y           |             |
| Chrome 2.0.157.0     | GET (via Object)       |             | 0           |                 | Y           |             |
| Chrome 2.0.157.0     | GET (via XHR)          |             | 0           |                 | Y           |             |
| Chrome 2.0.157.0     | POST (via XHR)         |             | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 2.0.157.0     | GET (via 2DCanvas)     | *           | 1           |                 | Y           |             |
| Chrome 2.0.157.0     | GET (via BitmapCanvas) | *           | 1           |                 | Y           |             |
| Chrome 2.0.157.0     | GET (via Iframe)       | *           | 1           |                 | Y           |             |
| Chrome 2.0.157.0     | GET (via Object)       | *           | 1           |                 | Y           |             |
| Chrome 2.0.157.0     | GET (via XHR)          | *           | 1           |                 | Y           |             |
| Chrome 2.0.157.0     | POST (via XHR)         | *           | 1           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 2.0.157.0     | GET (via 2DCanvas)     | *           | 0           |                 | Y           |             |
| Chrome 2.0.157.0     | GET (via BitmapCanvas) | *           | 0           |                 | Y           |             |
| Chrome 2.0.157.0     | GET (via Iframe)       | *           | 0           |                 | Y           |             |
| Chrome 2.0.157.0     | GET (via Object)       | *           | 0           |                 | Y           |             |
| Chrome 2.0.157.0     | POST (via XHR)         | *           | 0           |                 | Y           |             |
| Chrome 2.0.157.0     | GET (via XHR)          | *           | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 2.0.157.0     | GET (via 2DCanvas)     | {ECHO}      | 1           |                 | Y           |             |
| Chrome 2.0.157.0     | GET (via BitmapCanvas) | {ECHO}      | 1           |                 | Y           |             |
| Chrome 2.0.157.0     | GET (via Iframe)       | {ECHO}      | 1           |                 | Y           |             |
| Chrome 2.0.157.0     | GET (via Object)       | {ECHO}      | 1           |                 | Y           |             |
| Chrome 2.0.157.0     | GET (via XHR)          | {ECHO}      | 1           |                 | Y           |             |
| Chrome 2.0.157.0     | POST (via XHR)         | {ECHO}      | 1           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 2.0.157.0     | GET (via 2DCanvas)     | {ECHO}      | 0           |                 | Y           |             |
| Chrome 2.0.157.0     | GET (via BitmapCanvas) | {ECHO}      | 0           |                 | Y           |             |
| Chrome 2.0.157.0     | GET (via Iframe)       | {ECHO}      | 0           |                 | Y           |             |
| Chrome 2.0.157.0     | GET (via Object)       | {ECHO}      | 0           |                 | Y           |             |
| Chrome 2.0.157.0     | GET (via XHR)          | {ECHO}      | 0           |                 | Y           |             |
| Chrome 2.0.157.0     | POST (via XHR)         | {ECHO}      | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 2.0.160.0     | GET (via 2DCanvas)     |             | 0           |                 | Y           |             |
| Chrome 2.0.160.0     | GET (via BitmapCanvas) |             | 0           |                 | Y           |             |
| Chrome 2.0.160.0     | GET (via Iframe)       |             | 0           |                 | Y           |             |
| Chrome 2.0.160.0     | GET (via Object)       |             | 0           |                 | Y           |             |
| Chrome 2.0.160.0     | POST (via XHR)         |             | 0           |                 | Y           |             |
| Chrome 2.0.160.0     | GET (via XHR)          |             | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 2.0.160.0     | GET (via 2DCanvas)     | *           | 1           |                 | Y           |             |
| Chrome 2.0.160.0     | GET (via BitmapCanvas) | *           | 1           |                 | Y           |             |
| Chrome 2.0.160.0     | GET (via Iframe)       | *           | 1           |                 | Y           |             |
| Chrome 2.0.160.0     | GET (via Object)       | *           | 1           |                 | Y           |             |
| Chrome 2.0.160.0     | GET (via XHR)          | *           | 1           |                 | Y           |             |
| Chrome 2.0.160.0     | POST (via XHR)         | *           | 1           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 2.0.160.0     | GET (via 2DCanvas)     | *           | 0           |                 | Y           |             |
| Chrome 2.0.160.0     | GET (via BitmapCanvas) | *           | 0           |                 | Y           |             |
| Chrome 2.0.160.0     | GET (via Iframe)       | *           | 0           |                 | Y           |             |
| Chrome 2.0.160.0     | GET (via Object)       | *           | 0           |                 | Y           |             |
| Chrome 2.0.160.0     | GET (via XHR)          | *           | 0           |                 | Y           |             |
| Chrome 2.0.160.0     | POST (via XHR)         | *           | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 2.0.160.0     | GET (via 2DCanvas)     | {ECHO}      | 1           |                 | Y           |             |
| Chrome 2.0.160.0     | GET (via BitmapCanvas) | {ECHO}      | 1           |                 | Y           |             |
| Chrome 2.0.160.0     | GET (via Iframe)       | {ECHO}      | 1           |                 | Y           |             |
| Chrome 2.0.160.0     | GET (via Object)       | {ECHO}      | 1           |                 | Y           |             |
| Chrome 2.0.160.0     | POST (via XHR)         | {ECHO}      | 1           |                 | Y           |             |
| Chrome 2.0.160.0     | GET (via XHR)          | {ECHO}      | 1           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 2.0.160.0     | GET (via 2DCanvas)     | {ECHO}      | 0           |                 | Y           |             |
| Chrome 2.0.160.0     | GET (via BitmapCanvas) | {ECHO}      | 0           |                 | Y           |             |
| Chrome 2.0.160.0     | GET (via Iframe)       | {ECHO}      | 0           |                 | Y           |             |
| Chrome 2.0.160.0     | GET (via Object)       | {ECHO}      | 0           |                 | Y           |             |
| Chrome 2.0.160.0     | POST (via XHR)         | {ECHO}      | 0           |                 | Y           |             |
| Chrome 2.0.160.0     | GET (via XHR)          | {ECHO}      | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 2.0.165.0     | GET (via 2DCanvas)     |             | 0           |                 | Y           |             |
| Chrome 2.0.165.0     | GET (via BitmapCanvas) |             | 0           |                 | Y           |             |
| Chrome 2.0.165.0     | GET (via Iframe)       |             | 0           |                 | Y           |             |
| Chrome 2.0.165.0     | GET (via Object)       |             | 0           |                 | Y           |             |
| Chrome 2.0.165.0     | GET (via XHR)          |             | 0           |                 | Y           |             |
| Chrome 2.0.165.0     | POST (via XHR)         |             | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 2.0.165.0     | GET (via 2DCanvas)     | *           | 1           |                 | Y           |             |
| Chrome 2.0.165.0     | GET (via BitmapCanvas) | *           | 1           |                 | Y           |             |
| Chrome 2.0.165.0     | GET (via Iframe)       | *           | 1           |                 | Y           |             |
| Chrome 2.0.165.0     | GET (via Object)       | *           | 1           |                 | Y           |             |
| Chrome 2.0.165.0     | GET (via XHR)          | *           | 1           |                 | Y           | Y           |
| Chrome 2.0.165.0     | POST (via XHR)         | *           | 1           |                 | Y           | Y           |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 2.0.165.0     | GET (via 2DCanvas)     | *           | 0           |                 | Y           |             |
| Chrome 2.0.165.0     | GET (via BitmapCanvas) | *           | 0           |                 | Y           |             |
| Chrome 2.0.165.0     | GET (via Iframe)       | *           | 0           |                 | Y           |             |
| Chrome 2.0.165.0     | GET (via Object)       | *           | 0           |                 | Y           |             |
| Chrome 2.0.165.0     | POST (via XHR)         | *           | 0           |                 | Y           | Y           |
| Chrome 2.0.165.0     | GET (via XHR)          | *           | 0           |                 | Y           | Y           |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 2.0.165.0     | GET (via 2DCanvas)     | {ECHO}      | 1           |                 | Y           |             |
| Chrome 2.0.165.0     | GET (via BitmapCanvas) | {ECHO}      | 1           |                 | Y           |             |
| Chrome 2.0.165.0     | GET (via Iframe)       | {ECHO}      | 1           |                 | Y           |             |
| Chrome 2.0.165.0     | GET (via Object)       | {ECHO}      | 1           |                 | Y           |             |
| Chrome 2.0.165.0     | POST (via XHR)         | {ECHO}      | 1           |                 | Y           | Y           |
| Chrome 2.0.165.0     | GET (via XHR)          | {ECHO}      | 1           |                 | Y           | Y           |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 2.0.165.0     | GET (via 2DCanvas)     | {ECHO}      | 0           |                 | Y           |             |
| Chrome 2.0.165.0     | GET (via BitmapCanvas) | {ECHO}      | 0           |                 | Y           |             |
| Chrome 2.0.165.0     | GET (via Iframe)       | {ECHO}      | 0           |                 | Y           |             |
| Chrome 2.0.165.0     | GET (via Object)       | {ECHO}      | 0           |                 | Y           |             |
| Chrome 2.0.165.0     | POST (via XHR)         | {ECHO}      | 0           |                 | Y           | Y           |
| Chrome 2.0.165.0     | GET (via XHR)          | {ECHO}      | 0           |                 | Y           | Y           |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 2.0.173.0     | GET (via 2DCanvas)     |             | 0           |                 | Y           |             |
| Chrome 2.0.173.0     | GET (via BitmapCanvas) |             | 0           |                 | Y           |             |
| Chrome 2.0.173.0     | GET (via Iframe)       |             | 0           |                 | Y           |             |
| Chrome 2.0.173.0     | GET (via Object)       |             | 0           |                 | Y           |             |
| Chrome 2.0.173.0     | GET (via XHR)          |             | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 2.0.173.0     | GET (via 2DCanvas)     | *           | 1           |                 | Y           |             |
| Chrome 2.0.173.0     | GET (via BitmapCanvas) | *           | 1           |                 | Y           |             |
| Chrome 2.0.173.0     | GET (via Iframe)       | *           | 1           |                 | Y           |             |
| Chrome 2.0.173.0     | GET (via Object)       | *           | 1           |                 | Y           |             |
| Chrome 2.0.173.0     | POST (via XHR)         | *           | 1           | Y (with Cookie) | Y           | Y           |
| Chrome 2.0.173.0     | GET (via XHR)          | *           | 1           |                 | Y           | Y           |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 2.0.173.0     | GET (via 2DCanvas)     | *           | 0           |                 | Y           |             |
| Chrome 2.0.173.0     | GET (via BitmapCanvas) | *           | 0           |                 | Y           |             |
| Chrome 2.0.173.0     | GET (via Iframe)       | *           | 0           |                 | Y           |             |
| Chrome 2.0.173.0     | GET (via Object)       | *           | 0           |                 | Y           |             |
| Chrome 2.0.173.0     | POST (via XHR)         | *           | 0           | Y (with Cookie) | Y           | Y           |
| Chrome 2.0.173.0     | GET (via XHR)          | *           | 0           |                 | Y           | Y           |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 2.0.173.0     | GET (via 2DCanvas)     | {ECHO}      | 1           |                 | Y           |             |
| Chrome 2.0.173.0     | GET (via BitmapCanvas) | {ECHO}      | 1           |                 | Y           |             |
| Chrome 2.0.173.0     | GET (via Iframe)       | {ECHO}      | 1           |                 | Y           |             |
| Chrome 2.0.173.0     | GET (via Object)       | {ECHO}      | 1           |                 | Y           |             |
| Chrome 2.0.173.0     | POST (via XHR)         | {ECHO}      | 1           | Y (with Cookie) | Y           | Y           |
| Chrome 2.0.173.0     | GET (via XHR)          | {ECHO}      | 1           |                 | Y           | Y           |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 2.0.173.0     | GET (via 2DCanvas)     | {ECHO}      | 0           |                 | Y           |             |
| Chrome 2.0.173.0     | GET (via BitmapCanvas) | {ECHO}      | 0           |                 | Y           |             |
| Chrome 2.0.173.0     | GET (via Iframe)       | {ECHO}      | 0           |                 | Y           |             |
| Chrome 2.0.173.0     | GET (via Object)       | {ECHO}      | 0           |                 | Y           |             |
| Chrome 2.0.173.0     | GET (via XHR)          | {ECHO}      | 0           |                 | Y           | Y           |
| Chrome 2.0.173.0     | POST (via XHR)         | {ECHO}      | 0           | Y (with Cookie) | Y           | Y           |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 2.0.178.0     | GET (via 2DCanvas)     |             | 0           |                 | Y           |             |
| Chrome 2.0.178.0     | GET (via BitmapCanvas) |             | 0           |                 | Y           |             |
| Chrome 2.0.178.0     | GET (via Iframe)       |             | 0           |                 | Y           |             |
| Chrome 2.0.178.0     | GET (via Object)       |             | 0           |                 | Y           |             |
| Chrome 2.0.178.0     | GET (via XHR)          |             | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 2.0.178.0     | GET (via 2DCanvas)     | *           | 1           |                 | Y           |             |
| Chrome 2.0.178.0     | GET (via BitmapCanvas) | *           | 1           |                 | Y           |             |
| Chrome 2.0.178.0     | GET (via Iframe)       | *           | 1           |                 | Y           |             |
| Chrome 2.0.178.0     | GET (via Object)       | *           | 1           |                 | Y           |             |
| Chrome 2.0.178.0     | GET (via XHR)          | *           | 1           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 2.0.178.0     | GET (via 2DCanvas)     | *           | 0           |                 | Y           |             |
| Chrome 2.0.178.0     | GET (via BitmapCanvas) | *           | 0           |                 | Y           |             |
| Chrome 2.0.178.0     | GET (via Iframe)       | *           | 0           |                 | Y           |             |
| Chrome 2.0.178.0     | GET (via Object)       | *           | 0           |                 | Y           |             |
| Chrome 2.0.178.0     | GET (via XHR)          | *           | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 2.0.178.0     | GET (via 2DCanvas)     | {ECHO}      | 1           |                 | Y           |             |
| Chrome 2.0.178.0     | GET (via BitmapCanvas) | {ECHO}      | 1           |                 | Y           |             |
| Chrome 2.0.178.0     | GET (via Iframe)       | {ECHO}      | 1           |                 | Y           |             |
| Chrome 2.0.178.0     | GET (via Object)       | {ECHO}      | 1           |                 | Y           |             |
| Chrome 2.0.178.0     | GET (via XHR)          | {ECHO}      | 1           |                 | Y           | Y           |
| Chrome 2.0.178.0     | POST (via XHR)         | {ECHO}      | 1           | Y (with Cookie) | Y           | Y           |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 2.0.178.0     | GET (via 2DCanvas)     | {ECHO}      | 0           |                 | Y           |             |
| Chrome 2.0.178.0     | GET (via BitmapCanvas) | {ECHO}      | 0           |                 | Y           |             |
| Chrome 2.0.178.0     | GET (via Iframe)       | {ECHO}      | 0           |                 | Y           |             |
| Chrome 2.0.178.0     | GET (via Object)       | {ECHO}      | 0           |                 | Y           |             |
| Chrome 2.0.178.0     | GET (via XHR)          | {ECHO}      | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 20.0.1103.0   | GET (via 2DCanvas)     |             | 0           |                 | Y           |             |
| Chrome 20.0.1103.0   | GET (via BitmapCanvas) |             | 0           |                 | Y           |             |
| Chrome 20.0.1103.0   | GET (via Iframe)       |             | 0           |                 | Y           |             |
| Chrome 20.0.1103.0   | GET (via Object)       |             | 0           |                 | Y           |             |
| Chrome 20.0.1103.0   | GET (via XHR)          |             | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 20.0.1103.0   | GET (via 2DCanvas)     | *           | 1           |                 | Y           |             |
| Chrome 20.0.1103.0   | GET (via BitmapCanvas) | *           | 1           |                 | Y           |             |
| Chrome 20.0.1103.0   | GET (via Iframe)       | *           | 1           |                 | Y           |             |
| Chrome 20.0.1103.0   | GET (via Object)       | *           | 1           |                 | Y           |             |
| Chrome 20.0.1103.0   | GET (via XHR)          | *           | 1           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 20.0.1103.0   | GET (via 2DCanvas)     | *           | 0           |                 | Y           |             |
| Chrome 20.0.1103.0   | GET (via BitmapCanvas) | *           | 0           |                 | Y           |             |
| Chrome 20.0.1103.0   | GET (via Iframe)       | *           | 0           |                 | Y           |             |
| Chrome 20.0.1103.0   | GET (via Object)       | *           | 0           |                 | Y           |             |
| Chrome 20.0.1103.0   | GET (via XHR)          | *           | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 20.0.1103.0   | GET (via 2DCanvas)     | {ECHO}      | 1           |                 | Y           | Y           |
| Chrome 20.0.1103.0   | GET (via BitmapCanvas) | {ECHO}      | 1           |                 | Y           |             |
| Chrome 20.0.1103.0   | GET (via Iframe)       | {ECHO}      | 1           |                 | Y           |             |
| Chrome 20.0.1103.0   | GET (via Object)       | {ECHO}      | 1           |                 | Y           |             |
| Chrome 20.0.1103.0   | POST (via XHR)         | {ECHO}      | 1           | Y               | Y           | Y           |
| Chrome 20.0.1103.0   | GET (via XHR)          | {ECHO}      | 1           |                 | Y           | Y           |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 20.0.1103.0   | GET (via 2DCanvas)     | {ECHO}      | 0           |                 | Y           |             |
| Chrome 20.0.1103.0   | GET (via BitmapCanvas) | {ECHO}      | 0           |                 | Y           |             |
| Chrome 20.0.1103.0   | GET (via Iframe)       | {ECHO}      | 0           |                 | Y           |             |
| Chrome 20.0.1103.0   | GET (via Object)       | {ECHO}      | 0           |                 | Y           |             |
| Chrome 20.0.1103.0   | GET (via XHR)          | {ECHO}      | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 21.0.1169.0   | GET (via 2DCanvas)     |             | 0           |                 | Y           |             |
| Chrome 21.0.1169.0   | GET (via BitmapCanvas) |             | 0           |                 | Y           |             |
| Chrome 21.0.1169.0   | GET (via Iframe)       |             | 0           |                 | Y           |             |
| Chrome 21.0.1169.0   | GET (via Object)       |             | 0           |                 | Y           |             |
| Chrome 21.0.1169.0   | GET (via XHR)          |             | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 21.0.1169.0   | GET (via 2DCanvas)     | *           | 1           |                 | Y           |             |
| Chrome 21.0.1169.0   | GET (via BitmapCanvas) | *           | 1           |                 | Y           |             |
| Chrome 21.0.1169.0   | GET (via Iframe)       | *           | 1           |                 | Y           |             |
| Chrome 21.0.1169.0   | GET (via Object)       | *           | 1           |                 | Y           |             |
| Chrome 21.0.1169.0   | GET (via XHR)          | *           | 1           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 21.0.1169.0   | GET (via 2DCanvas)     | *           | 0           |                 | Y           |             |
| Chrome 21.0.1169.0   | GET (via BitmapCanvas) | *           | 0           |                 | Y           |             |
| Chrome 21.0.1169.0   | GET (via Iframe)       | *           | 0           |                 | Y           |             |
| Chrome 21.0.1169.0   | GET (via Object)       | *           | 0           |                 | Y           |             |
| Chrome 21.0.1169.0   | GET (via XHR)          | *           | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 21.0.1169.0   | GET (via 2DCanvas)     | {ECHO}      | 1           |                 | Y           | Y           |
| Chrome 21.0.1169.0   | GET (via BitmapCanvas) | {ECHO}      | 1           |                 | Y           |             |
| Chrome 21.0.1169.0   | GET (via Iframe)       | {ECHO}      | 1           |                 | Y           |             |
| Chrome 21.0.1169.0   | GET (via Object)       | {ECHO}      | 1           |                 | Y           |             |
| Chrome 21.0.1169.0   | POST (via XHR)         | {ECHO}      | 1           | Y               | Y           | Y           |
| Chrome 21.0.1169.0   | GET (via XHR)          | {ECHO}      | 1           |                 | Y           | Y           |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 21.0.1169.0   | GET (via 2DCanvas)     | {ECHO}      | 0           |                 | Y           |             |
| Chrome 21.0.1169.0   | GET (via BitmapCanvas) | {ECHO}      | 0           |                 | Y           |             |
| Chrome 21.0.1169.0   | GET (via Iframe)       | {ECHO}      | 0           |                 | Y           |             |
| Chrome 21.0.1169.0   | GET (via Object)       | {ECHO}      | 0           |                 | Y           |             |
| Chrome 21.0.1169.0   | GET (via XHR)          | {ECHO}      | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 23.0.1232.0   | GET (via 2DCanvas)     |             | 0           |                 | Y           |             |
| Chrome 23.0.1232.0   | GET (via BitmapCanvas) |             | 0           |                 | Y           |             |
| Chrome 23.0.1232.0   | GET (via Iframe)       |             | 0           |                 | Y           |             |
| Chrome 23.0.1232.0   | GET (via Object)       |             | 0           |                 | Y           |             |
| Chrome 23.0.1232.0   | GET (via XHR)          |             | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 23.0.1232.0   | GET (via 2DCanvas)     | *           | 1           |                 | Y           |             |
| Chrome 23.0.1232.0   | GET (via BitmapCanvas) | *           | 1           |                 | Y           |             |
| Chrome 23.0.1232.0   | GET (via Iframe)       | *           | 1           |                 | Y           |             |
| Chrome 23.0.1232.0   | GET (via Object)       | *           | 1           |                 | Y           |             |
| Chrome 23.0.1232.0   | GET (via XHR)          | *           | 1           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 23.0.1232.0   | GET (via 2DCanvas)     | *           | 0           |                 | Y           |             |
| Chrome 23.0.1232.0   | GET (via BitmapCanvas) | *           | 0           |                 | Y           |             |
| Chrome 23.0.1232.0   | GET (via Iframe)       | *           | 0           |                 | Y           |             |
| Chrome 23.0.1232.0   | GET (via Object)       | *           | 0           |                 | Y           |             |
| Chrome 23.0.1232.0   | GET (via XHR)          | *           | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 23.0.1232.0   | GET (via 2DCanvas)     | {ECHO}      | 1           |                 | Y           | Y           |
| Chrome 23.0.1232.0   | GET (via BitmapCanvas) | {ECHO}      | 1           |                 | Y           |             |
| Chrome 23.0.1232.0   | GET (via Iframe)       | {ECHO}      | 1           |                 | Y           |             |
| Chrome 23.0.1232.0   | GET (via Object)       | {ECHO}      | 1           |                 | Y           |             |
| Chrome 23.0.1232.0   | POST (via XHR)         | {ECHO}      | 1           | Y               | Y           | Y           |
| Chrome 23.0.1232.0   | GET (via XHR)          | {ECHO}      | 1           |                 | Y           | Y           |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 23.0.1232.0   | GET (via 2DCanvas)     | {ECHO}      | 0           |                 | Y           |             |
| Chrome 23.0.1232.0   | GET (via BitmapCanvas) | {ECHO}      | 0           |                 | Y           |             |
| Chrome 23.0.1232.0   | GET (via Iframe)       | {ECHO}      | 0           |                 | Y           |             |
| Chrome 23.0.1232.0   | GET (via Object)       | {ECHO}      | 0           |                 | Y           |             |
| Chrome 23.0.1232.0   | GET (via XHR)          | {ECHO}      | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 24.0.1294.0   | GET (via 2DCanvas)     |             | 0           |                 | Y           |             |
| Chrome 24.0.1294.0   | GET (via BitmapCanvas) |             | 0           |                 | Y           |             |
| Chrome 24.0.1294.0   | GET (via Iframe)       |             | 0           |                 | Y           |             |
| Chrome 24.0.1294.0   | GET (via Object)       |             | 0           |                 | Y           |             |
| Chrome 24.0.1294.0   | GET (via XHR)          |             | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 24.0.1294.0   | GET (via 2DCanvas)     | *           | 1           |                 | Y           |             |
| Chrome 24.0.1294.0   | GET (via BitmapCanvas) | *           | 1           |                 | Y           |             |
| Chrome 24.0.1294.0   | GET (via Iframe)       | *           | 1           |                 | Y           |             |
| Chrome 24.0.1294.0   | GET (via Object)       | *           | 1           |                 | Y           |             |
| Chrome 24.0.1294.0   | GET (via XHR)          | *           | 1           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 24.0.1294.0   | GET (via 2DCanvas)     | *           | 0           |                 | Y           |             |
| Chrome 24.0.1294.0   | GET (via BitmapCanvas) | *           | 0           |                 | Y           |             |
| Chrome 24.0.1294.0   | GET (via Iframe)       | *           | 0           |                 | Y           |             |
| Chrome 24.0.1294.0   | GET (via Object)       | *           | 0           |                 | Y           |             |
| Chrome 24.0.1294.0   | GET (via XHR)          | *           | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 24.0.1294.0   | GET (via 2DCanvas)     | {ECHO}      | 1           |                 | Y           | Y           |
| Chrome 24.0.1294.0   | GET (via BitmapCanvas) | {ECHO}      | 1           |                 | Y           |             |
| Chrome 24.0.1294.0   | GET (via Iframe)       | {ECHO}      | 1           |                 | Y           |             |
| Chrome 24.0.1294.0   | GET (via Object)       | {ECHO}      | 1           |                 | Y           |             |
| Chrome 24.0.1294.0   | GET (via XHR)          | {ECHO}      | 1           |                 | Y           | Y           |
| Chrome 24.0.1294.0   | POST (via XHR)         | {ECHO}      | 1           | Y               | Y           | Y           |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 24.0.1294.0   | GET (via 2DCanvas)     | {ECHO}      | 0           |                 | Y           |             |
| Chrome 24.0.1294.0   | GET (via BitmapCanvas) | {ECHO}      | 0           |                 | Y           |             |
| Chrome 24.0.1294.0   | GET (via Iframe)       | {ECHO}      | 0           |                 | Y           |             |
| Chrome 24.0.1294.0   | GET (via Object)       | {ECHO}      | 0           |                 | Y           |             |
| Chrome 24.0.1294.0   | GET (via XHR)          | {ECHO}      | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 26.0.1401.0   | GET (via 2DCanvas)     |             | 0           |                 | Y           |             |
| Chrome 26.0.1401.0   | GET (via BitmapCanvas) |             | 0           |                 | Y           |             |
| Chrome 26.0.1401.0   | GET (via Iframe)       |             | 0           |                 | Y           |             |
| Chrome 26.0.1401.0   | GET (via Object)       |             | 0           |                 | Y           |             |
| Chrome 26.0.1401.0   | GET (via XHR)          |             | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 26.0.1401.0   | GET (via 2DCanvas)     | *           | 1           |                 | Y           |             |
| Chrome 26.0.1401.0   | GET (via BitmapCanvas) | *           | 1           |                 | Y           |             |
| Chrome 26.0.1401.0   | GET (via Iframe)       | *           | 1           |                 | Y           |             |
| Chrome 26.0.1401.0   | GET (via Object)       | *           | 1           |                 | Y           |             |
| Chrome 26.0.1401.0   | GET (via XHR)          | *           | 1           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 26.0.1401.0   | GET (via 2DCanvas)     | *           | 0           |                 | Y           |             |
| Chrome 26.0.1401.0   | GET (via BitmapCanvas) | *           | 0           |                 | Y           |             |
| Chrome 26.0.1401.0   | GET (via Iframe)       | *           | 0           |                 | Y           |             |
| Chrome 26.0.1401.0   | GET (via Object)       | *           | 0           |                 | Y           |             |
| Chrome 26.0.1401.0   | GET (via XHR)          | *           | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 26.0.1401.0   | GET (via 2DCanvas)     | {ECHO}      | 1           |                 | Y           | Y           |
| Chrome 26.0.1401.0   | GET (via BitmapCanvas) | {ECHO}      | 1           |                 | Y           |             |
| Chrome 26.0.1401.0   | GET (via Iframe)       | {ECHO}      | 1           |                 | Y           |             |
| Chrome 26.0.1401.0   | GET (via Object)       | {ECHO}      | 1           |                 | Y           |             |
| Chrome 26.0.1401.0   | POST (via XHR)         | {ECHO}      | 1           | Y               | Y           | Y           |
| Chrome 26.0.1401.0   | GET (via XHR)          | {ECHO}      | 1           |                 | Y           | Y           |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 26.0.1401.0   | GET (via 2DCanvas)     | {ECHO}      | 0           |                 | Y           |             |
| Chrome 26.0.1401.0   | GET (via BitmapCanvas) | {ECHO}      | 0           |                 | Y           |             |
| Chrome 26.0.1401.0   | GET (via Iframe)       | {ECHO}      | 0           |                 | Y           |             |
| Chrome 26.0.1401.0   | GET (via Object)       | {ECHO}      | 0           |                 | Y           |             |
| Chrome 26.0.1401.0   | GET (via XHR)          | {ECHO}      | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 29.0.1539.0   | GET (via 2DCanvas)     |             | 0           |                 | Y           |             |
| Chrome 29.0.1539.0   | GET (via BitmapCanvas) |             | 0           |                 | Y           |             |
| Chrome 29.0.1539.0   | GET (via Iframe)       |             | 0           |                 | Y           |             |
| Chrome 29.0.1539.0   | GET (via Object)       |             | 0           |                 | Y           |             |
| Chrome 29.0.1539.0   | GET (via XHR)          |             | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 29.0.1539.0   | GET (via 2DCanvas)     | *           | 1           |                 | Y           |             |
| Chrome 29.0.1539.0   | GET (via BitmapCanvas) | *           | 1           |                 | Y           |             |
| Chrome 29.0.1539.0   | GET (via Iframe)       | *           | 1           |                 | Y           |             |
| Chrome 29.0.1539.0   | GET (via Object)       | *           | 1           |                 | Y           |             |
| Chrome 29.0.1539.0   | GET (via XHR)          | *           | 1           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 29.0.1539.0   | GET (via 2DCanvas)     | *           | 0           |                 | Y           |             |
| Chrome 29.0.1539.0   | GET (via BitmapCanvas) | *           | 0           |                 | Y           |             |
| Chrome 29.0.1539.0   | GET (via Iframe)       | *           | 0           |                 | Y           |             |
| Chrome 29.0.1539.0   | GET (via Object)       | *           | 0           |                 | Y           |             |
| Chrome 29.0.1539.0   | GET (via XHR)          | *           | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 29.0.1539.0   | GET (via 2DCanvas)     | {ECHO}      | 1           |                 | Y           | Y           |
| Chrome 29.0.1539.0   | GET (via BitmapCanvas) | {ECHO}      | 1           |                 | Y           |             |
| Chrome 29.0.1539.0   | GET (via Iframe)       | {ECHO}      | 1           |                 | Y           |             |
| Chrome 29.0.1539.0   | GET (via Object)       | {ECHO}      | 1           |                 | Y           |             |
| Chrome 29.0.1539.0   | GET (via XHR)          | {ECHO}      | 1           |                 | Y           | Y           |
| Chrome 29.0.1539.0   | POST (via XHR)         | {ECHO}      | 1           | Y               | Y           | Y           |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 29.0.1539.0   | GET (via 2DCanvas)     | {ECHO}      | 0           |                 | Y           |             |
| Chrome 29.0.1539.0   | GET (via BitmapCanvas) | {ECHO}      | 0           |                 | Y           |             |
| Chrome 29.0.1539.0   | GET (via Iframe)       | {ECHO}      | 0           |                 | Y           |             |
| Chrome 29.0.1539.0   | GET (via Object)       | {ECHO}      | 0           |                 | Y           |             |
| Chrome 29.0.1539.0   | GET (via XHR)          | {ECHO}      | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 3.0.187.0     | GET (via 2DCanvas)     |             | 0           |                 | Y           |             |
| Chrome 3.0.187.0     | GET (via BitmapCanvas) |             | 0           |                 | Y           |             |
| Chrome 3.0.187.0     | GET (via Iframe)       |             | 0           |                 | Y           |             |
| Chrome 3.0.187.0     | GET (via Object)       |             | 0           |                 | Y           |             |
| Chrome 3.0.187.0     | GET (via XHR)          |             | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 3.0.187.0     | GET (via 2DCanvas)     | *           | 1           |                 | Y           |             |
| Chrome 3.0.187.0     | GET (via BitmapCanvas) | *           | 1           |                 | Y           |             |
| Chrome 3.0.187.0     | GET (via Iframe)       | *           | 1           |                 | Y           |             |
| Chrome 3.0.187.0     | GET (via Object)       | *           | 1           |                 | Y           |             |
| Chrome 3.0.187.0     | GET (via XHR)          | *           | 1           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 3.0.187.0     | GET (via 2DCanvas)     | *           | 0           |                 | Y           |             |
| Chrome 3.0.187.0     | GET (via BitmapCanvas) | *           | 0           |                 | Y           |             |
| Chrome 3.0.187.0     | GET (via Iframe)       | *           | 0           |                 | Y           |             |
| Chrome 3.0.187.0     | GET (via Object)       | *           | 0           |                 | Y           |             |
| Chrome 3.0.187.0     | GET (via XHR)          | *           | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 3.0.187.0     | GET (via 2DCanvas)     | {ECHO}      | 1           |                 | Y           |             |
| Chrome 3.0.187.0     | GET (via BitmapCanvas) | {ECHO}      | 1           |                 | Y           |             |
| Chrome 3.0.187.0     | GET (via Iframe)       | {ECHO}      | 1           |                 | Y           |             |
| Chrome 3.0.187.0     | GET (via Object)       | {ECHO}      | 1           |                 | Y           |             |
| Chrome 3.0.187.0     | GET (via XHR)          | {ECHO}      | 1           |                 | Y           | Y           |
| Chrome 3.0.187.0     | POST (via XHR)         | {ECHO}      | 1           | Y (with Cookie) | Y           | Y           |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 3.0.187.0     | GET (via 2DCanvas)     | {ECHO}      | 0           |                 | Y           |             |
| Chrome 3.0.187.0     | GET (via BitmapCanvas) | {ECHO}      | 0           |                 | Y           |             |
| Chrome 3.0.187.0     | GET (via Iframe)       | {ECHO}      | 0           |                 | Y           |             |
| Chrome 3.0.187.0     | GET (via Object)       | {ECHO}      | 0           |                 | Y           |             |
| Chrome 3.0.187.0     | GET (via XHR)          | {ECHO}      | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 31.0.1631.0   | GET (via 2DCanvas)     |             | 0           |                 | Y           |             |
| Chrome 31.0.1631.0   | GET (via BitmapCanvas) |             | 0           |                 | Y           |             |
| Chrome 31.0.1631.0   | GET (via Iframe)       |             | 0           |                 | Y           |             |
| Chrome 31.0.1631.0   | GET (via Object)       |             | 0           |                 | Y           |             |
| Chrome 31.0.1631.0   | GET (via XHR)          |             | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 31.0.1631.0   | GET (via 2DCanvas)     | *           | 1           |                 | Y           |             |
| Chrome 31.0.1631.0   | GET (via BitmapCanvas) | *           | 1           |                 | Y           |             |
| Chrome 31.0.1631.0   | GET (via Iframe)       | *           | 1           |                 | Y           |             |
| Chrome 31.0.1631.0   | GET (via Object)       | *           | 1           |                 | Y           |             |
| Chrome 31.0.1631.0   | GET (via XHR)          | *           | 1           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 31.0.1631.0   | GET (via 2DCanvas)     | *           | 0           |                 | Y           |             |
| Chrome 31.0.1631.0   | GET (via BitmapCanvas) | *           | 0           |                 | Y           |             |
| Chrome 31.0.1631.0   | GET (via Iframe)       | *           | 0           |                 | Y           |             |
| Chrome 31.0.1631.0   | GET (via Object)       | *           | 0           |                 | Y           |             |
| Chrome 31.0.1631.0   | GET (via XHR)          | *           | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 31.0.1631.0   | GET (via 2DCanvas)     | {ECHO}      | 1           |                 | Y           | Y           |
| Chrome 31.0.1631.0   | GET (via BitmapCanvas) | {ECHO}      | 1           |                 | Y           |             |
| Chrome 31.0.1631.0   | GET (via Iframe)       | {ECHO}      | 1           |                 | Y           |             |
| Chrome 31.0.1631.0   | GET (via Object)       | {ECHO}      | 1           |                 | Y           |             |
| Chrome 31.0.1631.0   | POST (via XHR)         | {ECHO}      | 1           | Y               | Y           | Y           |
| Chrome 31.0.1631.0   | GET (via XHR)          | {ECHO}      | 1           |                 | Y           | Y           |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 31.0.1631.0   | GET (via 2DCanvas)     | {ECHO}      | 0           |                 | Y           |             |
| Chrome 31.0.1631.0   | GET (via BitmapCanvas) | {ECHO}      | 0           |                 | Y           |             |
| Chrome 31.0.1631.0   | GET (via Iframe)       | {ECHO}      | 0           |                 | Y           |             |
| Chrome 31.0.1631.0   | GET (via Object)       | {ECHO}      | 0           |                 | Y           |             |
| Chrome 31.0.1631.0   | GET (via XHR)          | {ECHO}      | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 34.0.1758.0   | GET (via 2DCanvas)     |             | 0           |                 | Y           |             |
| Chrome 34.0.1758.0   | GET (via BitmapCanvas) |             | 0           |                 | Y           |             |
| Chrome 34.0.1758.0   | GET (via Iframe)       |             | 0           |                 | Y           |             |
| Chrome 34.0.1758.0   | GET (via Object)       |             | 0           |                 | Y           |             |
| Chrome 34.0.1758.0   | GET (via XHR)          |             | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 34.0.1758.0   | GET (via 2DCanvas)     | *           | 1           |                 | Y           |             |
| Chrome 34.0.1758.0   | GET (via BitmapCanvas) | *           | 1           |                 | Y           |             |
| Chrome 34.0.1758.0   | GET (via Iframe)       | *           | 1           |                 | Y           |             |
| Chrome 34.0.1758.0   | GET (via Object)       | *           | 1           |                 | Y           |             |
| Chrome 34.0.1758.0   | GET (via XHR)          | *           | 1           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 34.0.1758.0   | GET (via 2DCanvas)     | *           | 0           |                 | Y           |             |
| Chrome 34.0.1758.0   | GET (via BitmapCanvas) | *           | 0           |                 | Y           |             |
| Chrome 34.0.1758.0   | GET (via Iframe)       | *           | 0           |                 | Y           |             |
| Chrome 34.0.1758.0   | GET (via Object)       | *           | 0           |                 | Y           |             |
| Chrome 34.0.1758.0   | GET (via XHR)          | *           | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 34.0.1758.0   | GET (via 2DCanvas)     | {ECHO}      | 1           |                 | Y           | Y           |
| Chrome 34.0.1758.0   | GET (via BitmapCanvas) | {ECHO}      | 1           |                 | Y           |             |
| Chrome 34.0.1758.0   | GET (via Iframe)       | {ECHO}      | 1           |                 | Y           |             |
| Chrome 34.0.1758.0   | GET (via Object)       | {ECHO}      | 1           |                 | Y           |             |
| Chrome 34.0.1758.0   | POST (via XHR)         | {ECHO}      | 1           | Y               | Y           | Y           |
| Chrome 34.0.1758.0   | GET (via XHR)          | {ECHO}      | 1           |                 | Y           | Y           |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 34.0.1758.0   | GET (via 2DCanvas)     | {ECHO}      | 0           |                 | Y           |             |
| Chrome 34.0.1758.0   | GET (via BitmapCanvas) | {ECHO}      | 0           |                 | Y           |             |
| Chrome 34.0.1758.0   | GET (via Iframe)       | {ECHO}      | 0           |                 | Y           |             |
| Chrome 34.0.1758.0   | GET (via Object)       | {ECHO}      | 0           |                 | Y           |             |
| Chrome 34.0.1758.0   | GET (via XHR)          | {ECHO}      | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 37.0.2046.0   | GET (via 2DCanvas)     |             | 0           |                 | Y           |             |
| Chrome 37.0.2046.0   | GET (via BitmapCanvas) |             | 0           |                 | Y           |             |
| Chrome 37.0.2046.0   | GET (via Iframe)       |             | 0           |                 | Y           |             |
| Chrome 37.0.2046.0   | GET (via Object)       |             | 0           |                 | Y           |             |
| Chrome 37.0.2046.0   | GET (via XHR)          |             | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 37.0.2046.0   | GET (via 2DCanvas)     | *           | 1           |                 | Y           |             |
| Chrome 37.0.2046.0   | GET (via BitmapCanvas) | *           | 1           |                 | Y           |             |
| Chrome 37.0.2046.0   | GET (via Iframe)       | *           | 1           |                 | Y           |             |
| Chrome 37.0.2046.0   | GET (via Object)       | *           | 1           |                 | Y           |             |
| Chrome 37.0.2046.0   | GET (via XHR)          | *           | 1           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 37.0.2046.0   | GET (via 2DCanvas)     | *           | 0           |                 | Y           |             |
| Chrome 37.0.2046.0   | GET (via BitmapCanvas) | *           | 0           |                 | Y           |             |
| Chrome 37.0.2046.0   | GET (via Iframe)       | *           | 0           |                 | Y           |             |
| Chrome 37.0.2046.0   | GET (via Object)       | *           | 0           |                 | Y           |             |
| Chrome 37.0.2046.0   | GET (via XHR)          | *           | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 37.0.2046.0   | GET (via 2DCanvas)     | {ECHO}      | 1           |                 | Y           | Y           |
| Chrome 37.0.2046.0   | GET (via BitmapCanvas) | {ECHO}      | 1           |                 | Y           |             |
| Chrome 37.0.2046.0   | GET (via Iframe)       | {ECHO}      | 1           |                 | Y           |             |
| Chrome 37.0.2046.0   | GET (via Object)       | {ECHO}      | 1           |                 | Y           |             |
| Chrome 37.0.2046.0   | GET (via XHR)          | {ECHO}      | 1           |                 | Y           | Y           |
| Chrome 37.0.2046.0   | POST (via XHR)         | {ECHO}      | 1           | Y               | Y           | Y           |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 37.0.2046.0   | GET (via 2DCanvas)     | {ECHO}      | 0           |                 | Y           |             |
| Chrome 37.0.2046.0   | GET (via BitmapCanvas) | {ECHO}      | 0           |                 | Y           |             |
| Chrome 37.0.2046.0   | GET (via Iframe)       | {ECHO}      | 0           |                 | Y           |             |
| Chrome 37.0.2046.0   | GET (via Object)       | {ECHO}      | 0           |                 | Y           |             |
| Chrome 37.0.2046.0   | GET (via XHR)          | {ECHO}      | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 4.0.205.0     | GET (via 2DCanvas)     |             | 0           |                 | Y           |             |
| Chrome 4.0.205.0     | GET (via BitmapCanvas) |             | 0           |                 | Y           |             |
| Chrome 4.0.205.0     | GET (via Iframe)       |             | 0           |                 | Y           |             |
| Chrome 4.0.205.0     | GET (via Object)       |             | 0           |                 | Y           |             |
| Chrome 4.0.205.0     | GET (via XHR)          |             | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 4.0.205.0     | GET (via 2DCanvas)     | *           | 1           |                 | Y           |             |
| Chrome 4.0.205.0     | GET (via BitmapCanvas) | *           | 1           |                 | Y           |             |
| Chrome 4.0.205.0     | GET (via Iframe)       | *           | 1           |                 | Y           |             |
| Chrome 4.0.205.0     | GET (via Object)       | *           | 1           |                 | Y           |             |
| Chrome 4.0.205.0     | GET (via XHR)          | *           | 1           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 4.0.205.0     | GET (via 2DCanvas)     | *           | 0           |                 | Y           |             |
| Chrome 4.0.205.0     | GET (via BitmapCanvas) | *           | 0           |                 | Y           |             |
| Chrome 4.0.205.0     | GET (via Iframe)       | *           | 0           |                 | Y           |             |
| Chrome 4.0.205.0     | GET (via Object)       | *           | 0           |                 | Y           |             |
| Chrome 4.0.205.0     | GET (via XHR)          | *           | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 4.0.205.0     | GET (via 2DCanvas)     | {ECHO}      | 1           |                 | Y           |             |
| Chrome 4.0.205.0     | GET (via BitmapCanvas) | {ECHO}      | 1           |                 | Y           |             |
| Chrome 4.0.205.0     | GET (via Iframe)       | {ECHO}      | 1           |                 | Y           |             |
| Chrome 4.0.205.0     | GET (via Object)       | {ECHO}      | 1           |                 | Y           |             |
| Chrome 4.0.205.0     | GET (via XHR)          | {ECHO}      | 1           |                 | Y           | Y           |
| Chrome 4.0.205.0     | POST (via XHR)         | {ECHO}      | 1           | Y (with Cookie) | Y           | Y           |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 4.0.205.0     | GET (via 2DCanvas)     | {ECHO}      | 0           |                 | Y           |             |
| Chrome 4.0.205.0     | GET (via BitmapCanvas) | {ECHO}      | 0           |                 | Y           |             |
| Chrome 4.0.205.0     | GET (via Iframe)       | {ECHO}      | 0           |                 | Y           |             |
| Chrome 4.0.205.0     | GET (via Object)       | {ECHO}      | 0           |                 | Y           |             |
| Chrome 4.0.205.0     | GET (via XHR)          | {ECHO}      | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 40.0.2199.0   | GET (via 2DCanvas)     |             | 0           |                 | Y           |             |
| Chrome 40.0.2199.0   | GET (via BitmapCanvas) |             | 0           |                 | Y           |             |
| Chrome 40.0.2199.0   | GET (via Iframe)       |             | 0           |                 | Y           |             |
| Chrome 40.0.2199.0   | GET (via Object)       |             | 0           |                 | Y           |             |
| Chrome 40.0.2199.0   | GET (via XHR)          |             | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 40.0.2199.0   | GET (via 2DCanvas)     | *           | 1           |                 | Y           |             |
| Chrome 40.0.2199.0   | GET (via BitmapCanvas) | *           | 1           |                 | Y           |             |
| Chrome 40.0.2199.0   | GET (via Iframe)       | *           | 1           |                 | Y           |             |
| Chrome 40.0.2199.0   | GET (via Object)       | *           | 1           |                 | Y           |             |
| Chrome 40.0.2199.0   | GET (via XHR)          | *           | 1           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 40.0.2199.0   | GET (via 2DCanvas)     | *           | 0           |                 | Y           |             |
| Chrome 40.0.2199.0   | GET (via BitmapCanvas) | *           | 0           |                 | Y           |             |
| Chrome 40.0.2199.0   | GET (via Iframe)       | *           | 0           |                 | Y           |             |
| Chrome 40.0.2199.0   | GET (via Object)       | *           | 0           |                 | Y           |             |
| Chrome 40.0.2199.0   | GET (via XHR)          | *           | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 40.0.2199.0   | GET (via 2DCanvas)     | {ECHO}      | 1           |                 | Y           | Y           |
| Chrome 40.0.2199.0   | GET (via BitmapCanvas) | {ECHO}      | 1           |                 | Y           |             |
| Chrome 40.0.2199.0   | GET (via Iframe)       | {ECHO}      | 1           |                 | Y           |             |
| Chrome 40.0.2199.0   | GET (via Object)       | {ECHO}      | 1           |                 | Y           |             |
| Chrome 40.0.2199.0   | GET (via XHR)          | {ECHO}      | 1           |                 | Y           | Y           |
| Chrome 40.0.2199.0   | POST (via XHR)         | {ECHO}      | 1           | Y               | Y           | Y           |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 40.0.2199.0   | GET (via 2DCanvas)     | {ECHO}      | 0           |                 | Y           |             |
| Chrome 40.0.2199.0   | GET (via BitmapCanvas) | {ECHO}      | 0           |                 | Y           |             |
| Chrome 40.0.2199.0   | GET (via Iframe)       | {ECHO}      | 0           |                 | Y           |             |
| Chrome 40.0.2199.0   | GET (via Object)       | {ECHO}      | 0           |                 | Y           |             |
| Chrome 40.0.2199.0   | GET (via XHR)          | {ECHO}      | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 42.0.2290.0   | GET (via 2DCanvas)     |             | 0           |                 | Y           |             |
| Chrome 42.0.2290.0   | GET (via BitmapCanvas) |             | 0           |                 | Y           |             |
| Chrome 42.0.2290.0   | GET (via Iframe)       |             | 0           |                 | Y           |             |
| Chrome 42.0.2290.0   | GET (via Object)       |             | 0           |                 | Y           |             |
| Chrome 42.0.2290.0   | GET (via XHR)          |             | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 42.0.2290.0   | GET (via 2DCanvas)     | *           | 1           |                 | Y           |             |
| Chrome 42.0.2290.0   | GET (via BitmapCanvas) | *           | 1           |                 | Y           |             |
| Chrome 42.0.2290.0   | GET (via Iframe)       | *           | 1           |                 | Y           |             |
| Chrome 42.0.2290.0   | GET (via Object)       | *           | 1           |                 | Y           |             |
| Chrome 42.0.2290.0   | GET (via XHR)          | *           | 1           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 42.0.2290.0   | GET (via 2DCanvas)     | *           | 0           |                 | Y           |             |
| Chrome 42.0.2290.0   | GET (via BitmapCanvas) | *           | 0           |                 | Y           |             |
| Chrome 42.0.2290.0   | GET (via Iframe)       | *           | 0           |                 | Y           |             |
| Chrome 42.0.2290.0   | GET (via Object)       | *           | 0           |                 | Y           |             |
| Chrome 42.0.2290.0   | GET (via XHR)          | *           | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 42.0.2290.0   | GET (via 2DCanvas)     | {ECHO}      | 1           |                 | Y           | Y           |
| Chrome 42.0.2290.0   | GET (via BitmapCanvas) | {ECHO}      | 1           |                 | Y           |             |
| Chrome 42.0.2290.0   | GET (via Iframe)       | {ECHO}      | 1           |                 | Y           |             |
| Chrome 42.0.2290.0   | GET (via Object)       | {ECHO}      | 1           |                 | Y           |             |
| Chrome 42.0.2290.0   | POST (via XHR)         | {ECHO}      | 1           | Y               | Y           | Y           |
| Chrome 42.0.2290.0   | GET (via XHR)          | {ECHO}      | 1           |                 | Y           | Y           |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 42.0.2290.0   | GET (via 2DCanvas)     | {ECHO}      | 0           |                 | Y           |             |
| Chrome 42.0.2290.0   | GET (via BitmapCanvas) | {ECHO}      | 0           |                 | Y           |             |
| Chrome 42.0.2290.0   | GET (via Iframe)       | {ECHO}      | 0           |                 | Y           |             |
| Chrome 42.0.2290.0   | GET (via Object)       | {ECHO}      | 0           |                 | Y           |             |
| Chrome 42.0.2290.0   | GET (via XHR)          | {ECHO}      | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 44.0.2386.0   | GET (via 2DCanvas)     |             | 0           |                 | Y           |             |
| Chrome 44.0.2386.0   | GET (via BitmapCanvas) |             | 0           |                 | Y           |             |
| Chrome 44.0.2386.0   | GET (via Iframe)       |             | 0           |                 | Y           |             |
| Chrome 44.0.2386.0   | GET (via Object)       |             | 0           |                 | Y           |             |
| Chrome 44.0.2386.0   | GET (via XHR)          |             | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 44.0.2386.0   | GET (via 2DCanvas)     | *           | 1           |                 | Y           |             |
| Chrome 44.0.2386.0   | GET (via BitmapCanvas) | *           | 1           |                 | Y           |             |
| Chrome 44.0.2386.0   | GET (via Iframe)       | *           | 1           |                 | Y           |             |
| Chrome 44.0.2386.0   | GET (via Object)       | *           | 1           |                 | Y           |             |
| Chrome 44.0.2386.0   | GET (via XHR)          | *           | 1           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 44.0.2386.0   | GET (via 2DCanvas)     | *           | 0           |                 | Y           |             |
| Chrome 44.0.2386.0   | GET (via BitmapCanvas) | *           | 0           |                 | Y           |             |
| Chrome 44.0.2386.0   | GET (via Iframe)       | *           | 0           |                 | Y           |             |
| Chrome 44.0.2386.0   | GET (via Object)       | *           | 0           |                 | Y           |             |
| Chrome 44.0.2386.0   | GET (via XHR)          | *           | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 44.0.2386.0   | GET (via 2DCanvas)     | {ECHO}      | 1           |                 | Y           | Y           |
| Chrome 44.0.2386.0   | GET (via BitmapCanvas) | {ECHO}      | 1           |                 | Y           |             |
| Chrome 44.0.2386.0   | GET (via Iframe)       | {ECHO}      | 1           |                 | Y           |             |
| Chrome 44.0.2386.0   | GET (via Object)       | {ECHO}      | 1           |                 | Y           |             |
| Chrome 44.0.2386.0   | GET (via XHR)          | {ECHO}      | 1           |                 | Y           | Y           |
| Chrome 44.0.2386.0   | POST (via XHR)         | {ECHO}      | 1           | Y               | Y           | Y           |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 44.0.2386.0   | GET (via 2DCanvas)     | {ECHO}      | 0           |                 | Y           |             |
| Chrome 44.0.2386.0   | GET (via BitmapCanvas) | {ECHO}      | 0           |                 | Y           |             |
| Chrome 44.0.2386.0   | GET (via Iframe)       | {ECHO}      | 0           |                 | Y           |             |
| Chrome 44.0.2386.0   | GET (via Object)       | {ECHO}      | 0           |                 | Y           |             |
| Chrome 44.0.2386.0   | GET (via XHR)          | {ECHO}      | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 46.0.2485.0   | GET (via 2DCanvas)     |             | 0           |                 | Y           |             |
| Chrome 46.0.2485.0   | GET (via BitmapCanvas) |             | 0           |                 | Y           |             |
| Chrome 46.0.2485.0   | GET (via Iframe)       |             | 0           |                 | Y           |             |
| Chrome 46.0.2485.0   | GET (via Object)       |             | 0           |                 | Y           |             |
| Chrome 46.0.2485.0   | GET (via XHR)          |             | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 46.0.2485.0   | GET (via 2DCanvas)     | *           | 1           |                 | Y           |             |
| Chrome 46.0.2485.0   | GET (via BitmapCanvas) | *           | 1           |                 | Y           |             |
| Chrome 46.0.2485.0   | GET (via Iframe)       | *           | 1           |                 | Y           |             |
| Chrome 46.0.2485.0   | GET (via Object)       | *           | 1           |                 | Y           |             |
| Chrome 46.0.2485.0   | GET (via XHR)          | *           | 1           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 46.0.2485.0   | GET (via 2DCanvas)     | *           | 0           |                 | Y           |             |
| Chrome 46.0.2485.0   | GET (via BitmapCanvas) | *           | 0           |                 | Y           |             |
| Chrome 46.0.2485.0   | GET (via Iframe)       | *           | 0           |                 | Y           |             |
| Chrome 46.0.2485.0   | GET (via Object)       | *           | 0           |                 | Y           |             |
| Chrome 46.0.2485.0   | GET (via XHR)          | *           | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 46.0.2485.0   | GET (via 2DCanvas)     | {ECHO}      | 1           |                 | Y           | Y           |
| Chrome 46.0.2485.0   | GET (via BitmapCanvas) | {ECHO}      | 1           |                 | Y           |             |
| Chrome 46.0.2485.0   | GET (via Iframe)       | {ECHO}      | 1           |                 | Y           |             |
| Chrome 46.0.2485.0   | GET (via Object)       | {ECHO}      | 1           |                 | Y           |             |
| Chrome 46.0.2485.0   | POST (via XHR)         | {ECHO}      | 1           | Y               | Y           | Y           |
| Chrome 46.0.2485.0   | GET (via XHR)          | {ECHO}      | 1           |                 | Y           | Y           |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 46.0.2485.0   | GET (via 2DCanvas)     | {ECHO}      | 0           |                 | Y           |             |
| Chrome 46.0.2485.0   | GET (via BitmapCanvas) | {ECHO}      | 0           |                 | Y           |             |
| Chrome 46.0.2485.0   | GET (via Iframe)       | {ECHO}      | 0           |                 | Y           |             |
| Chrome 46.0.2485.0   | GET (via Object)       | {ECHO}      | 0           |                 | Y           |             |
| Chrome 46.0.2485.0   | GET (via XHR)          | {ECHO}      | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 49.0.2586.0   | GET (via 2DCanvas)     |             | 0           |                 | Y           |             |
| Chrome 49.0.2586.0   | GET (via BitmapCanvas) |             | 0           |                 | Y           |             |
| Chrome 49.0.2586.0   | GET (via Iframe)       |             | 0           |                 | Y           |             |
| Chrome 49.0.2586.0   | GET (via Object)       |             | 0           |                 | Y           |             |
| Chrome 49.0.2586.0   | GET (via XHR)          |             | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 49.0.2586.0   | GET (via 2DCanvas)     | *           | 1           |                 | Y           |             |
| Chrome 49.0.2586.0   | GET (via BitmapCanvas) | *           | 1           |                 | Y           |             |
| Chrome 49.0.2586.0   | GET (via Iframe)       | *           | 1           |                 | Y           |             |
| Chrome 49.0.2586.0   | GET (via Object)       | *           | 1           |                 | Y           |             |
| Chrome 49.0.2586.0   | GET (via XHR)          | *           | 1           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 49.0.2586.0   | GET (via 2DCanvas)     | *           | 0           |                 | Y           |             |
| Chrome 49.0.2586.0   | GET (via BitmapCanvas) | *           | 0           |                 | Y           |             |
| Chrome 49.0.2586.0   | GET (via Iframe)       | *           | 0           |                 | Y           |             |
| Chrome 49.0.2586.0   | GET (via Object)       | *           | 0           |                 | Y           |             |
| Chrome 49.0.2586.0   | GET (via XHR)          | *           | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 49.0.2586.0   | GET (via 2DCanvas)     | {ECHO}      | 1           |                 | Y           | Y           |
| Chrome 49.0.2586.0   | GET (via BitmapCanvas) | {ECHO}      | 1           |                 | Y           |             |
| Chrome 49.0.2586.0   | GET (via Iframe)       | {ECHO}      | 1           |                 | Y           |             |
| Chrome 49.0.2586.0   | GET (via Object)       | {ECHO}      | 1           |                 | Y           |             |
| Chrome 49.0.2586.0   | POST (via XHR)         | {ECHO}      | 1           | Y               | Y           | Y           |
| Chrome 49.0.2586.0   | GET (via XHR)          | {ECHO}      | 1           |                 | Y           | Y           |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 49.0.2586.0   | GET (via 2DCanvas)     | {ECHO}      | 0           |                 | Y           |             |
| Chrome 49.0.2586.0   | GET (via BitmapCanvas) | {ECHO}      | 0           |                 | Y           |             |
| Chrome 49.0.2586.0   | GET (via Iframe)       | {ECHO}      | 0           |                 | Y           |             |
| Chrome 49.0.2586.0   | GET (via Object)       | {ECHO}      | 0           |                 | Y           |             |
| Chrome 49.0.2586.0   | GET (via XHR)          | {ECHO}      | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 5.0.338.0     | GET (via 2DCanvas)     |             | 0           |                 | Y           |             |
| Chrome 5.0.338.0     | GET (via BitmapCanvas) |             | 0           |                 | Y           |             |
| Chrome 5.0.338.0     | GET (via Iframe)       |             | 0           |                 | Y           |             |
| Chrome 5.0.338.0     | GET (via Object)       |             | 0           |                 | Y           |             |
| Chrome 5.0.338.0     | GET (via XHR)          |             | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 5.0.338.0     | GET (via 2DCanvas)     | *           | 1           |                 | Y           |             |
| Chrome 5.0.338.0     | GET (via BitmapCanvas) | *           | 1           |                 | Y           |             |
| Chrome 5.0.338.0     | GET (via Iframe)       | *           | 1           |                 | Y           |             |
| Chrome 5.0.338.0     | GET (via Object)       | *           | 1           |                 | Y           |             |
| Chrome 5.0.338.0     | GET (via XHR)          | *           | 1           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 5.0.338.0     | GET (via 2DCanvas)     | *           | 0           |                 | Y           |             |
| Chrome 5.0.338.0     | GET (via BitmapCanvas) | *           | 0           |                 | Y           |             |
| Chrome 5.0.338.0     | GET (via Iframe)       | *           | 0           |                 | Y           |             |
| Chrome 5.0.338.0     | GET (via Object)       | *           | 0           |                 | Y           |             |
| Chrome 5.0.338.0     | GET (via XHR)          | *           | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 5.0.338.0     | GET (via 2DCanvas)     | {ECHO}      | 1           |                 | Y           |             |
| Chrome 5.0.338.0     | GET (via BitmapCanvas) | {ECHO}      | 1           |                 | Y           |             |
| Chrome 5.0.338.0     | GET (via Iframe)       | {ECHO}      | 1           |                 | Y           |             |
| Chrome 5.0.338.0     | GET (via Object)       | {ECHO}      | 1           |                 | Y           |             |
| Chrome 5.0.338.0     | POST (via XHR)         | {ECHO}      | 1           | Y (with Cookie) | Y           | Y           |
| Chrome 5.0.338.0     | GET (via XHR)          | {ECHO}      | 1           |                 | Y           | Y           |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 5.0.338.0     | GET (via 2DCanvas)     | {ECHO}      | 0           |                 | Y           |             |
| Chrome 5.0.338.0     | GET (via BitmapCanvas) | {ECHO}      | 0           |                 | Y           |             |
| Chrome 5.0.338.0     | GET (via Iframe)       | {ECHO}      | 0           |                 | Y           |             |
| Chrome 5.0.338.0     | GET (via Object)       | {ECHO}      | 0           |                 | Y           |             |
| Chrome 5.0.338.0     | GET (via XHR)          | {ECHO}      | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 51.0.2683.0   | GET (via 2DCanvas)     |             | 0           |                 | Y           |             |
| Chrome 51.0.2683.0   | GET (via BitmapCanvas) |             | 0           |                 | Y           |             |
| Chrome 51.0.2683.0   | GET (via Iframe)       |             | 0           |                 | Y           |             |
| Chrome 51.0.2683.0   | GET (via Object)       |             | 0           |                 | Y           |             |
| Chrome 51.0.2683.0   | GET (via XHR)          |             | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 51.0.2683.0   | GET (via 2DCanvas)     | *           | 1           |                 | Y           |             |
| Chrome 51.0.2683.0   | GET (via BitmapCanvas) | *           | 1           |                 | Y           |             |
| Chrome 51.0.2683.0   | GET (via Iframe)       | *           | 1           |                 | Y           |             |
| Chrome 51.0.2683.0   | GET (via Object)       | *           | 1           |                 | Y           |             |
| Chrome 51.0.2683.0   | GET (via XHR)          | *           | 1           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 51.0.2683.0   | GET (via 2DCanvas)     | *           | 0           |                 | Y           |             |
| Chrome 51.0.2683.0   | GET (via BitmapCanvas) | *           | 0           |                 | Y           |             |
| Chrome 51.0.2683.0   | GET (via Iframe)       | *           | 0           |                 | Y           |             |
| Chrome 51.0.2683.0   | GET (via Object)       | *           | 0           |                 | Y           |             |
| Chrome 51.0.2683.0   | GET (via XHR)          | *           | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 51.0.2683.0   | GET (via 2DCanvas)     | {ECHO}      | 1           |                 | Y           | Y           |
| Chrome 51.0.2683.0   | GET (via BitmapCanvas) | {ECHO}      | 1           |                 | Y           |             |
| Chrome 51.0.2683.0   | GET (via Iframe)       | {ECHO}      | 1           |                 | Y           |             |
| Chrome 51.0.2683.0   | GET (via Object)       | {ECHO}      | 1           |                 | Y           |             |
| Chrome 51.0.2683.0   | GET (via XHR)          | {ECHO}      | 1           |                 | Y           | Y           |
| Chrome 51.0.2683.0   | POST (via XHR)         | {ECHO}      | 1           | Y               | Y           | Y           |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 51.0.2683.0   | GET (via 2DCanvas)     | {ECHO}      | 0           |                 | Y           |             |
| Chrome 51.0.2683.0   | GET (via BitmapCanvas) | {ECHO}      | 0           |                 | Y           |             |
| Chrome 51.0.2683.0   | GET (via Iframe)       | {ECHO}      | 0           |                 | Y           |             |
| Chrome 51.0.2683.0   | GET (via Object)       | {ECHO}      | 0           |                 | Y           |             |
| Chrome 51.0.2683.0   | GET (via XHR)          | {ECHO}      | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 7.0.501.0     | GET (via 2DCanvas)     |             | 0           |                 | Y           |             |
| Chrome 7.0.501.0     | GET (via BitmapCanvas) |             | 0           |                 | Y           |             |
| Chrome 7.0.501.0     | GET (via Iframe)       |             | 0           |                 | Y           |             |
| Chrome 7.0.501.0     | GET (via Object)       |             | 0           |                 | Y           |             |
| Chrome 7.0.501.0     | GET (via XHR)          |             | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 7.0.501.0     | GET (via 2DCanvas)     | *           | 1           |                 | Y           |             |
| Chrome 7.0.501.0     | GET (via BitmapCanvas) | *           | 1           |                 | Y           |             |
| Chrome 7.0.501.0     | GET (via Iframe)       | *           | 1           |                 | Y           |             |
| Chrome 7.0.501.0     | GET (via Object)       | *           | 1           |                 | Y           |             |
| Chrome 7.0.501.0     | GET (via XHR)          | *           | 1           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 7.0.501.0     | GET (via 2DCanvas)     | *           | 0           |                 | Y           |             |
| Chrome 7.0.501.0     | GET (via BitmapCanvas) | *           | 0           |                 | Y           |             |
| Chrome 7.0.501.0     | GET (via Iframe)       | *           | 0           |                 | Y           |             |
| Chrome 7.0.501.0     | GET (via Object)       | *           | 0           |                 | Y           |             |
| Chrome 7.0.501.0     | GET (via XHR)          | *           | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 7.0.501.0     | GET (via 2DCanvas)     | {ECHO}      | 1           |                 | Y           |             |
| Chrome 7.0.501.0     | GET (via BitmapCanvas) | {ECHO}      | 1           |                 | Y           |             |
| Chrome 7.0.501.0     | GET (via Iframe)       | {ECHO}      | 1           |                 | Y           |             |
| Chrome 7.0.501.0     | GET (via Object)       | {ECHO}      | 1           |                 | Y           |             |
| Chrome 7.0.501.0     | POST (via XHR)         | {ECHO}      | 1           | Y (with Cookie) | Y           | Y           |
| Chrome 7.0.501.0     | GET (via XHR)          | {ECHO}      | 1           |                 | Y           | Y           |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Chrome 7.0.501.0     | GET (via 2DCanvas)     | {ECHO}      | 0           |                 | Y           |             |
| Chrome 7.0.501.0     | GET (via BitmapCanvas) | {ECHO}      | 0           |                 | Y           |             |
| Chrome 7.0.501.0     | GET (via Iframe)       | {ECHO}      | 0           |                 | Y           |             |
| Chrome 7.0.501.0     | GET (via Object)       | {ECHO}      | 0           |                 | Y           |             |
| Chrome 7.0.501.0     | GET (via XHR)          | {ECHO}      | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Edge 17.17134        | GET (via 2DCanvas)     |             | 0           |                 | Y           |             |
| Edge 17.17134        | GET (via BitmapCanvas) |             | 0           |                 | Y           |             |
| Edge 17.17134        | GET (via Iframe)       |             | 0           |                 | Y           |             |
| Edge 17.17134        | GET (via Object)       |             | 0           |                 | Y           |             |
| Edge 17.17134        | HEAD (via Object)      |             | 0           |                 | Y           |             |
| Edge 17.17134        | GET (via XHR)          |             | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Edge 17.17134        | GET (via 2DCanvas)     | *           | 1           |                 | Y           |             |
| Edge 17.17134        | GET (via BitmapCanvas) | *           | 1           |                 | Y           |             |
| Edge 17.17134        | GET (via Iframe)       | *           | 1           |                 | Y           |             |
| Edge 17.17134        | HEAD (via Object)      | *           | 1           |                 | Y           |             |
| Edge 17.17134        | GET (via Object)       | *           | 1           |                 | Y           |             |
| Edge 17.17134        | GET (via XHR)          | *           | 1           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Edge 17.17134        | GET (via 2DCanvas)     | *           | 0           |                 | Y           |             |
| Edge 17.17134        | GET (via BitmapCanvas) | *           | 0           |                 | Y           |             |
| Edge 17.17134        | GET (via Iframe)       | *           | 0           |                 | Y           |             |
| Edge 17.17134        | GET (via Object)       | *           | 0           |                 | Y           |             |
| Edge 17.17134        | HEAD (via Object)      | *           | 0           |                 | Y           |             |
| Edge 17.17134        | GET (via XHR)          | *           | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Edge 17.17134        | GET (via 2DCanvas)     | {ECHO}      | 1           |                 | Y           | Y           |
| Edge 17.17134        | GET (via BitmapCanvas) | {ECHO}      | 1           |                 | Y           |             |
| Edge 17.17134        | GET (via Iframe)       | {ECHO}      | 1           |                 | Y           |             |
| Edge 17.17134        | HEAD (via Object)      | {ECHO}      | 1           |                 | Y           |             |
| Edge 17.17134        | GET (via Object)       | {ECHO}      | 1           |                 | Y           |             |
| Edge 17.17134        | GET (via XHR)          | {ECHO}      | 1           |                 | Y           | Y           |
| Edge 17.17134        | POST (via XHR)         | {ECHO}      | 1           | Y               | Y           | Y           |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Edge 17.17134        | GET (via 2DCanvas)     | {ECHO}      | 0           |                 | Y           |             |
| Edge 17.17134        | GET (via BitmapCanvas) | {ECHO}      | 0           |                 | Y           |             |
| Edge 17.17134        | GET (via Iframe)       | {ECHO}      | 0           |                 | Y           |             |
| Edge 17.17134        | GET (via Object)       | {ECHO}      | 0           |                 | Y           |             |
| Edge 17.17134        | HEAD (via Object)      | {ECHO}      | 0           |                 | Y           |             |
| Edge 17.17134        | GET (via XHR)          | {ECHO}      | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Firefox 1.0          | GET (via 2DCanvas)     |             | 0           |                 | Y           |             |
| Firefox 1.0          | GET (via BitmapCanvas) |             | 0           |                 | Y           |             |
| Firefox 1.0          | GET (via Iframe)       |             | 0           |                 | Y           |             |
| Firefox 1.0          | GET (via Object)       |             | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Firefox 1.0          | GET (via 2DCanvas)     | *           | 1           |                 | Y           |             |
| Firefox 1.0          | GET (via BitmapCanvas) | *           | 1           |                 | Y           |             |
| Firefox 1.0          | GET (via Iframe)       | *           | 1           |                 | Y           |             |
| Firefox 1.0          | GET (via Object)       | *           | 1           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Firefox 1.0          | GET (via 2DCanvas)     | *           | 0           |                 | Y           |             |
| Firefox 1.0          | GET (via BitmapCanvas) | *           | 0           |                 | Y           |             |
| Firefox 1.0          | GET (via Iframe)       | *           | 0           |                 | Y           |             |
| Firefox 1.0          | GET (via Object)       | *           | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Firefox 1.0          | GET (via 2DCanvas)     | {ECHO}      | 1           |                 | Y           |             |
| Firefox 1.0          | GET (via BitmapCanvas) | {ECHO}      | 1           |                 | Y           |             |
| Firefox 1.0          | GET (via Iframe)       | {ECHO}      | 1           |                 | Y           |             |
| Firefox 1.0          | GET (via Object)       | {ECHO}      | 1           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Firefox 1.0          | GET (via 2DCanvas)     | {ECHO}      | 0           |                 | Y           |             |
| Firefox 1.0          | GET (via BitmapCanvas) | {ECHO}      | 0           |                 | Y           |             |
| Firefox 1.0          | GET (via Iframe)       | {ECHO}      | 0           |                 | Y           |             |
| Firefox 1.0          | GET (via Object)       | {ECHO}      | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Firefox 10.0         | GET (via 2DCanvas)     |             | 0           |                 | Y           |             |
| Firefox 10.0         | GET (via BitmapCanvas) |             | 0           |                 | Y           |             |
| Firefox 10.0         | GET (via Iframe)       |             | 0           |                 | Y           |             |
| Firefox 10.0         | GET (via Object)       |             | 0           |                 | Y           |             |
| Firefox 10.0         | GET (via XHR)          |             | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Firefox 10.0         | GET (via 2DCanvas)     | *           | 1           |                 | Y           |             |
| Firefox 10.0         | GET (via BitmapCanvas) | *           | 1           |                 | Y           |             |
| Firefox 10.0         | GET (via Iframe)       | *           | 1           |                 | Y           |             |
| Firefox 10.0         | GET (via Object)       | *           | 1           |                 | Y           |             |
| Firefox 10.0         | GET (via XHR)          | *           | 1           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Firefox 10.0         | GET (via 2DCanvas)     | *           | 0           |                 | Y           |             |
| Firefox 10.0         | GET (via BitmapCanvas) | *           | 0           |                 | Y           |             |
| Firefox 10.0         | GET (via Iframe)       | *           | 0           |                 | Y           |             |
| Firefox 10.0         | GET (via Object)       | *           | 0           |                 | Y           |             |
| Firefox 10.0         | GET (via XHR)          | *           | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Firefox 10.0         | GET (via 2DCanvas)     | {ECHO}      | 1           |                 | Y           | Y           |
| Firefox 10.0         | GET (via BitmapCanvas) | {ECHO}      | 1           |                 | Y           |             |
| Firefox 10.0         | GET (via Iframe)       | {ECHO}      | 1           |                 | Y           |             |
| Firefox 10.0         | GET (via Object)       | {ECHO}      | 1           |                 | Y           |             |
| Firefox 10.0         | POST (via XHR)         | {ECHO}      | 1           | Y               | Y           | Y           |
| Firefox 10.0         | GET (via XHR)          | {ECHO}      | 1           |                 | Y           | Y           |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Firefox 10.0         | GET (via 2DCanvas)     | {ECHO}      | 0           |                 | Y           |             |
| Firefox 10.0         | GET (via BitmapCanvas) | {ECHO}      | 0           |                 | Y           |             |
| Firefox 10.0         | GET (via Iframe)       | {ECHO}      | 0           |                 | Y           |             |
| Firefox 10.0         | GET (via Object)       | {ECHO}      | 0           |                 | Y           |             |
| Firefox 10.0         | GET (via XHR)          | {ECHO}      | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Firefox 18.0         | GET (via 2DCanvas)     |             | 0           |                 | Y           |             |
| Firefox 18.0         | GET (via BitmapCanvas) |             | 0           |                 | Y           |             |
| Firefox 18.0         | GET (via Iframe)       |             | 0           |                 | Y           |             |
| Firefox 18.0         | GET (via Object)       |             | 0           |                 | Y           |             |
| Firefox 18.0         | GET (via XHR)          |             | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Firefox 18.0         | GET (via 2DCanvas)     | *           | 1           |                 | Y           |             |
| Firefox 18.0         | GET (via BitmapCanvas) | *           | 1           |                 | Y           |             |
| Firefox 18.0         | GET (via Iframe)       | *           | 1           |                 | Y           |             |
| Firefox 18.0         | GET (via Object)       | *           | 1           |                 | Y           |             |
| Firefox 18.0         | GET (via XHR)          | *           | 1           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Firefox 18.0         | GET (via 2DCanvas)     | *           | 0           |                 | Y           |             |
| Firefox 18.0         | GET (via BitmapCanvas) | *           | 0           |                 | Y           |             |
| Firefox 18.0         | GET (via Iframe)       | *           | 0           |                 | Y           |             |
| Firefox 18.0         | GET (via Object)       | *           | 0           |                 | Y           |             |
| Firefox 18.0         | GET (via XHR)          | *           | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Firefox 18.0         | GET (via 2DCanvas)     | {ECHO}      | 1           |                 | Y           | Y           |
| Firefox 18.0         | GET (via BitmapCanvas) | {ECHO}      | 1           |                 | Y           |             |
| Firefox 18.0         | GET (via Iframe)       | {ECHO}      | 1           |                 | Y           |             |
| Firefox 18.0         | GET (via Object)       | {ECHO}      | 1           |                 | Y           |             |
| Firefox 18.0         | GET (via XHR)          | {ECHO}      | 1           |                 | Y           | Y           |
| Firefox 18.0         | POST (via XHR)         | {ECHO}      | 1           | Y               | Y           | Y           |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Firefox 18.0         | GET (via 2DCanvas)     | {ECHO}      | 0           |                 | Y           |             |
| Firefox 18.0         | GET (via BitmapCanvas) | {ECHO}      | 0           |                 | Y           |             |
| Firefox 18.0         | GET (via Iframe)       | {ECHO}      | 0           |                 | Y           |             |
| Firefox 18.0         | GET (via Object)       | {ECHO}      | 0           |                 | Y           |             |
| Firefox 18.0         | GET (via XHR)          | {ECHO}      | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Firefox 2.0          | GET (via 2DCanvas)     |             | 0           |                 | Y           |             |
| Firefox 2.0          | GET (via BitmapCanvas) |             | 0           |                 | Y           |             |
| Firefox 2.0          | GET (via Iframe)       |             | 0           |                 | Y           |             |
| Firefox 2.0          | GET (via Object)       |             | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Firefox 2.0          | GET (via 2DCanvas)     | *           | 1           |                 | Y           |             |
| Firefox 2.0          | GET (via BitmapCanvas) | *           | 1           |                 | Y           |             |
| Firefox 2.0          | GET (via Iframe)       | *           | 1           |                 | Y           |             |
| Firefox 2.0          | GET (via Object)       | *           | 1           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Firefox 2.0          | GET (via 2DCanvas)     | *           | 0           |                 | Y           |             |
| Firefox 2.0          | GET (via BitmapCanvas) | *           | 0           |                 | Y           |             |
| Firefox 2.0          | GET (via Iframe)       | *           | 0           |                 | Y           |             |
| Firefox 2.0          | GET (via Object)       | *           | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Firefox 2.0          | GET (via 2DCanvas)     | {ECHO}      | 1           |                 | Y           |             |
| Firefox 2.0          | GET (via BitmapCanvas) | {ECHO}      | 1           |                 | Y           |             |
| Firefox 2.0          | GET (via Iframe)       | {ECHO}      | 1           |                 | Y           |             |
| Firefox 2.0          | GET (via Object)       | {ECHO}      | 1           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Firefox 2.0          | GET (via 2DCanvas)     | {ECHO}      | 0           |                 | Y           |             |
| Firefox 2.0          | GET (via BitmapCanvas) | {ECHO}      | 0           |                 | Y           |             |
| Firefox 2.0          | GET (via Iframe)       | {ECHO}      | 0           |                 | Y           |             |
| Firefox 2.0          | GET (via Object)       | {ECHO}      | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Firefox 27.0         | GET (via 2DCanvas)     |             | 0           |                 | Y           |             |
| Firefox 27.0         | GET (via BitmapCanvas) |             | 0           |                 | Y           |             |
| Firefox 27.0         | GET (via Iframe)       |             | 0           |                 | Y           |             |
| Firefox 27.0         | GET (via Object)       |             | 0           |                 | Y           |             |
| Firefox 27.0         | GET (via XHR)          |             | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Firefox 27.0         | GET (via 2DCanvas)     | *           | 1           |                 | Y           |             |
| Firefox 27.0         | GET (via BitmapCanvas) | *           | 1           |                 | Y           |             |
| Firefox 27.0         | GET (via Iframe)       | *           | 1           |                 | Y           |             |
| Firefox 27.0         | GET (via Object)       | *           | 1           |                 | Y           |             |
| Firefox 27.0         | GET (via XHR)          | *           | 1           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Firefox 27.0         | GET (via 2DCanvas)     | *           | 0           |                 | Y           |             |
| Firefox 27.0         | GET (via BitmapCanvas) | *           | 0           |                 | Y           |             |
| Firefox 27.0         | GET (via Iframe)       | *           | 0           |                 | Y           |             |
| Firefox 27.0         | GET (via Object)       | *           | 0           |                 | Y           |             |
| Firefox 27.0         | GET (via XHR)          | *           | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Firefox 27.0         | GET (via 2DCanvas)     | {ECHO}      | 1           |                 | Y           | Y           |
| Firefox 27.0         | GET (via BitmapCanvas) | {ECHO}      | 1           |                 | Y           |             |
| Firefox 27.0         | GET (via Iframe)       | {ECHO}      | 1           |                 | Y           |             |
| Firefox 27.0         | GET (via Object)       | {ECHO}      | 1           |                 | Y           |             |
| Firefox 27.0         | GET (via XHR)          | {ECHO}      | 1           |                 | Y           | Y           |
| Firefox 27.0         | POST (via XHR)         | {ECHO}      | 1           | Y               | Y           | Y           |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Firefox 27.0         | GET (via 2DCanvas)     | {ECHO}      | 0           |                 | Y           |             |
| Firefox 27.0         | GET (via BitmapCanvas) | {ECHO}      | 0           |                 | Y           |             |
| Firefox 27.0         | GET (via Iframe)       | {ECHO}      | 0           |                 | Y           |             |
| Firefox 27.0         | GET (via Object)       | {ECHO}      | 0           |                 | Y           |             |
| Firefox 27.0         | GET (via XHR)          | {ECHO}      | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Firefox 3.0          | GET (via 2DCanvas)     |             | 0           |                 | Y           |             |
| Firefox 3.0          | GET (via BitmapCanvas) |             | 0           |                 | Y           |             |
| Firefox 3.0          | GET (via Iframe)       |             | 0           |                 | Y           |             |
| Firefox 3.0          | GET (via Object)       |             | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Firefox 3.0          | GET (via 2DCanvas)     | *           | 1           |                 | Y           |             |
| Firefox 3.0          | GET (via BitmapCanvas) | *           | 1           |                 | Y           |             |
| Firefox 3.0          | GET (via Iframe)       | *           | 1           |                 | Y           |             |
| Firefox 3.0          | GET (via Object)       | *           | 1           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Firefox 3.0          | GET (via 2DCanvas)     | *           | 0           |                 | Y           |             |
| Firefox 3.0          | GET (via BitmapCanvas) | *           | 0           |                 | Y           |             |
| Firefox 3.0          | GET (via Iframe)       | *           | 0           |                 | Y           |             |
| Firefox 3.0          | GET (via Object)       | *           | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Firefox 3.0          | GET (via 2DCanvas)     | {ECHO}      | 1           |                 | Y           |             |
| Firefox 3.0          | GET (via BitmapCanvas) | {ECHO}      | 1           |                 | Y           |             |
| Firefox 3.0          | GET (via Iframe)       | {ECHO}      | 1           |                 | Y           |             |
| Firefox 3.0          | GET (via Object)       | {ECHO}      | 1           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Firefox 3.0          | GET (via 2DCanvas)     | {ECHO}      | 0           |                 | Y           |             |
| Firefox 3.0          | GET (via BitmapCanvas) | {ECHO}      | 0           |                 | Y           |             |
| Firefox 3.0          | GET (via Iframe)       | {ECHO}      | 0           |                 | Y           |             |
| Firefox 3.0          | GET (via Object)       | {ECHO}      | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Firefox 3.5          | GET (via 2DCanvas)     |             | 0           |                 | Y           |             |
| Firefox 3.5          | GET (via BitmapCanvas) |             | 0           |                 | Y           |             |
| Firefox 3.5          | GET (via Iframe)       |             | 0           |                 | Y           |             |
| Firefox 3.5          | GET (via Object)       |             | 0           |                 | Y           |             |
| Firefox 3.5          | GET (via XHR)          |             | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Firefox 3.5          | GET (via 2DCanvas)     | *           | 1           |                 | Y           |             |
| Firefox 3.5          | GET (via BitmapCanvas) | *           | 1           |                 | Y           |             |
| Firefox 3.5          | GET (via Iframe)       | *           | 1           |                 | Y           |             |
| Firefox 3.5          | GET (via Object)       | *           | 1           |                 | Y           |             |
| Firefox 3.5          | GET (via XHR)          | *           | 1           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Firefox 3.5          | GET (via 2DCanvas)     | *           | 0           |                 | Y           |             |
| Firefox 3.5          | GET (via BitmapCanvas) | *           | 0           |                 | Y           |             |
| Firefox 3.5          | GET (via Iframe)       | *           | 0           |                 | Y           |             |
| Firefox 3.5          | GET (via Object)       | *           | 0           |                 | Y           |             |
| Firefox 3.5          | GET (via XHR)          | *           | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Firefox 3.5          | GET (via 2DCanvas)     | {ECHO}      | 1           |                 | Y           |             |
| Firefox 3.5          | GET (via BitmapCanvas) | {ECHO}      | 1           |                 | Y           |             |
| Firefox 3.5          | GET (via Iframe)       | {ECHO}      | 1           |                 | Y           |             |
| Firefox 3.5          | GET (via Object)       | {ECHO}      | 1           |                 | Y           |             |
| Firefox 3.5          | GET (via XHR)          | {ECHO}      | 1           |                 | Y           | Y           |
| Firefox 3.5          | POST (via XHR)         | {ECHO}      | 1           | Y               | Y           | Y           |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Firefox 3.5          | GET (via 2DCanvas)     | {ECHO}      | 0           |                 | Y           |             |
| Firefox 3.5          | GET (via BitmapCanvas) | {ECHO}      | 0           |                 | Y           |             |
| Firefox 3.5          | GET (via Iframe)       | {ECHO}      | 0           |                 | Y           |             |
| Firefox 3.5          | GET (via Object)       | {ECHO}      | 0           |                 | Y           |             |
| Firefox 3.5          | GET (via XHR)          | {ECHO}      | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Firefox 3.6          | GET (via 2DCanvas)     |             | 0           |                 | Y           |             |
| Firefox 3.6          | GET (via BitmapCanvas) |             | 0           |                 | Y           |             |
| Firefox 3.6          | GET (via Iframe)       |             | 0           |                 | Y           |             |
| Firefox 3.6          | GET (via Object)       |             | 0           |                 | Y           |             |
| Firefox 3.6          | GET (via XHR)          |             | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Firefox 3.6          | GET (via 2DCanvas)     | *           | 1           |                 | Y           |             |
| Firefox 3.6          | GET (via BitmapCanvas) | *           | 1           |                 | Y           |             |
| Firefox 3.6          | GET (via Iframe)       | *           | 1           |                 | Y           |             |
| Firefox 3.6          | GET (via Object)       | *           | 1           |                 | Y           |             |
| Firefox 3.6          | GET (via XHR)          | *           | 1           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Firefox 3.6          | GET (via 2DCanvas)     | *           | 0           |                 | Y           |             |
| Firefox 3.6          | GET (via BitmapCanvas) | *           | 0           |                 | Y           |             |
| Firefox 3.6          | GET (via Iframe)       | *           | 0           |                 | Y           |             |
| Firefox 3.6          | GET (via Object)       | *           | 0           |                 | Y           |             |
| Firefox 3.6          | GET (via XHR)          | *           | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Firefox 3.6          | GET (via 2DCanvas)     | {ECHO}      | 1           |                 | Y           |             |
| Firefox 3.6          | GET (via BitmapCanvas) | {ECHO}      | 1           |                 | Y           |             |
| Firefox 3.6          | GET (via Iframe)       | {ECHO}      | 1           |                 | Y           |             |
| Firefox 3.6          | GET (via Object)       | {ECHO}      | 1           |                 | Y           |             |
| Firefox 3.6          | GET (via XHR)          | {ECHO}      | 1           |                 | Y           | Y           |
| Firefox 3.6          | POST (via XHR)         | {ECHO}      | 1           | Y               | Y           | Y           |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Firefox 3.6          | GET (via 2DCanvas)     | {ECHO}      | 0           |                 | Y           |             |
| Firefox 3.6          | GET (via BitmapCanvas) | {ECHO}      | 0           |                 | Y           |             |
| Firefox 3.6          | GET (via Iframe)       | {ECHO}      | 0           |                 | Y           |             |
| Firefox 3.6          | GET (via Object)       | {ECHO}      | 0           |                 | Y           |             |
| Firefox 3.6          | GET (via XHR)          | {ECHO}      | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Firefox 35.0         | GET (via 2DCanvas)     |             | 0           |                 | Y           |             |
| Firefox 35.0         | GET (via BitmapCanvas) |             | 0           |                 | Y           |             |
| Firefox 35.0         | GET (via Iframe)       |             | 0           |                 | Y           |             |
| Firefox 35.0         | GET (via Object)       |             | 0           |                 | Y           |             |
| Firefox 35.0         | GET (via XHR)          |             | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Firefox 35.0         | GET (via 2DCanvas)     | *           | 1           |                 | Y           |             |
| Firefox 35.0         | GET (via BitmapCanvas) | *           | 1           |                 | Y           |             |
| Firefox 35.0         | GET (via Iframe)       | *           | 1           |                 | Y           |             |
| Firefox 35.0         | GET (via Object)       | *           | 1           |                 | Y           |             |
| Firefox 35.0         | GET (via XHR)          | *           | 1           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Firefox 35.0         | GET (via 2DCanvas)     | *           | 0           |                 | Y           |             |
| Firefox 35.0         | GET (via BitmapCanvas) | *           | 0           |                 | Y           |             |
| Firefox 35.0         | GET (via Iframe)       | *           | 0           |                 | Y           |             |
| Firefox 35.0         | GET (via Object)       | *           | 0           |                 | Y           |             |
| Firefox 35.0         | GET (via XHR)          | *           | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Firefox 35.0         | GET (via 2DCanvas)     | {ECHO}      | 1           |                 | Y           | Y           |
| Firefox 35.0         | GET (via BitmapCanvas) | {ECHO}      | 1           |                 | Y           |             |
| Firefox 35.0         | GET (via Iframe)       | {ECHO}      | 1           |                 | Y           |             |
| Firefox 35.0         | GET (via Object)       | {ECHO}      | 1           |                 | Y           |             |
| Firefox 35.0         | POST (via XHR)         | {ECHO}      | 1           | Y               | Y           | Y           |
| Firefox 35.0         | GET (via XHR)          | {ECHO}      | 1           |                 | Y           | Y           |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Firefox 35.0         | GET (via 2DCanvas)     | {ECHO}      | 0           |                 | Y           |             |
| Firefox 35.0         | GET (via BitmapCanvas) | {ECHO}      | 0           |                 | Y           |             |
| Firefox 35.0         | GET (via Iframe)       | {ECHO}      | 0           |                 | Y           |             |
| Firefox 35.0         | GET (via Object)       | {ECHO}      | 0           |                 | Y           |             |
| Firefox 35.0         | GET (via XHR)          | {ECHO}      | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Firefox 4.0          | GET (via 2DCanvas)     |             | 0           |                 | Y           |             |
| Firefox 4.0          | GET (via BitmapCanvas) |             | 0           |                 | Y           |             |
| Firefox 4.0          | GET (via Iframe)       |             | 0           |                 | Y           |             |
| Firefox 4.0          | GET (via Object)       |             | 0           |                 | Y           |             |
| Firefox 4.0          | GET (via XHR)          |             | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Firefox 4.0          | GET (via 2DCanvas)     | *           | 1           |                 | Y           |             |
| Firefox 4.0          | GET (via BitmapCanvas) | *           | 1           |                 | Y           |             |
| Firefox 4.0          | GET (via Iframe)       | *           | 1           |                 | Y           |             |
| Firefox 4.0          | GET (via Object)       | *           | 1           |                 | Y           |             |
| Firefox 4.0          | GET (via XHR)          | *           | 1           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Firefox 4.0          | GET (via 2DCanvas)     | *           | 0           |                 | Y           |             |
| Firefox 4.0          | GET (via BitmapCanvas) | *           | 0           |                 | Y           |             |
| Firefox 4.0          | GET (via Iframe)       | *           | 0           |                 | Y           |             |
| Firefox 4.0          | GET (via Object)       | *           | 0           |                 | Y           |             |
| Firefox 4.0          | GET (via XHR)          | *           | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Firefox 4.0          | GET (via 2DCanvas)     | {ECHO}      | 1           |                 | Y           |             |
| Firefox 4.0          | GET (via BitmapCanvas) | {ECHO}      | 1           |                 | Y           |             |
| Firefox 4.0          | GET (via Iframe)       | {ECHO}      | 1           |                 | Y           |             |
| Firefox 4.0          | GET (via Object)       | {ECHO}      | 1           |                 | Y           |             |
| Firefox 4.0          | GET (via XHR)          | {ECHO}      | 1           |                 | Y           | Y           |
| Firefox 4.0          | POST (via XHR)         | {ECHO}      | 1           | Y               | Y           | Y           |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Firefox 4.0          | GET (via 2DCanvas)     | {ECHO}      | 0           |                 | Y           |             |
| Firefox 4.0          | GET (via BitmapCanvas) | {ECHO}      | 0           |                 | Y           |             |
| Firefox 4.0          | GET (via Iframe)       | {ECHO}      | 0           |                 | Y           |             |
| Firefox 4.0          | GET (via Object)       | {ECHO}      | 0           |                 | Y           |             |
| Firefox 4.0          | GET (via XHR)          | {ECHO}      | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Firefox 44.0         | GET (via 2DCanvas)     |             | 0           |                 | Y           |             |
| Firefox 44.0         | GET (via BitmapCanvas) |             | 0           |                 | Y           |             |
| Firefox 44.0         | GET (via Iframe)       |             | 0           |                 | Y           |             |
| Firefox 44.0         | GET (via Object)       |             | 0           |                 | Y           |             |
| Firefox 44.0         | GET (via XHR)          |             | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Firefox 44.0         | GET (via 2DCanvas)     | *           | 1           |                 | Y           |             |
| Firefox 44.0         | GET (via BitmapCanvas) | *           | 1           |                 | Y           |             |
| Firefox 44.0         | GET (via Iframe)       | *           | 1           |                 | Y           |             |
| Firefox 44.0         | GET (via Object)       | *           | 1           |                 | Y           |             |
| Firefox 44.0         | GET (via XHR)          | *           | 1           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Firefox 44.0         | GET (via 2DCanvas)     | *           | 0           |                 | Y           |             |
| Firefox 44.0         | GET (via BitmapCanvas) | *           | 0           |                 | Y           |             |
| Firefox 44.0         | GET (via Iframe)       | *           | 0           |                 | Y           |             |
| Firefox 44.0         | GET (via Object)       | *           | 0           |                 | Y           |             |
| Firefox 44.0         | GET (via XHR)          | *           | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Firefox 44.0         | GET (via 2DCanvas)     | {ECHO}      | 1           |                 | Y           | Y           |
| Firefox 44.0         | GET (via BitmapCanvas) | {ECHO}      | 1           |                 | Y           |             |
| Firefox 44.0         | GET (via Iframe)       | {ECHO}      | 1           |                 | Y           |             |
| Firefox 44.0         | GET (via Object)       | {ECHO}      | 1           |                 | Y           |             |
| Firefox 44.0         | GET (via XHR)          | {ECHO}      | 1           |                 | Y           | Y           |
| Firefox 44.0         | POST (via XHR)         | {ECHO}      | 1           | Y               | Y           | Y           |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Firefox 44.0         | GET (via 2DCanvas)     | {ECHO}      | 0           |                 | Y           |             |
| Firefox 44.0         | GET (via BitmapCanvas) | {ECHO}      | 0           |                 | Y           |             |
| Firefox 44.0         | GET (via Iframe)       | {ECHO}      | 0           |                 | Y           |             |
| Firefox 44.0         | GET (via Object)       | {ECHO}      | 0           |                 | Y           |             |
| Firefox 44.0         | GET (via XHR)          | {ECHO}      | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Firefox 5.0          | GET (via 2DCanvas)     |             | 0           |                 | Y           |             |
| Firefox 5.0          | GET (via BitmapCanvas) |             | 0           |                 | Y           |             |
| Firefox 5.0          | GET (via Iframe)       |             | 0           |                 | Y           |             |
| Firefox 5.0          | GET (via Object)       |             | 0           |                 | Y           |             |
| Firefox 5.0          | GET (via XHR)          |             | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Firefox 5.0          | GET (via 2DCanvas)     | *           | 1           |                 | Y           |             |
| Firefox 5.0          | GET (via BitmapCanvas) | *           | 1           |                 | Y           |             |
| Firefox 5.0          | GET (via Iframe)       | *           | 1           |                 | Y           |             |
| Firefox 5.0          | GET (via Object)       | *           | 1           |                 | Y           |             |
| Firefox 5.0          | GET (via XHR)          | *           | 1           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Firefox 5.0          | GET (via 2DCanvas)     | *           | 0           |                 | Y           |             |
| Firefox 5.0          | GET (via BitmapCanvas) | *           | 0           |                 | Y           |             |
| Firefox 5.0          | GET (via Iframe)       | *           | 0           |                 | Y           |             |
| Firefox 5.0          | GET (via Object)       | *           | 0           |                 | Y           |             |
| Firefox 5.0          | GET (via XHR)          | *           | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Firefox 5.0          | GET (via 2DCanvas)     | {ECHO}      | 1           |                 | Y           |             |
| Firefox 5.0          | GET (via BitmapCanvas) | {ECHO}      | 1           |                 | Y           |             |
| Firefox 5.0          | GET (via Iframe)       | {ECHO}      | 1           |                 | Y           |             |
| Firefox 5.0          | GET (via Object)       | {ECHO}      | 1           |                 | Y           |             |
| Firefox 5.0          | GET (via XHR)          | {ECHO}      | 1           |                 | Y           | Y           |
| Firefox 5.0          | POST (via XHR)         | {ECHO}      | 1           | Y               | Y           | Y           |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Firefox 5.0          | GET (via 2DCanvas)     | {ECHO}      | 0           |                 | Y           |             |
| Firefox 5.0          | GET (via BitmapCanvas) | {ECHO}      | 0           |                 | Y           |             |
| Firefox 5.0          | GET (via Iframe)       | {ECHO}      | 0           |                 | Y           |             |
| Firefox 5.0          | GET (via Object)       | {ECHO}      | 0           |                 | Y           |             |
| Firefox 5.0          | GET (via XHR)          | {ECHO}      | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Firefox 52.0         | GET (via 2DCanvas)     |             | 0           |                 | Y           |             |
| Firefox 52.0         | GET (via BitmapCanvas) |             | 0           |                 | Y           |             |
| Firefox 52.0         | GET (via Iframe)       |             | 0           |                 | Y           |             |
| Firefox 52.0         | GET (via Object)       |             | 0           |                 | Y           |             |
| Firefox 52.0         | GET (via XHR)          |             | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Firefox 52.0         | GET (via 2DCanvas)     | *           | 1           |                 | Y           |             |
| Firefox 52.0         | GET (via BitmapCanvas) | *           | 1           |                 | Y           |             |
| Firefox 52.0         | GET (via Iframe)       | *           | 1           |                 | Y           |             |
| Firefox 52.0         | GET (via Object)       | *           | 1           |                 | Y           |             |
| Firefox 52.0         | GET (via XHR)          | *           | 1           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Firefox 52.0         | GET (via 2DCanvas)     | *           | 0           |                 | Y           |             |
| Firefox 52.0         | GET (via BitmapCanvas) | *           | 0           |                 | Y           |             |
| Firefox 52.0         | GET (via Iframe)       | *           | 0           |                 | Y           |             |
| Firefox 52.0         | GET (via Object)       | *           | 0           |                 | Y           |             |
| Firefox 52.0         | GET (via XHR)          | *           | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Firefox 52.0         | GET (via 2DCanvas)     | {ECHO}      | 1           |                 | Y           | Y           |
| Firefox 52.0         | GET (via BitmapCanvas) | {ECHO}      | 1           |                 | Y           | Y           |
| Firefox 52.0         | GET (via Iframe)       | {ECHO}      | 1           |                 | Y           |             |
| Firefox 52.0         | GET (via Object)       | {ECHO}      | 1           |                 | Y           |             |
| Firefox 52.0         | POST (via XHR)         | {ECHO}      | 1           | Y               | Y           | Y           |
| Firefox 52.0         | GET (via XHR)          | {ECHO}      | 1           |                 | Y           | Y           |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Firefox 52.0         | GET (via 2DCanvas)     | {ECHO}      | 0           |                 | Y           |             |
| Firefox 52.0         | GET (via BitmapCanvas) | {ECHO}      | 0           |                 | Y           |             |
| Firefox 52.0         | GET (via Iframe)       | {ECHO}      | 0           |                 | Y           |             |
| Firefox 52.0         | GET (via Object)       | {ECHO}      | 0           |                 | Y           |             |
| Firefox 52.0         | GET (via XHR)          | {ECHO}      | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Firefox 58.0         | GET (via 2DCanvas)     |             | 0           |                 | Y           |             |
| Firefox 58.0         | GET (via BitmapCanvas) |             | 0           |                 | Y           |             |
| Firefox 58.0         | GET (via Iframe)       |             | 0           |                 | Y           |             |
| Firefox 58.0         | GET (via Object)       |             | 0           |                 | Y           |             |
| Firefox 58.0         | GET (via XHR)          |             | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Firefox 58.0         | GET (via 2DCanvas)     | *           | 1           |                 | Y           |             |
| Firefox 58.0         | GET (via BitmapCanvas) | *           | 1           |                 | Y           |             |
| Firefox 58.0         | GET (via Iframe)       | *           | 1           |                 | Y           |             |
| Firefox 58.0         | GET (via Object)       | *           | 1           |                 | Y           |             |
| Firefox 58.0         | GET (via XHR)          | *           | 1           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Firefox 58.0         | GET (via 2DCanvas)     | *           | 0           |                 | Y           |             |
| Firefox 58.0         | GET (via BitmapCanvas) | *           | 0           |                 | Y           |             |
| Firefox 58.0         | GET (via Iframe)       | *           | 0           |                 | Y           |             |
| Firefox 58.0         | GET (via Object)       | *           | 0           |                 | Y           |             |
| Firefox 58.0         | GET (via XHR)          | *           | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Firefox 58.0         | GET (via 2DCanvas)     | {ECHO}      | 1           |                 | Y           | Y           |
| Firefox 58.0         | GET (via BitmapCanvas) | {ECHO}      | 1           |                 | Y           | Y           |
| Firefox 58.0         | GET (via Iframe)       | {ECHO}      | 1           |                 | Y           |             |
| Firefox 58.0         | GET (via Object)       | {ECHO}      | 1           |                 | Y           |             |
| Firefox 58.0         | POST (via XHR)         | {ECHO}      | 1           | Y               | Y           | Y           |
| Firefox 58.0         | GET (via XHR)          | {ECHO}      | 1           |                 | Y           | Y           |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Firefox 58.0         | GET (via 2DCanvas)     | {ECHO}      | 0           |                 | Y           |             |
| Firefox 58.0         | GET (via BitmapCanvas) | {ECHO}      | 0           |                 | Y           |             |
| Firefox 58.0         | GET (via Iframe)       | {ECHO}      | 0           |                 | Y           |             |
| Firefox 58.0         | GET (via Object)       | {ECHO}      | 0           |                 | Y           |             |
| Firefox 58.0         | GET (via XHR)          | {ECHO}      | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Firefox 63.0         | GET (via 2DCanvas)     |             | 0           |                 | Y           |             |
| Firefox 63.0         | GET (via BitmapCanvas) |             | 0           |                 | Y           |             |
| Firefox 63.0         | GET (via Iframe)       |             | 0           |                 | Y           |             |
| Firefox 63.0         | GET (via Object)       |             | 0           |                 | Y           |             |
| Firefox 63.0         | GET (via XHR)          |             | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Firefox 63.0         | GET (via 2DCanvas)     | *           | 1           |                 | Y           |             |
| Firefox 63.0         | GET (via BitmapCanvas) | *           | 1           |                 | Y           |             |
| Firefox 63.0         | GET (via Iframe)       | *           | 1           |                 | Y           |             |
| Firefox 63.0         | GET (via Object)       | *           | 1           |                 | Y           |             |
| Firefox 63.0         | GET (via XHR)          | *           | 1           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Firefox 63.0         | GET (via 2DCanvas)     | *           | 0           |                 | Y           |             |
| Firefox 63.0         | GET (via BitmapCanvas) | *           | 0           |                 | Y           |             |
| Firefox 63.0         | GET (via Iframe)       | *           | 0           |                 | Y           |             |
| Firefox 63.0         | GET (via Object)       | *           | 0           |                 | Y           |             |
| Firefox 63.0         | GET (via XHR)          | *           | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Firefox 63.0         | GET (via 2DCanvas)     | {ECHO}      | 1           |                 | Y           | Y           |
| Firefox 63.0         | GET (via BitmapCanvas) | {ECHO}      | 1           |                 | Y           | Y           |
| Firefox 63.0         | GET (via Iframe)       | {ECHO}      | 1           |                 | Y           |             |
| Firefox 63.0         | GET (via Object)       | {ECHO}      | 1           |                 | Y           |             |
| Firefox 63.0         | POST (via XHR)         | {ECHO}      | 1           | Y               | Y           | Y           |
| Firefox 63.0         | GET (via XHR)          | {ECHO}      | 1           |                 | Y           | Y           |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Firefox 63.0         | GET (via 2DCanvas)     | {ECHO}      | 0           |                 | Y           |             |
| Firefox 63.0         | GET (via BitmapCanvas) | {ECHO}      | 0           |                 | Y           |             |
| Firefox 63.0         | GET (via Iframe)       | {ECHO}      | 0           |                 | Y           |             |
| Firefox 63.0         | GET (via Object)       | {ECHO}      | 0           |                 | Y           |             |
| Firefox 63.0         | GET (via XHR)          | {ECHO}      | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| IE 10.0 (Win 6.1)    | GET (via 2DCanvas)     |             | 0           |                 | Y           |             |
| IE 10.0 (Win 6.1)    | GET (via BitmapCanvas) |             | 0           |                 | Y           |             |
| IE 10.0 (Win 6.1)    | GET (via Iframe)       |             | 0           |                 | Y           |             |
| IE 10.0 (Win 6.1)    | HEAD (via Object)      |             | 0           |                 | Y           |             |
| IE 10.0 (Win 6.1)    | GET (via Object)       |             | 0           |                 | Y           |             |
| IE 10.0 (Win 6.1)    | GET (via XHR)          |             | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| IE 10.0 (Win 6.1)    | GET (via 2DCanvas)     | *           | 1           |                 | Y           |             |
| IE 10.0 (Win 6.1)    | GET (via BitmapCanvas) | *           | 1           |                 | Y           |             |
| IE 10.0 (Win 6.1)    | GET (via Iframe)       | *           | 1           |                 | Y           |             |
| IE 10.0 (Win 6.1)    | HEAD (via Object)      | *           | 1           |                 | Y           |             |
| IE 10.0 (Win 6.1)    | GET (via Object)       | *           | 1           |                 | Y           |             |
| IE 10.0 (Win 6.1)    | GET (via XHR)          | *           | 1           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| IE 10.0 (Win 6.1)    | GET (via 2DCanvas)     | *           | 0           |                 | Y           |             |
| IE 10.0 (Win 6.1)    | GET (via BitmapCanvas) | *           | 0           |                 | Y           |             |
| IE 10.0 (Win 6.1)    | GET (via Iframe)       | *           | 0           |                 | Y           |             |
| IE 10.0 (Win 6.1)    | HEAD (via Object)      | *           | 0           |                 | Y           |             |
| IE 10.0 (Win 6.1)    | GET (via Object)       | *           | 0           |                 | Y           |             |
| IE 10.0 (Win 6.1)    | GET (via XHR)          | *           | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| IE 10.0 (Win 6.1)    | GET (via 2DCanvas)     | {ECHO}      | 1           |                 | Y           |             |
| IE 10.0 (Win 6.1)    | GET (via BitmapCanvas) | {ECHO}      | 1           |                 | Y           |             |
| IE 10.0 (Win 6.1)    | GET (via Iframe)       | {ECHO}      | 1           |                 | Y           |             |
| IE 10.0 (Win 6.1)    | GET (via Object)       | {ECHO}      | 1           |                 | Y           |             |
| IE 10.0 (Win 6.1)    | HEAD (via Object)      | {ECHO}      | 1           |                 | Y           |             |
| IE 10.0 (Win 6.1)    | GET (via XHR)          | {ECHO}      | 1           |                 | Y           | Y           |
| IE 10.0 (Win 6.1)    | POST (via XHR)         | {ECHO}      | 1           | Y               | Y           | Y           |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| IE 10.0 (Win 6.1)    | GET (via 2DCanvas)     | {ECHO}      | 0           |                 | Y           |             |
| IE 10.0 (Win 6.1)    | GET (via BitmapCanvas) | {ECHO}      | 0           |                 | Y           |             |
| IE 10.0 (Win 6.1)    | GET (via Iframe)       | {ECHO}      | 0           |                 | Y           |             |
| IE 10.0 (Win 6.1)    | GET (via Object)       | {ECHO}      | 0           |                 | Y           |             |
| IE 10.0 (Win 6.1)    | HEAD (via Object)      | {ECHO}      | 0           |                 | Y           |             |
| IE 10.0 (Win 6.1)    | GET (via XHR)          | {ECHO}      | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| IE 11.0 (Win 10.0)   | GET (via 2DCanvas)     |             | 0           |                 | Y           |             |
| IE 11.0 (Win 10.0)   | GET (via BitmapCanvas) |             | 0           |                 | Y           |             |
| IE 11.0 (Win 10.0)   | GET (via Iframe)       |             | 0           |                 | Y           |             |
| IE 11.0 (Win 10.0)   | GET (via Object)       |             | 0           |                 | Y           |             |
| IE 11.0 (Win 10.0)   | HEAD (via Object)      |             | 0           |                 | Y           |             |
| IE 11.0 (Win 10.0)   | GET (via XHR)          |             | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| IE 11.0 (Win 10.0)   | GET (via 2DCanvas)     | *           | 1           |                 | Y           |             |
| IE 11.0 (Win 10.0)   | GET (via BitmapCanvas) | *           | 1           |                 | Y           |             |
| IE 11.0 (Win 10.0)   | GET (via Iframe)       | *           | 1           |                 | Y           |             |
| IE 11.0 (Win 10.0)   | GET (via Object)       | *           | 1           |                 | Y           |             |
| IE 11.0 (Win 10.0)   | HEAD (via Object)      | *           | 1           |                 | Y           |             |
| IE 11.0 (Win 10.0)   | GET (via XHR)          | *           | 1           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| IE 11.0 (Win 10.0)   | GET (via 2DCanvas)     | *           | 0           |                 | Y           |             |
| IE 11.0 (Win 10.0)   | GET (via BitmapCanvas) | *           | 0           |                 | Y           |             |
| IE 11.0 (Win 10.0)   | GET (via Iframe)       | *           | 0           |                 | Y           |             |
| IE 11.0 (Win 10.0)   | HEAD (via Object)      | *           | 0           |                 | Y           |             |
| IE 11.0 (Win 10.0)   | GET (via Object)       | *           | 0           |                 | Y           |             |
| IE 11.0 (Win 10.0)   | GET (via XHR)          | *           | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| IE 11.0 (Win 10.0)   | GET (via 2DCanvas)     | {ECHO}      | 1           |                 | Y           | Y           |
| IE 11.0 (Win 10.0)   | GET (via BitmapCanvas) | {ECHO}      | 1           |                 | Y           |             |
| IE 11.0 (Win 10.0)   | GET (via Iframe)       | {ECHO}      | 1           |                 | Y           |             |
| IE 11.0 (Win 10.0)   | GET (via Object)       | {ECHO}      | 1           |                 | Y           |             |
| IE 11.0 (Win 10.0)   | HEAD (via Object)      | {ECHO}      | 1           |                 | Y           |             |
| IE 11.0 (Win 10.0)   | POST (via XHR)         | {ECHO}      | 1           | Y               | Y           | Y           |
| IE 11.0 (Win 10.0)   | GET (via XHR)          | {ECHO}      | 1           |                 | Y           | Y           |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| IE 11.0 (Win 10.0)   | GET (via 2DCanvas)     | {ECHO}      | 0           |                 | Y           |             |
| IE 11.0 (Win 10.0)   | GET (via BitmapCanvas) | {ECHO}      | 0           |                 | Y           |             |
| IE 11.0 (Win 10.0)   | GET (via Iframe)       | {ECHO}      | 0           |                 | Y           |             |
| IE 11.0 (Win 10.0)   | HEAD (via Object)      | {ECHO}      | 0           |                 | Y           |             |
| IE 11.0 (Win 10.0)   | GET (via Object)       | {ECHO}      | 0           |                 | Y           |             |
| IE 11.0 (Win 10.0)   | GET (via XHR)          | {ECHO}      | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| IE 11.0 (Win 6.3)    | GET (via 2DCanvas)     |             | 0           |                 | Y           |             |
| IE 11.0 (Win 6.3)    | GET (via BitmapCanvas) |             | 0           |                 | Y           |             |
| IE 11.0 (Win 6.3)    | GET (via Iframe)       |             | 0           |                 | Y           |             |
| IE 11.0 (Win 6.3)    | HEAD (via Object)      |             | 0           |                 | Y           |             |
| IE 11.0 (Win 6.3)    | GET (via Object)       |             | 0           |                 | Y           |             |
| IE 11.0 (Win 6.3)    | GET (via XHR)          |             | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| IE 11.0 (Win 6.3)    | GET (via 2DCanvas)     | *           | 1           |                 | Y           |             |
| IE 11.0 (Win 6.3)    | GET (via BitmapCanvas) | *           | 1           |                 | Y           |             |
| IE 11.0 (Win 6.3)    | GET (via Iframe)       | *           | 1           |                 | Y           |             |
| IE 11.0 (Win 6.3)    | GET (via Object)       | *           | 1           |                 | Y           |             |
| IE 11.0 (Win 6.3)    | HEAD (via Object)      | *           | 1           |                 | Y           |             |
| IE 11.0 (Win 6.3)    | GET (via XHR)          | *           | 1           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| IE 11.0 (Win 6.3)    | GET (via 2DCanvas)     | *           | 0           |                 | Y           |             |
| IE 11.0 (Win 6.3)    | GET (via BitmapCanvas) | *           | 0           |                 | Y           |             |
| IE 11.0 (Win 6.3)    | GET (via Iframe)       | *           | 0           |                 | Y           |             |
| IE 11.0 (Win 6.3)    | HEAD (via Object)      | *           | 0           |                 | Y           |             |
| IE 11.0 (Win 6.3)    | GET (via Object)       | *           | 0           |                 | Y           |             |
| IE 11.0 (Win 6.3)    | GET (via XHR)          | *           | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| IE 11.0 (Win 6.3)    | GET (via 2DCanvas)     | {ECHO}      | 1           |                 | Y           | Y           |
| IE 11.0 (Win 6.3)    | GET (via BitmapCanvas) | {ECHO}      | 1           |                 | Y           |             |
| IE 11.0 (Win 6.3)    | GET (via Iframe)       | {ECHO}      | 1           |                 | Y           |             |
| IE 11.0 (Win 6.3)    | HEAD (via Object)      | {ECHO}      | 1           |                 | Y           |             |
| IE 11.0 (Win 6.3)    | GET (via Object)       | {ECHO}      | 1           |                 | Y           |             |
| IE 11.0 (Win 6.3)    | POST (via XHR)         | {ECHO}      | 1           | Y               | Y           | Y           |
| IE 11.0 (Win 6.3)    | GET (via XHR)          | {ECHO}      | 1           |                 | Y           | Y           |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| IE 11.0 (Win 6.3)    | GET (via 2DCanvas)     | {ECHO}      | 0           |                 | Y           |             |
| IE 11.0 (Win 6.3)    | GET (via BitmapCanvas) | {ECHO}      | 0           |                 | Y           |             |
| IE 11.0 (Win 6.3)    | GET (via Iframe)       | {ECHO}      | 0           |                 | Y           |             |
| IE 11.0 (Win 6.3)    | GET (via Object)       | {ECHO}      | 0           |                 | Y           |             |
| IE 11.0 (Win 6.3)    | HEAD (via Object)      | {ECHO}      | 0           |                 | Y           |             |
| IE 11.0 (Win 6.3)    | GET (via XHR)          | {ECHO}      | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| IE 6.0 (Win 6.2)     | GET (via 2DCanvas)     |             | 0           |                 | Y           |             |
| IE 6.0 (Win 6.2)     | GET (via BitmapCanvas) |             | 0           |                 | Y           |             |
| IE 6.0 (Win 6.2)     | GET (via Iframe)       |             | 0           |                 | Y           |             |
| IE 6.0 (Win 6.2)     | GET (via Object)       |             | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| IE 6.0 (Win 6.2)     | GET (via 2DCanvas)     | *           | 1           |                 | Y           |             |
| IE 6.0 (Win 6.2)     | GET (via BitmapCanvas) | *           | 1           |                 | Y           |             |
| IE 6.0 (Win 6.2)     | GET (via Iframe)       | *           | 1           |                 | Y           |             |
| IE 6.0 (Win 6.2)     | GET (via Object)       | *           | 1           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| IE 6.0 (Win 6.2)     | GET (via 2DCanvas)     | *           | 0           |                 | Y           |             |
| IE 6.0 (Win 6.2)     | GET (via BitmapCanvas) | *           | 0           |                 | Y           |             |
| IE 6.0 (Win 6.2)     | GET (via Iframe)       | *           | 0           |                 | Y           |             |
| IE 6.0 (Win 6.2)     | GET (via Object)       | *           | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| IE 6.0 (Win 6.2)     | GET (via 2DCanvas)     | {ECHO}      | 1           |                 | Y           |             |
| IE 6.0 (Win 6.2)     | GET (via BitmapCanvas) | {ECHO}      | 1           |                 | Y           |             |
| IE 6.0 (Win 6.2)     | GET (via Iframe)       | {ECHO}      | 1           |                 | Y           |             |
| IE 6.0 (Win 6.2)     | GET (via Object)       | {ECHO}      | 1           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| IE 6.0 (Win 6.2)     | GET (via 2DCanvas)     | {ECHO}      | 0           |                 | Y           |             |
| IE 6.0 (Win 6.2)     | GET (via BitmapCanvas) | {ECHO}      | 0           |                 | Y           |             |
| IE 6.0 (Win 6.2)     | GET (via Iframe)       | {ECHO}      | 0           |                 | Y           |             |
| IE 6.0 (Win 6.2)     | GET (via Object)       | {ECHO}      | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| IE 7.0 (Win 6.0)     | GET (via 2DCanvas)     |             | 0           |                 | Y           |             |
| IE 7.0 (Win 6.0)     | GET (via BitmapCanvas) |             | 0           |                 | Y           |             |
| IE 7.0 (Win 6.0)     | GET (via Iframe)       |             | 0           |                 | Y           |             |
| IE 7.0 (Win 6.0)     | GET (via Object)       |             | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| IE 7.0 (Win 6.0)     | GET (via 2DCanvas)     | *           | 1           |                 | Y           |             |
| IE 7.0 (Win 6.0)     | GET (via BitmapCanvas) | *           | 1           |                 | Y           |             |
| IE 7.0 (Win 6.0)     | GET (via Iframe)       | *           | 1           |                 | Y           |             |
| IE 7.0 (Win 6.0)     | GET (via Object)       | *           | 1           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| IE 7.0 (Win 6.0)     | GET (via 2DCanvas)     | *           | 0           |                 | Y           |             |
| IE 7.0 (Win 6.0)     | GET (via BitmapCanvas) | *           | 0           |                 | Y           |             |
| IE 7.0 (Win 6.0)     | GET (via Iframe)       | *           | 0           |                 | Y           |             |
| IE 7.0 (Win 6.0)     | GET (via Object)       | *           | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| IE 7.0 (Win 6.0)     | GET (via 2DCanvas)     | {ECHO}      | 1           |                 | Y           |             |
| IE 7.0 (Win 6.0)     | GET (via BitmapCanvas) | {ECHO}      | 1           |                 | Y           |             |
| IE 7.0 (Win 6.0)     | GET (via Iframe)       | {ECHO}      | 1           |                 | Y           |             |
| IE 7.0 (Win 6.0)     | GET (via Object)       | {ECHO}      | 1           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| IE 7.0 (Win 6.0)     | GET (via 2DCanvas)     | {ECHO}      | 0           |                 | Y           |             |
| IE 7.0 (Win 6.0)     | GET (via BitmapCanvas) | {ECHO}      | 0           |                 | Y           |             |
| IE 7.0 (Win 6.0)     | GET (via Iframe)       | {ECHO}      | 0           |                 | Y           |             |
| IE 7.0 (Win 6.0)     | GET (via Object)       | {ECHO}      | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| IE 8.0 (Win 6.1)     | GET (via 2DCanvas)     |             | 0           |                 | Y           |             |
| IE 8.0 (Win 6.1)     | GET (via BitmapCanvas) |             | 0           |                 | Y           |             |
| IE 8.0 (Win 6.1)     | GET (via Iframe)       |             | 0           |                 | Y           |             |
| IE 8.0 (Win 6.1)     | GET (via Object)       |             | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| IE 8.0 (Win 6.1)     | GET (via 2DCanvas)     | *           | 1           |                 | Y           |             |
| IE 8.0 (Win 6.1)     | GET (via BitmapCanvas) | *           | 1           |                 | Y           |             |
| IE 8.0 (Win 6.1)     | GET (via Iframe)       | *           | 1           |                 | Y           |             |
| IE 8.0 (Win 6.1)     | GET (via Object)       | *           | 1           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| IE 8.0 (Win 6.1)     | GET (via 2DCanvas)     | *           | 0           |                 | Y           |             |
| IE 8.0 (Win 6.1)     | GET (via BitmapCanvas) | *           | 0           |                 | Y           |             |
| IE 8.0 (Win 6.1)     | GET (via Iframe)       | *           | 0           |                 | Y           |             |
| IE 8.0 (Win 6.1)     | GET (via Object)       | *           | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| IE 8.0 (Win 6.1)     | GET (via 2DCanvas)     | {ECHO}      | 1           |                 | Y           |             |
| IE 8.0 (Win 6.1)     | GET (via BitmapCanvas) | {ECHO}      | 1           |                 | Y           |             |
| IE 8.0 (Win 6.1)     | GET (via Iframe)       | {ECHO}      | 1           |                 | Y           |             |
| IE 8.0 (Win 6.1)     | GET (via Object)       | {ECHO}      | 1           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| IE 8.0 (Win 6.1)     | GET (via 2DCanvas)     | {ECHO}      | 0           |                 | Y           |             |
| IE 8.0 (Win 6.1)     | GET (via BitmapCanvas) | {ECHO}      | 0           |                 | Y           |             |
| IE 8.0 (Win 6.1)     | GET (via Iframe)       | {ECHO}      | 0           |                 | Y           |             |
| IE 8.0 (Win 6.1)     | GET (via Object)       | {ECHO}      | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| IE 9.0 (Win 6.1)     | GET (via 2DCanvas)     |             | 0           |                 | Y           |             |
| IE 9.0 (Win 6.1)     | GET (via BitmapCanvas) |             | 0           |                 | Y           |             |
| IE 9.0 (Win 6.1)     | GET (via Iframe)       |             | 0           |                 | Y           |             |
| IE 9.0 (Win 6.1)     | GET (via Object)       |             | 0           |                 | Y           |             |
| IE 9.0 (Win 6.1)     | HEAD (via Object)      |             | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| IE 9.0 (Win 6.1)     | GET (via 2DCanvas)     | *           | 1           |                 | Y           |             |
| IE 9.0 (Win 6.1)     | GET (via BitmapCanvas) | *           | 1           |                 | Y           |             |
| IE 9.0 (Win 6.1)     | GET (via Iframe)       | *           | 1           |                 | Y           |             |
| IE 9.0 (Win 6.1)     | HEAD (via Object)      | *           | 1           |                 | Y           |             |
| IE 9.0 (Win 6.1)     | GET (via Object)       | *           | 1           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| IE 9.0 (Win 6.1)     | GET (via 2DCanvas)     | *           | 0           |                 | Y           |             |
| IE 9.0 (Win 6.1)     | GET (via BitmapCanvas) | *           | 0           |                 | Y           |             |
| IE 9.0 (Win 6.1)     | GET (via Iframe)       | *           | 0           |                 | Y           |             |
| IE 9.0 (Win 6.1)     | GET (via Object)       | *           | 0           |                 | Y           |             |
| IE 9.0 (Win 6.1)     | HEAD (via Object)      | *           | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| IE 9.0 (Win 6.1)     | GET (via 2DCanvas)     | {ECHO}      | 1           |                 | Y           |             |
| IE 9.0 (Win 6.1)     | GET (via BitmapCanvas) | {ECHO}      | 1           |                 | Y           |             |
| IE 9.0 (Win 6.1)     | GET (via Iframe)       | {ECHO}      | 1           |                 | Y           |             |
| IE 9.0 (Win 6.1)     | HEAD (via Object)      | {ECHO}      | 1           |                 | Y           |             |
| IE 9.0 (Win 6.1)     | GET (via Object)       | {ECHO}      | 1           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| IE 9.0 (Win 6.1)     | GET (via 2DCanvas)     | {ECHO}      | 0           |                 | Y           |             |
| IE 9.0 (Win 6.1)     | GET (via BitmapCanvas) | {ECHO}      | 0           |                 | Y           |             |
| IE 9.0 (Win 6.1)     | GET (via Iframe)       | {ECHO}      | 0           |                 | Y           |             |
| IE 9.0 (Win 6.1)     | HEAD (via Object)      | {ECHO}      | 0           |                 | Y           |             |
| IE 9.0 (Win 6.1)     | GET (via Object)       | {ECHO}      | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Opera 10.00          | GET (via 2DCanvas)     |             | 0           |                 | Y           |             |
| Opera 10.00          | GET (via BitmapCanvas) |             | 0           |                 | Y           |             |
| Opera 10.00          | GET (via Iframe)       |             | 0           |                 | Y           |             |
| Opera 10.00          | GET (via Object)       |             | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Opera 10.00          | GET (via 2DCanvas)     | *           | 1           |                 | Y           |             |
| Opera 10.00          | GET (via BitmapCanvas) | *           | 1           |                 | Y           |             |
| Opera 10.00          | GET (via Iframe)       | *           | 1           |                 | Y           |             |
| Opera 10.00          | GET (via Object)       | *           | 1           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Opera 10.00          | GET (via 2DCanvas)     | *           | 0           |                 | Y           |             |
| Opera 10.00          | GET (via BitmapCanvas) | *           | 0           |                 | Y           |             |
| Opera 10.00          | GET (via Iframe)       | *           | 0           |                 | Y           |             |
| Opera 10.00          | GET (via Object)       | *           | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Opera 10.00          | GET (via 2DCanvas)     | {ECHO}      | 1           |                 | Y           |             |
| Opera 10.00          | GET (via BitmapCanvas) | {ECHO}      | 1           |                 | Y           |             |
| Opera 10.00          | GET (via Iframe)       | {ECHO}      | 1           |                 | Y           |             |
| Opera 10.00          | GET (via Object)       | {ECHO}      | 1           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Opera 10.00          | GET (via 2DCanvas)     | {ECHO}      | 0           |                 | Y           |             |
| Opera 10.00          | GET (via BitmapCanvas) | {ECHO}      | 0           |                 | Y           |             |
| Opera 10.00          | GET (via Iframe)       | {ECHO}      | 0           |                 | Y           |             |
| Opera 10.00          | GET (via Object)       | {ECHO}      | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Opera 10.10          | GET (via 2DCanvas)     |             | 0           |                 | Y           |             |
| Opera 10.10          | GET (via BitmapCanvas) |             | 0           |                 | Y           |             |
| Opera 10.10          | GET (via Iframe)       |             | 0           |                 | Y           |             |
| Opera 10.10          | GET (via Object)       |             | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Opera 10.10          | GET (via 2DCanvas)     | *           | 1           |                 | Y           |             |
| Opera 10.10          | GET (via BitmapCanvas) | *           | 1           |                 | Y           |             |
| Opera 10.10          | GET (via Iframe)       | *           | 1           |                 | Y           |             |
| Opera 10.10          | GET (via Object)       | *           | 1           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Opera 10.10          | GET (via 2DCanvas)     | *           | 0           |                 | Y           |             |
| Opera 10.10          | GET (via BitmapCanvas) | *           | 0           |                 | Y           |             |
| Opera 10.10          | GET (via Iframe)       | *           | 0           |                 | Y           |             |
| Opera 10.10          | GET (via Object)       | *           | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Opera 10.10          | GET (via 2DCanvas)     | {ECHO}      | 1           |                 | Y           |             |
| Opera 10.10          | GET (via BitmapCanvas) | {ECHO}      | 1           |                 | Y           |             |
| Opera 10.10          | GET (via Iframe)       | {ECHO}      | 1           |                 | Y           |             |
| Opera 10.10          | GET (via Object)       | {ECHO}      | 1           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Opera 10.10          | GET (via 2DCanvas)     | {ECHO}      | 0           |                 | Y           |             |
| Opera 10.10          | GET (via BitmapCanvas) | {ECHO}      | 0           |                 | Y           |             |
| Opera 10.10          | GET (via Iframe)       | {ECHO}      | 0           |                 | Y           |             |
| Opera 10.10          | GET (via Object)       | {ECHO}      | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Opera 10.50          | GET (via 2DCanvas)     |             | 0           |                 | Y           |             |
| Opera 10.50          | GET (via BitmapCanvas) |             | 0           |                 | Y           |             |
| Opera 10.50          | GET (via Iframe)       |             | 0           |                 | Y           |             |
| Opera 10.50          | GET (via Object)       |             | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Opera 10.50          | GET (via 2DCanvas)     | *           | 1           |                 | Y           |             |
| Opera 10.50          | GET (via BitmapCanvas) | *           | 1           |                 | Y           |             |
| Opera 10.50          | GET (via Iframe)       | *           | 1           |                 | Y           |             |
| Opera 10.50          | GET (via Object)       | *           | 1           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Opera 10.50          | GET (via 2DCanvas)     | *           | 0           |                 | Y           |             |
| Opera 10.50          | GET (via BitmapCanvas) | *           | 0           |                 | Y           |             |
| Opera 10.50          | GET (via Iframe)       | *           | 0           |                 | Y           |             |
| Opera 10.50          | GET (via Object)       | *           | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Opera 10.50          | GET (via 2DCanvas)     | {ECHO}      | 1           |                 | Y           |             |
| Opera 10.50          | GET (via BitmapCanvas) | {ECHO}      | 1           |                 | Y           |             |
| Opera 10.50          | GET (via Iframe)       | {ECHO}      | 1           |                 | Y           |             |
| Opera 10.50          | GET (via Object)       | {ECHO}      | 1           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Opera 10.50          | GET (via 2DCanvas)     | {ECHO}      | 0           |                 | Y           |             |
| Opera 10.50          | GET (via BitmapCanvas) | {ECHO}      | 0           |                 | Y           |             |
| Opera 10.50          | GET (via Iframe)       | {ECHO}      | 0           |                 | Y           |             |
| Opera 10.50          | GET (via Object)       | {ECHO}      | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Opera 11.00          | GET (via 2DCanvas)     |             | 0           |                 | Y           |             |
| Opera 11.00          | GET (via BitmapCanvas) |             | 0           |                 | Y           |             |
| Opera 11.00          | GET (via Iframe)       |             | 0           |                 | Y           |             |
| Opera 11.00          | GET (via Object)       |             | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Opera 11.00          | GET (via 2DCanvas)     | *           | 1           |                 | Y           |             |
| Opera 11.00          | GET (via BitmapCanvas) | *           | 1           |                 | Y           |             |
| Opera 11.00          | GET (via Iframe)       | *           | 1           |                 | Y           |             |
| Opera 11.00          | GET (via Object)       | *           | 1           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Opera 11.00          | GET (via 2DCanvas)     | *           | 0           |                 | Y           |             |
| Opera 11.00          | GET (via BitmapCanvas) | *           | 0           |                 | Y           |             |
| Opera 11.00          | GET (via Iframe)       | *           | 0           |                 | Y           |             |
| Opera 11.00          | GET (via Object)       | *           | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Opera 11.00          | GET (via 2DCanvas)     | {ECHO}      | 1           |                 | Y           |             |
| Opera 11.00          | GET (via BitmapCanvas) | {ECHO}      | 1           |                 | Y           |             |
| Opera 11.00          | GET (via Iframe)       | {ECHO}      | 1           |                 | Y           |             |
| Opera 11.00          | GET (via Object)       | {ECHO}      | 1           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Opera 11.00          | GET (via 2DCanvas)     | {ECHO}      | 0           |                 | Y           |             |
| Opera 11.00          | GET (via BitmapCanvas) | {ECHO}      | 0           |                 | Y           |             |
| Opera 11.00          | GET (via Iframe)       | {ECHO}      | 0           |                 | Y           |             |
| Opera 11.00          | GET (via Object)       | {ECHO}      | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Opera 11.52          | GET (via 2DCanvas)     |             | 0           |                 | Y           |             |
| Opera 11.52          | GET (via BitmapCanvas) |             | 0           |                 | Y           |             |
| Opera 11.52          | GET (via Iframe)       |             | 0           |                 | Y           |             |
| Opera 11.52          | GET (via Object)       |             | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Opera 11.52          | GET (via 2DCanvas)     | *           | 1           |                 | Y           |             |
| Opera 11.52          | GET (via BitmapCanvas) | *           | 1           |                 | Y           |             |
| Opera 11.52          | GET (via Iframe)       | *           | 1           |                 | Y           |             |
| Opera 11.52          | GET (via Object)       | *           | 1           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Opera 11.52          | GET (via 2DCanvas)     | *           | 0           |                 | Y           |             |
| Opera 11.52          | GET (via BitmapCanvas) | *           | 0           |                 | Y           |             |
| Opera 11.52          | GET (via Iframe)       | *           | 0           |                 | Y           |             |
| Opera 11.52          | GET (via Object)       | *           | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Opera 11.52          | GET (via 2DCanvas)     | {ECHO}      | 1           |                 | Y           |             |
| Opera 11.52          | GET (via BitmapCanvas) | {ECHO}      | 1           |                 | Y           |             |
| Opera 11.52          | GET (via Iframe)       | {ECHO}      | 1           |                 | Y           |             |
| Opera 11.52          | GET (via Object)       | {ECHO}      | 1           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Opera 11.52          | GET (via 2DCanvas)     | {ECHO}      | 0           |                 | Y           |             |
| Opera 11.52          | GET (via BitmapCanvas) | {ECHO}      | 0           |                 | Y           |             |
| Opera 11.52          | GET (via Iframe)       | {ECHO}      | 0           |                 | Y           |             |
| Opera 11.52          | GET (via Object)       | {ECHO}      | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Opera 12.10          | GET (via 2DCanvas)     |             | 0           |                 | Y           |             |
| Opera 12.10          | GET (via BitmapCanvas) |             | 0           |                 | Y           |             |
| Opera 12.10          | GET (via Iframe)       |             | 0           |                 | Y           |             |
| Opera 12.10          | GET (via Object)       |             | 0           |                 | Y           |             |
| Opera 12.10          | GET (via XHR)          |             | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Opera 12.10          | GET (via 2DCanvas)     | *           | 1           |                 | Y           |             |
| Opera 12.10          | GET (via BitmapCanvas) | *           | 1           |                 | Y           |             |
| Opera 12.10          | GET (via Iframe)       | *           | 1           |                 | Y           |             |
| Opera 12.10          | GET (via Object)       | *           | 1           |                 | Y           |             |
| Opera 12.10          | GET (via XHR)          | *           | 1           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Opera 12.10          | GET (via 2DCanvas)     | *           | 0           |                 | Y           |             |
| Opera 12.10          | GET (via BitmapCanvas) | *           | 0           |                 | Y           |             |
| Opera 12.10          | GET (via Iframe)       | *           | 0           |                 | Y           |             |
| Opera 12.10          | GET (via Object)       | *           | 0           |                 | Y           |             |
| Opera 12.10          | GET (via XHR)          | *           | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Opera 12.10          | GET (via 2DCanvas)     | {ECHO}      | 1           |                 | Y           | Y           |
| Opera 12.10          | GET (via BitmapCanvas) | {ECHO}      | 1           |                 | Y           |             |
| Opera 12.10          | GET (via Iframe)       | {ECHO}      | 1           |                 | Y           |             |
| Opera 12.10          | GET (via Object)       | {ECHO}      | 1           |                 | Y           |             |
| Opera 12.10          | GET (via XHR)          | {ECHO}      | 1           |                 | Y           | Y           |
| Opera 12.10          | POST (via XHR)         | {ECHO}      | 1           | Y (with Cookie) | Y           | Y           |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Opera 12.10          | GET (via 2DCanvas)     | {ECHO}      | 0           |                 | Y           |             |
| Opera 12.10          | GET (via BitmapCanvas) | {ECHO}      | 0           |                 | Y           |             |
| Opera 12.10          | GET (via Iframe)       | {ECHO}      | 0           |                 | Y           |             |
| Opera 12.10          | GET (via Object)       | {ECHO}      | 0           |                 | Y           |             |
| Opera 12.10          | GET (via XHR)          | {ECHO}      | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Opera 17.0.1241.45   | GET (via 2DCanvas)     |             | 0           |                 | Y           |             |
| Opera 17.0.1241.45   | GET (via BitmapCanvas) |             | 0           |                 | Y           |             |
| Opera 17.0.1241.45   | GET (via Iframe)       |             | 0           |                 | Y           |             |
| Opera 17.0.1241.45   | GET (via Object)       |             | 0           |                 | Y           |             |
| Opera 17.0.1241.45   | GET (via XHR)          |             | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Opera 17.0.1241.45   | GET (via 2DCanvas)     | *           | 1           |                 | Y           |             |
| Opera 17.0.1241.45   | GET (via BitmapCanvas) | *           | 1           |                 | Y           |             |
| Opera 17.0.1241.45   | GET (via Iframe)       | *           | 1           |                 | Y           |             |
| Opera 17.0.1241.45   | GET (via Object)       | *           | 1           |                 | Y           |             |
| Opera 17.0.1241.45   | GET (via XHR)          | *           | 1           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Opera 17.0.1241.45   | GET (via 2DCanvas)     | *           | 0           |                 | Y           |             |
| Opera 17.0.1241.45   | GET (via BitmapCanvas) | *           | 0           |                 | Y           |             |
| Opera 17.0.1241.45   | GET (via Iframe)       | *           | 0           |                 | Y           |             |
| Opera 17.0.1241.45   | GET (via Object)       | *           | 0           |                 | Y           |             |
| Opera 17.0.1241.45   | GET (via XHR)          | *           | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Opera 17.0.1241.45   | GET (via 2DCanvas)     | {ECHO}      | 1           |                 | Y           | Y           |
| Opera 17.0.1241.45   | GET (via BitmapCanvas) | {ECHO}      | 1           |                 | Y           |             |
| Opera 17.0.1241.45   | GET (via Iframe)       | {ECHO}      | 1           |                 | Y           |             |
| Opera 17.0.1241.45   | GET (via Object)       | {ECHO}      | 1           |                 | Y           |             |
| Opera 17.0.1241.45   | POST (via XHR)         | {ECHO}      | 1           | Y               | Y           | Y           |
| Opera 17.0.1241.45   | GET (via XHR)          | {ECHO}      | 1           |                 | Y           | Y           |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Opera 17.0.1241.45   | GET (via 2DCanvas)     | {ECHO}      | 0           |                 | Y           |             |
| Opera 17.0.1241.45   | GET (via BitmapCanvas) | {ECHO}      | 0           |                 | Y           |             |
| Opera 17.0.1241.45   | GET (via Iframe)       | {ECHO}      | 0           |                 | Y           |             |
| Opera 17.0.1241.45   | GET (via Object)       | {ECHO}      | 0           |                 | Y           |             |
| Opera 17.0.1241.45   | GET (via XHR)          | {ECHO}      | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Opera 24.0.1558.53   | GET (via 2DCanvas)     |             | 0           |                 | Y           |             |
| Opera 24.0.1558.53   | GET (via BitmapCanvas) |             | 0           |                 | Y           |             |
| Opera 24.0.1558.53   | GET (via Iframe)       |             | 0           |                 | Y           |             |
| Opera 24.0.1558.53   | GET (via Object)       |             | 0           |                 | Y           |             |
| Opera 24.0.1558.53   | GET (via XHR)          |             | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Opera 24.0.1558.53   | GET (via 2DCanvas)     | *           | 1           |                 | Y           |             |
| Opera 24.0.1558.53   | GET (via BitmapCanvas) | *           | 1           |                 | Y           |             |
| Opera 24.0.1558.53   | GET (via Iframe)       | *           | 1           |                 | Y           |             |
| Opera 24.0.1558.53   | GET (via Object)       | *           | 1           |                 | Y           |             |
| Opera 24.0.1558.53   | GET (via XHR)          | *           | 1           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Opera 24.0.1558.53   | GET (via 2DCanvas)     | *           | 0           |                 | Y           |             |
| Opera 24.0.1558.53   | GET (via BitmapCanvas) | *           | 0           |                 | Y           |             |
| Opera 24.0.1558.53   | GET (via Iframe)       | *           | 0           |                 | Y           |             |
| Opera 24.0.1558.53   | GET (via Object)       | *           | 0           |                 | Y           |             |
| Opera 24.0.1558.53   | GET (via XHR)          | *           | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Opera 24.0.1558.53   | GET (via 2DCanvas)     | {ECHO}      | 1           |                 | Y           | Y           |
| Opera 24.0.1558.53   | GET (via BitmapCanvas) | {ECHO}      | 1           |                 | Y           |             |
| Opera 24.0.1558.53   | GET (via Iframe)       | {ECHO}      | 1           |                 | Y           |             |
| Opera 24.0.1558.53   | GET (via Object)       | {ECHO}      | 1           |                 | Y           |             |
| Opera 24.0.1558.53   | GET (via XHR)          | {ECHO}      | 1           |                 | Y           | Y           |
| Opera 24.0.1558.53   | POST (via XHR)         | {ECHO}      | 1           | Y               | Y           | Y           |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Opera 24.0.1558.53   | GET (via 2DCanvas)     | {ECHO}      | 0           |                 | Y           |             |
| Opera 24.0.1558.53   | GET (via BitmapCanvas) | {ECHO}      | 0           |                 | Y           |             |
| Opera 24.0.1558.53   | GET (via Iframe)       | {ECHO}      | 0           |                 | Y           |             |
| Opera 24.0.1558.53   | GET (via Object)       | {ECHO}      | 0           |                 | Y           |             |
| Opera 24.0.1558.53   | GET (via XHR)          | {ECHO}      | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Opera 32.0.1948.25   | GET (via 2DCanvas)     |             | 0           |                 | Y           |             |
| Opera 32.0.1948.25   | GET (via BitmapCanvas) |             | 0           |                 | Y           |             |
| Opera 32.0.1948.25   | GET (via Iframe)       |             | 0           |                 | Y           |             |
| Opera 32.0.1948.25   | GET (via Object)       |             | 0           |                 | Y           |             |
| Opera 32.0.1948.25   | GET (via XHR)          |             | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Opera 32.0.1948.25   | GET (via 2DCanvas)     | *           | 1           |                 | Y           |             |
| Opera 32.0.1948.25   | GET (via BitmapCanvas) | *           | 1           |                 | Y           |             |
| Opera 32.0.1948.25   | GET (via Iframe)       | *           | 1           |                 | Y           |             |
| Opera 32.0.1948.25   | GET (via Object)       | *           | 1           |                 | Y           |             |
| Opera 32.0.1948.25   | GET (via XHR)          | *           | 1           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Opera 32.0.1948.25   | GET (via 2DCanvas)     | *           | 0           |                 | Y           |             |
| Opera 32.0.1948.25   | GET (via BitmapCanvas) | *           | 0           |                 | Y           |             |
| Opera 32.0.1948.25   | GET (via Iframe)       | *           | 0           |                 | Y           |             |
| Opera 32.0.1948.25   | GET (via Object)       | *           | 0           |                 | Y           |             |
| Opera 32.0.1948.25   | GET (via XHR)          | *           | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Opera 32.0.1948.25   | GET (via 2DCanvas)     | {ECHO}      | 1           |                 | Y           | Y           |
| Opera 32.0.1948.25   | GET (via BitmapCanvas) | {ECHO}      | 1           |                 | Y           |             |
| Opera 32.0.1948.25   | GET (via Iframe)       | {ECHO}      | 1           |                 | Y           |             |
| Opera 32.0.1948.25   | GET (via Object)       | {ECHO}      | 1           |                 | Y           |             |
| Opera 32.0.1948.25   | POST (via XHR)         | {ECHO}      | 1           | Y               | Y           | Y           |
| Opera 32.0.1948.25   | GET (via XHR)          | {ECHO}      | 1           |                 | Y           | Y           |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Opera 32.0.1948.25   | GET (via 2DCanvas)     | {ECHO}      | 0           |                 | Y           |             |
| Opera 32.0.1948.25   | GET (via BitmapCanvas) | {ECHO}      | 0           |                 | Y           |             |
| Opera 32.0.1948.25   | GET (via Iframe)       | {ECHO}      | 0           |                 | Y           |             |
| Opera 32.0.1948.25   | GET (via Object)       | {ECHO}      | 0           |                 | Y           |             |
| Opera 32.0.1948.25   | GET (via XHR)          | {ECHO}      | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Opera 40.0.2308.54   | GET (via 2DCanvas)     |             | 0           |                 | Y           |             |
| Opera 40.0.2308.54   | GET (via BitmapCanvas) |             | 0           |                 | Y           |             |
| Opera 40.0.2308.54   | GET (via Iframe)       |             | 0           |                 | Y           |             |
| Opera 40.0.2308.54   | GET (via Object)       |             | 0           |                 | Y           |             |
| Opera 40.0.2308.54   | GET (via XHR)          |             | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Opera 40.0.2308.54   | GET (via 2DCanvas)     | *           | 1           |                 | Y           |             |
| Opera 40.0.2308.54   | GET (via BitmapCanvas) | *           | 1           |                 | Y           |             |
| Opera 40.0.2308.54   | GET (via Iframe)       | *           | 1           |                 | Y           |             |
| Opera 40.0.2308.54   | GET (via Object)       | *           | 1           |                 | Y           |             |
| Opera 40.0.2308.54   | GET (via XHR)          | *           | 1           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Opera 40.0.2308.54   | GET (via 2DCanvas)     | *           | 0           |                 | Y           |             |
| Opera 40.0.2308.54   | GET (via BitmapCanvas) | *           | 0           |                 | Y           |             |
| Opera 40.0.2308.54   | GET (via Iframe)       | *           | 0           |                 | Y           |             |
| Opera 40.0.2308.54   | GET (via Object)       | *           | 0           |                 | Y           |             |
| Opera 40.0.2308.54   | GET (via XHR)          | *           | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Opera 40.0.2308.54   | GET (via 2DCanvas)     | {ECHO}      | 1           |                 | Y           | Y           |
| Opera 40.0.2308.54   | GET (via BitmapCanvas) | {ECHO}      | 1           |                 | Y           |             |
| Opera 40.0.2308.54   | GET (via Iframe)       | {ECHO}      | 1           |                 | Y           |             |
| Opera 40.0.2308.54   | GET (via Object)       | {ECHO}      | 1           |                 | Y           |             |
| Opera 40.0.2308.54   | GET (via XHR)          | {ECHO}      | 1           |                 | Y           | Y           |
| Opera 40.0.2308.54   | POST (via XHR)         | {ECHO}      | 1           | Y               | Y           | Y           |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Opera 40.0.2308.54   | GET (via 2DCanvas)     | {ECHO}      | 0           |                 | Y           |             |
| Opera 40.0.2308.54   | GET (via BitmapCanvas) | {ECHO}      | 0           |                 | Y           |             |
| Opera 40.0.2308.54   | GET (via Iframe)       | {ECHO}      | 0           |                 | Y           |             |
| Opera 40.0.2308.54   | GET (via Object)       | {ECHO}      | 0           |                 | Y           |             |
| Opera 40.0.2308.54   | GET (via XHR)          | {ECHO}      | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Opera 48.0.2685.32   | GET (via 2DCanvas)     |             | 0           |                 | Y           |             |
| Opera 48.0.2685.32   | GET (via BitmapCanvas) |             | 0           |                 | Y           |             |
| Opera 48.0.2685.32   | GET (via Iframe)       |             | 0           |                 | Y           |             |
| Opera 48.0.2685.32   | GET (via Object)       |             | 0           |                 | Y           |             |
| Opera 48.0.2685.32   | GET (via XHR)          |             | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Opera 48.0.2685.32   | GET (via 2DCanvas)     | *           | 1           |                 | Y           |             |
| Opera 48.0.2685.32   | GET (via BitmapCanvas) | *           | 1           |                 | Y           |             |
| Opera 48.0.2685.32   | GET (via Iframe)       | *           | 1           |                 | Y           |             |
| Opera 48.0.2685.32   | GET (via Object)       | *           | 1           |                 | Y           |             |
| Opera 48.0.2685.32   | GET (via XHR)          | *           | 1           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Opera 48.0.2685.32   | GET (via 2DCanvas)     | *           | 0           |                 | Y           |             |
| Opera 48.0.2685.32   | GET (via BitmapCanvas) | *           | 0           |                 | Y           |             |
| Opera 48.0.2685.32   | GET (via Iframe)       | *           | 0           |                 | Y           |             |
| Opera 48.0.2685.32   | GET (via Object)       | *           | 0           |                 | Y           |             |
| Opera 48.0.2685.32   | GET (via XHR)          | *           | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Opera 48.0.2685.32   | GET (via 2DCanvas)     | {ECHO}      | 1           |                 | Y           | Y           |
| Opera 48.0.2685.32   | GET (via BitmapCanvas) | {ECHO}      | 1           |                 | Y           |             |
| Opera 48.0.2685.32   | GET (via Iframe)       | {ECHO}      | 1           |                 | Y           |             |
| Opera 48.0.2685.32   | GET (via Object)       | {ECHO}      | 1           |                 | Y           |             |
| Opera 48.0.2685.32   | POST (via XHR)         | {ECHO}      | 1           | Y               | Y           | Y           |
| Opera 48.0.2685.32   | GET (via XHR)          | {ECHO}      | 1           |                 | Y           | Y           |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Opera 48.0.2685.32   | GET (via 2DCanvas)     | {ECHO}      | 0           |                 | Y           |             |
| Opera 48.0.2685.32   | GET (via BitmapCanvas) | {ECHO}      | 0           |                 | Y           |             |
| Opera 48.0.2685.32   | GET (via Iframe)       | {ECHO}      | 0           |                 | Y           |             |
| Opera 48.0.2685.32   | GET (via Object)       | {ECHO}      | 0           |                 | Y           |             |
| Opera 48.0.2685.32   | GET (via XHR)          | {ECHO}      | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Opera 56.0.3051.31   | GET (via 2DCanvas)     |             | 0           |                 | Y           |             |
| Opera 56.0.3051.31   | GET (via BitmapCanvas) |             | 0           |                 | Y           |             |
| Opera 56.0.3051.31   | GET (via Iframe)       |             | 0           |                 | Y           |             |
| Opera 56.0.3051.31   | GET (via Object)       |             | 0           |                 | Y           |             |
| Opera 56.0.3051.31   | GET (via XHR)          |             | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Opera 56.0.3051.31   | GET (via 2DCanvas)     | *           | 1           |                 | Y           |             |
| Opera 56.0.3051.31   | GET (via BitmapCanvas) | *           | 1           |                 | Y           |             |
| Opera 56.0.3051.31   | GET (via Iframe)       | *           | 1           |                 | Y           |             |
| Opera 56.0.3051.31   | GET (via Object)       | *           | 1           |                 | Y           |             |
| Opera 56.0.3051.31   | GET (via XHR)          | *           | 1           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Opera 56.0.3051.31   | GET (via 2DCanvas)     | *           | 0           |                 | Y           |             |
| Opera 56.0.3051.31   | GET (via BitmapCanvas) | *           | 0           |                 | Y           |             |
| Opera 56.0.3051.31   | GET (via Iframe)       | *           | 0           |                 | Y           |             |
| Opera 56.0.3051.31   | GET (via Object)       | *           | 0           |                 | Y           |             |
| Opera 56.0.3051.31   | GET (via XHR)          | *           | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Opera 56.0.3051.31   | GET (via 2DCanvas)     | {ECHO}      | 1           |                 | Y           | Y           |
| Opera 56.0.3051.31   | GET (via BitmapCanvas) | {ECHO}      | 1           |                 | Y           | Y           |
| Opera 56.0.3051.31   | GET (via Iframe)       | {ECHO}      | 1           |                 | Y           |             |
| Opera 56.0.3051.31   | GET (via Object)       | {ECHO}      | 1           |                 | Y           |             |
| Opera 56.0.3051.31   | GET (via XHR)          | {ECHO}      | 1           |                 | Y           | Y           |
| Opera 56.0.3051.31   | POST (via XHR)         | {ECHO}      | 1           | Y               | Y           | Y           |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Opera 56.0.3051.31   | GET (via 2DCanvas)     | {ECHO}      | 0           |                 | Y           |             |
| Opera 56.0.3051.31   | GET (via BitmapCanvas) | {ECHO}      | 0           |                 | Y           |             |
| Opera 56.0.3051.31   | GET (via Iframe)       | {ECHO}      | 0           |                 | Y           |             |
| Opera 56.0.3051.31   | GET (via Object)       | {ECHO}      | 0           |                 | Y           |             |
| Opera 56.0.3051.31   | GET (via XHR)          | {ECHO}      | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Opera 9.00           | GET (via 2DCanvas)     |             | 0           |                 | Y           |             |
| Opera 9.00           | GET (via BitmapCanvas) |             | 0           |                 | Y           |             |
| Opera 9.00           | GET (via Iframe)       |             | 0           |                 | Y           |             |
| Opera 9.00           | GET (via Object)       |             | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Opera 9.00           | GET (via 2DCanvas)     | *           | 1           |                 | Y           |             |
| Opera 9.00           | GET (via BitmapCanvas) | *           | 1           |                 | Y           |             |
| Opera 9.00           | GET (via Iframe)       | *           | 1           |                 | Y           |             |
| Opera 9.00           | GET (via Object)       | *           | 1           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Opera 9.00           | GET (via 2DCanvas)     | *           | 0           |                 | Y           |             |
| Opera 9.00           | GET (via BitmapCanvas) | *           | 0           |                 | Y           |             |
| Opera 9.00           | GET (via Iframe)       | *           | 0           |                 | Y           |             |
| Opera 9.00           | GET (via Object)       | *           | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Opera 9.00           | GET (via 2DCanvas)     | {ECHO}      | 1           |                 | Y           |             |
| Opera 9.00           | GET (via BitmapCanvas) | {ECHO}      | 1           |                 | Y           |             |
| Opera 9.00           | GET (via Iframe)       | {ECHO}      | 1           |                 | Y           |             |
| Opera 9.00           | GET (via Object)       | {ECHO}      | 1           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Opera 9.00           | GET (via 2DCanvas)     | {ECHO}      | 0           |                 | Y           |             |
| Opera 9.00           | GET (via BitmapCanvas) | {ECHO}      | 0           |                 | Y           |             |
| Opera 9.00           | GET (via Iframe)       | {ECHO}      | 0           |                 | Y           |             |
| Opera 9.00           | GET (via Object)       | {ECHO}      | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Opera 9.20           | GET (via 2DCanvas)     |             | 0           |                 | Y           |             |
| Opera 9.20           | GET (via BitmapCanvas) |             | 0           |                 | Y           |             |
| Opera 9.20           | GET (via Iframe)       |             | 0           |                 | Y           |             |
| Opera 9.20           | GET (via Object)       |             | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Opera 9.20           | GET (via 2DCanvas)     | *           | 1           |                 | Y           |             |
| Opera 9.20           | GET (via BitmapCanvas) | *           | 1           |                 | Y           |             |
| Opera 9.20           | GET (via Iframe)       | *           | 1           |                 | Y           |             |
| Opera 9.20           | GET (via Object)       | *           | 1           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Opera 9.20           | GET (via 2DCanvas)     | *           | 0           |                 | Y           |             |
| Opera 9.20           | GET (via BitmapCanvas) | *           | 0           |                 | Y           |             |
| Opera 9.20           | GET (via Iframe)       | *           | 0           |                 | Y           |             |
| Opera 9.20           | GET (via Object)       | *           | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Opera 9.20           | GET (via 2DCanvas)     | {ECHO}      | 1           |                 | Y           |             |
| Opera 9.20           | GET (via BitmapCanvas) | {ECHO}      | 1           |                 | Y           |             |
| Opera 9.20           | GET (via Iframe)       | {ECHO}      | 1           |                 | Y           |             |
| Opera 9.20           | GET (via Object)       | {ECHO}      | 1           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Opera 9.20           | GET (via 2DCanvas)     | {ECHO}      | 0           |                 | Y           |             |
| Opera 9.20           | GET (via BitmapCanvas) | {ECHO}      | 0           |                 | Y           |             |
| Opera 9.20           | GET (via Iframe)       | {ECHO}      | 0           |                 | Y           |             |
| Opera 9.20           | GET (via Object)       | {ECHO}      | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Opera 9.60           | GET (via 2DCanvas)     |             | 0           |                 | Y           |             |
| Opera 9.60           | GET (via BitmapCanvas) |             | 0           |                 | Y           |             |
| Opera 9.60           | GET (via Iframe)       |             | 0           |                 | Y           |             |
| Opera 9.60           | GET (via Object)       |             | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Opera 9.60           | GET (via 2DCanvas)     | *           | 1           |                 | Y           |             |
| Opera 9.60           | GET (via BitmapCanvas) | *           | 1           |                 | Y           |             |
| Opera 9.60           | GET (via Iframe)       | *           | 1           |                 | Y           |             |
| Opera 9.60           | GET (via Object)       | *           | 1           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Opera 9.60           | GET (via 2DCanvas)     | *           | 0           |                 | Y           |             |
| Opera 9.60           | GET (via BitmapCanvas) | *           | 0           |                 | Y           |             |
| Opera 9.60           | GET (via Iframe)       | *           | 0           |                 | Y           |             |
| Opera 9.60           | GET (via Object)       | *           | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Opera 9.60           | GET (via 2DCanvas)     | {ECHO}      | 1           |                 | Y           |             |
| Opera 9.60           | GET (via BitmapCanvas) | {ECHO}      | 1           |                 | Y           |             |
| Opera 9.60           | GET (via Iframe)       | {ECHO}      | 1           |                 | Y           |             |
| Opera 9.60           | GET (via Object)       | {ECHO}      | 1           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
| Opera 9.60           | GET (via 2DCanvas)     | {ECHO}      | 0           |                 | Y           |             |
| Opera 9.60           | GET (via BitmapCanvas) | {ECHO}      | 0           |                 | Y           |             |
| Opera 9.60           | GET (via Iframe)       | {ECHO}      | 0           |                 | Y           |             |
| Opera 9.60           | GET (via Object)       | {ECHO}      | 0           |                 | Y           |             |
| ~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~~~~~ | ~~~~~~~~~~~ | ~~~~~~~~~~~ |
