import selenium
from selenium import webdriver
from bs4 import BeautifulSoup

from utils import clear_strings
from utils import clear_string



class Crawler:
    DELIMITER = {
        'TJSP' : '8.26',
        'TJMS' : '8.12'
    }

    URL = {
        'TJSP' : 'https://esaj.tjsp.jus.br/cpopg/open.do',
        'TJMS' : 'https://esaj.tjms.jus.br/cpopg5/open.do',
    }

    #TODO: check for wrong process number

    def __init__(self, court, silent=True):

        if silent:
            chromeOptions = webdriver.ChromeOptions()
            prefs = {'profile.managed_default_content_settings.images':2} # no imgs
            chromeOptions.add_experimental_option("prefs", prefs)
            chromeOptions.add_argument("--headless")
            self.driver = webdriver.Chrome(options=chromeOptions)
        else:
            self.driver = webdriver.Chrome()

        self.court = court
        self.url = Crawler.URL[court] #TODO: necessário armazenar?
        self.delimiter = Crawler.DELIMITER[court]
        self.driver.get(self.url)
        
    def get_descriptors(self, process_number):
        delimiter_index = process_number.find(self.delimiter)
        numero_digito_unificado = process_number[:delimiter_index-1]
        foro_numero_unificado = process_number[delimiter_index+1 + len(self.delimiter):]

        return numero_digito_unificado, foro_numero_unificado

    def enter_process_page(self, numero_digito_unificado, foro_numero_unificado):
        input_numero_digito_unificado = self.driver.find_element_by_id("numeroDigitoAnoUnificado")
        input_foro_numero_unificado = self.driver.find_element_by_id("foroNumeroUnificado")

        input_numero_digito_unificado.send_keys(numero_digito_unificado)
        input_foro_numero_unificado.send_keys(foro_numero_unificado)

        self.driver.find_element_by_name("pbEnviar").click()

        #TODO: verificar processos que precisam de senha

        errors = self.driver.find_elements_by_class_name("tituloMensagem")

        return errors

    def extract_process_data(self):      
        data_table = self.driver.find_element_by_xpath("/html/body/div/table[4]/tbody/tr/td/div[1]/table[2]/tbody")

        entries = data_table.find_elements_by_tag_name("tr")
        tuples = map(lambda x: x.text.split(":"), set(entries)) # Split to format [key, value]
        tuples = [clear_strings(t) for t in tuples if len(t) == 2] # Filter out single elements and clear

        process_data = {t[0]: ' '.join(t[1:]) for t in tuples}

        return process_data

    def extract_party(self, party_str):
        party_name, *raw_representants = party_str.split("\n")

        representants = []
        for rep in raw_representants:
            role, name = rep.split(":")

            representants.append({
                "Nome": clear_string(name),
                "Atribuição" : clear_string(role)
            })

        return {
            "Nome" : party_name,
            "Representantes": representants
        }

    def extract_parties(self):
        all_parties = {}
        data_table = None
        try:
            self.driver.find_element_by_id("linkpartes").click()
            data_table = self.driver.find_element_by_xpath("//*[@id=\"tableTodasPartes\"]")
        except selenium.common.exceptions.NoSuchElementException:
            data_table = self.driver.find_element_by_xpath("//*[@id=\"tablePartesPrincipais\"]")

        raw_entries = data_table.find_elements_by_tag_name("td")

        for i in range(0, len(raw_entries), 2):
            role = clear_string(raw_entries[i].text)
            party_str = raw_entries[i+1].text
            party = self.extract_party(party_str)  

            role_representants = all_parties.get(role, [])
            role_representants.append(party)
            all_parties[role] = role_representants

        return all_parties
        
    # TODO: adicionar documentos
    def extract_transactions(self):
        transactions_table = None

        try:
            self.driver.find_element_by_id('linkmovimentacoes').click()
            transactions_table = self.driver.find_element_by_xpath("//*[@id=\"tabelaTodasMovimentacoes\"]")
        except:
            transactions_table = self.driver.find_element_by_xpath("//*[@id=\"tabelaUltimasMovimentacoes\"]")

        soup = BeautifulSoup(transactions_table.get_attribute("innerHTML"), "html.parser")

        raw_transactions = soup.find_all("tr")

        transactions = []
        for raw_transaction in raw_transactions:
            elements = raw_transaction.find_all(string=True)
            date, title, *description = clear_strings(elements)

            transaction = {
                "Data": date,
                "Título" : title,
                "Descrição" : " ".join(description).strip()
            }

            transactions.append(transaction)
        
        return transactions

    def run(self, process_number):
        n, f = self.get_descriptors(process_number)
        self.enter_process_page(n, f)
        data = self.extract_process_data()
        transactions = {"Movimentações" : self.extract_transactions()}
        parties = self.extract_parties()

        import json
        all_data = {**data, **parties, **transactions}
        #print(json.dumps(all_data))
        return all_data
        self.quit()

    def quit(self):
        self.driver.quit()

process_number = "1002298-86.2015.8.26.0271"
c = Crawler("TJSP", silent=True)
c.run(process_number)