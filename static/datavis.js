//var apiUrl = 'https://protected-refuge-7067.herokuapp.com';
var apiUrl = '';
var chartHolder;
var userTemplate;
makeGetRequest = function(url, onSuccess, onFailure) {
		$.ajax({
			type: 'GET',
			url: apiUrl + url,
            contentType: "application/json",
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
    chartHolder = $('#allChartHolder');
    //chartHolder = $('body');
    userTemplate = $('#user-template')[0].outerHTML;
    chartHolder.html('');
    
	/*var chart = new CanvasJS.Chart("chartContainer");

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
	*/
    var render_users = function(data,id){
        
        var newElem = $(userTemplate);
        newElem.removeAttr('id');
        newElem.attr('id','test'+id);
        chartHolder.append(newElem);
        
        var chart = new CanvasJS.Chart('test'+id);
        chart.options.axisY = { prefix: "Chunks Sent "};
        chart.options.data = [];
        var caches = {};
        
        var i = 0;
        for(i = 0; i < data.length; i++){
            var cache_data_for_user = data[i]['data'];
            var series = {
                type: "column",
                name: cache_data_for_user['full_address'],
                showInLegend: true
            };
            
            chart.options.data.push(series);
            
            series.dataPoints = [
                { label: cache_data_for_user['full_address'], y: cache_data_for_user['number_of_chunks'] }
                ];   
            
        };
        chart.render();
        
        
    };
    
    
	
	window.setInterval(function(){
		h = new Date();
		//series1.dataPoints[0].y = h.getSeconds();
		//chart.render();
		
		var onSuccess = function(data){
			//Return dictionary of {professor: prof_name, rating_1: value, rating_2: value, etc}
			console.log(data)
            chartHolder.html('');
            var i = 0;
            for(i = 0; i < data.length; i++){
            render_users(data[i],i);
            };
            
		};
		var onFailure = function(data){
		//console.error('could not retreive overall ratings');
            console.error(data);
            console.log('there was an error');
		};
		makeGetRequest('/req/GET_CACHE_DATA', onSuccess, onFailure);
		
		
		
		
		
	}, 10000);
	
	
	
	
	
	
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