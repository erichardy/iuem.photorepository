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


// Disable right click script
// source http://www.electrictoolbox.com/jquery-modify-right-click-menu/
jq(document).ready(function() {
	jq('div.viewImage img').bind("contextmenu", function(e) {
	    return false;
	});
});
