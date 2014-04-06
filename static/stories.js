$(document).ready( function() {
	$("#submit").click( function() {
		var form = JSON.stringify(
				{
					title: $("#title").val(),
					body_text: $("#story").val()
				});
		console.log(form);
		$.ajax({
			url: "/",
			contentType: "application/json",
			dataType: "json",
			type: "POST",
			data: form,
			success: function(data) {
				$("#storyID").val(document.URL + data["id"]);
				$("#storyID").toggle("fast");
			}
		});
	});
});
