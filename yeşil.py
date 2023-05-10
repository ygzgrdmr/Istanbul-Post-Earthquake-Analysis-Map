import folium
import pandas as pd

# Load the park data from the CSV file into a Pandas DataFrame
df = pd.read_excel('park-ve-yeil-alan-koordinatlar.xlsx')


def func1(coordinates):
    if coordinates is not None:
        coordinates_split = []
        try:
            if "," in coordinates:
                coordinates_split = coordinates.split(',')
                for i in range(len(coordinates_split)):
                    coordinates_split[i] = float(coordinates_split[i].strip())
            elif '\n' in coordinates:
                coordinates_split = coordinates.split('\n')
                for i in range(len(coordinates_split)):
                    coordinates_split[i] = float(coordinates_split[i].strip())
            else:
                coordinates_split = coordinates.strip().split(' ')
                for i in range(len(coordinates_split)):
                    coordinates_split[i] = float(coordinates_split[i].strip())
        except:
            pass
        return coordinates_split
    return None


# Create a map centered around the average coordinates of the parks
koordinat = df['KOORDİNAT (Yatay , Dikey)']
koordinat = koordinat.apply(func1)
print(koordinat.head())
#print(f"splitted: {list(map(lambda x: float(x.strip()), koordinat.split(',')))}")



avg_lat = df['KOORDİNAT (Yatay , Dikey)'].str.split(',').map(lambda x: float(x[0].strip())).mean()
avg_lon = df['KOORDİNAT (Yatay , Dikey)'].str.split(',').map(lambda x: float(x[1].strip())).mean()


m = folium.Map(location=[avg_lat, avg_lon], zoom_start=12)

# Add the parks as markers on the map
for i, row in df.iterrows():
    lat, lon = map(float, row['koordinat(yatay, dikey)'].split(','))
    folium.Marker(
        location=[lat, lon],
        popup=row['MAHAL ADI']

    ).add_to(m)

# Save the map to an HTML file
m.save('parks.html')