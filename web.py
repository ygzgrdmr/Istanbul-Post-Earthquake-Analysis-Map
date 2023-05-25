import folium
import json
from shapely.geometry import shape
import base64
import csv
import io
import matplotlib.pyplot as plt
import pandas as pd
import math
from PIL import Image
import base64
from io import BytesIO
# Load the GeoJSON file with Istanbul district boundaries
with open('istanbul-districts.json', 'r') as f:
    istanbul_geojson = json.load(f)

def image_to_data_url(png_path):
    # Open an image file
    with Image.open(png_path) as img:
        # Convert the image to RGBA to ensure it's compatible
        img = img.convert("RGBA")
        # Resize the image if it's too big. Adjust the size as needed.
        img.thumbnail((32, 32))
        # Create a BytesIO object and save the image to it
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        # Create a data URL
        img_str = base64.b64encode(buffered.getvalue()).decode()
        return f"data:image/png;base64,{img_str}"

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

def in_istanbul(row, lat_name, lon_name):
    coordinates = row[lat_name]
    mahal_adi = row['MAHAL ADI']
    if coordinates is not None and len(coordinates) == 2:
        lat, lon = coordinates
        if (40.8121 <= lat <= 41.3613 and 28.5461 <= lon <= 29.5377) and not mahal_adi.startswith('ORTA MAHALLE'):
            return True
    return False

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

def plot_graph(data, title):
    fig, ax = plt.subplots(figsize=(6, 6))  # Adjust the figsize as per your preference
    data.plot(kind='bar', ax=ax)
    ax.set_title(title)
    ax.tick_params(axis='x', labelrotation=0)  # Reset labelrotation parameter
    ax.set_xticklabels(data.index, rotation=45, ha='right')  # Rotate and align x-axis labels

    for i, value in enumerate(data):
        ax.text(i, value, str(value), ha='right', va='bottom')

    plt.tight_layout()  # Adjust layout to prevent cropping
    plt.close(fig)
    return fig



def fig_to_html(fig):
    # Convert plot to PNG image
    img = io.BytesIO()
    fig.savefig(img, format='png')
    img.seek(0)

    # Convert PNG image to base64 string
    img_base64 = base64.b64encode(img.getvalue()).decode('utf-8')
    html = f'<img src="data:image/png;base64,{img_base64}" style="max-width: 400%; height: auto;">'
    return html

building_info=pd.read_csv('2017-yl-mahalle-bazl-bina-saylar.csv', encoding='windows-1254', sep=';')

# Normalize the district name
building_info['ilce_adi'] = building_info['ilce_adi'].apply(normalize_district_name)

# Update earthquake_stats for each district with the new building info
for i, row in building_info.iterrows():
    district = row['ilce_adi']
    stats = {
        '1980_oncesi': int(row['1980_oncesi']),
        '1980-2000_arasi': int(row['1980-2000_arasi']),
        '2000_sonrasi': int(row['2000_sonrasi']),
        '1-4 kat_arasi': int(row['1-4 kat_arasi']),
        '5-9 kat_arasi': int(row['5-9 kat_arasi']),
        '9-19 kat_arasi': int(row['9-19 kat_arasi']),
    }
    update_earthquake_stats(district, stats)

# Update the plot_graphs function to include new graphs for the building info
def plot_graphs(district):
    groups = [
        ['Çok Ağır Hasarlı Bina Sayısı', 'Ağır Hasarlı Bina Sayısı', 'Orta Hasarlı Bina Sayısı', 'Hafif Hasarlı Bina Sayısı'],
        ['Can Kaybı Sayısı', 'Ağır Yaralı Sayısı', 'Hastanede Tedavi Sayısı', 'Hafif Yaralı Sayısı'],
        ['1980_oncesi', '1980-2000_arasi', '2000_sonrasi'],
        ['1-4 kat_arasi', '5-9 kat_arasi', '9-19 kat_arasi']
    ]
    group_names = ['Building Damage', 'Human Impact', 'Building Age Distribution', 'Building Floor Distribution']

    html = ''
    for group_name, group in zip(group_names, groups):
        stats = {key: earthquake_stats[district].get(key, 0) for key in group}
        stats_series = pd.Series(stats)
        fig = plot_graph(stats_series, f'{group_name}: {district}')
        html += fig_to_html(fig)
    return html

def preprocess_coordinates(coordinates):
    try:
        if coordinates is not None and not (type(coordinates) == float and math.isnan(coordinates)):
            coordinates_split = []
            if "," in coordinates:
                coordinates_split = coordinates.split(',')
                for i in range(len(coordinates_split)):
                    try:
                        coordinates_split[i] = float(coordinates_split[i].strip())
                    except ValueError:
                        return None
            elif '\n' in coordinates:
                coordinates_split = coordinates.split('\n')
                for i in range(len(coordinates_split)):
                    try:
                        coordinates_split[i] = float(coordinates_split[i].strip())
                    except ValueError:
                        return None
            else:
                coordinates_split = coordinates.strip().split(' ')
                for i in range(len(coordinates_split)):
                    try:
                        coordinates_split[i] = float(coordinates_split[i].strip())
                    except ValueError:
                        return None
            return coordinates_split
    except:
        pass
    return None




# Create a map centered on Istanbul
df = pd.read_excel('park-ve-yeil-alan-koordinatlar.xlsx')
# Your park data code here
parks_layer = folium.FeatureGroup(name='Parks')
df = df.dropna(subset=['KOORDİNAT (Yatay , Dikey)'])
koordinat = df['KOORDİNAT (Yatay , Dikey)']
koordinat = koordinat.apply(preprocess_coordinates)
df['KOORDİNAT (Yatay , Dikey)'] = koordinat


df= df[df.apply(in_istanbul, args=('KOORDİNAT (Yatay , Dikey)', 'KOORDİNAT (Yatay , Dikey)'), axis=1)]
df = df[df['TÜR'] == 'PARK']
# Create a map centered on Istanbul
m = folium.Map(location=[41.0082, 28.9784], zoom_start=9)

# Add earthquake stats layer
earthquake_stats_layer = folium.FeatureGroup(name='Earthquake Stats')


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
).add_to(m)



for feature in istanbul_geojson['features']:
    district_name = feature['properties']['name']
    if district_name in earthquake_stats:
        html = plot_graphs(district_name)
        folium.Popup(html, max_width=400).add_to(folium.GeoJson(data=feature).add_to(earthquake_stats_layer))

earthquake_stats_layer.add_to(m)

# Add parks layer
icon_url = image_to_data_url("park.png")
for i, row in df.iterrows():
    lat, lon = row['KOORDİNAT (Yatay , Dikey)'][0], row['KOORDİNAT (Yatay , Dikey)'][1]
    folium.Marker(
        location=[lat, lon],
        popup=row['MAHAL ADI'],
        icon = folium.CustomIcon(icon_url, icon_size=(25, 25))  # Set the icon URL and size
    ).add_to(parks_layer)

parks_layer.add_to(m)

# Add layer control
folium.LayerControl().add_to(m)

m.save('istanbul_map_temp.html')
