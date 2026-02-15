from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.clock import Clock

# تنظیم رنگ
Window.clearcolor = (0.1, 0.1, 0.1, 1)

class ChatApp(App):
    def build(self):
        main = BoxLayout(orientation='vertical')
        
        # ناحیه چت
        self.scroll = ScrollView()
        self.chat_area = BoxLayout(orientation='vertical', size_hint_y=None)
        self.chat_area.bind(minimum_height=self.chat_area.setter('height'))
        self.scroll.add_widget(self.chat_area)
        
        # ناحیه ورودی
        bottom = BoxLayout(size_hint_y=0.1)
        self.input = TextInput(multiline=False)
        btn = Button(text='Send', size_hint_x=0.2)
        btn.bind(on_press=self.send_message)
        
        bottom.add_widget(self.input)
        bottom.add_widget(btn)
        
        main.add_widget(self.scroll)
        main.add_widget(bottom)
        
        # پیام خوش‌آمدگویی
        self.add_message("سلام! چطور می‌تونم کمک کنم؟", False)
        
        return main
    
    def send_message(self, instance):
        msg = self.input.text.strip()
        if msg:
            self.add_message(msg, True)
            self.input.text = ""
            
            # پاسخ خودکار
            if any(word in msg.lower() for word in ['سلام', 'hi', 'hello']):
                response = "سلام! حالت چطوره؟"
            else:
                response = "متوجه نشدم. میشه واضح‌تر بگی؟"
            
            Clock.schedule_once(lambda dt: self.add_message(response, False), 0.5)
    
    def add_message(self, text, is_user):
        label = Label(
            text=text,
            size_hint_y=None,
            height=40,
            color=(1,1,1,1),
            halign='right' if is_user else 'left'
        )
        self.chat_area.add_widget(label)
        self.scroll.scroll_y = 0

if __name__ == '__main__':
    ChatApp().run()
