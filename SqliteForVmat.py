import sqlite3
import xml.etree.ElementTree as ET  # xml dosyası ayırmak için gerekli modül

conn = sqlite3.connect('database.db')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS materials')
cur.execute('CREATE TABLE materials (materialIndex INTEGER, materialName TEXT, materialFormula TEXT, materialDensityValue FLOAT, materialDensityUnit TEXT, materialSubElements TEXT)')

# print('TABLO OLUSTURULDU')

tree = ET.parse('gg3.vmat')

root = tree.getroot()

parse_list = []

# for child in root:
#     mylist.append(child.attrib)

# print(mylist[0])


# parse_list = root[0][0].text.split('\n')      # Tek bir child düzenleyip ayırmak için oluşturulmuş kod
#                                               # Daha döngüye sokuluyor ve tekrar yazılıyor
# removing_blank = [x.strip(' ') for x in parse_list]
#
# ng_space = [x for x in removing_blank if x.strip()]

# print(root[1][0].tag)
# print(root[0].attrib["name"])

count = 0

for material in root.findall('Material'):
    density = material.find('strings').text
    name = material.get('name')
    # print(name, density)

    count += 1

    parse_list = density.split('\n')  # <strings> içerisindekileri ayırarak listeye atar

    removing_blank = [x.strip(' ') for x in parse_list] # boşlukları kaldırmak için strip ile list comprehension kullanılır

    removing_space = [x for x in removing_blank if x.strip()]  # listenin başındaki boşlukları kaldırır

    number = removing_space[0].split('=')[1].strip('" ')  # Density value ayırır ve number listeye ekler

    list = [c.split('=')[1].strip('" ') for c in removing_space[1:]]

    # print(number, list)       # Element içerikleri olan listeyi ve number 'a atanmış Density Value kontrol amacıyla yazdırılır

    cur.execute('INSERT INTO materials (materialIndex, materialName, materialFormula, materialDensityValue, materialDensityUnit, materialSubElements) VALUES (?, ?, ?, ?, ?, ?)', (count, name, name, number, 'g/cm3',  ''.join([f'F#{list[i].strip()},{list[i + 1]}/' for i in range(0, len(list), 2)])))
    # print('F#' + ''.join([f'{list[i].strip()},{list[i + 1]}/' for i in range(0, len(list), 2)]))
    # print('TABLO OLUSTURULDU')

conn.commit()
