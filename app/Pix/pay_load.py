from typing import Any


class PayLoad:
    """
    IDs do Payload do Pix
    @var string
    """
    ID_PAYLOAD_FORMAT_INDICATOR = '00'
    ID_MERCHANT_ACCOUNT_INFORMATION = '26'
    ID_MERCHANT_ACCOUNT_INFORMATION_GUI = '00'
    ID_MERCHANT_ACCOUNT_INFORMATION_KEY = '01'
    ID_MERCHANT_ACCOUNT_INFORMATION_DESCRIPTION = '02'
    ID_MERCHANT_CATEGORY_CODE = '52'
    ID_TRANSACTION_CURRENCY = '53'
    ID_TRANSACTION_AMOUNT = '54'
    ID_COUNTRY_CODE = '58'
    ID_MERCHANT_NAME = '59'
    ID_MERCHANT_CITY = '60'
    ID_ADDITIONAL_DATA_FIELD_TEMPLATE = '62'
    ID_ADDITIONAL_DATA_FIELD_TEMPLATE_TXID = '05'
    ID_CRC16 = '63'

    """
    Chave Pix
    """
    _pix_key: str = ''

    """
    Descrição do pagamento
    """
    _description: str = ''

    """
    Nome do titular da conta
    """
    _merchant_name: str = ''

    """
    Cidade do titular da conta
    """
    _merchant_city: str = ''

    """
    ID da Transação
    """
    _txid: str = ''

    """
    Valor da transação
    """
    _amount: str = ''

    @property
    def pix_key(self) -> str:
        return self._pix_key

    @pix_key.setter
    def pix_key(self, new_value: Any) -> None:
        self._pix_key = str(new_value)

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, new_value: Any) -> None:
        self._description = str(new_value)

    @property
    def merchant_name(self) -> str:
        return self._merchant_name

    @merchant_name.setter
    def merchant_name(self, new_value: Any) -> None:
        self._merchant_name = str(new_value)

    @property
    def merchant_city(self) -> str:
        return self._merchant_city

    @merchant_city.setter
    def merchant_city(self, new_value: Any) -> None:
        self._merchant_city = str(new_value)

    @property
    def txid(self) -> str:
        return self._txid

    @txid.setter
    def txid(self, new_value: Any) -> None:
        self._txid = str(new_value)

    @property
    def amount(self) -> str:
        return self._amount

    @amount.setter
    def amount(self, new_value: Any) -> None:
        self._amount = str(new_value)

    def get_value(self, id: str, value: str) -> str:
        return id + (f'{len(value)}' if len(value) > 9 else f'{len(value):0>2}') + value

    def get_merchant_account_info(self) -> str:
        gui = self.get_value(self.ID_MERCHANT_ACCOUNT_INFORMATION_GUI, 'br.gov.bcb.pix')
        
        key = self.get_value(self.ID_MERCHANT_ACCOUNT_INFORMATION_KEY, self.pix_key)
        
        description = self.get_value(self.ID_MERCHANT_ACCOUNT_INFORMATION_DESCRIPTION, self.description) if len(self.description) > 0 else ''

        return self.get_value(self.ID_MERCHANT_ACCOUNT_INFORMATION, gui + key + description)

    def get_addicional_data_field_template(self) -> str:
        # TXID
        txid = self.get_value(self.ID_ADDITIONAL_DATA_FIELD_TEMPLATE_TXID, self.txid)
        return self.get_value(self.ID_ADDITIONAL_DATA_FIELD_TEMPLATE, txid)

    def get_pay_load(self) -> str:
        payload: str = (
            self.get_value(self.ID_PAYLOAD_FORMAT_INDICATOR, '01') + 
            self.get_merchant_account_info() +
            self.get_value(self.ID_MERCHANT_CATEGORY_CODE, '0000') +
            self.get_value(self.ID_TRANSACTION_CURRENCY, '986') +
            self.get_value(self.ID_TRANSACTION_AMOUNT, self.amount) +
            self.get_value(self.ID_COUNTRY_CODE, 'BR') +
            self.get_value(self.ID_MERCHANT_NAME, self.merchant_name) +
            self.get_value(self.ID_MERCHANT_CITY, self.merchant_city) +
            self.get_addicional_data_field_template()
        )
        return payload + self.get_CRC16(payload)

    def get_CRC16(self, pay_load: str) -> str:
        payload = pay_load + self.ID_CRC16 + '04'
        print(payload)

        polinomio = 0x1021
        resultado = 0xFFFF
        length = len(payload)

        if length > 0:
            for offset in range(0, length, 1):
                resultado ^= ord(payload[offset]) << 8

                for bitwise in range(0, 8, 1):
                    resultado <<= 1 
                    if ((resultado << 1) & 0x10000):
                        resultado ^= polinomio
                    resultado &= 0xFFFF

        return self.ID_CRC16 + '04' + str(hex(resultado)).upper()






