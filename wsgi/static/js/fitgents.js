$(document).ready( function() {

	$(".editrow_food").on("click", function(e) {
		e.preventDefault();
		
		var recordNum = $(this).data('record');
		console.log("User clicked editrow link for record number "+ String(recordNum));
		
		$.ajax({
			url: '/food/record/'+recordNum,
			type: 'get',
			dataType: 'json',
			success: function(ajaxResult){
				console.log("Successful ajax call for food record request, launching modal");
				var recordModal = $("#modal_food");
								
				$("#inputDate").val(ajaxResult['timestamp']);
				$("#inputCalories").val(ajaxResult['calories']);
				$("#inputCarbohydrates").val(ajaxResult['carbohydrates']);
				$("#inputCheatDay").val(ajaxResult['cheat_day']);
				$("#inputFat").val(ajaxResult['fat']);
				$("#inputNotes").val(ajaxResult['notes']);
				$("#inputProtein").val(ajaxResult['protein']);
				
				recordModal.modal('show');
			},
			error: function() {
				console.log("Error with AJAX request");
			},
		});
	});
});