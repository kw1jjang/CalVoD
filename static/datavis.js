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

	var render_user = function(data,id){
        var newElem = $(userTemplate);
        newElem.removeAttr('id');
        newElem.attr('id', id);
        chartHolder.append(newElem);
        
        var chart = new CanvasJS.Chart(id);
		chartDict[id] = chart;
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
	var delete_user = function(id){
			delete chartDict[id];
			$('#' + id).remove();
			
		};

	var start_window = function() {	
		var onSuccess = function(data){
			//Return dictionary of {professor: prof_name, rating_1: value, rating_2: value, etc}
			console.log(data)
            //chartHolder.html('');
            var i = 0;
			oldUsers = currentUsers;
			currentUsers = [];
			
			//For each of the current users, either update their graph or render a new graph
			for(i = 0; i < data.length; i++){
				currentUsers.push(data[i][0]['data']['user_name']);
			};
			
			for(i = 0; i < data.length; i++){
				var old_user = oldUsers[i];
				if((currentUsers.indexOf(old_user) == -1) && (old_user != null)){
					delete_user(old_user);	
				};
			};
			
            for(i = 0; i < data.length; i++){
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
