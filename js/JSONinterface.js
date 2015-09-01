 function loadJSON(callback) 
 {   
    var xobj = new XMLHttpRequest();
        xobj.overrideMimeType("application/json");
		xobj.open('GET', 'my_data.json', true); // Replace 'my_data' with the path to your file
		xobj.onreadystatechange = function() 
		{
			if (xobj.readyState == 4 && xobj.status == "200")
			{
				callback(xobj.responseText);
			}
		};
    xobj.send(null);  
 }