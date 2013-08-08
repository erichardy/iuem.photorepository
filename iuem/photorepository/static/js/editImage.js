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

// Resize box _selected and _unselected depending on max nodes number. Max is 20 and min 5
// this script is to be modified :
// * change algoritm : determine size before everything by count of items, then apply widget size
// * (option) onChange : resize according to the number of items in each side of the widget
// * must apply to photographer field also
jq(document).ready(function() {
	var fieldTab = ['general','science','where','laboratory','reseachproject'];
	const MINFIELD = 5;
	const MAXFIELD = 20;
	
	function itemsCount(elementId) {
		return jq(elementId).attr('length');
	}
	for (var i=0; i<fieldTab.length; i++) {
		elementSelected   = jq('select#' + fieldTab[i] + '_selected');
		elementUnselected = jq('select#' + fieldTab[i] + '_unselected');
		if (elementSelected.length == 0) {
			console.log('on n est pas dans une page d edition');
			return false;
		}
		selectedLength   = itemsCount(elementSelected);
		unselectedLength = itemsCount(elementUnselected);
		console.log(selectedLength + ' ' + unselectedLength);
		newSize = Math.max(selectedLength , unselectedLength);
		console.log('newSize = ' + newSize);
		if (newSize < 20) { newSize = 5 ;}
		elementSelected.attr('size' , Math.min(newSize , 20));
		elementUnselected.attr('size' , Math.min(newSize , 20));
	}
});

/*
jq(document).ready(function() {
	var fieldTab = ['general','science','where','laboratory','reseachproject'];
	const MINFIELD = 5;
	const MAXFIELD = 20;
	for (var i=0; i<fieldTab.length; i++) {
		var fieldSelectedLength = jq('#' + fieldTab[i] + '_selected').attr('length');
		var fieldUnselectedLength = jq('#' + fieldTab[i] + '_unselected').attr('length');
		if(fieldSelectedLength >= fieldUnselectedLength) {
			if(fieldSelectedLength > MINFIELD)  {
				if(fieldSelectedLength > MAXFIELD) {
					jq('#' + fieldTab[i] + '_selected').attr('size', MAXFIELD);
					jq('#' + fieldTab[i] + '_unselected').attr('size', MAXFIELD);
				} else {
					jq('#' + fieldTab[i] + '_selected').attr('size', fieldSelectedLength);
					jq('#' + fieldTab[i] + '_unselected').attr('size', fieldSelectedLength);
				}
			} 
		} else {
			if(fieldUnselectedLength > MINFIELD)  {
				if(fieldUnselectedLength > MAXFIELD) {
					jq('#' + fieldTab[i] + '_unselected').attr('size', MAXFIELD);
					jq('#' + fieldTab[i] + '_selected').attr('size', MAXFIELD);
				} else {
					jq('#' + fieldTab[i] + '_unselected').attr('size', fieldUnselectedLength);
					jq('#' + fieldTab[i] + '_selected').attr('size', fieldUnselectedLength);
				}
			} 
		}
	}		
});
*/
