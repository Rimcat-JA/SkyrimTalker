import sys
import json
import os
from PySide6.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QFont

LOG_PATH = r"\\wsl.localhost\DwemerAI4Skyrim3\var\www\html\HerikaServer\log\output_from_llm.log"
POS_X = 690
POS_Y = 1000
WIDTH = 1500

class Overlay(QWidget):
    def __init__(self):
        super().__init__()
        self.last_json_raw = ""
        self.initUI()

    def initUI(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.WindowTransparentForInput | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.layout = QVBoxLayout()
        self.label = QLabel("Waiting ", self)
        
        self.label.setFont(QFont("Meiryo", 24, QFont.Bold))
        self.label.setStyleSheet("""
            color: rgba(255, 255, 255, 255); 
            background-color: rgba(0, 0, 0, 0); 
            padding: 15px;
        """)
        self.label.setWordWrap(True)
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)
        self.setGeometry(POS_X, POS_Y, WIDTH, 400)
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_all)
        self.timer.start(500)

    def update_all(self):
        self.check_log()
        self.raise_()

    def check_log(self):
        if not os.path.exists(LOG_PATH):
            return
        
        try:
            with open(LOG_PATH, 'r', encoding='utf-8') as f:
                content = f.read()
                if not content: return
                
                start_idx = content.rfind('{')
                end_idx = content.rfind('}')
                
                if start_idx != -1 and end_idx != -1 and start_idx < end_idx:
                    json_raw = content[start_idx:end_idx+1]
                    
                    if json_raw == self.last_json_raw:
                        return
                    
                    try:
                        data = json.loads(json_raw)
                        char = data.get("character") or "Unknown"
                        listener = data.get("listener") or "Anyone"
                        msg = data.get("message") or data.get("text")

                        if not msg:
                            for key, val in data.items():
                                if isinstance(val, dict):
                                    msg = val.get("text")
                                    char = key

                        if msg:
                            self.label.setText(f"【{char} → {listener}】\n{msg}")
                            self.last_json_raw = json_raw
                    except json.JSONDecodeError:
                        pass
        except Exception as e:
            print(f"Error: {e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Overlay()
    ex.show()
    sys.exit(app.exec())