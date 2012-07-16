jq(document).ready(function() {
    // Accordion
    jq("#accordion").accordion({ header: "h3" });
});

jq(document).ready(function() {
	$(".iuemCollapsedHeading.iuemCollapsed").next().hide();
 
	$(".iuemCollapsedHeading").click(function() {
	  $(this).next().slideToggle("fast");
	  $(this).toggleClass("iuemCollapsed");
	});
});