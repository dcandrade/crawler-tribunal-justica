class InvalidProcessNumberException(Exception):
    def __init__(self, process_number,  errors):
        super(InvalidProcessNumberException, self).__init__("O número do processo {} é inválido".format(process_number))
        self.errors = errors

    def get_errors(self):
        return self.errors

class PasswordProtectedProcess(Exception):
    def __init__(self, process_number):
        super(PasswordProtectedProcess, self).__init__("O número do processo {} é protegido por senha".format(process_number))

    def get_errors(self):
        return {
            'Processo Inacessível' : 'Protegido por senha'
        }