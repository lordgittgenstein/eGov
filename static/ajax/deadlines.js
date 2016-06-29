$(document).ready(function() {
	$("#my_content_div").load("/corect/ajax_mydeadlines/" + $("#my_page_number").val());	

	$("#sub_content_div").load("/corect/ajax_subdeadlines/" + $("#sub_page_number").val());

	$("#search_box").keyup(function() {
		$("#search_div").load("/corect/ajax_search/" + $("#search_box").val());
	});
});
function my_previous_button_fun() {
	var page = parseInt($("#my_page_number").val()) - 1;
	$("#my_page_number").attr('value', page);
	if (page > 0)
		$("#my_content_div").load("/corect/ajax_mydeadlines/" + page);
	else
		$("#my_content_div").load("/corect/ajax_mydeadlines/1");
}
function my_next_button_fun() {
	var page = parseInt($("#my_page_number").val()) + 1;
	$("#my_page_number").attr('value', page);
	if (page != 0)
		$("#my_content_div").load("/corect/ajax_mydeadlines/" + page);
	else
		$("#my_content_div").load("/corect/ajax_mydeadlines/1");
}
function my_i_button_fun(i) {
	var page = i;
	$("#my_page_number").attr('value', page);
	if (page != 0)
		$("#my_content_div").load("/corect/ajax_mydeadlines/" + page);
	else
		$("#my_content_div").load("/corect/ajax_mydeadlines/1");
}
function my_first_button_fun() {
	$("#my_page_number").attr('value', 1);
	$("#my_content_div").load("/corect/ajax_mydeadlines/1");
}
function my_last_button_fun() {
	var page = $("#my_total_pages").attr('value');
	$("#my_page_number").attr('value', page);
	if (page > 0)
		$("#my_content_div").load("/corect/ajax_mydeadlines/" + page);
	else
		$("#my_content_div").load("/corect/ajax_mydeadlines/1");
}
function sub_previous_button_fun() {
	var page = parseInt($("#sub_page_number").val()) - 1;
	$("#sub_page_number").attr('value', page);
	if (page > 0)
		$("#sub_content_div").load("/corect/ajax_subdeadlines/" + page);
	else
		$("#sub_content_div").load("/corect/ajax_subdeadlines/1");
}
function sub_next_button_fun() {
	var page = parseInt($("#sub_page_number").val()) + 1;
	$("#sub_page_number").attr('value', page);
	if (page != 0)
		$("#sub_content_div").load("/corect/ajax_subdeadlines/" + page);
	else
		$("#sub_content_div").load("/corect/ajax_subdeadlines/1");
}
function sub_i_button_fun(i) {
	var page = i;
	$("#sub_page_number").attr('value', page);
	if (page != 0)
		$("#sub_content_div").load("/corect/ajax_subdeadlines/" + page);
	else
		$("#sub_content_div").load("/corect/ajax_subdeadlines/1");
}
function sub_first_button_fun() {
	$("#sub_page_number").attr('value', 1);
	$("#sub_content_div").load("/corect/ajax_subdeadlines/1");
}
function sub_last_button_fun() {
	var page = $("#sub_total_pages").attr('value');
	$("#sub_page_number").attr('value', page);
	if (page > 0)
		$("#sub_content_div").load("/corect/ajax_subdeadlines/" + page);
	else
		$("#sub_content_div").load("/corect/ajax_subdeadlines/1");
}