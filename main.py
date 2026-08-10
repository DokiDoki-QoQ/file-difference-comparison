from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserList
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
import os
from file_processor import FileProcessor

class DifAppUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10
        
        self.processor = FileProcessor()
        
        # File chooser
        self.file_chooser = FileChooserList()
        self.add_widget(self.file_chooser)
        
        # Button bar
        button_layout = BoxLayout(size_hint_y=0.15, spacing=5)
        
        compare_btn = Button(text='Compare Files')
        compare_btn.bind(on_press=self.compare_files)
        button_layout.add_widget(compare_btn)
        
        extract_btn = Button(text='Extract Text')
        extract_btn.bind(on_press=self.extract_text)
        button_layout.add_widget(extract_btn)
        
        self.add_widget(button_layout)
        
        # Result display
        self.result_label = Label(text='Ready', size_hint_y=0.2)
        scroll = ScrollView()
        scroll.add_widget(self.result_label)
        self.add_widget(scroll)
    
    def compare_files(self, instance):
        if len(self.file_chooser.selection) < 2:
            self.result_label.text = 'Please select at least 2 files'
            return
        
        file1, file2 = self.file_chooser.selection[0], self.file_chooser.selection[1]
        try:
            result = self.processor.compare_text(file1, file2)
            self.result_label.text = result
        except Exception as e:
            self.result_label.text = f'Error: {str(e)}'
    
    def extract_text(self, instance):
        if not self.file_chooser.selection:
            self.result_label.text = 'Please select a file'
            return
        
        file_path = self.file_chooser.selection[0]
        try:
            text = self.processor.extract_text_from_file(file_path)
            self.result_label.text = f'Extracted ({len(text)} chars):\n\n{text[:500]}...'
        except Exception as e:
            self.result_label.text = f'Error: {str(e)}'

class DifApp(App):
    def build(self):
        return DifAppUI()

if __name__ == '__main__':
    DifApp().run()
