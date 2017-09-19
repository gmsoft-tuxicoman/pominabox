$(document).ready( function() {
	pib.init()
	pibUI.init()
});

var pib = {};

pib.api_url_base = '/api';
pib.ui_url_base = '/ui';

pib.init = function() {

	

}

pib.getUrlParam = function(param_name) {
	url = decodeURIComponent(window.location.search.substring(1));
	url_vars = url.split('&');

	for (var i = 0; i < url_vars.length; i++) {
		param = url_vars[i].split('=');

	        if (param[0] === param_name)
			return param[1] === undefined ? true : param[1];
	}

	return undefined;
}

pib.get = function(endpoint, success) {
	
	$.getJSON(pib.api_url_base + endpoint, success);
}

pib.call = function(method, endpoint, data, success, error) {

	$.ajax({
		url : pib.api_url_base + endpoint,
		method : method,
		contentType : "application/json",
		data : JSON.stringify(data),
		success : success,
		error : error
	});
}

pib.node_add = function(name, url, test, success, error) {
	data = { url: url, test : test }
	this.call("PUT", "/nodes/" + name, data, success, error)
}

