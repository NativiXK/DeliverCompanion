from typing import Pattern
from urllib import request
from bs4 import BeautifulSoup as Soup
import pandas as pd
from pandas.io import parsers

#31210106347409006953550060009454751196026791 -> TESTE


class Delivery:

    def __init__(self, DANFe_key):
        self.danfe = DANFe_key
        self.__site = "http://ssw.inf.br"
        try:
            self.__package = self.__load_danfe(DANFe_key)
        except Exception as e:
            print(e)
            raise Exception("DANFe não localizada, por favor verifique a chave digital!")


    def __load_danfe(self, DANFe_key):
        package = {}
        pattern = "/2/rastreamento_danfe?urlori=&danfe="
        url = self.__site + pattern + DANFe_key
        
        #request the url with the DANFe key
        response = request.urlopen(url).read()

        #Creates the HTML soup
        soup = Soup(response, "lxml")
        #Get URL response for the DANFe
        danfe_url = soup.find("body")["onload"]
        danfe_url = danfe_url.replace("$('danfe').focus();flyto('", "").replace("');", "")

        #make a new request based on the new URL
        url = self.__site + danfe_url
        response = request.urlopen(url).read()

        #Change the HTML soup
        soup = Soup(response, "lxml")
        items_rows = soup.find_all(["td", "span"], class_ = ["rastreamento", "tdb"])
        #populates the dict with header info
        last_key = ""
        for ind in range(len(items_rows) - 2):
            item = items_rows[ind]
            if item.text == ' ':
                next
            if item.name == "span" and item["class"] == ['rastreamento']:
                last_key = item.text
                package[last_key] = ""
            elif item.name == "span" and item["class"] == ['tdb']:
                package[last_key] = item.text

        #read the logs
        table = soup.findAll("table")[1]
        table = table.find_all("tr")[:-5]
        package["logs"] = []
        for tr in table:
            #Exract the event of the log
            event = tr.find("p", class_ = "titulo")
            #check if it isn't Nonetype
            if event is not None:
                event_str = event.text
            else:
                event_str = ""

            #Remove the event from the string, strip it and split where it breakline
            text = tr.get_text(" ").replace(str(event_str), "").strip().split("\n")
            if event_str != "":
                text.insert(1, event_str)
            
            if len(text) == 1:
                next
            else:
                filter_case = lambda x : False if len(x) == 1 else True
                text = list(filter(filter_case, text))

                package["logs"].append(text)

        package["logs"][0].insert(1, "Evento")
        return package

    """
    Returns a pandas dataframe with all the registered LOGS 
    """
    def get_events(self):
        header = self.__package["logs"].pop(0)
        dt = pd.DataFrame(self.__package["logs"], columns=header)
        return dt

def teste():
    deli = Delivery("31210106347409006953550060009454751196026791")
    dt = deli.get_events()
    #Prints all the data inside the data frame
    print(dt)
    #Shows the last event registered in the log
    print("Last event: " + dt["Evento"].iloc[-1])

if __name__ == "__main__":
    teste()