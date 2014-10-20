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

function getPearsonCorrelation(x, y) {
	// Correlation equation for statical analysis
	
	// -.3 - .3 = Low
	// -.8 - .8 = High
	//  -1 -  1 = Perfect
	
	var shortestArrayLength = 0;
	 
	if(x.length == y.length) {
		shortestArrayLength = x.length;
	} else if(x.length > y.length) {
		shortestArrayLength = y.length;
		console.error('x has more items in it, the last ' + (x.length - shortestArrayLength) + ' item(s) will be ignored');
	} else {
		shortestArrayLength = x.length;
		console.error('y has more items in it, the last ' + (y.length - shortestArrayLength) + ' item(s) will be ignored');
	}
  
	var xy = [];
	var x2 = [];
	var y2 = [];
  
	for(var i=0; i<shortestArrayLength; i++) {
		xy.push(x[i] * y[i]);
		x2.push(x[i] * x[i]);
		y2.push(y[i] * y[i]);
	}
  
	var sum_x = 0;
	var sum_y = 0;
	var sum_xy = 0;
	var sum_x2 = 0;
	var sum_y2 = 0;
  
	for(var i=0; i< shortestArrayLength; i++) {
		sum_x += x[i];
		sum_y += y[i];
		sum_xy += xy[i];
		sum_x2 += x2[i];
		sum_y2 += y2[i];
	}
  
	var step1 = (shortestArrayLength * sum_xy) - (sum_x * sum_y);
	var step2 = (shortestArrayLength * sum_x2) - (sum_x * sum_x);
	var step3 = (shortestArrayLength * sum_y2) - (sum_y * sum_y);
	var step4 = Math.sqrt(step2 * step3);
	var answer = step1 / step4;
  
	return answer;
}
