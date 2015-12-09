//var apiUrl = 'https://protected-refuge-7067.herokuapp.com';
//DataVis = function(){

var apiUrl = '';
var chartHolder;
var userTemplate;
var currentUsers = [];
var oldUsers = [];
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
		console.log('updating user ' + id);
		var chart = chartDict[id];
		chart.options.data = [];
		var series = {};
		series.type = 'column';
		series.name = data[0]['data']['video_name'];
		series.showInLegend = true;
		series.dataPoints = [];
       
		var i = 0;
        for(i = 0; i < data.length; i++){
            var cache_data_for_user = data[i]['data'];
			//series.dataPoints.push({label: cache_data_for_user['full_address'], y: cache_data_for_user['number_of_chunks']});
        	series.dataPoints.push({x: i, label: cache_data_for_user['full_address'], y: cache_data_for_user['number_of_chunks']});
        
		};
		chart.options.data.push(series);
        chart.render();
		
	};

	var render_user = function(data,id){
		console.log('adding user ' + id);
        var newElem = $(userTemplate);
        newElem.removeAttr('id');
        newElem.attr('id', id);
        chartHolder.append(newElem);
        
        var chart = new CanvasJS.Chart(id);
		chartDict[id] = chart;
        chart.options.axisY = { title: "Chunks Received"};
		chart.options.axisX = { title: "Caches"};
        chart.options.title = { text: id };
        chart.options.data = [];
		var series = {};
		series.type = 'column';
		series.name = data[0]['data']['video_name'];
		series.showInLegend = true;
		series.dataPoints = [];
       
		var i = 0;
        for(i = 0; i < data.length; i++){
            var cache_data_for_user = data[i]['data'];
			//series.dataPoints.push({label: cache_data_for_user['full_address'], y: cache_data_for_user['number_of_chunks']});
        	series.dataPoints.push({x: i, label: cache_data_for_user['full_address'], y: cache_data_for_user['number_of_chunks']});
        
		};
		chart.options.data.push(series);
        chart.render();
    };
	var delete_user = function(id){
		console.log('removing user ' + id);
			delete chartDict[id];
			document.getElementById(id).remove();
			
		};

	var start_window = function() {	
		var onSuccess = function(data){
			console.log(data)
            //chartHolder.html('');
            var i = 0;
			oldUsers = currentUsers;
			currentUsers = [];
			
			//For each of the current users, either update their graph or render a new graph
			for(i = 0; i < data.length; i++){
				currentUsers.push(data[i][0]['data']['user_name']);
			};
			
			for(i = 0; i < oldUsers.length; i++){
				var old_user = oldUsers[i];
				if((currentUsers.indexOf(old_user) == -1) && (old_user != null)){
					delete_user(old_user);	
				};
			};
			
            for(i = 0; i < currentUsers.length; i++){
				var u_name = currentUsers[i];
				if(oldUsers.indexOf(u_name) == -1){
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
		makeGetRequest('/req/GET_CACHE_DATA', onSuccess, onFailure);
		
		window.setInterval(function(){
		makeGetRequest('/req/GET_CACHE_DATA', onSuccess, onFailure);	
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
	/*
		return {
		start: start
	};
	*/
