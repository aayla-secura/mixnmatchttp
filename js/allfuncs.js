// textContent on IE8 and earlier
// thanks to https://stackoverflow.com/a/35213210
// sadly does not work on Opera 8.5 which has neither textContent nor Object.defineProperty, nor Object.getOwnPropertyDescriptor
// if (Object.defineProperty
//   && Object.getOwnPropertyDescriptor
//   && Object.getOwnPropertyDescriptor(Element.prototype, "textContent");
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
	// 	logToConsole('DOM loaded');
	// });

	// Not working in Opera 10.10
	// document.onreadystatechange = function () {
	// 	logToConsole('Doc state is ' + document.readyState);
	// 	// interactive not triggering in Opera 11.52
	// 	if (document.readyState === 'complete') {
	// 	}
	// };

	window.onload = function () {
		if (typeof document.readyState !== 'undefined') {
			//DEBUG logToConsole('Doc state is ' + document.readyState);
		}
		else {
			logToConsole('Doc state is undefined');
		}
		// interactive not triggering in Opera 11.52
		if (typeof document.readyState === 'undefined' ||
			document.readyState === 'complete') {
			func.call(this);
		}
	};
};

function registerOnLoad(obj, func) {
	// attachEvent does not work for script tags in IE so use this to attach
	// handlers for all browsers, taken from jQuery
	obj.onload = obj.onreadystatechange = function () {
		if ( !this.readyState || this.readyState  == 4 ||
			this.readyState === 'loaded' || this.readyState === 'complete' ) {
			// Handle memory leak in IE
			this.onload = this.onreadystatechange = null;

			func.call(this);
		}
	};
};

function registerOnError(obj, func) {
	if (obj.attachEvent) { // IE
		var wrapper = function () {
			// Handle memory leak in IE
			this.detachEvent('onerror', wrapper);

			func.call(this);
		};
		obj.attachEvent('onerror', wrapper);
	} else { // old browsers may not support addEventListener
		obj.onerror = func;
	}
};

function rand(len) {
	if (typeof len === 'undefined' || ! len) { len = 20 };
	return Math.floor(Math.random()*Math.pow(2,4*len)).toString(16);
};

function addElement(tag, attr, appendTo, onload, onerror) {
	var el = document.createElement(tag);
	for (var prop in attr) {
		if (attr.hasOwnProperty(prop)) {
			el.setAttribute(prop, attr[prop]);
		}
	}
	if (onload) { registerOnLoad(el, onload); }
	if (onerror) { registerOnError(el, onerror); }
	if (typeof appendTo === 'undefined' || appendTo === null) {
		appendTo = document.body;
	}
	if (appendTo) {
		// otherwise it must have been '', so disable append
		appendTo.appendChild(el);
	}
	return el;
};

function getPar(parname) {
	var pars = window.location.search.slice(1).split('&');
	for (var i = 0; i < pars.length; i++) {
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
	else if (window.location.hostname === 'localhost') {
		reqHost = '127.0.0.1:' + window.location.port;
	}
	else if (window.location.hostname === '127.0.0.1') {
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
	for (var i = 0; i < filteredPars.length; i++) {
		// also match parameters without value, e.g. foo in &foo&bar=baz
		r = new RegExp('&' + filteredPars[i] + '(=[^&]*)?($|&)','g');
		result = result.replace(r, '&');
	}
	return result.slice(1); // remove leading &
};

function logToPage(msg, msgStyle, divStyle, logId, quiet) {
	if (typeof logId === 'undefined' || logId === null) {
		logId = 'log';
	}
	if (typeof msgStyle === 'undefined' || msgStyle === null) {
		msgStyle = 'font-family: monospace';
	}
	if (typeof divStyle === 'undefined' || divStyle === null) {
		divStyle = 'margin-top: 20px; margin-bottom: 20px';
	}
	var log = document.getElementById(logId);
	if (log === null) {
		log = addElement('div', {id: logId, style: divStyle});

		if (typeof quiet === 'undefined' || ! quiet) {
			// logToConsole('Created log div');
		}
	}
	else if (typeof quiet === 'undefined' || ! quiet) {
		// logToConsole('Using old log div');
	}
	var newlog = addElement('p', {
			style: 'margin-top: 0px; margin-bottom: 0px; ' + msgStyle}, log);
	setTextContent(newlog, msg);
};

function logToConsole(msg) {
	if (typeof DEBUG === 'undefined' || ! DEBUG) { return; }
	// There's no console in Opera 10.10 and IE => log to page
	logToPage('[' + window.location.search + ']: ' + msg, CSS['redMono'],
		null, 'errLog', true);
};

function getData(baseReqURL, baseSendURL, callback, exfMethods) {
	var currOrigin = getCurrOrigin();
	function genReqSendURLs(origin, creds, method, via) {
		var creds = (creds ? '1' : '0');
		if (baseReqURL.split('?').length > 1) { var reqSep = '&'; }
		else { reqSep = '?'; }
		if (baseSendURL.split('?').length > 1) { var sendSep = '&'; }
		else { sendSep = '?'; }
		return {
			req: baseReqURL + reqSep +
				'origin=' + encodeURIComponent(origin) +
				'&creds=' + creds +
				'&via=' + via +
				'&reqBy=' + encodeURIComponent(currOrigin), // requests for object and iframe may not include the Origin header
			send: baseSendURL + sendSep +
				'allowOrigin=' + encodeURIComponent(origin) +
				'&allowCreds=' + creds +
				'&method=' + method +
				'&via=' + via
			};
	};

	if (! exfMethods) {
		exfMethods = [ 'XHR', 'Iframe', 'Object', '2DCanvas', 'BitmapCanvas' ];
	}
	reqMethods = {
		'XHR': ['GET', 'POST'],
		'Iframe': ['GET'],
		'Object': ['GET'],
		'2DCanvas': ['GET'],
		'BitmapCanvas': ['GET']
	};
	corsCombos = [
		{ origin: currOrigin, creds: 1 },
		{ origin: currOrigin, creds: 0 },
		{ origin: '*',        creds: 1 },
		{ origin: '*',        creds: 0 },
		{ origin: '',         creds: 0 }
	];

	if (typeof window.requestsLeft === 'undefined') {
		window.requestsLeft = 0;
	}
	var callbackWrapper = function (data) {
		window.requestsLeft--;
		if (callback) { callback.call(this, data) };
		//logToPage('callback: ' + window.requestsLeft + ' to go'); //DEBUG
	};

	for (var e = 0; e < exfMethods.length; e++) {
		exfM = exfMethods[e];
		for (var r = 0; r < reqMethods[exfM].length; r++) {
			reqM = reqMethods[exfM][r];
			for (var c = 0; c < corsCombos.length; c++) {
				corsC = corsCombos[c];

				window.requestsLeft++;
				urls = genReqSendURLs(corsC['origin'], corsC['creds'], reqM, exfM);
				func = window['getDataVia' + exfM];
				try {
					func(urls['req'], (reqM === 'POST'), urls['send'], callbackWrapper);
				} catch(err) {
					window.requestsLeft--;
					//logToPage('error during getData*: ' + window.requestsLeft + ' to go'); //DEBUG
					logToConsole(err.message);
				}
			}
		}
	}

	if (typeof window.doneChecker === 'undefined') {
		window.doneChecker = setInterval(function () {
			if (window.requestsLeft <= 0) {
				clearInterval(window.doneChecker);
				if (window.requestsLeft == 0) {
					logToPage('All requests done!', CSS['green']);
				} else { //DEBUG
					logToPage('BUG: requestsLeft is ' + window.requestsLeft, CSS['redMono']);
				}
			}
		}, 1000);
	}
};

function getTryHandlerWrapper (handler, onerror, ondone) {
	return function () {
		// old browsers support neither .bind, nor lambda functions so we use closure
		var currThis = this;
		try {
			handler.call(currThis);
		} catch(err) {
			logToConsole(err.message);
			if (onerror) { onerror.call(currThis) };
		} finally {
			if (ondone) { ondone.call(currThis) };
		}
	};
};

function getDataViaXHR(reqURL, reqViaPOST, sendURL, callback) {
	var logId = 'log_' + rand(); // unique log ID for each request
	var req = new XMLHttpRequest();
	var readyState = 0;
	var callbackWrapper = function () {
		if (readyState != 4) { return; }
		if (callback) { callback(data); }
	};
	if (reqViaPOST) {
		logToPage('POSTing to ' + reqURL, null, null, logId);
		req.open('POST', reqURL);
		req.setRequestHeader('Content-Type',
			'application/json;charset=UTF-8');
	} else {
		logToPage('GETting ' + reqURL, null, null, logId);
		req.open('GET', reqURL);
	}
	req.withCredentials = true;
	var data = null;
	req.onreadystatechange = getTryHandlerWrapper(function () {
		readyState = this.readyState;
		if (readyState != 4) { return; }
		data = this.responseText;
		logToPage(data, CSS['red'], null, logId);
		sendData(data, this.getResponseHeader('content-type'), sendURL);
	}, null, callbackWrapper);
	if (reqViaPOST) {
		req.send("{}"); // Opera 8.5 doesn't support JSON
	} else {
		req.send();
	}
};

function getDataViaIframe(reqURL, reqViaPOST, sendURL, callback) {
	var logId = 'log_' + rand(); // unique log ID for each request
	logToPage('Embedding in an iframe ' + reqURL, null, null, logId);
	var data = null;
	var callbackWrapper = function () {
		if (callback) { callback(data); }
	};
	var func = getTryHandlerWrapper(function () {
		//DEBUG if (this == window){logToPage('this is window', CSS['red'], null, logId);return}
		var doc = this.contentDocument || (this.contentWindow ? this.contentWindow.document : null);
		data = doc.body.innerHTML;
		logToPage(getTextContent(data), null, null, logId);
		sendData(data, doc.contentType, sendURL);
	}, null, callbackWrapper);
	var ifr = addElement('iframe', {src: reqURL, style: CSS['hidden']},
		null, func, callbackWrapper);
};

function getDataViaObject(reqURL, reqViaPOST, sendURL, callback) {
	var logId = 'log_' + rand(); // unique log ID for each request
	logToPage('Embedding in an object ' + reqURL, null, null, logId);
	var data = null;
	var callbackWrapper = function () {
		if (callback) { callback(data); }
	};
	var func = function () {
		//DEBUG if (this == window){logToPage('this is window', CSS['red'], null, logId);return}
		// the onload handler of <object> fires too soon so we call it from setTimeout
		// old browsers support neither .bind, nor lambda functions so we use closure
		var currThis = this;
		var sendDataLater = getTryHandlerWrapper(function () {
			var doc = currThis.contentDocument || (currThis.contentWindow ? currThis.contentWindow.document : null);
			if (doc && doc.body) {
				data = currThis.contentDocument.body.innerHTML;
				logToPage(data, CSS['red'], null, logId);
				sendData(data, 'text/plain', sendURL);
			}
		}, null, callbackWrapper);
		setTimeout(sendDataLater, 2000);
	};
	// don't think crossorigin is used for object, but meh
	var obj = addElement('object', {crossorigin: 'use-credentials',
		data: reqURL, type: 'text/plain', style: CSS['hidden']},
		null, func, callbackWrapper);
};

function getDataVia2DCanvas(reqURL, reqViaPOST, sendURL, callback) {
	var logId = 'log_' + rand(); // unique log ID for each request
	logToPage('Embedding in a 2D canvas ' + reqURL, null, null, logId);
	var data = null;
	var callbackWrapper = function () {
		if (callback) { callback(data); }
	};
	var func = function () {
		//DEBUG if (this == window){logToPage('this is window', CSS['red'], null, logId);return}
		// the onload handler of <img> fires too soon in IE9 so we call it from setTimeout
		// old browsers support neither .bind, nor lambda functions so we use closure
		var currThis = this;
		var sendDataLater = getTryHandlerWrapper(function () {
			var can = document.createElement('canvas');
			var ctx = can.getContext('2d');
			ctx.drawImage(currThis, 0, 0);
			var dataParts = /^data:([^;,]+)(;base64)?,(.*)/.exec(can.toDataURL());
			var ctype = dataParts[1];
			var alreadyEncoded = Boolean(dataParts[2]);
			data = dataParts[3];
			logToPage(data, CSS['red'], null, logId);
			sendData(data, ctype, sendURL, alreadyEncoded);
		}, null, callbackWrapper);
		setTimeout(sendDataLater, 1000);
	};
	var img = addElement('img', {crossorigin: 'use-credentials',
		src: reqURL, style: CSS['hidden']}, null, func, callbackWrapper);
};

function getDataViaBitmapCanvas(reqURL, reqViaPOST, sendURL, callback) {
	var logId = 'log_' + rand(); // unique log ID for each request
	logToPage('Embedding in a bitmap canvas ' + reqURL, null, null, logId);
	var data = null;
	var callbackWrapper = function () {
		if (callback) { callback(data); }
	};
	var func = getTryHandlerWrapper(function () {
		//DEBUG if (this == window){logToPage('this is window', CSS['red'], null, logId);return}
		createImageBitmap(this, 0, 0, 100, 100).then(function(bmap) {
			var can = document.createElement('canvas');
			var ctx = can.getContext('bitmaprenderer');
			ctx.transferFromImageBitmap(bmap);
			var dataParts = /^data:([^;,]+)(;base64)?,(.*)/.exec(can.toDataURL());
			var ctype = dataParts[1];
			var alreadyEncoded = Boolean(dataParts[2]);
			data = dataParts[3];
			logToPage(data, CSS['red'], null, logId);
			sendData(data, ctype, sendURL, alreadyEncoded);
		}, function(err) {
			throw err; // let the surrounding code handle this
		});
	}, null, callbackWrapper);
	var img = addElement('img', {crossorigin: 'use-credentials',
		src: reqURL, style: CSS['hidden']}, null, func, callbackWrapper);
};

function sendData(data, ctype, sendURL, alreadyEncoded) {
	// Opera 8.5 doesn't support JSON, so the JSON is constructed "by
	// hand"; the base64 data is safe, ctype shouldn't normally contain
	// characters special to JSON, i.e.  " or \, but we escape them in any
	// case. Unicode ranges are not supported in very old browsers, assume there
	// are no other characters special to JSON.
	if (! data || ! sendURL) { return; }
	if (typeof alreadyEncoded === 'undefined' || alreadyEncoded === null) {
		alreadyEncoded = false;
	}
	// ctype = type.replace(/[\\"]/g,'');
	if (ctype) {
		ctype = ctype.replace(/\\/g,'\\\\').replace(/"/g,'\\"');
	}
	var exf = new XMLHttpRequest();
	exf.open('POST', sendURL);
	exf.setRequestHeader('Content-Type',
		'application/json;charset=UTF-8');
	if(typeof btoa === 'undefined' || typeof Base64 === 'undefined'
		|| !window.btoa.__using_external) { //DEBUG
		logToPage('Base64 did not load', CSS['red'])
	}
	exf.send('{"data":"' + (alreadyEncoded ? data : btoa(data)) +
		(ctype ? '", "type": "' + ctype + '"}' : '"}'));
};

// old browsers support neither .bind, nor lambda functions so we use closure
function createBoundedWrapper(object, method) {
	return function() {
		return method.apply(object, arguments);
	};
}

// old IE and Opera don't have btoa/atob
// also, even some modern browsers have issues with base64-encoding unicode
// data
// /js/base64.js, taken from http://www.webtoolkit.info works
(function () {
	var func = function () {
		//DEBUG if (this == window){logToPage('Base64: this is window', CSS['red']);return}
		if(typeof Base64 === 'undefined') { //DEBUG
			logToPage('Base64: '+typeof Base64, CSS['red'])
			logToPage('Base64: state: '+this.readyState, CSS['red']);
		}
		window.atob = createBoundedWrapper(Base64, Base64.decode);
		window.btoa = createBoundedWrapper(Base64, Base64.encode);
		window.atob.__using_external = true;
		window.btoa.__using_external = true;
	};
	// some old browsers don't support document.head
	var head = document.head || document.getElementsByTagName('head')[0];
	var b64scr = addElement('script', {src: '/js/base64.js'}, head, func);
})();
// if (typeof btoa === 'undefined') {
// 	atob = function (data) {
// 		if (! data) { return; }
// 		return "Can't find base64 implementation";
// 	};
// 	btoa = function (data) {
// 		if (! data) { return; }
// 		return 'Q2FuJ3QgZmluZCBiYXNlNjQgaW1wbGVtZW50YXRpb24K';
// 	};
// }

window.DEBUG = getBoolPar('debug');
window.CSS = {
	hidden: 'visibility: hidden; width: 0; height: 0; border: 0; border: none;',
	redMono: 'font-family: monospace; color: white; background-color: red;',
	red: 'color: red; font-weight: bold',
	green: 'color: green; font-weight: bold'
};
