jq(document).ready(function() {
    // Accordion
    jq("#accordion").accordion({ header: "h3" });
});

jq(document).ready(function() {
	jq(".iuemCollapsedHeading.iuemCollapsed").next().hide();
 
	jq(".iuemCollapsedHeading").click(function() {
	  jq(this).next().slideToggle("fast");
	  jq(this).toggleClass("iuemCollapsed");
	});
});
