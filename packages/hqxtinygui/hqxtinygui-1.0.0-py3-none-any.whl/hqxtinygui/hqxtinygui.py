import sys
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QColor

class InputDialog(QDialog):
    def __init__(self, prompt="", parent=None):
        super(InputDialog, self).__init__(parent)

        self.setStyleSheet("""
            QDialog {
                background-color: white;
                padding:0px;
                margin:0px;
            }
            QLineEdit {
                border-top: 5px solid gray;  /* 上边框 */
                border-left: 5px solid gray;
                border-right:5px solid #CCCCCC;
                border-bottom:5px solid #CCCCCC;
                padding: 5px;
            }
            QPushButton {
                border-top: 3px solid #CCCCCC;  /* 上边框 */
                border-left: 3px solid #CCCCCC;
                border-right:3px solid gray;
                border-bottom:3px solid gray;
                min-width: 80px;
                padding: 5px;
                background-color:#CCCCCC;
            }
            QPushButton:pressed {
                background-color: white;
            }
        """)

        self.setWindowTitle("输入框")
        self.setFixedSize(QSize(500,180))

        self.main_layout = QVBoxLayout()
        self.main_layout.setSpacing(0)  # 设置组件之间的间距为20像素

        # 添加间距
        self.main_layout.addSpacing(-30)
        self.prompt_label = QLabel(prompt, alignment=Qt.AlignCenter)
        self.prompt_label.setStyleSheet('margin-top:0px;')
        self.main_layout.addWidget(self.prompt_label)
        #添加间距
        self.main_layout.addSpacing(0)

        self.input_line_edit = QLineEdit(self)
        self.input_line_edit.setMinimumWidth(400)
        self.main_layout.addWidget(self.input_line_edit, alignment=Qt.AlignTop | Qt.AlignHCenter)

        #添加间距
        self.main_layout.addSpacing(15)
        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignTop)

        self.ok_button = QPushButton("确定", self)
        self.cancel_button = QPushButton("取消", self)

        button_layout.addWidget(self.ok_button, alignment=Qt.AlignLeft)
        button_layout.addWidget(self.cancel_button, alignment=Qt.AlignRight)

        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

        # 设置布局的外边距
        button_layout.setContentsMargins(40, 0, 40, 0)

        self.main_layout.addLayout(button_layout)

        self.setLayout(self.main_layout)

    def get_input(self):
        if self.exec_():
            return self.input_line_edit.text()
        else:
            return ""

def input_text(prompt=""):
    dialog = InputDialog(prompt=prompt)
    result = dialog.get_input()
    dialog.close()
    return result

import sys
app = QApplication(sys.argv)
