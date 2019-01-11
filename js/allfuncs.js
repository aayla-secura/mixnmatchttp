function registerOnReady(func) {
	// logToConsole('registerOnReady');
	// Not working in Opera 11.52
	// $(document).ready(function () {
	// 	func();
	// 	logToConsole('ready')
	// });

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

function createElement(tag, attr, appendTo) {
	if (typeof appendTo === 'undefined') {
		appendTo = document.body;
	}
	el = document.createElement(tag);
	for (prop in attr) {
		if (attr.hasOwnProperty(prop)) {
			el.setAttribute(prop, attr[prop]);
		}
	}
	appendTo.appendChild(el);
	return el;
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
	// var log = $('#' + logId);
	var log = document.getElementById(logId);
	// if (log.length === 0) {
	if (log === null) {
		// log = $('<div></div>', {id: logId, style: divStyle}).appendTo('body');
		log = createElement('div', {id: logId, style: divStyle})

		if (typeof quiet === 'undefined' || ! quiet) {
			logToConsole('Created log div');
		}
	}
	else if (typeof quiet === 'undefined' || ! quiet) {
		logToConsole('Using old log div');
	}
	// newlog = $('<p>', {style: 'margin-top: 0px; margin-bottom: 0px; ' + msgStyle});
	newlog = createElement('p', {style: 'margin-top: 0px; margin-bottom: 0px; ' + msgStyle});
	// newlog.text(msg);
	newlog.textContent = msg;
	// log.append(newlog)
	log.appendChild(newlog)
};

function logToConsole(msg) {
	if (typeof DEBUG === 'undefined' || ! DEBUG) { return; }
	// There's no console in Opera 10.10
	// if (typeof console === 'undefined') {
		window.top.logToPage('[' + document.location.search + ']: ' + msg, '', 'font-family: monospace; color: white; background-color: red;', 'errLog', true)
	// }
	// else {
	//	console.log(msg);
	// }
};

function getData(reqURL, doPOST, sendURL, force_preflight) {
	var req = new XMLHttpRequest();
	if (doPOST) {
		logToPage('POSTing to ' + reqURL);
		req.open('POST',reqURL);
		req.setRequestHeader('Content-Type', 'application/json;charset=UTF-8');
	} else {
		logToPage('GETting ' + reqURL);
		req.open('GET', reqURL);
	}
	req.withCredentials = true;
	if (force_preflight) {
		req.setRequestHeader('X-Foo', 'Custom header');
	}
	req.onreadystatechange = function reqListener(){
		if (this.readyState != 4) { return; }
		logToPage(this.responseText, 'color: red; font-weight: bold');
		if (sendURL) {
			// not tested with old browsers
			var exf = new XMLHttpRequest();
			exf.open('GET', sendURL+'/?STATUS='+this.status+'?CONTENT='+btoa(escape(this.responseText)));
			exf.send();
		}
	};
	if (doPOST) {
		req.send("{}"); // old browsers don't support JSON
	} else {
		req.send();
	}
};

function getPar(docLocation, parname) {
	// pass me document.location
	pars = document.location.search.slice(1).split('&');
	for (i = 0; i < pars.length; i++){
		if (pars[i].substr(0, parname.length) === parname) {
			return pars[i].slice(parname.length + 1);
		}
	}
};
