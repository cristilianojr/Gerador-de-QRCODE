# from sys import exit
# from kivy.app import App

# class AppBuilder(App):
#     pass

# if __name__ == '__main__':
#     APP = AppBuilder()
#     APP.run()
#     exit(APP)

from app import pay_load
from app.pay_load import PayLoad

if __name__ == '__main__':
    payload = PayLoad()
    payload.pix_key = '12345678900'
    payload.description = 'Pagamento do pedido 123456'
    payload.merchant_name = 'William Costa'
    payload.merchant_city = 'SÃO PAULO'
    payload.amount = 100.00
    payload.txid = 'WDEV1234'

    # print('-' * 50)
    # print(payload.pix_key)
    # print(payload.description)
    # print(payload.merchant_name)
    # print(payload.merchant_city)
    # print(payload.amount)
    # print(payload.txid)
    # print('-' * 50)

    print(payload.get_pay_load())
# Buffer imagens