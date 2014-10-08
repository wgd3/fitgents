$(document).ready( function() {
	
	var statLog = $(".statlog-background");
	
	var animationSec = 3;
	var animationProgress = 0;
	var animationEnd = .5;
	var animationSpeed = (animationEnd/animationSec);

	
	while (animationProgress <= animationEnd) {
		statLog.css({"background": "linear-gradient(to right, rgba(223, 105, 26, animationProgress), rgba(223, 105, 26, animationProgress+animationSpeed))"});
		setTimeout(function(){animationProgress += animationSpeed}, animationSpeed);
	}
});
