$(document).ready(function() {

	$("#new_chk").attr('checked', true);
	
	$("#new_chk").change(function() {
		if (this.checked) {
			$("#refer_chk").attr('checked', false);
			$("#old_chk").attr('checked', false);
			window.location.href = "/corect/complaint/";
		}
		else{
			window.location.href = "/corect/complaint/";
		}		
	});

	$("#old_chk").change(function() {
		if (this.checked) {
			$("#new_chk").attr('checked', false);
			$("#refer_chk").attr('checked', false);
			$("#refer_form_div").load("/corect/ajax_form_check");
		}
		else{
			window.location.href = "/corect/complaint/";
		}
	});

	$("#refer_chk").change(function() {
		if (this.checked) {
			$("#new_chk").attr('checked', false);
			$("#old_chk").attr('checked', false);
			$("#refer_form_div").load("/corect/ajax_form_a2");
		}
		else{
			window.location.href = "/corect/complaint/";
		}
	});

	$("#id_division").change(function() {
		$.ajax({
			type : "POST",
			url : "/corect/ajax_locations_under/",
			data : {
				"type" : "division",
				"value" : $("#id_division").val(),
			},
			success : function(data) {
				$("#id_district").html(data);
			},
			error : function() {
				alert("Error: 10203.");
			}
		});
	});

	$("#id_district").change(function() {
		$.ajax({
			type : "POST",
			url : "/corect/ajax_locations_under/",
			data : {
				"type" : "district",
				"value" : $("#id_district").val(),
			},
			success : function(data) {
				$("#id_subdistrict").html(data);
			},
			error : function() {
				alert("Error: 10203.");
			}
		});
	});

	$("#id_subdistrict").change(function() {
		$.ajax({
			type : "POST",
			url : "/corect/ajax_locations_under/",
			data : {
				"type" : "subdistrict",
				"value" : $("#id_subdistrict").val(),
			},
			success : function(data) {
				$("#id_locality").html(data);
			},
			error : function() {
				alert("Error: 10203.");
			}
		});
	});
});
