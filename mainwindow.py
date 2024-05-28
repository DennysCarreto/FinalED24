from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel
from PyQt6.QtGui import QFont

from Binarie_Tree_View import MainWindowAB
from Binarie_search_Tree_View import MainWindowABB
from Avl_Tree_View import MainWindowAVL


# Clase para la ventana principal del proyecto
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Se crea la ventana, se le asigna un nombre y tamaño
        self.setWindowTitle("Ventana Principal")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()
        layout.setSpacing(10)


        # Nombre de los botones
        # button_names = ["Arboles binarios",
        #                 "Arboles de busqueda",
        #                 "Arboles AVL"]
        button_names = ['Arboles de busqueda']

        # Ciclo que crea los botones y se les da el estilo
        for name in button_names:
            button = QPushButton(name)
            button.setStyleSheet(
                "QPushButton {"
                "   background-color: #4CAF50;"
                "   border: 2px solid #4CAF50;"
                "   color: white;"
                "   border-radius: 10px;"
                "   padding: 10px 20px;"
                "}"
                "QPushButton:hover {"
                "   background-color: #45a049;"
                "}"
            )
            font = QFont("Arial", 12)
            button.setFont(font)
            layout.addWidget(button)

            # Conectar los botones
            if name == "Arboles binarios":
                button.clicked.connect(self.open_ab_window)
            elif name == "Arboles de busqueda":
                button.clicked.connect(self.open_adb_window)
            elif name == "Arboles AVL":
                button.clicked.connect(self.open_AVL_window)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    # Funciones para los botones del menu principal
    def open_ab_window(self):
        self.graficaAB_window = MainWindowAB()
        self.graficaAB_window.show()

    def open_adb_window(self):
        self.graficaAdB_window = MainWindowABB()
        self.graficaAdB_window.show()

    def open_AVL_window(self):
        self.aavl_window = MainWindowAVL()
        self.aavl_window.show()

