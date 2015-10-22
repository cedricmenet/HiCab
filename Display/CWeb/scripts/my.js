
var canvas;
var ctx;

var ctxWidth;
var ctxHeight;
var txt_height;

var JsonMapParsed;
var JSONCab

var id =1// id de la map


$( document ).ready( function (e) {

	canvas = $("#CMap")[0];
	console.log(canvas);


	JsonMapParsed = JSON.parse(JsonMap);

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

function cabRequest(event){
	console.log("click " + event.clientX + " " + event.clientY )
	var tmp = JsonMapParsed["areas"][id]["map"]["streets"]
	
	
	var shouldreverse = 1
	var nearestStreet
	var bestDist = 100000
	var bestdx
	var bestdy
	var progression = 1
	
	for(var i = 0 ; i < tmp.length; i++){
		
		//get vertex of street
		var va = getVerticeByName(JsonMapParsed["areas"][id]["map"]["vertices"], tmp[i]["path"][0]);
		var vb = getVerticeByName(JsonMapParsed["areas"][id]["map"]["vertices"], tmp[i]["path"][1]);
		
		var ax = va["x"];
		var ay = va["y"];
		var bx = vb["x"];
		var by = vb["y"];
		
		if(ax > bx){
			var tmpAx = ax;
			var tmpAy = ay;
			ax = bx;
			ay = by;
			bx = tmpAx;
			by = tmpBy;
			
		}
		
		var dist = 100000;
		var cx = event.clientX / ctxWidth;
		var cy = event.clientY / ctxHeight;
		
		// find d
		var dx;
		var dy;
		
			
		if(ax == bx){
			dist = Math.abs(ax - cx);
			dx = ax;
			dy = cy;
		}
		else if ( ay == by){
			dist = Math.abs(ay - cy);
			dx = cx;
			dy = ay;
		}
		else{
			var v0 = (bx-ax)*(cy-ay*)*(by-ay);
			var v1 = cx*Math.pow(bx-ax,2)+ax*Math.pow(by-ay,2);
			var v2 = (Math.pow(bx-ax,2)+Math.pow(by-ay));
			
			dx = (v0 + v1) / v2;
			dy = (by-ay)/(bx-ax)*(dx-ax)+ay;
			
			dist= Math.sqrt(Math.pow(cx-dx,2)+Math.pow(cy-dy,2));
			
			
		}
		
		if((( dx >= ax && dx <=bx) || (dx <= ax && dx >=bx)) && (( dx >= ay && dy <=by) || (dy <= ay && dy >=by)))
		{
			//candidat
			if(bestDist > dist){
				progression = Math.sqrt(Math.pow(ax-dx,2)+Math.pow(ay-dy,2))/Math.sqrt(Math.pow(ax-bx,2)+Math.pow(ay-by,2))
				if(shouldreverse == 1)
					progression = 1 - progression;
				
				bestDist = dist
				nearestStreet = tmp[i]
				bestdx = dx
				bestdy = dy
			}	
				
		}
		
	
	}
	
	var JSONrequest =
	{
		"location": {
			"backward": false,
			"name": nearestStreet["name"],
			"weight": 1.0,
			"area": nearestStreet["area"],
			"loc_type": "street",
			"path": [nearestStreet["path"][0],nearestStreet["path"][1]],
			"oneway": nearestStreet["oneway"],
			"progression": progression,
			"coord": {
				"y": dy,
				"x": dx
			}
		}
	}
	
}


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


	/*if(JsonMapParsed["areas"][1] != undefined){
		id = 1;
	}
	else */
	if(JsonMapParsed["areas"][id] != undefined)
	{
		var vertices = JsonMapParsed["areas"][id]["map"]["vertices"];

		console.log(JsonMapParsed);
		var streets = JsonMapParsed["areas"][id]["map"]["streets"];
		
		for(var i = 0 ; i < streets.length; i++){
			
			if (streets[i]["path"].length != 2)
			console.log("ERREUR : Path contain more than 2 vertices");
			else{
				
				//getting vertices
				var verticeA = getVerticeByName(vertices,streets[i]["path"][0]);
				var verticeB = getVerticeByName(vertices,streets[i]["path"][1])
				
				//drawing line between 2 vertices
				
				ctx.lineWidth = 5;
				ctx.beginPath();
				ctx.moveTo(verticeA["x"]*ctxWidth,verticeA["y"]*ctxHeight);
				ctx.lineTo(verticeB["x"]*ctxWidth,verticeB["y"]*ctxHeight);
				ctx.stroke();
				
				
				
				//drawing street Name				
				var txt = streets[i]["name"];
				ctx.font="30px Verdana";
				txt_height = 30;
				var txt_width = ctx.measureText(txt).width;
				
				var center_txt_x = verticeA["x"] + Math.abs(verticeA["x"] - verticeB["x"])/2;
				var center_txt_y = verticeA["y"] + Math.abs(verticeA["y"] - verticeB["y"])/2;
				
				// normalise to canavas
				center_txt_x *= ctxWidth; 
				center_txt_y *= ctxHeight;
				
				
				ctx.beginPath();
				ctx.fillStyle = 'white';
				
				ctx.lineWidth = 2;
				ctx.strokeStyle = 'black';
				
				ctx.fillRect(center_txt_x-txt_width/2,center_txt_y-txt_height/2,txt_width,txt_height);
				ctx.rect(center_txt_x-txt_width/2,center_txt_y-txt_height/2,txt_width,txt_height);
				ctx.stroke();
				
				
				ctx.fillStyle = 'black';
				ctx.textAlign = 'center';
				ctx.textBaseline = 'middle';
				ctx.fillText(txt,center_txt_x,center_txt_y);
				
				
				
			}

			
		}
	
	
	

		for(var i = 0 ; i < vertices.length; i++){
			console.log(vertices[i]["x"]*ctxWidth);
			var txt = vertices[i]["name"]
			ctx.font="30px Verdana";
			var txt_width = ctx.measureText(txt).width;
			console.log(ctx.measureText(txt));
			
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
			ctx.textBaseline = 'middle';
			ctx.fillText(txt,centerX,centerY);
		}
	}
	console.log("cab")
	if(JSONCab != undefined && JSONCab["cab_infos"] != undefined)
	{console.log("cab")
		for(var i = 0;i<JSONCab["cab_infos"].length;i++){
			console.log("cab")
			if(JSONCab["cab_infos"][i]["location"]["area"] == JsonMapParsed["areas"][id]["name"])
			{
				// on est sur la bonne map
				var shortcut = JSONCab["cab_infos"][i]["location"];

				var x = shortcut["coord"]["x"]*ctxWidth;
				var y = shortcut["coord"]["y"]*ctxHeight;

				ctx.beginPath();
				ctx.arc(x, y, 20, 0, 2 * Math.PI, false);
				ctx.fillStyle = 'blue';
				ctx.fill();
				ctx.lineWidth = 5;
				ctx.strokeStyle = 'grey';
				ctx.stroke();

				ctx.fillStyle = 'grey';
				ctx.textAlign = 'center';
				ctx.textBaseline = 'middle';
				ctx.fillText(JSONCab["cab_infos"][i]["id_cab"],x,y);
				
				



			}
		}
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







