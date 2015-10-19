

var RaspPyIP = "192.168.1.1";

$(document).ready(function(){

	$.ajax( {
		type:'Get',
		url:'http://' + RaspPyIP + '/getmap',
		success:function(data) {
			console.log(data);
			
			JsonMapParsed = data;
		}
	});

});
