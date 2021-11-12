from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.picker import MDDatePicker
from insta_downnloader import insta_D
from PIL import Image
import easygui
from googletrans import Translator

# https://www.techwithtim.net/tutorials/kivy-tutorial/floatlayout/
def show_alert_dialog(self,erro):
    
    # sla = self.dialog.dismiss(force=True)
    if not self.dialog:
        self.dialog = MDDialog(
            text=str(erro),
            buttons=[
                MDFlatButton(
                    text="SAIR", on_release = self.close_dialog,
                ),
            ],
            )
    self.dialog.open()



class LoginScreen(Screen):
    def close_dialog(self,erro):
        self.dialog.dismiss()

    dialog = None
    user = ObjectProperty(None)
    key = ObjectProperty(None)

    def Login(self):
        user = self.user.text
        key = self.key.text
        login = insta_D.Login(user, key)
        if (login == True):
            sm.current = "input"
        else:
            # retorno = login
            # error = Translator.translate(str(retorno), dest="pt-br")
            show_alert_dialog(self,login)

class InputScreen(Screen):
    def close_dialog(self,erro):
        self.dialog.dismiss()

    dialog = None
    hashtag = ObjectProperty(None)
    dia = ObjectProperty(None)
    qtd = ObjectProperty(None)
    file_text = ObjectProperty(None)

    def Back(self):
        sm.current = "login"

    def on_save(self,instance, value, date_range):
        day = value.strftime("%d/%m/%Y")
        self.dia.text = day
        
    def show_time_picker(self):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save)
        date_dialog.open()      

    def ImagesPicker(self):
        hashtag = self.hashtag.text
        qtd = self.qtd.text
        dia = self.dia.text
        if dia == "Insira a data da publicação":
            dia = ""
        get_images = insta_D.ByHashtag(str(hashtag), int(qtd), dia)
        if(get_images == True):
            sm.current = "images"
        else:
            # error = Translator.translate(str(get_images), dest="pt-br")
            show_alert_dialog(self,get_images)

    def FileInput(self):
        file = easygui.fileopenbox()
        try:
            file_nameC = file.rsplit("\\")
            for i in range(len(file_nameC)):
                file_name = file_nameC[i]
            self.file_text.text = file_name
            # type = file_name.rsplit('.')
            banner = Image.open(file)
            banner = banner.convert("RGB")
            banner = banner.save("banner.jpg")

        except Exception as e:
            print(e)

class ImagesScreen(Screen):
    pass

class WindowManager(ScreenManager):
    pass

sm = WindowManager()

class MyApp(MDApp):
    def build(self):
        
        self.icon = "stollker logo.png"
        self.title = "Stollker"

        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.primary_hue = "600"
        kv = Builder.load_file("desing.kv")

        screens = [LoginScreen(name="login"), InputScreen(
            name="input"), ImagesScreen(name="images")]
        for screen in screens:
            sm.add_widget(screen)
        sm.current = "login"
        return sm

if __name__ == "__main__":
    MyApp().run()
