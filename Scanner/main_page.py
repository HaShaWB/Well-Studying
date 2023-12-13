import sys
import os
import fitz  # PyMuPDF
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QToolBar, QPushButton, QWidget, QHBoxLayout, QVBoxLayout,
    QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QFileDialog, QGraphicsRectItem,
    QLineEdit,QComboBox
)
from PySide6.QtGui import QPixmap, QImage, QColor
from PySide6.QtCore import Qt, QRectF

class CustomGraphicsView(QGraphicsView):
    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self.main_window = main_window  # MainWindow 인스턴스에 대한 참조
        self.drag_start_point = None
        self.selection_rect = None

    def mousePressEvent(self, event):
        self.drag_start_point = self.mapToScene(event.position().toPoint())
        self.selection_rect = QGraphicsRectItem()
        self.selection_rect.setBrush(QColor(0, 0, 0, 50))  # 반투명 검은색
        self.scene().addItem(self.selection_rect)
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.selection_rect and self.drag_start_point:
            drag_end_point = self.mapToScene(event.position().toPoint())
            left_anchor_x = min(self.drag_start_point.x(), drag_end_point.x())
            right_anchor_x = max(self.drag_start_point.x(), drag_end_point.x())
            rect = QRectF(left_anchor_x, self.drag_start_point.y(), right_anchor_x - left_anchor_x, drag_end_point.y() - self.drag_start_point.y())
            self.selection_rect.setRect(rect)
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.selection_rect:
            rect = self.selection_rect.rect()
            self.scene().removeItem(self.selection_rect)
            self.selection_rect = None
            if self.main_window:
                self.main_window.capture_selected_area(rect)
        super().mouseReleaseEvent(event)
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_A:
            self.main_window.prev_page()
        elif event.key() == Qt.Key_D:
            self.main_window.next_page()
        super().keyPressEvent(event)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDF 문제 출제기")
        self.setMinimumSize(900, 1000)
        self.document_path = None
        self.current_page = 0
        self.document = None
        self.capture_folder = None
        self.capture_counter = 1
        self.selected_rect = None

        # 메인 레이아웃 설정
        self.layout = QVBoxLayout()
        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

        # 툴바 생성 및 설정
        self.toolbar = QToolBar("Main Toolbar")
        self.addToolBar(Qt.TopToolBarArea, self.toolbar)

        self.file_load_button = QPushButton("파일 불러오기")
        self.file_load_button.clicked.connect(self.load_file)
        self.toolbar.addWidget(self.file_load_button)

        # 이름 입력 필드
        self.name_field = QLineEdit()
        self.name_field.setPlaceholderText("이름 입력")
        self.name_field.setFixedWidth(300)
        self.toolbar.addWidget(self.name_field)

        # 번호 입력 필드
        self.number_field = QLineEdit()
        self.number_field.setPlaceholderText("번호")
        self.number_field.setFixedWidth(50)
        self.toolbar.addWidget(self.number_field)

        # + 버튼 생성 및 설정
        self.increment_button = QPushButton("+")
        self.increment_button.clicked.connect(self.increment_number)
        self.increment_button.setFixedWidth(50)
        self.toolbar.addWidget(self.increment_button)

        # - 버튼 생성 및 설정
        self.decrement_button = QPushButton("-")
        self.decrement_button.clicked.connect(self.decrement_number)
        self.decrement_button.setFixedWidth(50)
        self.toolbar.addWidget(self.decrement_button)

        self.subject_type_selector = QComboBox()
        self.subject_type_selector.addItems(["수학 - 공통과목", "수학 - 선택과목", "탐구"])
        self.toolbar.addWidget(self.subject_type_selector)
        # PDF 뷰어 설정
        self.viewer = CustomGraphicsView(self)
        self.scene = QGraphicsScene()
        self.viewer.setScene(self.scene)
        self.layout.addWidget(self.viewer)

        # 페이지 네비게이션 버튼
        self.prev_page_button = QPushButton("이전 페이지")
        self.prev_page_button.clicked.connect(self.prev_page)
        self.next_page_button = QPushButton("다음 페이지")
        self.next_page_button.clicked.connect(self.next_page)
        self.navigation_layout = QHBoxLayout()
        self.navigation_layout.addWidget(self.prev_page_button)
        self.navigation_layout.addWidget(self.next_page_button)
        self.layout.addLayout(self.navigation_layout)
        
    def increment_number(self):
        current_number = int(self.number_field.text())
        self.number_field.setText(str(current_number + 1))

    def decrement_number(self):
        current_number = int(self.number_field.text())
        if current_number > 0:  # 0보다 작아지지 않도록 제한
            self.number_field.setText(str(current_number - 1))

    def load_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "PDF Files (*.pdf)")
        if file_path:
            self.document = fitz.open(file_path)
            self.document_path = file_path  # 파일 경로 저장
            self.current_page = 0
            self.show_page(self.current_page)
            self.capture_folder = QFileDialog.getExistingDirectory(self, "Select Folder to Save Images")
            self.capture_counter = 1

            # 파일 이름을 name_field의 기본값으로 설정
            file_name = os.path.basename(self.document_path)
            file_name_without_extension = os.path.splitext(file_name)[0]  # 확장자 제거
            self.name_field.setText(file_name_without_extension)

            # number_field에 기본값 설정
            self.number_field.setText("1")


    def show_page(self, page_number):
        if self.document:
            page = self.document.load_page(page_number)
            zoom_factor = 1.0
            mat = fitz.Matrix(zoom_factor, zoom_factor)
            pix = page.get_pixmap(matrix=mat)
            image = QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(image)
            item = QGraphicsPixmapItem(pixmap)
            self.scene.clear()
            self.scene.addItem(item)
            self.viewer.setSceneRect(item.boundingRect())
            self.update_navigation_buttons()

    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.show_page(self.current_page)

    def next_page(self):
        if self.current_page < self.document.page_count - 1:
            self.current_page += 1
            self.show_page(self.current_page)

    def update_navigation_buttons(self):
        self.prev_page_button.setEnabled(self.current_page > 0)
        self.next_page_button.setEnabled(self.current_page < self.document.page_count - 1)

    def capture_selected_area(self, rect):
        try:
            if self.document and self.capture_folder and not rect.isEmpty():
                custom_name = self.name_field.text().strip()
                custom_number = self.number_field.text().strip()
                subject_type = self.subject_type_selector.currentText()

                # PDF 파일 이름 추출 (확장자 제외)
                pdf_file_name = os.path.splitext(os.path.basename(self.document_path))[0]

                if "math" in pdf_file_name:
                    pdf_file_name = pdf_file_name[:-3]

                # 저장할 디렉토리 경로 설정
                save_directory = os.path.join(self.capture_folder, pdf_file_name)
                if not os.path.exists(save_directory):
                    os.makedirs(save_directory)

                # 파일 이름 설정
                if subject_type == "수학 - 공통과목":
                    capture_file_name = f"{custom_name[:-3]}_{custom_number}.png"
                elif subject_type == "수학 - 선택과목":
                    capture_file_name = f"{custom_name}_{custom_number}.png"
                elif subject_type == "탐구":
                    capture_file_name = f"{custom_name}_{custom_number}.png"


                full_path = os.path.join(save_directory, capture_file_name)

                page = self.document.load_page(self.current_page)
                zoom_factor = 5  # 실제 사용되는 확대/축소 비율
                mat = fitz.Matrix(zoom_factor, zoom_factor)

                # 화면 좌표를 PDF 문서 좌표로 변환
                pdf_rect = fitz.Rect(
                    rect.left(),
                    rect.top(),
                    rect.right(),
                    rect.bottom()
                )

                pix = page.get_pixmap(matrix=mat, clip=pdf_rect)
                image = QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format_RGB888)
                # 이미지 객체 상태 확인
                if not image.isNull():
                    pixmap = QPixmap.fromImage(image)
                    if pixmap.save(full_path):
                        print(f"Captured and saved: {full_path}")
                        # 번호 업데이트
                        new_number = int(custom_number) + 1
                        self.number_field.setText(str(new_number))
                    else:
                        print("Failed to save the image")
                else:
                    print("Failed to create QImage object")
            else:
                print("Capture skipped: Invalid document, folder, or selection")
        except Exception as e:
            print(f"Error during capture: {e}")




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
