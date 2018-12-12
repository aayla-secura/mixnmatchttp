function getData(reqURL) {
	var doPOST = false;
	// var sendURL = 'https://localhost:58081';
	var req = new XMLHttpRequest();
	if (doPOST) {
		console.log("POSTing to " + reqURL);
		req.open("POST",reqURL);
		req.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
	} else {
		console.log("GETting " + reqURL);
		req.open("GET",reqURL);
	}
	req.withCredentials = true;
	// req.setRequestHeader("X-Foo", "Custom header");
	req.onreadystatechange = function reqListener(){
		if (this.readyState != 4) { return; }
		logData(this.responseText);
		// var exf = new XMLHttpRequest();
		// exf.open('GET', sendURL+'/?STATUS='+this.status+'?CONTENT='+btoa(escape(this.responseText)));
		// exf.send();
	};
	if (doPOST) {
		var data = {};
		req.send(JSON.stringify(data));
	} else {
		req.send();
	}
};

function logData(data) {
	var log = $('#log');
	if (log.length === 0) {
		log = $('<div></div>');
		log.id = 'log';
		$('body').append(log);
		console.log('Created log div');
	}
	else {
		console.log('Using old log div');
	}
	console.log('Got data: ' + data);
	err = $('<p>');
	err.text(data);
	log.append(err)
};

function getPar(docLocation, parname) {
	// pass document.location
	pars = document.location.search.slice(1).split('&');
	for (i = 0; i < pars.length; i++){
		if (pars[i].substr(0, parname.length) === parname) {
			return pars[i].slice(parname.length + 1);
		}
	}
}

function getMyIP(cbk) {
	window.RTCPeerConnection = window.RTCPeerConnection || window.mozRTCPeerConnection || window.webkitRTCPeerConnection;
	var pc = new RTCPeerConnection({iceServers:[]}), noop = function(){};
	pc.createDataChannel('');
	pc.createOffer(pc.setLocalDescription.bind(pc), noop);
	pc.onicecandidate = function(ice)
	{
		if (ice && ice.candidate && ice.candidate.candidate)
		{
			var myIP = /([0-9]{1,3}(\.[0-9]{1,3}){3}|[a-f0-9]{1,4}(:[a-f0-9]{1,4}){7})/.exec(ice.candidate.candidate)[1];
			logData('my IP: ' + myIP);
			cbk(myIP);
			pc.onicecandidate = noop;
		}
	};
};

function enumPorts(ports, cbk) {
	if (ports.length == 0) {
		// for (let i = 1; i != 65535; ++i) ports.push(i);
		ports = [21,22,80,443,993,5900];
	};

	function enumNextPort(i) {
		var port = ports[i];
		var oReq = new XMLHttpRequest();
		oReq.timeout = 1000;
		// logData('GET https://localhost:' + port);
		oReq.open('GET', 'https://localhost:' + port, true);
		// oReq.onreadystatechange = function(){
		//   elapsed = Date.now() - startms;
		//   logData('[' + port + '] ' + elapsed + 'ms: state is ' + oReq.readyState + ' + status is ' + oReq.status);
		// };
		// oReq.onerror = function(){
		//   elapsed = Date.now() - startms;
		//   logData('[' + port + '] ' + elapsed + 'ms: ERROR');
		// };
		oReq.onload = function(){
		//   elapsed = Date.now() - startms;
		//   logData('[' + port + '] ' + elapsed + 'ms: LOAD');
			logData('Port ' + port + ' is OPEN [got response]');
			cbk(port);
		};
		// oReq.onloadend = function(){
		//   elapsed = Date.now() - startms;
		//   logData('[' + port + '] ' + elapsed + 'ms: LOADEND');
		// };
		// oReq.onloadstart = function(){
		//   elapsed = Date.now() - startms;
		//   logData('[' + port + '] ' + elapsed + 'ms: LOADSTART');
		// };
		// oReq.onprogress = function(){
		//   elapsed = Date.now() - startms;
		//   logData('[' + port + '] ' + elapsed + 'ms: PROGRESS');
		// };
		oReq.ontimeout = function(){
			// elapsed = Date.now() - startms;
			// logData('[' + port + '] ' + elapsed + 'ms: TIMEOUT');
			logData('Port ' + port + ' is OPEN/FILTERED [no response]');
			cbk(port);
		};
		var startms = Date.now();
		oReq.send();
		if (i+1 < ports.length) {
			setTimeout(function(){enumNextPort(i+1);},50);
		};
	};

	enumNextPort(0);
};

function writeFile(filename) {
	function errorHandler(e) {
		var msg = '';
		logData(e.message);

		switch (e.code) {
			case FileError.QUOTA_EXCEEDED_ERR:
				msg = 'QUOTA_EXCEEDED_ERR';
				break;
			case FileError.NOT_FOUND_ERR:
				msg = 'NOT_FOUND_ERR';
				break;
			case FileError.SECURITY_ERR:
				msg = 'SECURITY_ERR';
				break;
			case FileError.INVALID_MODIFICATION_ERR:
				msg = 'INVALID_MODIFICATION_ERR';
				break;
			case FileError.INVALID_STATE_ERR:
				msg = 'INVALID_STATE_ERR';
				break;
			default:
				msg = 'Unknown Error';
				break;
		};

		logData('Error: ' + msg);
	}

	function onInitFs(fs) {
		fs.root.getFile(filename, {create: true, exclusive: true}, function(fileEntry) {
			logData('Created file "' + fileEntry.fullPath + '"');
			logData(fileEntry);
		}, errorHandler);
		logData('created');

		fs.root.getFile(filename, {create: false, exclusive: false}, function(fileEntry) {
			fileEntry.createWriter(function(fileWriter) {
				fileWriter.seek(fileWriter.length);
				var blob = new Blob(['Hello World'], {type: 'text/plain'});
				fileWriter.write(blob);
			}, errorHandler);
		logData('wrote');

		fs.root.getFile(filename, {create: false, exclusive: false}, function(fileEntry) {
			fileEntry.file(function(file) {
				var reader = new FileReader();
				reader.onloadend = function(e) {
					logData('Read: ' + this.result);
				};
				reader.readAsText(file);
			}, errorHandler);
		}, errorHandler);

		}, errorHandler);
	}

	req = window.requestFileSystem || window.webkitRequestFileSystem;
	req(window.TEMPORARY, 1024, onInitFs, errorHandler);
}
