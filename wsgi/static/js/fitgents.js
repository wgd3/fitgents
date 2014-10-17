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
				console.log(ajaxResult);
				console.log("Successful ajax call for food record request, launching modal");
				var recordModal = $("#modal_food");
								
				$("#inputDate").val(ajaxResult['timestamp']);
				$("#inputCalories").val(ajaxResult['calories']);
				$("#inputCarbohydrates").val(ajaxResult['carbohydrates']);
				$("#inputCheatDay").val(ajaxResult['cheat_day']);
				$("#inputFat").val(ajaxResult['fat']);
				$("#inputNotes").val(ajaxResult['notes']);
				$("#inputProtein").val(ajaxResult['protein']);
				
				// update the URL to POST to
				recordModal.find("form").first().attr("action", "/food/record/"+recordNum);
				
				recordModal.modal('show');
			},
			error: function() {
				console.log("Error with AJAX request");
			},
		});
	});
	
	$('#modal_food').on('hidden.bs.modal', function (e) {
		// reset the modal any time it's closed
	
	  $(this).find("form").first().attr("action", "/food/new");
	  console.log("Reset the URL for the food modal form");
	  
	  $(this).find("input").each( function(){
	  	$(this).val("");
	  });
	})
	
	// This code segment is for dynamically calculating the lean muscle amount on the modal_bodylog page
	$("#inputBodyFat").change( function() {
		console.log("Detected a change in the inputBodyFat field");
		var bodyWeightInput = $("#inputWeight");
		var valBodyWeight = parseFloat(bodyWeightInput.val());
		
		if (valBodyWeight != 0) {
				var valBodyFat = parseFloat($(this).val())/100;
				console.log("Calculated body fat to be " + String(valBodyFat));
				
				var valLeanMusclePerc = 1 - valBodyFat;
				console.log("Found the lean muscle percentage to be " + String(valLeanMusclePerc));
				
				var valLeanMuscleWeight = valBodyWeight * valLeanMusclePerc;
				console.log("Found total lean muscle to be " + String(valLeanMuscleWeight));
				
				var leanMuscleInput = $("#inputLeanMuscle");
				leanMuscleInput.val(valLeanMuscleWeight.toFixed(2));
		} else {
			var leanMuscleInput = $("#inputLeanMuscle");
			leanMuscleInput.val("0");
		};
	});
});
