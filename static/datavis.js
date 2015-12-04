//var apiUrl = 'https://protected-refuge-7067.herokuapp.com';
    var apiUrl = '';

makeGetRequest = function(url, onSuccess, onFailure) {
		$.ajax({
			type: 'GET',
			url: apiUrl + url,
			dataType: "json",
			success: onSuccess,
			error: onFailure
		});
	};

	makePostRequest = function(url, data, onSuccess, onFailure) {
		$.ajax({
			type: 'POST',
			url: apiUrl + url,
			data: JSON.stringify(data),
			contentType: "application/json",
			dataType: "json",
			success: onSuccess,
			error: onFailure
		});
	};





$(document).ready(function() {
	var chart = new CanvasJS.Chart("chartContainer");

    chart.options.axisY = { prefix: "$", suffix: "K" };
    chart.options.title = { text: "Fruits sold in First & Second Quarter" };

    var series1 = { //dataSeries - first quarter
        type: "column",
        name: "First Quarter",
        showInLegend: true
    };


    chart.options.data = [];
    chart.options.data.push(series1);


    series1.dataPoints = [
            { label: "banana", y: 18 },
            { label: "orange", y: 29 },
            { label: "apple", y: 40 },
            { label: "mango", y: 34 },
            { label: "grape", y: 24 }
    ];

    chart.render();
	
	
	window.setInterval(function(){
		h = new Date();
		series1.dataPoints[0].y = h.getSeconds();
		chart.render();
		
		var onSuccess = function(data){
			//Return dictionary of {professor: prof_name, rating_1: value, rating_2: value, etc}
			console.log(data)
		};
		var onFailure = function(data){
		//console.error('could not retreive overall ratings');
            console.error(data);
		};
		makeGetRequest('/req/GET_SERVER_ADDRESS', onSuccess, onFailure);
		
		
		
		
		
	}, 1000);
	
	
	
	
	
	
});


/*

function analyze(){
   var f = new FileReader();

   f.onloadend = function(){
       console.log("success");
   }
   f.readAsText("cities.txt");
}

*/