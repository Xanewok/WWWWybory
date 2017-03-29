# http://prezydent2000.pkw.gov.pl/gminy/index.html
# Należy przygotować generator stron HTML, który weźmie wyniki
# (pliki w excelu lub skonwertowane csv) wyborów i przygotuje zestaw stron:

# Wyniki wyborów w całym kraju plus mapka z województwami, na których można klikać
# Wyniki wyborów w każdym z województw plus odnośniki do okręgów
# Wyniki wyborów w każdym okręgu plus odnośniki do gmin
# Wyniki wyborów w każdej gminie w podziale na obwody

# Wymagania dodatkowe

# Powinien być generowany poprawny HTML
# Powinien być generowany porawny CSS
# Strona powinna być responsywna
from wybory import data # Read resources/*.xls data
print(data.Obwod.objects)

from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello World!'

if __name__ == "__main__":
    app.run(debug=True)
