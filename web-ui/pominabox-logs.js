

var pibUI = {};

pibUI.init = function() {

	pibUI.logs.init()

}

pibUI.logs = {};

pibUI.logs.init = function() {

	$("#search input[type=submit]").button().click(pibUI.logs.search)
}

pibUI.logs.search = function() {
	
	query = {
		"input" : {
			"sort" : [
				{ "query_time" :
					{ "order" : "desc" }
				}
			],
			"size" : "1000",
			"query" : {
				"bool" : {
					"must_not" : {
						"match" : {
							"server_name" : "wiki.packet-o-matic.org"
						}
					}
				}
			}
		},
		"output" : {
			"format" : "$server_name $client_addr $username $url [$query_time] \"$first_line\" $status $response_size"
		}
	}

	pib.call("POST", "/db/search_template", query, function(data) {
		$("#results").html('<pre>' + data + '</pre>');
	});
}
