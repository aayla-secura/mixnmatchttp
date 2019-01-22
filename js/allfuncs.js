var CSShidden = 'visibility: hidden; width: 0; height: 0; border: 0; border: none;';

// Can't find base64 implementation that works on old IE and Opera
if (typeof btoa === 'undefined') {
	atob = function (data) {
		if (! data) { return; }
		return "Can't find base64 implementation";
	};
	btoa = function (data) {
		if (! data) { return; }
		return 'Q2FuJ3QgZmluZCBiYXNlNjQgaW1wbGVtZW50YXRpb24K';
	};
}

// textContent on IE8 and earlier
// thanks to https://stackoverflow.com/a/35213210
// sadly does not work on Opera 8.5 which has neither textContent nor Object.defineProperty, nor Object.getOwnPropertyDescriptor
// if (Object.defineProperty
//   && Object.getOwnPropertyDescriptor
//   && Object.getOwnPropertyDescriptor(Element.prototype, "textContent")
//   && !Object.getOwnPropertyDescriptor(Element.prototype, "textContent").get) {
//   (function() {
//     var innerText = Object.getOwnPropertyDescriptor(Element.prototype, "innerText");
//     Object.defineProperty(Element.prototype, "textContent",
//      {
//        get: function() {
//          return innerText.get.call(this);
//        },
//        set: function(s) {
//          return innerText.set.call(this, s);
//        }
//      }
//    );
//   })();
// }
// Hence the below "workaround"
function getTextContent(el) {
    if (typeof el.textContent === 'undefined') {
        return el.innerText;
    } else {
        return el.textContent;
    }
}
function setTextContent(el, s) {
    if (typeof el.textContent === 'undefined') {
        el.innerText = s;
    } else {
        el.textContent = s;
    }
}

function registerWinOnLoad(func) {
	// Not working in Opera 11.52
	// document.addEventListener("DOMContentLoaded", function (event) {
	// 	logToConsole('DOM loaded')
	// 	func();
	// });

	// Not working in Opera 10.10
	// document.onreadystatechange = function () {
	// 	logToConsole('Doc state is ' + document.readyState);
	// 	// interactive not triggering in Opera 11.52
	// 	if (document.readyState === 'complete') {
	// 		func();
	// 	}
	// };

	window.onload = function () {
		window.DEBUG = getBoolPar('debug');
		if (typeof window.top.requestsLeft != 'undefined') {
			if (typeof window.top.doneChecker == 'undefined') {
				window.top.doneChecker = setInterval(function () {
					if (window.top.requestsLeft == 0) {
						clearInterval(window.top.doneChecker);
						logToPage('Done!');
					}
				}, 1000);
			}
		}

		if (typeof document.readyState !== 'undefined') {
			logToConsole('Doc state is ' + document.readyState);
		}
		else {
			logToConsole('Doc state is undefined');
		}
		// interactive not triggering in Opera 11.52
		if (typeof document.readyState === 'undefined' || document.readyState === 'complete') {
			func();
		}
	};
};

function registerOnLoad(obj, func) {
	if (obj.attachEvent) { // IE
		obj.attachEvent('onload', func);
	} else { // old browsers may not support addEventListener
		obj.onload = func;
	}
};

function requestDone() {
	// very old browsers don't support postMessage, so instead check
	// a global variable periodically
	if (typeof window.top.requestsLeft != 'undefined') {
		window.top.requestsLeft--;
	}
};

function addElement(tag, attr, appendTo) {
	var el = document.createElement(tag);
	for (var prop in attr) {
		if (attr.hasOwnProperty(prop)) {
			el.setAttribute(prop, attr[prop]);
		}
	}
	if (typeof appendTo === 'undefined') {
		appendTo = document.body;
	}
	appendTo.appendChild(el);
	return el;
};

function getPar(parname) {
	var pars = window.location.search.slice(1).split('&');
	for (var i = 0; i < pars.length; i++){
		var par = pars[i].split('=');
		if (par[0] === parname) { return par[1]; }
	}
};

function getBoolPar(parname) {
	return Boolean(Number(getPar(parname)));
};

function getReqOrigin() {
	// check host, hostname and port URL parameters in this order;
	// otherwise if running on localhost or 127.0.0.1, use the other of the two;

	// check if full target host is given
	var reqHost = getPar('host');
	if (! reqHost) {
		// otherwise check hostname
		reqHost = getPar('hostname');
		if (reqHost) {
			reqHost += ':' + window.location.port;
		}
	}
	if (! reqHost) {
		// otherwise check port
		reqHost = getPar('port');
		if (reqHost) {
			reqHost = window.location.hostname + ':' + reqHost;
		}
	}

	// otherwise check if localhost
	if (reqHost) { }
	else if (window.location.hostname == 'localhost') {
		reqHost = '127.0.0.1:' + window.location.port;
	}
	else if (window.location.hostname == '127.0.0.1') {
		reqHost = 'localhost:' + window.location.port;
	}

	if (reqHost) {
		return window.location.protocol + '//' + decodeURIComponent(reqHost);
	}
};

function getCurrOrigin() {
	// return the current proto://domain:port
	return window.location.protocol + '//' + window.location.host;
};

function getCurrDir() {
	// includes trailing slash
	return window.location.pathname.substring(0,
		window.location.pathname.lastIndexOf("/") + 1);
};

function filterPars(filteredPars) {
	// replace leading ? with & so regex matches first param
	var result = '&' + window.location.search.slice(1);
	for (var i = 0; i < filteredPars.length; i++){
		// also match parameters without value, e.g. foo in &foo&bar=baz
		r = new RegExp('&' + filteredPars[i] + '(=[^&]*)?($|&)','g');
		result = result.replace(r, '&');
	}
	return result.slice(1); // remove leading &
};

function logToPage(msg, msgStyle, divStyle, logId, quiet) {
	if (typeof logId === 'undefined') {
		logId = 'log';
	}
	if (typeof msgStyle === 'undefined') {
		msgStyle = 'font-family: monospace';
	}
	if (typeof divStyle === 'undefined') {
		divStyle = '';
	}
	var log = document.getElementById(logId);
	if (log === null) {
		log = addElement('div', {id: logId, style: divStyle})

		if (typeof quiet === 'undefined' || ! quiet) {
			logToConsole('Created log div');
		}
	}
	else if (typeof quiet === 'undefined' || ! quiet) {
		logToConsole('Using old log div');
	}
	var newlog = addElement('p', {
			style: 'margin-top: 0px; margin-bottom: 0px; ' + msgStyle}, log);
	setTextContent(newlog, msg);
};

function logToConsole(msg) {
	if (typeof DEBUG === 'undefined' || ! DEBUG) { return; }
	// There's no console in Opera 10.10 and IE => log to page
	window.top.logToPage('[' + window.location.search + ']: ' + msg, '',
		'font-family: monospace; color: white; background-color: red;', 'errLog', true)
};

function getData(reqURL, reqViaPOST, sendURL, callback, custom_header) {
	if (reqURL.split('?')[1]) { reqURL += '&via='; }
	else { reqURL += '?via='; }
	if (sendURL) {
		if (sendURL.split('?')[1]) { sendURL += '&via='; }
		else { sendURL += '?via='; }
	}
	getDataViaXHR(reqURL + 'XHR', reqViaPOST, sendURL ? sendURL + 'XHR' : null, callback, custom_header);
	if (! reqViaPOST) {
		getDataViaObject(reqURL + 'Object', sendURL ? sendURL + 'Object' : null, callback);
	}
};

function getDataViaObject(reqURL, sendURL, callback) {
	logToPage('Embedding ' + reqURL);
	var img = addElement('object', {data: reqURL, crossOrigin: 'Anonymous',
		type: 'image/svg+xml', style: CSShidden});
	registerOnLoad(img, function () {
		// the onload handler of <object> fires too soon so we call it from setTimeout
		// IE11 doesn't support arrow functions, so we need to use bind
		// old browsers don't support .bind, nor lambda functions
		// getDataViaObject should be called only once in the current iFrame,
		// otherwise a random name for the variable in this call should be
		// generated
		window.dataViaObject = this;
		sendDataLater = (function () {
			try {
				if (window.dataViaObject.contentDocument) {
					// How to get the content-type??
					sendData(window.dataViaObject.contentDocument.body.childNodes[0].innerHTML,
						'text/plain', sendURL);
					if (callback) {
						callback(window.dataViaObject.contentDocument.body.childNodes[0].innerHTML);
					}
				}
			} catch(err) { logToConsole(err); }
			requestDone();
		});
		setTimeout(sendDataLater, 2000);
	});
};

function getDataViaXHR(reqURL, reqViaPOST, sendURL, callback, custom_header) {
	var req = new XMLHttpRequest();
	if (reqViaPOST) {
		logToPage('POSTing to ' + reqURL);
		req.open('POST', reqURL);
		req.setRequestHeader('Content-Type',
			'application/json;charset=UTF-8');
	} else {
		logToPage('GETting ' + reqURL);
		req.open('GET', reqURL);
	}
	req.withCredentials = true;
	if (custom_header) {
		// should force preflight and fail if header is not allowed
		req.setRequestHeader(custom_header, 'Custom header');
	}
	req.onreadystatechange = function (){
		if (this.readyState != 4) { return; }
		logToPage(this.responseText, 'color: red; font-weight: bold');
		sendData(this.responseText, this.getResponseHeader('content-type'),
			sendURL);
		if (callback) { callback(this.responseText); }
		requestDone();
	};
	if (reqViaPOST) {
		req.send("{}"); // Opera 8.5 doesn't support JSON
	} else {
		req.send();
	}
};

function sendData(data, type, sendURL) {
	// Opera 8.5 doesn't support JSON, so the JSON is constructed "by
	// hand"; the base64 data is safe, type shouldn't normally contain
	// characters special to JSON, i.e.  " or \, but we escape them in any
	// case. Unicode ranges are not supported in very old browsers, assume there
	// are no other characters special to JSON.
	if (! data || ! sendURL) { return; }
	// type = type.replace(/[\\"]/g,'');
	type = type.replace(/\\/g,'\\\\').replace(/"/g,'\\"');
	var exf = new XMLHttpRequest();
	exf.open('POST', sendURL);
	exf.setRequestHeader('Content-Type',
		'application/json;charset=UTF-8');
	exf.send('{"data":"' + btoa(data) +
		'", "type": "' + type + '"}');
};
