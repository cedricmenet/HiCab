
var canvas;
var ctx;

var ctxWidth;
var ctxHeight;
var txt_height;


$( document ).ready( function (e) {

canvas = $("#CMap")[0];
console.log(canvas);

ctx = canvas.getContext('2d');
ctx.clearRect(0, 0, canvas.width, canvas.height);
ctx.font="30px Verdana";
txt_height = 30;
ctx.fillStyle = 'black';
ctx.textAlign = 'center';




$(window).resize(onResizeCanvas);

console.log("hoy");

onResizeCanvas();

DrawMap();

});


function onResizeCanvas(){

	ctxWidth = ctx.canvas.width = canvas.offsetWidth;
	ctxHeight = ctx.canvas.height = canvas.offsetHeight;

	console.log("hey" + canvas.offsetWidth);
	DrawMap();
}

//dessine une map Json
function DrawMap(JMap){



		ctx.fillStyle = 'white';
      ctx.clearRect(0,0,canvas.width,canvas.height);
      var centerX = canvas.width / 2;
      var centerY = canvas.height / 2;
      var radius = 70;

      /*ctx.beginPath();
      ctx.arc(centerX, centerY, radius, 0, 2 * Math.PI, false);
      ctx.fillStyle = 'green';
      ctx.fill();
      ctx.lineWidth = 5;
      ctx.strokeStyle = '#003300';
      ctx.stroke();*/


      var JsonMapParsed = JSON.parse(JsonMap);
      var vertices = JsonMapParsed["areas"][0]["map"]["vertices"];

      console.log(JsonMapParsed);
	  var streets = JsonMapParsed["areas"][0]["map"]["streets"];
	  
		for(var i = 0 ; i < streets.length; i++){
			
			if (streets[i]["path"].length != 2)
				console.log("ERREUR : Path contain more than 2 vertices");
			else{
				var verticeA = getVerticeByName(vertices,streets[i]["path"][0]);
				var verticeB = getVerticeByName(vertices,streets[i]["path"][1])
				//drawing line between 2 vertices
				
				ctx.lineWidth = 5;
				ctx.beginPath();
				ctx.moveTo(verticeA["x"]*ctxWidth,verticeA["y"]*ctxHeight);
				ctx.lineTo(verticeB["x"]*ctxWidth,verticeB["y"]*ctxHeight);
				ctx.stroke();
				
				
			}

			
		}
	  
	  

      for(var i = 0 ; i < vertices.length; i++){
      	console.log(vertices[i]["x"]*ctxWidth);
		var txt = vertices[i]["name"]
		ctx.font="30px Verdana";
		var txt_width = ctx.measureText(txt).width;
		
		var centerX = vertices[i]["x"]*ctxWidth;
		var centerY = vertices[i]["y"]*ctxHeight;
		ctx.beginPath();
		ctx.arc(centerX, centerY, txt_width, 0, 2 * Math.PI, false);
		ctx.fillStyle = 'white';
		ctx.fill();
		ctx.lineWidth = 5;
		ctx.strokeStyle = 'black';
		ctx.stroke();
		
		ctx.fillStyle = 'black';
		
		ctx.textAlign = 'center';
		ctx.fillText(txt,centerX,centerY);
      }


}


function getVerticeByName(array, vertice_name){
	
	for(var i = 0 ; i < array.length;i++){
		if(array[i]["name"] == vertice_name)
			return array[i];
	}
	return undefined;
}


var JsonMap = "\
{\
	\"areas\": [\
	  	{ \"name\": \"Quartier Nord\",\
	    	\"map\": {\
		      	\"weight\": {\"w\": 1, \"h\": 1},\
		      	\"vertices\": [\
		        	{\"name\": \"m\", \"x\": 0.5, \"y\": 0.5},\
		        	{\"name\": \"b\", \"x\": 0.5, \"y\": 1}\
		      	],\
				\"streets\": [\
					{\"name\": \"mb\", \"path\": [\"m\", \"b\"], \"oneway\": false}\
				],\
			  	\"bridges\": [\
				    { \"from\": \"b\",\
				      \"to\": {\
				        \"area\": \"Quartier Sud\",\
				        \"vertex\": \"h\"},\
				      \"weight\": 2\
					} \
				]\
			}\
		}\
	]\
}";







