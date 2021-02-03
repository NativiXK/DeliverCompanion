from urllib import request as https
from bs4 import BeautifulSoup as Soup
import pandas as pd

tracking = []
df = []
table = []

# cpf = str(input("Qual o CPF? "))
url = "https://ssw.inf.br/2/resultSSW_dest?urlori=%2F2%2Frastreamento_pf&cnpjdest=10718750942"# + cpf
response = https.urlopen(url)
soup = Soup(response, "html.parser")

items = soup.find_all("a", class_="email")

for item in items:
    url_item = str(item["onclick"])
    url_item = url_item.replace("opx('", "https://ssw.inf.br").replace("')", "&w=x")
    tracking.append(url_item)

for package in tracking:
    soup = Soup(https.urlopen(package), features="lxml")
    for _ in soup.find_all("table")[1].find_all("tr"):
        table.append(_)

    #Limpa texto das tags
    for data in table:
        value = data.get_text(" ").strip().split("\n")
        if value != ['']:
            for i in value:
                if i == ' ':
                    value.remove(' ')
            df.append(value)

    #Remove rodapé inutil
    df = df[:-3]

    print(pd.DataFrame(df))
    table = []
    df = []
