$(document).ready(function() {
	$("#content_div").load("/corect/ajax_subordinates/" + $("#page_number").val());

	$("#search_box").keyup(function() {
		$("#search_div").load("/corect/ajax_search/" + $("#search_box").val());
	});

});

function sub_previous_button_fun() {
	var page = parseInt($("#page_number").val()) - 1;
	$("#page_number").attr('value', page);
	if (page > 0)
		$("#content_div").load("/corect/ajax_subordinates/" + page);
	else
		$("#content_div").load("/corect/ajax_subordinates/1");
}
function sub_next_button_fun() {
	var page = parseInt($("#page_number").val()) + 1;
	$("#page_number").attr('value', page);
	if (page != 0)
		$("#content_div").load("/corect/ajax_subordinates/" + page);
	else
		$("#content_div").load("/corect/ajax_subordinates/1");
}
function first_button_fun() {
	$("#page_number").attr('value', 1);
	$("#content_div").load("/corect/ajax_subordinates/1");
}

function last_button_fun() {
	var page = $("#total_pages").attr('value');
	$("#page_number").attr('value', page);
	if (page > 0)
		$("#content_div").load("/corect/ajax_subordinates/" + page);
	else
		$("#content_div").load("/corect/ajax_subordinates/1");

}
function i_button_fun(i) {
	var page = i;
	$("#page_number").attr('value', page);
	if (page != 0)
		$("#content_div").load("/corect/ajax_subordinates/" + page);
	else
		$("#content_div").load("/corect/ajax_subordinates/1");
}