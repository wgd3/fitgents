$(document).ready(function() {
	
	$(".editRowLink").on('click', function (e) {
		e.preventDefault();
		
		console.log("User triggered a row-editing modal for row " + String($(this).data('recordnum')));
		
		$("#modal_food_rowedit").modal('show');
		
		// add the correct action to the form (since this edit modal is multipurpose for all pages)
		var recordNum = $(this).data('recordnum');
		
		var editURL;
		var dbtable = $(this).data('dbtable');
		
		switch (dbtable) {
			case 'FoodHistory':
				editURL = '/food/edit/';
				break;
			case 'SleepHistory':
				editURL = '/sleep/edit/';
				break;
			case 'BodyHistory':
				editURL = '/body/edit/';
				break;
			case 'ExcerciseHistory':
				editURL = '/excercise/edit/';
				break;
		};
		
		$("#rowEditForm").attr("action", editURL+String(recordNum));
		console.log("Created edit URL: " + $("#rowEditForm").attr("action"));
		
		$("#rowEditForm").attr("method", "post");
		
		var dbtable = $(this).data('dbtable');
		console.log("Setting dbtable for rowEditForm to "+dbtable);
		$("#rowEditForm").data("dbtable", dbtable);
		
		
		
	});
});
