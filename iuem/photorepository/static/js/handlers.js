/*
jq(document).ready(function() { 
 jq('#where_new').blur(function() {
   alert('OK  ' + jq('#where_new').val() );
   jq('#where_new').load("UpdateVocs" , 'where'+'='+(jq('#where_new').val() ));
   // alert('Apres le load. ' + jq('#where_new').val() );
 });
});



jq(document).ready(function() { 
	 jq('#image-base-edit input[name=form.button.save]').click(function() {
	   alert('Apres le load... ' + (jq('#where_selected').val()) );
	   jq("#context").load("UpdateVocs");
	 });
	});

*/
/*
jq(document).ready(function() {
	jq("#plone_jscalendar").ready(function() {
	  var d = new Date();
	  //alert("date : " + d.getUTCFullYear());
	  jq(".edit_form_recording_date_time_0_year").value = d.getUTCFullYear();
	  jq(".edit_form_recording_date_time_0_month").value("01");
	  jq(".edit_form_recording_date_time_0_day").value("01");
	});
});
*/
