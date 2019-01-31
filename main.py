from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

from utils import clear_strings
from data_elements import PROCESS_DATA_XPATHS



class Crawler:
    DELIMITER = "8.26"
    URL = "https://esaj.tjsp.jus.br/cpopg/open.do"

    def __init__(self, silent=True):

        if silent:
            chromeOptions = webdriver.ChromeOptions()
            prefs = {'profile.managed_default_content_settings.images':2} # no imgs
            chromeOptions.add_experimental_option("prefs", prefs)
            chromeOptions.add_argument("--headless")
            self.driver = webdriver.Chrome(options=chromeOptions)
        else:
            self.driver = webdriver.Chrome()

        self.driver.get(Crawler.URL)
    
    # TODO: melhorar nome
    def get_descriptors(self, process_number):
        delimiter_index = process_number.find(Crawler.DELIMITER)
        numero_digito_unificado = process_number[:delimiter_index-1]
        foro_numero_unificado = process_number[delimiter_index+1 + len(Crawler.DELIMITER):]

        return numero_digito_unificado, foro_numero_unificado

    def enter_process_page(self, numero_digito_unificado, foro_numero_unificado):
        input_numero_digito_unificado = self.driver.find_element_by_id("numeroDigitoAnoUnificado")
        input_foro_numero_unificado = self.driver.find_element_by_id("foroNumeroUnificado")

        input_numero_digito_unificado.send_keys(numero_digito_unificado)
        input_foro_numero_unificado.send_keys(foro_numero_unificado)

        self.driver.find_element_by_name("pbEnviar").click()

        #TODO: verificar processos que precisam de senha

        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "linkmovimentacoes"))
            )
        except:
            raise EnvironmentError("Couldn't get process page")

        errors = self.driver.find_elements_by_class_name("tituloMensagem")

        return errors

    def expand_page(self):
        expandable_items_ids = [
            'linkmovimentacoes',
            'linkpartes'
        ]

        for item_id in expandable_items_ids:
            self.driver.find_element_by_id(item_id).click()

    def extract_process_data(self):
        process_data = {}
        for item_name, item_xpath in PROCESS_DATA_XPATHS.items():
            data_element = self.driver.find_element_by_xpath(item_xpath)
            process_data[item_name] = data_element.text

        return process_data

    def extract_party(self, data_table):
        from utils import clear_string
        
        soup = BeautifulSoup(data_table.get_attribute("innerHTML"), "html.parser")
        party_name = clear_string(soup.find(string=True))

        data = soup.find("span").find_all_next(string=True)
        data = map(clear_string, data)
        clean_data = [item for item in data if len(item) > 0]

        lawyers = []
        for i in range(1, len(clean_data), 2):
            #role = clean_data[i]
            name = clean_data[i]
            lawyers.append(name)

        return {
            "Nome" : party_name,
            "Advogados": lawyers
        }

    def extract_parties(self):
        parties = {}
        parties_data_table = self.driver.find_element_by_xpath("//*[@id=\"tableTodasPartes\"]/tbody")
        element_source = parties_data_table.get_attribute("innerHTML")
        num_victims = element_source.count("Reqte")
        num_defendants = element_source.count("Reqdo")

        base_party_xpath = "tr[{}]/td[2]"

        parties["Requerentes"] = []
        for i in range(num_victims):
            party_data_table = parties_data_table.find_element_by_xpath(base_party_xpath.format(i+1))
            parties["Requerentes"].append(self.extract_party(party_data_table))

        parties["Requeridos"] = []
        for i in range(num_defendants):
            index = num_victims + i + 1
            party_data_table = parties_data_table.find_element_by_xpath(base_party_xpath.format(index))
            parties["Requeridos"].append(self.extract_party(party_data_table))

        return parties
        
    def extract_transactions(self):
        transactions_table = self.driver.find_element_by_xpath("//*[@id=\"tabelaUltimasMovimentacoes\"]")
        soup = BeautifulSoup(transactions_table.get_attribute("innerHTML"), "html.parser")

        raw_transactions = soup.find_all("tr")

        transactions = []
        for raw_transaction in raw_transactions:
            elements = raw_transaction.find_all(string=True)
            date, title, description = clear_strings(elements)
            transaction = {
                "Data": date,
                "Título" : title,
                "Descrição" : description
            }
            transactions.append(transaction)
        
        return transactions

    def quit(self):
        self.driver.quit()

c = Crawler()

n, f = c.get_descriptors("1002298-86.2015.8.26.0271")
c.enter_process_page(n, f)
c.expand_page()
data = c.extract_process_data()
#print(data)
print(c.extract_parties())
#print("-----")
#print(c.extract_transactions())
