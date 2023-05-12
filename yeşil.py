import folium
import pandas as pd
import math

# Load the park data from the CSV file into a Pandas DataFrame
df = pd.read_excel('park-ve-yeil-alan-koordinatlar.xlsx')


def preprocess_coordinates(coordinates):
    print(coordinates)
    try:
        if coordinates is not None and not (type(coordinates) == float and math.isnan(coordinates)):
            coordinates_split = []
            print(f"IN: {coordinates}")
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
            return coordinates_split
    except:
        pass
    return None


# Create a map centered around the average coordinates of the parks
df = df.dropna(subset=['KOORDİNAT (Yatay , Dikey)'])
koordinat = df['KOORDİNAT (Yatay , Dikey)']
koordinat = koordinat.apply(preprocess_coordinates)
df['KOORDİNAT (Yatay , Dikey)'] = koordinat
print(koordinat.head())

# print(f"splitted: {list(map(lambda x: float(x.strip()), koordinat.split(',')))}")


avg_lat = koordinat.map(lambda x: x[0]).mean()
avg_lon = koordinat.map(lambda x: x[1]).mean()

m = folium.Map(location=[avg_lat, avg_lon], zoom_start=12)

# Add the parks as markers on the map
for i, row in df.iterrows():
    lat, lon = row['KOORDİNAT (Yatay , Dikey)'][0], row['KOORDİNAT (Yatay , Dikey)'][1]
    folium.Marker(
        location=[lat, lon],
        popup=row['MAHAL ADI']
    ).add_to(m)

# Save the map to an HTML file
m.save('parks.html')
