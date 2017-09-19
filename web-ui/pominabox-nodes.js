


pibUI.page_init = function() {

	pibUI.nodes.init()

}

pibUI.nodes = {};

pibUI.nodes.init = function() {

	var items = [];

	$("#nodes .content").html('<button id="add_node" class="action">Add a node</button>');
	$("#add_node").button().click(function(event) {
		pibUI.nodes.add_dlg();
	});

	pib.get("/nodes", function(data) {

		if (Object.keys(data['nodes']).length == 0) {
			$("#nodes .content").append("No node configured");
			return
		}


		$.each (data['nodes'], function(key, val) {
			items.push('<tr id="' + key + '"><td><a href="' + pib.ui_url_base + '/node.html?node=' + key + '">' + key + "</a></td><td>" + val['url'] + '</td><td>' + (val['enabled'] ? "Enabled" : "Disabled") + '</td></tr>');
		});
		$("#nodes .content").append('<table><thead><tr><th>Node</th><th>URL</th><th>Enabled</th></thead><tbody>' + items.join("") + '</tbody></table>');
	});



}

pibUI.nodes.add_dlg = function() {

	$("#dlg_node_add").dialog({
		resizable : false,
		modal: true,
		width: "auto",
		title: "Add a pom-ng node",
		buttons : {
			Ok : function() {
				node_name = $("#dlg_node_add #name").val();
				node_url = $("#dlg_node_add #url").val();
				pib.node_add(node_name, node_url, true, function(data) {
					pibUI.nodes.init();
					$("#dlg_node_add").dialog("close");
					window.location = pib.ui_url_base + '/node.html?node=' + node_name;
				}, function(jqXHR, status, error) {
					var data = jqXHR.responseJSON;
					$("#dlg_node_add #status").text(data['msg']);
				});
			},
			Cancel : function() {
				
				$(this).dialog("close");
			}

		}
	});

}

