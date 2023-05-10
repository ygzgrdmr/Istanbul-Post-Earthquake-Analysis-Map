import folium
import json
from shapely.geometry import shape
import base64
import csv
import pandas as pd
from unidecode import unidecode

# Function to insert image to HTML
def insert_image_to_html(input_file, output_file, image_file):
    with open(input_file, 'r') as f:
        html_content = f.read()

    image_data_url = image_to_data_url(image_file)
    image_tag = f'''
        <style>
            img.responsive-image {{ position:absolute; top:10px; right:10px; z-index:999; width:450px; height:200px; }}
        </style>
        <img id="dynamicImage" class="responsive-image" src="{image_data_url}">
        <script>
            document.addEventListener("DOMContentLoaded", function() {{
                var map = L.DomUtil.get('map');
                var dynamicImage = document.getElementById("dynamicImage");
                L.DomEvent.on(map, "zoomend", function(event) {{
                    var zoomLevel = map._leaflet_map.getZoom();
                    dynamicImage.style.width = (100 - zoomLevel * 5) + "px";
                    dynamicImage.style.height = (100 - zoomLevel * 5) + "px";
                }});
            }});
        </script>
        '''

    # Insert the image tag after the opening body tag
    modified_html = html_content.replace('<body>', f'<body>{image_tag}', 1)

    with open(output_file, 'w') as f:
        f.write(modified_html)

# Function to convert image to data URL
def image_to_data_url(filepath):
    with open(filepath, "rb") as image_file:
        return "data:image/png;base64," + base64.b64encode(image_file.read()).decode()

# Load the GeoJSON file with Istanbul district boundaries
with open('istanbul-districts.json', 'r') as f:
    istanbul_geojson = json.load(f)



# Create a dictionary with district names as keys and earthquake statistics as values


earthquake_stats = {
    "Adalar": {}, "Arnavutköy": {}, "Ataşehir": {},
    "Avcılar": {}, "Bağcılar": {},
    "Bahçelievler": {}, "Bakırköy": {}, "Başakşehir": {}, "Bayrampaşa": {},
    "Beşiktaş": {}, "Beykoz": {}, "Beylikdüzü": {}, "Beyoğlu": {}, "Büyükçekmece": {},
    "Çatalca": {}, "Çekmeköy": {}, "Esenler": {}, "Esenyurt": {}, "Eyüpsultan": {}, "Fatih": {},
    "Gaziosmanpaşa": {}, "Güngören": {}, "Kadıköy": {}, "Kağıthane": {}, "Kartal": {},
    "Küçükçekmece": {}, "Maltepe": {}, "Pendik": {}, "Sancaktepe": {}, "Sarıyer": {},
    "Silivri": {}, "Sultanbeyli": {}, "Sultangazi": {}, "Şile": {}, "Şişli": {}, "Tuzla": {},
    "Ümraniye": {}, "Üsküdar": {}, "Zeytinburnu": {}
}
def normalize_district_name(name):
    name = name.replace("İ", "i").replace("I", "ı").replace("Ü","ü")
    normalized_name = name.title()

    if normalized_name == "Eyüp":
        normalized_name = "Eyüpsultan"

    return normalized_name



# Function to update earthquake stats for a district
def update_earthquake_stats(district, stats):
    for key, value in stats.items():
        if key not in earthquake_stats[district]:
            earthquake_stats[district][key] = 0
        earthquake_stats[district][key] += value

# Read the CSV data
with open('deprem-senaryosu-analiz-sonuclar.csv', 'r', encoding='windows-1254') as f:
    csv_reader = csv.DictReader(f, delimiter=';')

    for row in csv_reader:
        district = normalize_district_name(row['ilce_adi'])
  # Convert the district name to the same format as in the dictionary
        stats = {

            'Çok Ağır Hasarlı Bina Sayısı': int(row['cok_agir_hasarli_bina_sayisi']),
            'Ağır Hasarlı Bına Sayısı': int(row['agir_hasarli_bina_sayisi']),
            'Orta Hasarlı Bina Sayısı': int(row['orta_hasarli_bina_sayisi']),
            'Hafif Hasarlı Bina Sayısı': int(row['hafif_hasarli_bina_sayisi']),
            'Can Kaybı Sayısı': int(row['can_kaybi_sayisi']),
            'Ağır Yaralı Sayısı': int(row['agir_yarali_sayisi']),
            'Hastanede Tedavi Sayısı': int(row['hastanede_tedavi_sayisi'])
        }
        update_earthquake_stats(district, stats)

# Create a map centered on Istanbul
istanbul_map = folium.Map(location=[41.0082, 28.9784], zoom_start=9)

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


for feature in istanbul_geojson['features']:
    district_name = feature['properties']['name']
    if district_name in earthquake_stats:
        geom = shape(feature['geometry'])  # Convert GeoJSON to Shapely geometry
        centroid = geom.centroid  # Calculate centroid of the geometry

        lat, lng = centroid.y, centroid.x
        popup_text = f"İlçe: {district_name}<br>Deprem Bilgileri {earthquake_stats[district_name]}"
        folium.Marker(
            location=[lat, lng],
            icon=None,
            popup=folium.Popup(popup_text, max_width=400),
        ).add_to(istanbul_map)
# Save the map as an HTML file
def image_to_data_url(filepath):
    with open(filepath, "rb") as image_file:
        return "data:image/png;base64," + base64.b64encode(image_file.read()).decode()

excel_data = pd.read_excel('park-ve-yeil-alan-koordinatlar.xlsx', engine='openpyxl')

# Filter the rows based on the TÜR column
filtered_data = excel_data[excel_data['TÜR'].isin(['PARK', 'KAMU', 'HATIRA ORMANI', 'KÖY PARKLARI'])]

# Add the points to the Folium map
count=0
for index, row in filtered_data.iterrows():
    tür = row['TÜR']
    mahal_adi = row['MAHAL ADI']
    ilce = row['İLÇE']
    coordinates_string = row['KOORDİNAT (Yatay , Dikey)'].replace('\n', '')
    print(f"counter: {count}, coordinat string {coordinates_string}")
    count+=1

    lat, lng = map(float, row['KOORDİNAT (Yatay , Dikey)'].replace('\n', '').split(','))


    folium.Marker(
        location=[lat, lng],
        icon=folium.Icon(icon='tree', prefix='fa', color='green'),
        popup=f"{tür}: {mahal_adi}<br>İlçe: {ilce}",
    ).add_to(istanbul_map)

# Add the image from the local folder
# Replace 'image.png' with the file name of your image

istanbul_map.save('istanbul_map_temp.html')

insert_image_to_html('istanbul_map_temp.html', 'istanbul_map.html', 'bina_hasarlar.png')
