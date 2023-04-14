import folium
import json

# Load the GeoJSON file with Istanbul district boundaries
with open('istanbul-districts.json', 'r') as f:
    istanbul_geojson = json.load(f)

# Create a map centered on Istanbul
istanbul_map = folium.Map(location=[41.0082, 28.9784], zoom_start=10)

# Add district boundaries to the map
folium.GeoJson(
    istanbul_geojson,
    style_function=lambda feature: {
        'fillColor': 'red',
        'color': 'black',
        'weight': 1,
        'fillOpacity': 0.3,
    },
    highlight_function=lambda x: {'weight': 3, 'fillOpacity': 0.6},
    tooltip=folium.GeoJsonTooltip(fields=['name'], labels=False),
    popup=folium.GeoJsonPopup(
        fields=['name'],
        labels=False,
        style="background-color: white;",
        popup_classname="folium-popup-content",
        parse_html=False,
        max_width="400",
        show=False,
    ),
).add_to(istanbul_map)

# Save the map as an HTML file
istanbul_map.save('istanbul_map.html')

# Define the HTML content of your web page
html = f"""
<!DOCTYPE html>
<html>
<head>
	<title>Istanbul Districts Map</title>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
	<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
	<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.16.0/umd/popper.min.js"></script>
	<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
</head>
<body>
	<div class="container-fluid">
		<h1 class="text-center my-4">Istanbul Districts Map</h1>
		<div class="row">
			<div class="col-lg-12">
				<iframe src="istanbul_map.html" width="100%" height="600" frameborder="0" style="border:0;"></iframe>
			</div>
			</div>
	</div>
</body>
</html>
"""

with open('index.html', 'w') as f:
    f.write(html)