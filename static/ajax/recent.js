$(document).ready(function() {
	$("#content_div").load("/corect/ajax_recent/" + $("#page_number").val());

	$("#search_box").keyup(function() {
		$("#search_div").load("/corect/ajax_recent/" + $("#search_box").val());
	});
});
function previous_button_fun() {
	var page = parseInt($("#page_number").val()) - 1;
	$("#page_number").attr('value', page);
	if (page > 0)
		$("#content_div").load("/corect/ajax_recent/" + page);
	else
		$("#content_div").load("/corect/ajax_recent/1");
}
function next_button_fun() {
	var page = parseInt($("#page_number").val()) + 1;
	$("#page_number").attr('value', page);
	if (page != 0)
		$("#content_div").load("/corect/ajax_recent/" + page);
	else
		$("#content_div").load("/corect/ajax_recent/1");
}
function i_button_fun(i) {
	var page = i;
	$("#page_number").attr('value', page);
	if (page != 0)
		$("#content_div").load("/corect/ajax_recent/" + page);
	else
		$("#content_div").load("/corect/ajax_recent/1");
}
function first_button_fun() {
	$("#page_number").attr('value', 1);
	$("#content_div").load("/corect/ajax_recent/1");
}
function last_button_fun() {
	var page = $("#total_pages").attr('value');
	$("#page_number").attr('value', page);
	if (page > 0)
		$("#content_div").load("/corect/ajax_recent/" + page);
	else
		$("#content_div").load("/corect/ajax_recent/1");
}