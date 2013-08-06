jq(document).ready(function() {
    // Accordion

    jq("#accordion").accordion({ header: "h3" });
    jq('#siteaction-sitemap a').prepOverlay({
        subtype: 'ajax',
        filter: '#content > *',
        config: {expose:{color:'#00f'}}
        });
    jq('#request-this-image').prepOverlay({
        subtype: 'ajax',
        filter: '#content > *',
        formselector: 'form',
        config: {expose:{color:'#00f'}}
        });
    jq('#request-album').prepOverlay({
        subtype: 'ajax',
        filter: '#content > *',
        formselector: 'form',
        config: {expose:{color:'#00f'}}
        });
});

/*
jq(document).ready(function() {
	jq("input#new-album-request:checked")({
		jq("#request-album-album-name").toggle("hidden");
	});
});
*/

jq(document).ready(function() {
	jq(".iuemCollapsedHeading.iuemCollapsed").next().hide();
	jq(".iuemCollapsedHeading").click(function() {
	  jq(this).next().slideToggle("fast");
	  jq(this).toggleClass("iuemCollapsed");
	});
});

jq(document).ready(function() {
	// Change AddRemoveWidget with radio button
	// With this method, the selected option is always shown first.
	// It should be better if the order is preserved but it is really difficult to obtain this behavior... 
	jq('#archetypes-fieldname-licencetype table').replaceWith(function() {
		var htmlButton = "";
		jq('#licencetype_selected option').each(function() {
			htmlButton = htmlButton + "<tr><td> <input class=\"radioButton\" type=\"radio\" name=\"licencetype_radio\" checked=\"checked\" value=" + jq(this).val() + "/> " + jq(this).text() + "</td></tr>";
		});
		jq('#licencetype_unselected option').each(function() {
			htmlButton = htmlButton + "<tr><td> <input class=\"radioButton\" type=\"radio\" name=\"licencetype_radio\" value=" + jq(this).val() + "/> " + jq(this).text() + "</td></tr>";
		});
		jq(htmlButton).insertBefore('#licencetype_container');
	});
	
	// Add Licencetype when click on radio button
	jq('#archetypes-fieldname-licencetype .radioButton').click(function() {
		var submitContainer  = document.getElementById("licencetype_container");

		// get rid of the hidden fields we have now
		while(submitContainer.hasChildNodes()) {
	        var node = submitContainer.childNodes[0];
	        var removed = submitContainer.removeChild(node);
		}
		// add hidden field
	    var value = jq(this).val();
	    var node = document.createElement('input');
	    node.type = "hidden";
	    node.name = "licencetype" + ":list";
		node.value = value;
		submitContainer.appendChild(node);
	});

});
