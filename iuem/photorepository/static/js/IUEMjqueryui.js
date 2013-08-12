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

// WATERMARK
// http://www.patrick-wied.at/static/watermarkjs/
// warning : the usage is not like the sources of the demo,
// see : http://stackoverflow.com/questions/10841367/how-do-i-add-a-watermark-to-an-image-client-side-with-javascript
// it should be more useful if the config is passed thru controlpannel...?
// TODO : adapt controlpanel for config of watermark... probably with textarea containing the javascript code
// for the config (see below 'var config = { ......')
jq(document).ready(function() {
	jq('div.toWatermark img').addClass('watermark');
	
	var config = {
		/* config goes here */
		"position": "bottom-left", // default "bottom-right"
		"opacity": 8, // default 50
		"className": "watermark", // default "watermark"
		"path": "filigrane2.png"  // this image must be placed in an accessible folder. ie. portal_skins/custom
	};
	jq(document).watermark(config);
	// alert (portal_url) ;
});