import selenium
from selenium import webdriver
from utils import clear_strings
from utils import clear_string
from config import COURTS
from exceptions import InvalidProcessNumberException, PasswordProtectedProcess
from process_dao import ProcessDAO
from collections import OrderedDict

class Crawler:

    def __init__(self, court, silent=True):
        self.court = court
        if silent:
            chromeOptions = webdriver.ChromeOptions()
            prefs = {'profile.managed_default_content_settings.images':2} # no imgs
            chromeOptions.add_experimental_option("prefs", prefs)
            chromeOptions.add_argument("--headless")
            self.driver = webdriver.Chrome(options=chromeOptions)
        else:
            self.driver = webdriver.Chrome()
        
        self.delimiter = COURTS[court]['delimiter'] #replace by static?
    
        self.driver.get(COURTS[court]['url'])
        
    def get_descriptors(self, process_number):
        self.process_number = process_number #TODO: fix
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

        errors = self.driver.find_elements_by_id("mensagemRetorno")
        errors = [error.text for error in errors]

        if len(errors) > 0:
            raise InvalidProcessNumberException(self.process_number, errors)
        print(errors)
        # TODO: refactor
        try:
            self.driver.find_element_by_id("popupModalDiv")

            raise PasswordProtectedProcess(self.process_number)
        except selenium.common.exceptions.NoSuchElementException:
            print("not raised")

            pass

        return True

    def extract_process_data(self):      
        data_table = self.driver.find_element_by_xpath("/html/body/div/table[4]/tbody/tr/td/div[1]/table[2]/tbody")

        entries = data_table.find_elements_by_tag_name("tr")
        tuples = map(lambda x: x.text.split(":"), set(entries)) # Split to format [key, value]
        # TODO: why 2?
        tuples = [clear_strings(t) for t in tuples if len(t) == 2] # Filter out single elements and clear

        process_data = {t[0]: ' '.join(t[1:]) for t in tuples} # t[0] is the title, t[1:] is the data

        p = process_data["Processo"]

        process_data["Processo"] = p.split(" ")[0]
            
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
            data_table = self.driver.find_element_by_id("tableTodasPartes")
        except selenium.common.exceptions.NoSuchElementException:
            data_table = self.driver.find_element_by_id("tablePartesPrincipais")

        raw_entries = data_table.find_elements_by_tag_name("td")

        for i in range(0, len(raw_entries), 2):
            role = clear_string(raw_entries[i].text)
            party_str = raw_entries[i+1].text
            party = self.extract_party(party_str)  

            role_representants = all_parties.get(role, [])
            role_representants.append(party)
            all_parties[role] = role_representants

        return all_parties
        
    def extract_transactions(self):
        transactions_table = None

        try:
            self.driver.find_element_by_id('linkmovimentacoes').click()
            transactions_table = self.driver.find_element_by_id("tabelaTodasMovimentacoes")
        except:
            transactions_table = self.driver.find_element_by_id("tabelaUltimasMovimentacoes")
        
        raw_transactions = transactions_table.find_elements_by_tag_name("td")

        transactions = []
        for i in range(0, len(raw_transactions), 3):
            date, _, full_description = raw_transactions[i: i+3] #date, empty space, desc. w/ title
            title, *description = full_description.text.split("\n")
            description = " ".join(description).strip()

            transaction = {
                "Data": clear_string(date.text),
                "Título" : clear_string(title),
                "Descrição" : clear_string(description)
            }

            transactions.append(transaction)
        
        return {"Movimentações" : transactions}

    def run(self, process_number):
        print("Getting ", process_number)

        n, f = self.get_descriptors(process_number)

        self.enter_process_page(n, f)

        data = self.extract_process_data()
        transactions = self.extract_transactions()
        parties = self.extract_parties()

        all_data = {**data, **parties, **transactions}
        #all_data = OrderedDict(sorted(all_data.items()))
        return all_data
    
    def reboot(self):
        self.driver.get(COURTS[self.court]['url'])

    def quit(self):
        self.driver.quit()

    def get_court(self):
        return self.court

class CrawlerWorker():
    def __init__(self, court):
        self.crawler = Crawler(court)
        self.dao = ProcessDAO() # TODO: singleton

    def run(self, process_number):
        process = self.dao.fetch_process(self.crawler.get_court(), process_number)

        if process is None:
            try:
                process = self.crawler.run(process_number)
            except(InvalidProcessNumberException, PasswordProtectedProcess) as err:
                return err.get_errors()

            process["_id"] = process_number
            self.dao.insert_process(self.crawler.get_court(), process)

        return process
    
    def reboot(self):
        self.crawler.reboot()
    
    def quit(self):
        self.crawler.quit()

if __name__ == "__main__":
    c = CrawlerWorker("TJSP")
    d = c.run("aaa")
    c.quit()
    
    from pprint import pprint
    pprint(d)
    import json
