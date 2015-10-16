
var canvas;
var ctx;

var ctxWidth;
var ctxHeight;


$( document ).ready( function (e) {

canvas = $("#CMap")[0];
console.log(canvas);

var context = canvas.getContext('2d');
context.clearRect(0, 0, canvas.width, canvas.height);
context.font = '18pt Calibri';
context.fillStyle = 'black';
//context.fillText("Dessine moi un mouton !", 10, 25);

ctx = context;



$(window).resize(onResizeCanvas);

console.log("hoy");

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




      var ctx = canvas.getContext('2d');
      var centerX = canvas.width / 2;
      var centerY = canvas.height / 2;
      var radius = 70;

      ctx.beginPath();
      ctx.arc(centerX, centerY, radius, 0, 2 * Math.PI, false);
      ctx.fillStyle = 'green';
      ctx.fill();
      ctx.lineWidth = 5;
      ctx.strokeStyle = '#003300';
      ctx.stroke();


      var JsonMapParsed = JSON.parse(JsonMap);
      var vertices = JsonMapParsed["areas"][0]["map"]["vertices"];

      console.log(JsonMapParsed);	

      for(var i = 0 ; i < vertices.length; i++){
      	console.log(vertices[i]["x"]*ctxWidth);
		var centerX = vertices[i]["x"]*ctxWidth;
		var centerY = vertices[i]["y"]*ctxHeight;
		ctx.beginPath();
		ctx.arc(centerX, centerY, 10, 0, 2 * Math.PI, false);
		ctx.fillStyle = 'green';
		ctx.fill();
		ctx.lineWidth = 5;
		ctx.strokeStyle = '#003300';
		ctx.stroke();
      }


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







