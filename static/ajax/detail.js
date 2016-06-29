$(document).ready(function() {

	$(function() {
		$("#id_date_input").datepicker({
			dateFormat : 'yy-mm-dd'
		});
	});

	$("#key_div").hide();	
	$("#key_button").click(function() {
		$("#key_button").hide();
		$("#key_div").show();
	});

});