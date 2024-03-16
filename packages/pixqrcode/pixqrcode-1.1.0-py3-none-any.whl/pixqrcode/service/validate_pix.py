from pixqrcode.model.pix_error import PixError
from pixqrcode.model.pix import Pix
from pixqrcode.service.key_identify import key_mobile, key_cpf, key_email, key_random, key_cnpj
from pixqrcode.utils.format_values import FormatValues


class ValidatePix:
    is_valid = False

    def __init__(self, pix: Pix):
        self.pix = pix

    def validate(self):
        self.name()
        self.amount()
        self.city()
        self.reference_label()
        self.is_valid = self.key()
        return self.is_valid

    def name(self):
        if not self.pix.name:
            raise PixError("nome não informado")

        self.pix.name = FormatValues.texts(self.pix.name)
        return True

    def city(self):
        if not self.pix.city:
            raise PixError("cidade não informada")

        self.pix.city = FormatValues.texts(self.pix.city)
        return True

    def amount(self):
        if self.pix.amount:
            self.pix.amount = FormatValues.amount(self.pix.amount)
        else:
            self.pix.amount = "0.00"
        return True

    def reference_label(self):
        if not self.pix.reference_label:
            self.pix.reference_label = "***"
        else:
            self.pix.reference_label = FormatValues.texts_no_space(self.pix.reference_label)

    def key(self):
        if not self.pix.key:
            raise PixError("chave pix não informada")
        local_is_valid = False
        for func in [key_email, key_cpf, key_cnpj, key_mobile, key_random]:
            exec_fun = func(self.pix.key)
            if exec_fun['status']:
                local_is_valid = True
                self.pix.key = exec_fun['value']
                self.pix.method = exec_fun['method']
                break
        return local_is_valid
