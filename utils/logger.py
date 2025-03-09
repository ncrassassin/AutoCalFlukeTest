from datetime import datetime

class Logger:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def log(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.text_widget.insert('end', f"{timestamp} - {message}\n")
        self.text_widget.see('end')
