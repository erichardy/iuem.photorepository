
jq(document).ready(function() { 
 jq('#where_new').blur(function() {
   // alert('OK  ' + jq('#where_new').val() );
   jq('#where_new').load("UpdateVocs" , 'where'+'='+(jq('#where_new').val() ));
   // alert('Apres le load. ' + jq('#where_new').val() );
 });
});