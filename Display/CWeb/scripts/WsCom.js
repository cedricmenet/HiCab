

var RaspPyIP = "192.168.1.1";

$(document).ready(function(){

	//get MAP
	$.ajax( {
		type:'Get',
		url:'http://' + RaspPyIP + '/getmap',
		success:function(data) {
			console.log(data);
			
			JsonMapParsed = data;
			DrawMap()
		}
	});
	
	//get Ws channel
	$.ajax( {
		type:'Get',
		url:'http://' + RaspPyIP + '/subscribe/display',
		success:function(data) {
			console.log(data);
			
			
			
			socket = new WebSocket("ws://" + location.host + "/"+data["channel"]);
			socket.onopen = function() {
				console.log("WS open")
				/*message = {'id_cab': $('#lbl_id').text() };
				socket.send(JSON.stringify(message));*/
			};
			socket.onclose = function() {
			   console.log("WS close");
			};
			socket.onmessage = function(evt){
				
				JSONCab = JSON.parse( eval(evt)["data"])
				console.log(JSONCab)
				
				console.log("WS MESSAGE :" + eval(evt));
				DrawMap()
				
				
				/*var string = '('+ evt["data"].replace(/None/g,"null") + ')';
				console.log(string);
				console.log(eval(string));
				console.log(JSON.stringify(eval(string)));*/
				
				
				
				/*
				
				
				*/
			}
			
			
			
			
		}
	});
	
	
	
	

});
