from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
import os

class ChatUI(BoxLayout):
    def __init__(self, **kwargs):
        super(ChatUI, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10

        # Chat History Display Area
        self.scroll = ScrollView(size_hint=(1, 0.8))
        self.chat_log = Label(
            text="[Sikandar AI Agent Initialized]\nSystem Ready (Offline/Online Mode)\n",
            size_hint_y=None,
            markup=True,
            valign='top',
            halign='left'
        )
        self.chat_log.bind(texture_size=self.chat_log.setter('texture_size'))
        self.scroll.add_widget(self.chat_log)
        self.add_widget(self.scroll)

        # Input Layout
        input_layout = BoxLayout(size_hint=(1, 0.1), spacing=5)
        self.user_input = TextInput(
            hint_text="Yahan apna message ya command likhein...",
            multiline=False
        )
        input_layout.add_widget(self.user_input)

        send_btn = Button(text="Send", size_hint_x=0.3)
        send_btn.bind(on_press=self.send_message)
        input_layout.add_widget(send_btn)

        self.add_widget(input_layout)

    def send_message(self, instance):
        text = self.user_input.text.strip()
        if text:
            self.chat_log.text += f"\n[You]: {text}"
            self.user_input.text = ""
            self.chat_log.text += f"\n[AI Agent]: Main samajh gaya, is par kaam kar raha hoon..."

class SikandarAIAgentApp(App):
    def build(self):
        self.title = "Sikandar AI Agent"
        return ChatUI()

if __name__ == '__main__':
    SikandarAIAgentApp().run()
