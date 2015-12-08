//var apiUrl = 'https://protected-refuge-7067.herokuapp.com';
//DataVis = function(){

var apiUrl = '';
var chartHolder;
var userTemplate;
var currentCaches = [];
var oldCaches = [];
var chartDict = {};

	var makeGetRequest = function(url, onSuccess, onFailure) {
		$.ajax({
			type: 'GET',
			url: apiUrl + url,
            contentType: "application/json",
			dataType: "json",
			success: onSuccess,
			error: onFailure
		});
	};

	var makePostRequest = function(url, data, onSuccess, onFailure) {
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
	
	var update_user = function(data,id){
		console.log('updating cache ' + id);
		var chart = chartDict[id];
		chart.options.data = [];
		var series = {};
		series.type = 'pie';
		series.startAngle = -20;
		series.showInLegend = false;
		series.dataPoints = [];
        //var caches = {};
        
        var i = 0;
        for(i = 0; i < data['cache']['contents'].length; i++){
			//data['cache']['contents'][i] is the data sent to the ith user
            var user_data_for_cache = data['cache']['contents'][i]['data'];
			series.dataPoints.push({name: user_data_for_cache['user_name'], y: user_data_for_cache['bytes_sent']});
        };
		chart.options.data.push(series);
        chart.render();	
	};

	var render_user = function(data,id){
		console.log('adding cache ' + id);
        var newElem = $(userTemplate);
        newElem.removeAttr('id');
        newElem.attr('id', id);
        chartHolder.append(newElem);
        
        var chart = new CanvasJS.Chart(id);
		chartDict[id] = chart;
		chart.options.toolTip = {enabled: true};
        chart.options.axisY = { prefix: "Chunks Sent "};
		chart.options.title = { text: 'Cache ' + id };
        chart.options.data = [];
		var series = {};
		series.type = 'pie';
		series.startAngle = -20;
		series.showInLegend = false;
		series.dataPoints = [];
        //var caches = {};
        
        var i = 0;
        for(i = 0; i < data['cache']['contents'].length; i++){
			//data['cache']['contents'][i] is the data sent to the ith user
            var user_data_for_cache = data['cache']['contents'][i]['data'];
			series.dataPoints.push({name: user_data_for_cache['user_name'], y: user_data_for_cache['bytes_sent']});
        };
		chart.options.data.push(series);
        chart.render();
    };
	var delete_user = function(id){
		console.log('removing cache ' + id);
			delete chartDict[id];
			$('#' + id).remove();
			
		};

	var start_window = function() {	
		var onSuccess = function(data){
			//Return dictionary of {professor: prof_name, rating_1: value, rating_2: value, etc}
			console.log(data)
            //chartHolder.html('');
            var i = 0;
			oldCaches = currentCaches;
			currentCaches = [];
			
			//For each of the current users, either update their graph or render a new graph
			for(i = 0; i < data.length; i++){
				currentCaches.push(data[i]['cache']['full_address']);
			};
			
			for(i = 0; i < oldCaches.length; i++){
				var old_user = oldCaches[i];
				if((currentCaches.indexOf(old_user) == -1) && (old_user != null)){
					delete_user(old_user);	
				};
			};
			
            for(i = 0; i < currentCaches.length; i++){
				var u_name = currentCaches[i];
				if(oldCaches.indexOf(u_name) == -1){
            		render_user(data[i],u_name);
				}else{
					update_user(data[i],u_name);	
				};
            };    
		};	
		var onFailure = function(data){
		//console.error('could not retreive overall ratings');
            console.error(data);
            console.log('there was an error');
		};
		makeGetRequest('/req/GET_CACHE_DATA2', onSuccess, onFailure);
		
		window.setInterval(function(){
		makeGetRequest('/req/GET_CACHE_DATA2', onSuccess, onFailure);	
	}, 10000);	
	};

	var start = function() {
    	chartHolder = $('#allChartHolder');
    	chartHolder = $('body');
    	userTemplate = $('#user-template')[0].outerHTML;
    	chartHolder.html('');
		
		
		start_window();	
};

$(document).ready(function() {
	start();	
});
