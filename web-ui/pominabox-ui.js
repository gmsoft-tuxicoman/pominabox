

var pibUI = {};

pibUI.init = function() {

	menu = [ 'index', 'logs' ]

	items = []

	for (var i = 0; i <  menu.length; i++ ) {
		m = menu[i];
		items.push('<li><a href="' + m + '.html">' + m + '</a></li>');
	}
	
	$("#main_menu").html('<ul>' + items.join("") + '</ul>');
	

	pibUI.page_init();

}

