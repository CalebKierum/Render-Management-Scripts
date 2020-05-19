//AppController.prototype.showConnectionBlackoutDialog
// Delay it to a high number



function doThis() {
	//document.getElementsByClassName("jspPane")[0].children[0].children.length
	el = document.getElementsByClassName("jspPane")[0]
	rows = el.children[0].children
	rangeStart = 9
	rangeEnd = 21

	errorClass = "ui-widget-content slick-row  selected ui-state-active odd  error rowtext noborder"
	notGottenToClass = "ui-widget-content slick-row  even  incomplete rowtext noborder"
	inProgress = "ui-widget-content slick-row  selected ui-state-active odd  active rowtext noborder"


	function getRndInteger(min, max) {
	  return Math.floor(Math.random() * (max - min + 1) ) + min;
	}

	console.log("We have " + rows.length)
	function initializeScene() {
		console.log("Initial Scene")
		// About row 30 is in view
		var i;
		for (i = 0; i < rangeEnd; i++) {
			row = rows[i]
			console.log(row)
			row.className = notGottenToClass
		}
	}

	function startUp(num) {
		row = rows[num]
		row.className = inProgress
	}
	function makeShutDown(j) {
		return function(){
	        row = rows[j]
			row.className = errorClass
	    };
	}
	function makeStartUp(j, time){
	    return function(){
	        row = rows[j]
			row.className = inProgress
			setTimeout(makeShutDown(j), getRndInteger(1, 3000));
	    };
	}
	function startThemUp() {
		console.log("Start Them up")
		// Some delay
		var i;
		var delay = 0;
		for (i = rangeEnd - 1; i >= rangeStart; i--) {
			var cpy = i
			delay += getRndInteger(10, 50) * 3
			var time = delay
			setTimeout(makeStartUp(cpy, time), time);

		}

	}
	console.log("TRYING")
	initializeScene()

	setTimeout(() => { startThemUp(); }, 1 * 1000);

	console.log("HI")

}
setTimeout(() => { doThis(); }, 5 * 1000);
