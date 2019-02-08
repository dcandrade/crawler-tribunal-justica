import selenium
from utils.webdriver_factory import get_webdriver
import config

from utils.string_clean import clear_strings, clear_string, process_key
from utils.exceptions import InvalidProcessNumberException, PasswordProtectedProcess
from db.process_dao import ProcessDAO


class _Crawler:

    def __init__(self, court, silent=True):
        self.__court = court
        self.__delimiter = config.COURTS[court]['delimiter']  # replace by static?
        self.__driver = get_webdriver(silent)
        self.__driver.get(config.COURTS[court]['url'])

    def get_descriptors(self, process_number):
        self.process_number = process_number

        delimiter_index = process_number.find(self.__delimiter)
        numero_digito_unificado = process_number[:delimiter_index - 1]
        foro_numero_unificado = process_number[delimiter_index + 1 + len(self.__delimiter):]

        return numero_digito_unificado, foro_numero_unificado

    def enter_process_page(self, numero_digito_unificado, foro_numero_unificado):
        input_numero_digito_unificado = self.__driver.find_element_by_id("numeroDigitoAnoUnificado")
        input_foro_numero_unificado = self.__driver.find_element_by_id("foroNumeroUnificado")

        input_numero_digito_unificado.send_keys(numero_digito_unificado)
        input_foro_numero_unificado.send_keys(foro_numero_unificado)

        self.__driver.find_element_by_name("pbEnviar").click()

        # Check if there is any error on input data
        errors = self.__driver.find_elements_by_id("mensagemRetorno")
        errors = [error.text for error in errors]

        # If true the process number is invalid
        if len(errors) > 0:
            raise InvalidProcessNumberException(self.process_number, errors)

        # The popupModalDiv asks for a password to access the process page. If it's not present, we can get the
        # process data
        try:
            self.__driver.find_element_by_id("popupModalDiv")
            raise PasswordProtectedProcess(self.process_number)
        except selenium.common.exceptions.NoSuchElementException:
            pass  # popupModalDiv is not here, go on

        return True

    def extract_process_data(self):
        data_table = self.__driver.find_element_by_xpath("/html/body/div/table[4]/tbody/tr/td/div[1]/table[2]/tbody")

        entries = data_table.find_elements_by_tag_name("tr")
        tuples = map(lambda x: x.text.split(":"), set(entries))  # Split to format [key, value]
        tuples = [clear_strings(t) for t in tuples if len(t) == 2]  # Filter out single elements and clear

        process_data = {t[0]: ' '.join(t[1:]) for t in tuples}  # t[0] is the title, t[1:] is the data

        process_data["Processo"] = self.process_number  # Data gathered may be dirty and we already have this info

        process_data = {process_key(k): v for k, v in process_data.items()}

        return process_data

    def extract_party(self, party_str):
        party_name, *raw_representants = party_str.split("\n")

        representants = []
        for rep in raw_representants:
            role, name = rep.split(":")

            representants.append({
                "Nome": clear_string(name),
                "Atribuição": clear_string(role)
            })

        return {
            "Nome": party_name,
            "Representantes": representants
        }

    def extract_parties(self):
        all_parties = {}

        # Some pages have only few parties and do not use the full table (tableTodasAsPartes) to display them,
        # while other pages have too much parties and display all of them only on the tableTodasAsPartes
        try:
            self.__driver.find_element_by_id("linkpartes").click()
            data_table = self.__driver.find_element_by_id("tableTodasPartes")
        except selenium.common.exceptions.NoSuchElementException:
            data_table = self.__driver.find_element_by_id("tablePartesPrincipais")

        # Extract role and representants of each role
        raw_entries = data_table.find_elements_by_tag_name("td")

        for i in range(0, len(raw_entries), 2):
            role = clear_string(raw_entries[i].text)
            role = process_key(role)
            party_str = raw_entries[i + 1].text
            party = self.extract_party(party_str)

            role_representants = all_parties.get(role, [])
            role_representants.append(party)
            all_parties[role] = role_representants

        return all_parties

    def extract_transactions(self):

        # Same logic of extract_parties
        try:
            self.__driver.find_element_by_id('linkmovimentacoes').click()
            transactions_table = self.__driver.find_element_by_id("tabelaTodasMovimentacoes")
        except:
            transactions_table = self.__driver.find_element_by_id("tabelaUltimasMovimentacoes")

        raw_transactions = transactions_table.find_elements_by_tag_name("td")

        transactions = []
        for i in range(0, len(raw_transactions), 3):
            date, _, full_description = raw_transactions[i: i + 3]  # date, empty space, description w/ title
            title, *description = full_description.text.split("\n")
            description = " ".join(description).strip()

            transaction = {
                "Data": clear_string(date.text),
                "Título": clear_string(title),
                "Descrição": clear_string(description)
            }

            transactions.append(transaction)

        return {"Movimentações": transactions}

    def run(self, process_number):
        n, f = self.get_descriptors(process_number)

        self.enter_process_page(n, f)

        data = self.extract_process_data()
        transactions = self.extract_transactions()
        parties = self.extract_parties()

        all_data = {**data, **parties, **transactions}
        return all_data

    def reboot(self):
        self.__driver.get(config.COURTS[self.__court]['url'])

    def quit(self):
        self.__driver.quit()

    def get_court(self):
        return self.__court


class CrawlerWorker():
    def __init__(self, court):
        self.__crawler = _Crawler(court)
        self.__dao = ProcessDAO.get_instance()

    def run(self, process_number):
        process = self.__dao.fetch_process(self.__crawler.get_court(), process_number)

        if process is None:
            try:
                process = self.__crawler.run(process_number)
            except(InvalidProcessNumberException, PasswordProtectedProcess) as err:
                return err.get_errors()

            process["_id"] = process_number
            self.__dao.insert_process(self.__crawler.get_court(), process)

        return process

    def reboot(self):
        self.__crawler.reboot()

    def quit(self):
        self.__crawler.quit()