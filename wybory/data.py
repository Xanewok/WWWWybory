import glob
import xlrd
from xlrd.timemachine import xrange


class Obwod:
    objects = []

    def __init__(self):
        self.wojewodztwo_criteria_id = 0
        self.nr_okregu = 0
        self.kod_gminy = 0
        self.gmina = ""
        self.powiat = ""
        self.nr_obwodu = 0
        self.typ_obwodu = ""
        self.wyniki = [] # size of 12, starting from index 12 (0-indexed)

    def __str__(self):
        return "Wojewodztwo: " + str(self.wojewodztwo_criteria_id) + ", gmina: " + self.gmina

# https://developers.google.com/adwords/api/docs/appendix/geotargeting
# Target Type: Region
# Country Code: PL
# Parent ID: 2616
# Criteria ID, Name
# 20847, Lower Silesian Voivodeship
# 20848, Kuyavian-Pomeranian
# 20849, Lubusz Voivodeship
# 20850, Lodz Voivodeship
# 20851, Lublin Voivodeship
# 20852, Lesser Poland Voivodeship
# 20853, Masovian Voivodeship
# 20854, Opole Voivodeship
# 20855, Podlaskie Voivodeship
# 20856, Podkarpackie Voivodeship
# 20857, Pomeranian Voivodeship
# 20858, Swietokrzyskie
# 20859, Silesian Voivodeship
# 20860, Warmian-Masurian Voivodeship
# 20861, Greater Poland Voivodeship
# 20862, West Pomeranian Voivodeship
def okreg_to_geotarget_criteria_id(num):
    if 1 <= num <= 4:    # województwo DOLNOŚLĄSKIE: 1 Wrocław, 2 Jelenia Góra, 3 Legnica, 4 Wałbrzych
        return 20847
    if 5 <= num <= 7:    # województwo KUJAWSKO-POMORSKIE: 5 Bydgoszcz, 6 Toruń, 7 Włocławek
        return 20848
    if 13 <= num <= 14:  # województwo LUBUSKIE: 13 Zielona Góra, 14 Gorzów Wielkopolski
        return 20849
    if 15 <= num <= 19:  # województwo ŁÓDZKIE: 15 Łodź, 16 Łodź, 17 Piotrków Trybunalski, 18 Sieradz, 19 Skierniewice
        return 20850
    if 8 <= num <= 12:   # województwo LUBELSKIE: 8 Lublin, 9 Biała Podlaska, 10 Chełm, 11 Puławy, 12 Zamość
        return 20851
    if 20 <= num <= 27:  # województwo MAŁOPOLSKIE: 20 Kraków, 21 Kraków, 22 Kraków, 23 Chrzanów, 24 Myślenice: 25 Nowy Sącz, 26 Nowy Targ, 27 Tarnów
        return 20852
    if 28 <= num <= 36:  # województwo MAZOWIECKIE: 28 Warszawa, 29 Warszawa, 30 Ciechanów, 31 Legionów, 32 Ostrołęka, 33 Piaseczno, 34 Płock, 35 Radom, 36 Siedlce
        return 20853
    if 37 <= num <= 38:  # województwo OPOLSKIE: 37 Opole: 38 Opole
        return 20854
    if 43 <= num <= 45:  # województwo PODLASKIE: 43 Białystok, 44 Łomża, 45 Suwałki
        return 20855
    if 39 <= num <= 42:  # województwo PODKARPACKIE: 39 Rzeszów, 40 Krosno, 41 Przemyśl, 42 Tarnobrzeg
        return 20856
    if 46 <= num <= 48:  # województwo POMORSKIE: 46 Gdańsk, 47 Gdańsk, 48 Słupsk
        return 20857
    if 55 <= num <= 56:  # województwo ŚWIĘTOKRZYSKIE: 55 Kielce: 56 Kielce
        return 20858
    if 49 <= num <= 54:  # województwo ŚLĄSKIE: 49 Katowice: 50 Bielsko-Biała, 51 Bytom, 52 Częstochowa, 53 Gliwice: 54 Sosnowiec
        return 20859
    if 57 <= num <= 59:  # województwo WARMIŃSKO-MAZURSKIE: 57 Olsztyn, 58 Elbląg, 59 Ełk
        return 20860
    if 60 <= num <= 64:  # województwo WIELKOPOLSKIE: 60 Poznań, 61 Kalisz, 62 Konin, 63 Leszno, 64 Piła
        return 20861
    if 65 <= num <= 68:  # województwo ZACHODNIOPOMORSKIE: 65 Szczecin, 66 Koszalin, 67 Stargard Szczeciński, 68 Szczecinek
        return 20862


def read_data():
    obw_files = glob.glob('resources/obw*.xls')
    for obw_file in obw_files:
        workbook = xlrd.open_workbook(obw_file)
        worksheet = workbook.sheet_by_index(0)  # Assume only single sheet

        for rownum in xrange(worksheet.nrows):
            if rownum == 0:  # Header
                continue

            obwod = Obwod()
            values = worksheet.row_values(rownum)
            obwod.wojewodztwo_criteria_id = okreg_to_geotarget_criteria_id(values[0])  # num
            obwod.nr_okregu = int(values[0])  # num
            obwod.kod_gminy = int(values[1])  # num
            obwod.gmina = values[2]
            obwod.powiat = values[3]
            obwod.nr_obwodu = values[4]  # num
            obwod.typ_obwodu = values[5]
            for i in range(0, 12): # 12 candidates
                obwod.wyniki.append(values[12 + i])  # num, values are values[12...23]

            Obwod.objects.append(obwod)

read_data()
