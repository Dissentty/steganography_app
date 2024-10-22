import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QFileDialog, QVBoxLayout,
                             QLabel, QLineEdit, QWidget, QDialog, QHBoxLayout)
from PyQt5.QtGui import QIcon
from stegano import lsb

dark_theme = """
QMainWindow {
    background-color: #2b2b2b;
}

QLabel {
    color: #ffffff;
}

QPushButton {
    background-color: #3c3f41;
    color: #ffffff;
    border: 1px solid #5a5a5a;
    padding: 5px;
}

QPushButton:hover {
    background-color: #4f4f51;
}

QPushButton:pressed {
    background-color: #2a2a2a;
}

QLineEdit {
    background-color: #3c3f41;
    color: #ffffff;
    border: 1px solid #5a5a5a;
    padding: 5px;
}

QDialog {
    background-color: #2b2b2b;
}

QFileDialog {
    background-color: #2b2b2b;
    color: #ffffff;
}

QMessageBox {
    background-color: #2b2b2b;
    color: #ffffff;
}
"""

class SuccessDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Успех")
        self.setGeometry(300, 300, 200, 100)
        self.setWindowIcon(QIcon('icon.ico'))
        self.success_label = QLabel("Операция прошла успешно!", self)
        ok_button = QPushButton("Ок", self)
        ok_button.clicked.connect(self.close)
        layout = QVBoxLayout()
        layout.addWidget(self.success_label)
        layout.addWidget(ok_button)
        self.setLayout(layout)

class SaveFileDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Сохранить файл")
        self.setGeometry(200, 200, 300, 100)
        self.setWindowIcon(QIcon('icon.ico'))

        self.save_button = QPushButton("Выбрать место для сохранения", self)
        self.save_button.clicked.connect(self.select_save_location)

        self.save_path_label = QLabel("Путь не выбран", self)

        layout = QVBoxLayout()
        layout.addWidget(self.save_path_label)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

    def select_save_location(self):
        options = QFileDialog.Options()
        save_file_path, _ = QFileDialog.getSaveFileName(self, "Сохранить файл как", "",
                                                        "Выберите куда и с каким названием сохранить файл", options=options)
        if save_file_path:
            self.save_path_label.setText(f"Сохранить как: {save_file_path}")
            self.selected_save_path = save_file_path
            self.accept()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Стеганография: Выбор файла")
        self.setGeometry(100, 100, 400, 200)
        self.setWindowIcon(QIcon('icon.ico'))

        self.label = QLabel("Файл не выбран", self)

        self.button = QPushButton("Выберите файл для стеганографии", self)
        self.button.clicked.connect(self.select_file)

        self.text_input = QLineEdit(self)
        self.text_input.setPlaceholderText("Введите текст для шифровки")

        self.encode_button = QPushButton("Начать стеганографию", self)
        self.encode_button.clicked.connect(self.start_steganography)

        self.decode_button = QPushButton("Расшифровка", self)
        self.decode_button.clicked.connect(self.select_decode_file)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button)
        layout.addWidget(self.text_input)
        layout.addWidget(self.encode_button)
        layout.addWidget(self.decode_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def select_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Выберите файл для стеганографии", "",
                                                   "Все файлы (*);;Изображения (*.png *.jpg *.bmp)", options=options)
        if file_name:
            self.label.setText(f"Выбран файл: {file_name}")
            self.selected_file = file_name

    def start_steganography(self):
        text_to_hide = self.text_input.text()

        if hasattr(self, 'selected_file') and text_to_hide:
            print(f"Файл: {self.selected_file}")
            print(f"Текст для шифровки: {text_to_hide}")

            save_dialog = SaveFileDialog()
            if save_dialog.exec_() == QDialog.Accepted:
                save_file_path = save_dialog.selected_save_path
                print(f"Файл будет сохранен как: {save_file_path}")
                secret = lsb.hide(self.selected_file, text_to_hide)
                secret.save(save_file_path+".png")
                success_dialog = SuccessDialog()
                success_dialog.exec_()
        else:
            print("Выберите файл и введите текст для шифровки.")

    def select_decode_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Выберите файл для расшифровки", "",
                                                   "Все файлы (*);;Изображения (*.png *.jpg *.bmp)", options=options)
        if file_name:
            decoded_text = lsb.reveal(file_name)
            if decoded_text:
                print(f"Расшифрованный текст: {decoded_text}")
                success_dialog = SuccessDialog()
                success_dialog.success_label.setText("Расшифровка прошла успешно! Текст: " + decoded_text)
                success_dialog.exec_()
            else:
                print("Не удалось расшифровать текст.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(dark_theme)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
