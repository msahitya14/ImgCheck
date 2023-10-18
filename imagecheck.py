import sys
import os
import pandas as pd
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImageReader
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QScrollArea, QScrollBar, QHBoxLayout, QLineEdit
from PyQt5.QtGui import QIcon

class ImageApprovalApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.image_folder = '../'
        self.image_list = [f for f in os.listdir(self.image_folder) if f.lower().endswith((".jpg", ".png"))]
        self.current_image = 0
        self.zoom_factor = 1.0

        self.image_data = pd.DataFrame(columns=["ImageName", "Approved"])

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Image Validation App")

        # Set the application icon using QIcon
        if os.path.exists('assets/icon.png'):
            app_icon = QIcon('assets/icon.png')  # Replace 'your_icon.png' with the actual icon file path
            self.setWindowIcon(app_icon)
        
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)

        self.approve_button = QPushButton("Approve", self)
        self.approve_button.clicked.connect(self.onApprove)

        self.not_approved_button = QPushButton("Deny", self)
        self.not_approved_button.clicked.connect(self.onNotApproved)

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidget(self.image_label)
        self.scroll_area.setWidgetResizable(True)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.approve_button)
        button_layout.addWidget(self.not_approved_button)

        save_layout = QHBoxLayout()
        self.filename_input = QLineEdit(self)
        self.filename_input.setPlaceholderText("Enter name for file : not with extension")  # Set a placeholder text

        save_button = QPushButton("Save", self)
        save_button.clicked.connect(self.saveDataFrameToExcel)
        save_layout.addWidget(self.filename_input)
        save_layout.addWidget(save_button)

        self.text_input = QLineEdit(self)  # Add a text input field
        self.text_input.setPlaceholderText("Add Comment")  # Set a placeholder text
        text_layout = QHBoxLayout()
        text_layout.addWidget(self.text_input)
        text_layout.addWidget(self.approve_button)
        text_layout.addWidget(self.not_approved_button)

        layout = QVBoxLayout()
        layout.addWidget(self.scroll_area)
        layout.addLayout(button_layout)
        layout.addLayout(text_layout)
        layout.addLayout(save_layout)

        container = QWidget(self)
        container.setLayout(layout)

        self.setCentralWidget(container)

        self.loadImage()

    def loadImage(self):
        if self.current_image < len(self.image_list):
            image_path = os.path.join(self.image_folder, self.image_list[self.current_image])
            image = QImageReader(image_path).read()
            pixmap = QPixmap.fromImage(image)
            
            # Ensure the image fits within the window size
            window_size = self.scroll_area.size()
            if pixmap.width() > window_size.width() or pixmap.height() > window_size.height():
                pixmap = pixmap.scaled(window_size, Qt.KeepAspectRatio)
            
            pixmap = pixmap.scaled(pixmap.width() * self.zoom_factor, pixmap.height() * self.zoom_factor)
            
            self.image_label.setPixmap(pixmap)
            self.scroll_area.horizontalScrollBar().setValue(0)
            self.scroll_area.verticalScrollBar().setValue(0)
            # Update the window title with the image count
            self.setWindowTitle(f"Image Approval App - Image {self.current_image + 1} of {len(self.image_list)}")
        else:
            self.image_label.clear()

    def onApprove(self):
        if self.current_image < len(self.image_list):
            image_name = self.image_list[self.current_image]
            text = self.text_input.text()
            new_data = {'ImageName': [image_name], 'Approved': ['Approved'], 'Comment': [text]}  # Add a 'Comment' column
            new_row = pd.DataFrame(new_data)
            self.image_data = pd.concat([self.image_data, new_row], ignore_index=True)
            self.current_image += 1
            self.loadImage()
            self.saveDataFrameToExcel()
            self.text_input.setText("")  # Reset the label text


    def onNotApproved(self):
        if self.current_image < len(self.image_list):
            image_name = self.image_list[self.current_image]
            text = self.text_input.text()
            new_data = {'ImageName': [image_name], 'Approved': ['Denied'], 'Comment': [text]}  # Add a 'Comment' column
            new_row = pd.DataFrame(new_data)
            self.image_data = pd.concat([self.image_data, new_row], ignore_index=True)
            self.current_image += 1
            self.loadImage()
            self.saveDataFrameToExcel()
            self.text_input.setText("")  # Reset the label text

            

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_W:
            self.zoomIn()
        elif event.key() == Qt.Key_S:
            self.zoomOut()
        elif event.key() == Qt.Key_D:
            self.nextImage()
        elif event.key() == Qt.Key_A:
            self.prevImage()

    def zoomIn(self):
        self.zoom_factor *= 1.1  # You can adjust the factor as needed
        self.loadImage()

    def zoomOut(self):
        self.zoom_factor /= 1.1  # You can adjust the factor as needed
        self.loadImage()

    def nextImage(self):
        if self.current_image < len(self.image_list) - 1:
            self.current_image += 1
            self.loadImage()

    def prevImage(self):
        if self.current_image > 0:
            self.current_image -= 1
            self.loadImage()

    def saveDataFrameToExcel(self):
        import datetime
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        filename = self.filename_input.text()
        if not filename:
            filename = current_date
        excel_filename = f"{filename}_image_approval.xlsx"
        excel_file_path = os.path.join(self.image_folder, excel_filename)
        self.image_data.to_excel(excel_filename, index=False)

def main():
    app = QApplication(sys.argv)
    window = ImageApprovalApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
