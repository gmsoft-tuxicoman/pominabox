


pibUI.page_init = function() {

	pibUI.node.init()

}

pibUI.node = {};

pibUI.node.init = function() {


	var node_name = pib.getUrlParam('node');

	if (!node_name) {
		alert("No node name specified");
		return
	}

	var items = [];

	pib.get("/nodes/" + node_name, function(data) {
		pibUI.node.evts = data['node']['events']
		var evt_names = Object.keys(pibUI.node.evts).sort();
		var tbody = $("#evts tbody");
		for (var i = 0; i < evt_names.length; i++) {
			var evt_name = evt_names[i]
			var evt = pibUI.node.evts[evt_name];
			tbody.append('<tr><td>' + evt_name + '</td><td>' + evt['description'] + '</td><td id="evt_en_' + evt_name + '" class="clickable"></td><tr/>');
			var itm = $("#evts tbody #evt_en_" + evt_name);
			if (evt['enabled']) {
				itm.text('Enabled');
				itm.addClass('clickable_enabled');
			} else {
				itm.text('Disabled');
				itm.addClass('clickable_disabled');
			}
			itm.click(function() {
				var evt_name = this.id.substring("evt_en".length + 1);
				var enabled = pibUI.node.evts[evt_name]['enabled'];
				pib.call("PUT", "/nodes/" + node_name + "/events/" + evt_name, { "enabled" : ! enabled }, function(data) {
					var itm = $("#evts tbody #evt_en_" + evt_name);
					if (enabled) {
						itm.removeClass('clickable_enabled');
						itm.addClass('clickable_disabled');
						itm.text('Disabled');
					} else {
						itm.removeClass('clickable_disabled');
						itm.addClass('clickable_enabled');
						itm.text('Enabled');
					}
				}

/*
				}. function(jqXHR, status, error) {
					alert("Error while toggling the event status");
				});
*/
	);

			});
		}
	});
}
