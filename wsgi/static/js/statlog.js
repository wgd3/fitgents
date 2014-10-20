$(document).ready( function() {
	
	var loadingRow = $("#statLoadRow");
	var statProgressBar = $("#statLoadProgress");
	var loadingHeader = $("#statLoadHeader");
	
	// The hope is to have 6 main "check points" for the loading of the page: 
	// Body/Sleep/Food trends
	// Comparing the data to one another: body vs sleep/body vs food/food vs sleep
	
	// Set headers and header index
	
	var headers = ["Initializing...",
					"Analyzing body trends...",
					"Analyzing sleep trends...",
					"Analyzing food trends...",
					"Comparing body and sleep patterns...",
					"Comparing body and food patterns...",
					"Comparing food and sleep patterns..."]
	var headerIndex = 0;
	
	// Start by setting the loading bar header
	loadingHeader.text(headers[headerIndex]);
	
	// Start with the body (and add in delay)
	headerIndex += 1;
	console.log("Header index: " + String(headerIndex));
	
	loadingHeader.text(headers[headerIndex]);
	console.log("Updating header text to: " + headers[headerIndex]);
	incrementLoadBar(headerIndex, headers.length, statProgressBar);

	// Kick off the animation and stat loading
	analyzeBody();
	
	function updateProgressBar() {
		headerIndex += 1;
		console.log("Header index: " + String(headerIndex));
		
		loadingHeader.text(headers[headerIndex]);
		console.log("Updating header text to: " + headers[headerIndex]);
		
		incrementLoadBar(headerIndex, headers.length, statProgressBar);
	};

	function incrementLoadBar() {
		var percentage = (headerIndex / headers.length) * 100;
		console.log("Increasing progress bar completion to " + String(percentage));
		
		statProgressBar.css({"width": String(percentage)+"%"});
		statProgressBar.text(String(parseInt(percentage))+"%");
		
		return true;
	};
	
	function analyzeBody() {
		console.log("analyzeBody called, starting")
		setTimeout(function() {
			updateProgressBar();
			analyzeSleep();
		}, 1500);
	};
	
	function analyzeSleep() {
		console.log("analyzeSleep called, starting")
		setTimeout(function() {
			updateProgressBar();
			analyzeFood();
		}, 1500);
	};
	
	function analyzeFood() {
		console.log("analyzeFood called, starting")
		setTimeout(function() {
			updateProgressBar();
			compareBodySleep();
		}, 1500);
	};
	
	function compareBodySleep(){
		console.log("compareBodySleep called, starting")
		setTimeout(function() {
			updateProgressBar();
			compareBodyFood();
		}, 1500);
	};
	
	function compareBodyFood(){
		console.log("compareBodyFood called, starting")
		setTimeout(function() {
			updateProgressBar();
			compareSleepFood();
		}, 1500);
	};
	
	function compareSleepFood(){
		console.log("compareSleepFood called, starting")
		updateProgressBar();
	};
});
