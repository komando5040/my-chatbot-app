"""
اپلیکیشن چت‌بات ساده با ظاهری شبیه چت‌جی‌پی‌تی
پاسخ به سلام و احوال‌پرستی
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.metrics import dp
import re

# تنظیم رنگ زمینه (شبیه چت‌جی‌پی‌تی)
Window.clearcolor = (0.1, 0.1, 0.1, 1)  # خاکستری تیره

class ChatBubble(BoxLayout):
    """حباب چت برای نمایش پیام‌ها"""
    def __init__(self, text, is_user=True, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal' if is_user else 'horizontal'
        self.size_hint_y = None
        self.height = dp(50)  # ارتفاع تقریبی
        self.padding = [dp(10), dp(5)]
        self.spacing = dp(10)

        # متن پیام
        message = Label(
            text=text,
            size_hint=(None, 1),
            width=dp(250),
            text_size=(dp(240), None),
            halign='left' if not is_user else 'right',
            valign='middle',
            color=(1, 1, 1, 1),
            markup=True
        )
        message.bind(texture_size=message.setter('size'))
        self.add_widget(message)

class ChatHistory(RecycleView):
    """نمایش تاریخچه چت با قابلیت اسکرول"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data = []
        self.message_list = []  # لیست پیام‌ها برای مدیریت ساده‌تر

    def add_message(self, text, is_user=True):
        """افزودن پیام جدید به تاریخچه"""
        self.message_list.append((text, is_user))
        # بروزرسانی RecycleView
        self.data = [{'text': msg[0], 'is_user': msg[1]} for msg in self.message_list]
        # اسکرول به پایین
        Clock.schedule_once(lambda dt: setattr(self, 'scroll_y', 0))

class ChatBotApp(App):
    def build(self):
        # صفحه اصلی
        main_layout = BoxLayout(orientation='vertical', spacing=dp(5), padding=dp(10))

        # تاریخچه چت
        self.history = ChatHistory()
        main_layout.add_widget(self.history)

        # ناحیه ورودی و دکمه ارسال
        input_layout = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(10))
        self.text_input = TextInput(
            hint_text="پیام خود را بنویسید...",
            multiline=False,
            background_color=(0.2, 0.2, 0.2, 1),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(1, 1, 1, 1)
        )
        self.text_input.bind(on_text_validate=self.send_message)  # ارسال با Enter
        input_layout.add_widget(self.text_input)

        send_btn = Button(
            text="ارسال",
            size_hint_x=None,
            width=dp(70),
            background_color=(0.2, 0.6, 1, 1)
        )
        send_btn.bind(on_release=self.send_message)
        input_layout.add_widget(send_btn)

        main_layout.add_widget(input_layout)
        return main_layout

    def send_message(self, instance):
        """پردازش پیام ارسالی کاربر و تولید پاسخ"""
        user_msg = self.text_input.text.strip()
        if not user_msg:
            return

        # نمایش پیام کاربر
        self.history.add_message(user_msg, is_user=True)
        self.text_input.text = ""

        # تولید پاسخ خودکار
        response = self.get_bot_response(user_msg)
        # کمی تأخیر برای طبیعی‌تر شدن
        Clock.schedule_once(lambda dt: self.history.add_message(response, is_user=False), 0.5)

    def get_bot_response(self, user_input):
        """پاسخ ساده بر اساس تشخیص کلمات کلیدی"""
        # تبدیل به حروف کوچک برای تطابق آسان‌تر
        text = user_input.lower()

        # الگوهای سلام و احوال‌پرستی
        greetings = ['سلام', 'hi', 'hello', 'درود', 'slm', 'hei']
        how_are_you = ['چطوری', 'حالت چطوره', 'how are you', 'چه خبر']

        # تشخیص
        for word in greetings:
            if word in text:
                return "سلام! چطور می‌تونم کمکت کنم؟"

        for phrase in how_are_you:
            if phrase in text:
                return "من خوبم، ممنون! تو چطوری؟"

        # پاسخ پیش‌فرض
        return "متوجه نشدم. می‌تونیم در مورد چیز دیگه‌ای صحبت کنیم؟"

if __name__ == '__main__':
    ChatBotApp().run()
