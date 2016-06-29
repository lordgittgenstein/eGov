$(document).ready(function() {
	$("#search_box").keyup(function() {
		$("#search_div").load("/corect/ajax_search/" + $("#search_box").val());
	});
	
	$("#search_box").bind("enterKey",function() {
		$("#search_div").load("/corect/ajax_search/" + $("#search_box").val());
	});
});