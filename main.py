from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.clock import Clock

Window.clearcolor = (0.1, 0.1, 0.1, 1)  # Dark background like ChatGPT

class ChatApp(App):
    def build(self):
        main = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Chat history area
        self.scroll = ScrollView()
        self.chat_area = BoxLayout(orientation='vertical', size_hint_y=None, spacing=5)
        self.chat_area.bind(minimum_height=self.chat_area.setter('height'))
        self.scroll.add_widget(self.chat_area)
        
        # Input area
        bottom = BoxLayout(size_hint_y=0.1, spacing=5)
        self.input = TextInput(
            multiline=False,
            hint_text='Type your message...',
            background_color=(0.2, 0.2, 0.2, 1),
            foreground_color=(1, 1, 1, 1)
        )
        send_btn = Button(
            text='Send',
            size_hint_x=0.2,
            background_color=(0.2, 0.6, 1, 1)
        )
        send_btn.bind(on_press=self.send_message)
        
        bottom.add_widget(self.input)
        bottom.add_widget(send_btn)
        
        main.add_widget(self.scroll)
        main.add_widget(bottom)
        
        # Welcome message
        self.add_message("Hi! How can I help you?", False)
        
        return main
    
    def send_message(self, instance):
        msg = self.input.text.strip()
        if not msg:
            return
        
        # Show user message
        self.add_message(f"You: {msg}", True)
        self.input.text = ""
        
        # Generate bot response based on keywords
        lower_msg = msg.lower()
        response = "Bot: "
        
        if any(word in lower_msg for word in ['hello', 'hi', 'hey']):
            response += "Hello! How are you?"
        elif any(word in lower_msg for word in ['how are you', 'how do you do']):
            response += "I'm fine, thank you! How about you?"
        elif any(word in lower_msg for word in ['good', 'great', 'fine', 'well']):
            response += "Glad to hear that!"
        elif any(word in lower_msg for word in ['bye', 'goodbye', 'see you']):
            response += "Goodbye! Have a nice day!"
        else:
            response += "I didn't understand. Could you please say that again?"
        
        # Delay response to feel more natural
        Clock.schedule_once(lambda dt: self.add_message(response, False), 0.5)
    
    def add_message(self, text, is_user):
        """Add a message bubble to the chat area"""
        label = Label(
            text=text,
            size_hint_y=None,
            height=40,
            color=(1, 1, 1, 1),
            halign='right' if is_user else 'left',
            valign='middle',
            text_size=(Window.width - 40, None)
        )
        label.bind(texture_size=label.setter('size'))
        self.chat_area.add_widget(label)
        # Auto-scroll to bottom
        Clock.schedule_once(lambda dt: setattr(self.scroll, 'scroll_y', 0), 0.1)

if __name__ == '__main__':
    ChatApp().run()
