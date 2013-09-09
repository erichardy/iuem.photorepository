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

// Resize box _selected and _unselected depending on items number.
// if the sum of items is beetween 5 and 20, the size is this sum
// else, the size of at min 5 and at max 20
// * must apply to photographer field also

jq(document).ready(function() {
	var fieldTab = ['general','science','where','laboratory','reseachproject'];
	const MINFIELD = 5;
	const MAXFIELD = 20;
	
	function itemsCount(elementId) {
		return jq(elementId).attr('length');
	}
	
	for (var i = 0 ; i < fieldTab.length ; i++) {
		elementSelected   = jq('select#' + fieldTab[i] + '_selected');
		elementUnselected = jq('select#' + fieldTab[i] + '_unselected');
		if (elementSelected.length == 0) {
			// console.log('on n est pas dans une page d edition');
			return false;
		}
		selectedLength   = itemsCount(elementSelected);
		unselectedLength = itemsCount(elementUnselected);
		newSize = selectedLength + unselectedLength ;
		console.log(selectedLength + ' ' + unselectedLength + ' ' + newSize);
		if (newSize < 5) { newSize = 5 ;}
		if (newSize > 20) { newSize = 20 ;}
		jq(elementSelected).attr('size' ,newSize);
		jq(elementUnselected).attr('size' , newSize);
		}
	photographer = jq('select#photographer') ;
	nbPhotographers = itemsCount(photographer);
	if (nbPhotographers > 20) { jq(photographer).attr('size',20); }
	else {
		if (nbPhotographers < 5) { jq(photographer).attr('size',5); }
		else {
			jq(photographer).attr('size',nbPhotographers);
			}
		}
	// nb = (nbPhotographers < 5) ? 5 : ((nbPhotographers > 20 ) ? 20 : nbPhotographers) ;
});
