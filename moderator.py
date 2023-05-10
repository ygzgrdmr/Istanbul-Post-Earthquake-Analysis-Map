import csv
from unidecode import unidecode
earthquake_stats = {
    "Adalar": {}, "Arnavutköy": {}, "Ataşehir": {},
    "Avcılar": {}, "Bağcılar": {},
    "Bahçelievler": {}, "Bakırköy": {}, "Başakşehir": {}, "Bayrampaşa": {},
    "Beşiktaş": {}, "Beykoz": {}, "Beylikdüzü": {}, "Beyoğlu": {}, "Büyükçekmece": {},
    "Çatalca": {}, "Çekmeköy": {}, "Esenler": {}, "Esenyurt": {}, "Eyüp": {}, "Fatih": {},
    "Gaziosmanpaşa": {}, "Güngören": {}, "Kadıköy": {}, "Kağıthane": {}, "Kartal": {},
    "Küçükçekmece": {}, "Maltepe": {}, "Pendik": {}, "Sancaktepe": {}, "Sarıyer": {},
    "Silivri": {}, "Sultanbeyli": {}, "Sultangazi": {}, "Şile": {}, "Şişli": {}, "Tuzla": {},
    "Ümraniye": {}, "Üsküdar": {}, "Zeytinburnu": {}
}
def normalize_district_name(name):
    name = name.replace("İ", "i").replace("I", "ı")
    return name.capitalize()

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
            'mahalle_koy_uavt': int(row['mahalle_koy_uavt']),
            'cok_agir_hasarli_bina_sayisi': int(row['cok_agir_hasarli_bina_sayisi']),
            'agir_hasarli_bina_sayisi': int(row['agir_hasarli_bina_sayisi']),
            'orta_hasarli_bina_sayisi': int(row['orta_hasarli_bina_sayisi']),
            'hafif_hasarli_bina_sayisi': int(row['hafif_hasarli_bina_sayisi']),
            'can_kaybi_sayisi': int(row['can_kaybi_sayisi']),
            'agir_yarali_sayisi': int(row['agir_yarali_sayisi']),
            'hastanede_tedavi_sayisi': int(row['hastanede_tedavi_sayisi'])
        }
        update_earthquake_stats(district, stats)

# Print the updated earthquake_stats dictionary
print(earthquake_stats)


filename = 'deprem-senaryosu-analiz-sonuclar.csv'

with open(filename, 'r', encoding='windows-1254') as file:
    lines = file.readlines()

district_names = set()
for line in lines[1:]:
    data = line.strip().split(',')
    district_name = data[0]
    district_names.add(district_name)

print('District names from the input file:')
for name in sorted(district_names):
    print(name)