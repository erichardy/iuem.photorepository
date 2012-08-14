jq(document).ready(function() {
    // Accordion
    jq("#accordion").accordion({ header: "h3" });
    jq('#siteaction-sitemap a').prepOverlay({
        subtype: 'ajax',
        filter: '#content > *',
        config: {expose:{color:'#00f'}}
        });
    jq('#ask-an-image').prepOverlay({
        subtype: 'ajax',
        filter: '#content > *',
        formselector: 'form',
        config: {expose:{color:'#00f'}}
        });


});

jq(document).ready(function() {
	jq(".iuemCollapsedHeading.iuemCollapsed").next().hide();
 
	jq(".iuemCollapsedHeading").click(function() {
	  jq(this).next().slideToggle("fast");
	  jq(this).toggleClass("iuemCollapsed");
	});
});
