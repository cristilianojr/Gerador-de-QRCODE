from re import MULTILINE
from sys import exit
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.graphics import Rectangle
from temp import DIR_PATH
import os
from qrcode import make
from kivy.properties import (
    ListProperty,
    OptionProperty,
    BooleanProperty,
    StringProperty,
)


class QRCode(FloatLayout):
    source: str = StringProperty('')

    def __init__(self, **kwargs):
        super(QRCode, self).__init__(**kwargs)

        self.fbind('source', self.update_canvas)
    
    def update_canvas(self, *args) -> None:
        self.canvas.clear()

        texture = Image(source=self.source).texture

        with self.canvas:
            Rectangle(pos=self.pos, size=self.size, texture=texture)

class QRGenerator(BoxLayout):
    orientation: str = 'vertical'
    
    counter = 0
    
    temp_path: str = f'temp/qr_code_current_%counter%.png'

    qr_code: QRCode = QRCode()
    qr_code.size_hint = None, None
    qr_code.size = 200, 200

    user_input: TextInput = TextInput()
    user_input.multiline = False
    user_input.size_hint = 1.0, None
    user_input.height = 30

    send_button: Button = Button(text='Gerar QR-Code')

    def  __init__(self, **kwargs):
        super(QRGenerator, self).__init__(**kwargs)

        self.send_button.on_release = lambda: self.build_qrcode(content=self.user_input.text) 
        
        self.add_widget(self.qr_code)
        self.add_widget(self.user_input)
        self.add_widget(self.send_button)

    def build_qrcode(self, content) -> None:
        self.counter += 1
        try:
    
            file_path: str = DIR_PATH + '\\' + f'qr_code_current_{self.counter - 1}.png' 

            os.remove(file_path)
        except Exception as Error:
            print(Error)
            
        self.temp_path = f'temp/qr_code_current_{self.counter}.png'
        self.qr_code.clear_widgets()

        qr_code_image = make(data=content)

        qr_code_image.save(self.temp_path)
        self.qr_code.x = self.x + self.width/2 - self.qr_code.width/2
        self.qr_code.source = self.temp_path


class Application(App):

    icon: str = r'assets\logo.png'
    title: str = 'JampaStyle CODE'
    def build(self) -> Widget:
        return QRGenerator()

if __name__ == '__main__':
    MAIN_APP = Application()
    MAIN_APP.run()
    exit(MAIN_APP)