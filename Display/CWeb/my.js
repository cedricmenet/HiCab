
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

      for(var i = 0 ; i < vertices.length; i++){
      	console.log(vertices[i]["x"]*ctxWidth);
		var txt = vertices[i]["name"]
		var txt_width = ctx.measureText(txt).width ;// nombre arbitraire pour avoir 20% de marge avec le texte dans le cercle
		
		var centerX = vertices[i]["x"]*ctxWidth;
		var centerY = vertices[i]["y"]*ctxHeight;
		ctx.beginPath();
		ctx.arc(centerX, centerY, txt_width, 0, 2 * Math.PI, false);
		ctx.fillStyle = 'green';
		//ctx.fill();
		ctx.lineWidth = 5;
		ctx.strokeStyle = '#003300';
		ctx.stroke();
		
		ctx.fillStyle = 'black';
		ctx.font="30px Verdana";
		ctx.textAlign = 'center';
		ctx.fillText(txt,centerX,centerY);
		
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







