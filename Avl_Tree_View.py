import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QTextEdit, \
    QScrollArea, QFileDialog
from PyQt6.QtGui import QPainter, QPaintEvent, QFont
from PyQt6.QtCore import Qt, QFile


class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izquierda = None
        self.derecha = None
        self.altura = 1

class ArbolAVL:
    def __init__(self):
        self.raiz = None

    def insertar(self, valor):
        self.raiz = self._insertar_recursivo(self.raiz, valor)

    def _insertar_recursivo(self, nodo, valor):
        if nodo is None:
            return Nodo(valor)

        if valor < nodo.valor:
            nodo.izquierda = self._insertar_recursivo(nodo.izquierda, valor)
        else:
            nodo.derecha = self._insertar_recursivo(nodo.derecha, valor)

        nodo.altura = 1 + max(self.obtener_altura(nodo.izquierda), self.obtener_altura(nodo.derecha))

        balance = self.obtener_balance(nodo)

        if balance > 1:
            if valor < nodo.izquierda.valor:
                return self.rotacion_derecha(nodo)
            else:
                nodo.izquierda = self.rotacion_izquierda(nodo.izquierda)
                return self.rotacion_derecha(nodo)

        if balance < -1:
            if valor > nodo.derecha.valor:
                return self.rotacion_izquierda(nodo)
            else:
                nodo.derecha = self.rotacion_derecha(nodo.derecha)
                return self.rotacion_izquierda(nodo)

        return nodo

    def eliminar(self, valor):
        self.raiz = self._eliminar_recursivo(self.raiz, valor)

    def _eliminar_recursivo(self, nodo, valor):
        if nodo is None:
            return nodo

        if valor < nodo.valor:
            nodo.izquierda = self._eliminar_recursivo(nodo.izquierda, valor)
        elif valor > nodo.valor:
            nodo.derecha = self._eliminar_recursivo(nodo.derecha, valor)
        else:
            if nodo.izquierda is None:
                return nodo.derecha
            elif nodo.derecha is None:
                return nodo.izquierda

            sucesor = self._encontrar_minimo(nodo.derecha)
            nodo.valor = sucesor.valor
            nodo.derecha = self._eliminar_recursivo(nodo.derecha, sucesor.valor)

        nodo.altura = 1 + max(self.obtener_altura(nodo.izquierda), self.obtener_altura(nodo.derecha))

        balance = self.obtener_balance(nodo)

        if balance > 1:
            if self.obtener_balance(nodo.izquierda) >= 0:
                return self.rotacion_derecha(nodo)
            else:
                nodo.izquierda = self.rotacion_izquierda(nodo.izquierda)
                return self.rotacion_derecha(nodo)

        if balance < -1:
            if self.obtener_balance(nodo.derecha) <= 0:
                return self.rotacion_izquierda(nodo)
            else:
                nodo.derecha = self.rotacion_derecha(nodo.derecha)
                return self.rotacion_izquierda(nodo)

        return nodo

    def _encontrar_minimo(self, nodo):
        while nodo.izquierda:
            nodo = nodo.izquierda
        return nodo

    def buscar(self, valor):
        return self._buscar_recursivo(self.raiz, valor)

    def _buscar_recursivo(self, nodo, valor):
        if nodo is None:
            return False
        if nodo.valor == valor:
            return True
        if valor < nodo.valor:
            return self._buscar_recursivo(nodo.izquierda, valor)
        return self._buscar_recursivo(nodo.derecha, valor)

    def obtener_altura(self, nodo):
        if nodo is None:
            return 0
        return nodo.altura

    def obtener_balance(self, nodo):
        if nodo is None:
            return 0
        return self.obtener_altura(nodo.izquierda) - self.obtener_altura(nodo.derecha)

    def rotacion_izquierda(self, nodo):
        nuevo_padre = nodo.derecha
        nodo.derecha = nuevo_padre.izquierda
        nuevo_padre.izquierda = nodo
        nodo.altura = 1 + max(self.obtener_altura(nodo.izquierda), self.obtener_altura(nodo.derecha))
        nuevo_padre.altura = 1 + max(self.obtener_altura(nuevo_padre.izquierda), self.obtener_altura(nuevo_padre.derecha))
        return nuevo_padre

    def rotacion_derecha(self, nodo):
        nuevo_padre = nodo.izquierda
        nodo.izquierda = nuevo_padre.derecha
        nuevo_padre.derecha = nodo
        nodo.altura = 1 + max(self.obtener_altura(nodo.izquierda), self.obtener_altura(nodo.derecha))
        nuevo_padre.altura = 1 + max(self.obtener_altura(nuevo_padre.izquierda), self.obtener_altura(nuevo_padre.derecha))
        return nuevo_padre

    def obtener_info(self):
        info = {
            "Tamaño": self.obtener_tamanio(),
            "Niveles": self.obtener_niveles(),
            "Balanceado": self.es_balanceado()
        }
        return info

    def obtener_tamanio(self):
        return self._obtener_tamanio_recursivo(self.raiz)

    def _obtener_tamanio_recursivo(self, nodo):
        if nodo is None:
            return 0
        return 1 + self._obtener_tamanio_recursivo(nodo.izquierda) + self._obtener_tamanio_recursivo(nodo.derecha)

    def obtener_niveles(self):
        return self._obtener_altura(self.raiz)

    def _obtener_altura(self, nodo):
        if nodo is None:
            return 0
        return nodo.altura

    def es_balanceado(self):
        return abs(self.obtener_balance(self.raiz)) <= 1 and self._es_balanceado_recursivo(self.raiz)

    def _es_balanceado_recursivo(self, nodo):
        if nodo is None:
            return True
        return abs(self.obtener_balance(nodo)) <= 1 and self._es_balanceado_recursivo(nodo.izquierda) and self._es_balanceado_recursivo(nodo.derecha)


class MainWindowAVL(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Interfaz de AVL")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.arbol = ArbolAVL()

        self.label = QLabel("Id:")
        self.layout.addWidget(self.label)
        self.id = QLineEdit()
        self.layout.addWidget(self.id)

        self.label = QLabel('Nombre:')
        self.layout.addWidget(self.label)
        self.nombre = QLineEdit()
        self.layout.addWidget(self.nombre)

        self.insertar_button = QPushButton("Insertar")
        self.insertar_button.clicked.connect(self.insertar_valor)
        self.layout.addWidget(self.insertar_button)

        self.eliminar_button = QPushButton("Eliminar")
        self.eliminar_button.clicked.connect(self.eliminar_valor)
        self.layout.addWidget(self.eliminar_button)

        self.buscar_button = QPushButton("Buscar")
        self.buscar_button.clicked.connect(self.buscar_valor)
        self.layout.addWidget(self.buscar_button)

        self.info_text = QTextEdit()
        self.info_text.setReadOnly(True)
        self.layout.addWidget(self.info_text)

        self.scroll_area = QScrollArea()
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.layout.addWidget(self.scroll_area)

        self.visualizacion_widget = VisualizacionWidget()
        self.scroll_area.setWidget(self.visualizacion_widget)

        self.actualizar_visualizacion()

        # Agregar botones para guardar y cargar
        self.guardar_button = QPushButton("Guardar")
        self.guardar_button.clicked.connect(self.guardar_archivo)
        self.layout.addWidget(self.guardar_button)

        self.cargar_button = QPushButton("Cargar")
        self.cargar_button.clicked.connect(self.cargar_archivo)
        self.layout.addWidget(self.cargar_button)

    def insertar_valor(self):
        valor = self.input_text.text()
        try:
            valor = valor  # Convertir a entero
            self.arbol.insertar(valor)
            self.actualizar_info()
            self.actualizar_visualizacion()
        except ValueError:
            self.info_text.append("Ingrese un valor entero válido.")

    def eliminar_valor(self):
        #valor = int(self.input_text.text())
        valor = self.input_text.text()
        self.arbol.eliminar(valor)
        self.actualizar_info()
        self.actualizar_visualizacion()

    def buscar_valor(self):
        #valor = int(self.input_text.text())
        valor = self.input_text.text()
        encontrado = self.arbol.buscar(valor)
        mensaje = f"El valor {valor} {'fue encontrado' if encontrado else 'no fue encontrado'} en el árbol."
        self.info_text.append(mensaje)

    def actualizar_info(self):
        info = self.arbol.obtener_info()
        self.info_text.clear()
        for clave, valor in info.items():
            self.info_text.append(f"{clave}: {valor}")

    def actualizar_visualizacion(self):
        self.visualizacion_widget.actualizar_arbol(self.arbol.raiz)

    def guardar_arbol(self, nodo, file):
        if nodo:
            file.write(str(nodo.valor) + "\n")
            self.guardar_arbol(nodo.izquierda, file)
            self.guardar_arbol(nodo.derecha, file)
        else:
            file.write("None\n")

    def guardar_archivo(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Guardar Archivo", "", "Archivos de Texto (*.txt)")

        if filename:
            with open(filename, 'w') as file:
                file.write("Árbol Binario:\n")
                self.guardar_arbol(self.arbol.raiz, file)

    def cargar_archivo(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Cargar Archivo", "", "Archivos de Texto (*.txt)")

        if filename:
            with open(filename, 'r') as file:
                self.arbol.raiz = self.cargar_arbol(file)
                self.actualizar_visualizacion()

    def cargar_arbol(self, file):
        # Leer la primera línea del archivo
        linea = file.readline().strip()

        # Ignorar la línea "Árbol Binario:"
        if linea == "Árbol Binario:":
            linea = file.readline().strip()

        # Comenzar la carga del árbol
        return self.cargar_nodo(linea, file)

    def cargar_nodo(self, linea, file):
        # Si la línea es "None", el nodo es nulo
        if linea == "None":
            return None

        # Crear un nodo con el valor de la línea
        #nodo = Nodo(int(linea))
        nodo = Nodo(linea)

        # Cargar el hijo izquierdo recursivamente
        nodo.izquierda = self.cargar_nodo(file.readline().strip(), file)

        # Cargar el hijo derecho recursivamente
        nodo.derecha = self.cargar_nodo(file.readline().strip(), file)

        return nodo


class VisualizacionWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(400, 300)
        self.arbol = None

    def actualizar_arbol(self, raiz):
        self.arbol = raiz
        self.update()

    def paintEvent(self, event):
        if self.arbol:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            self.dibujar_arbol(painter, self.arbol, 200, 50, 0)

    def dibujar_arbol(self, painter, nodo, x, y, nivel):
        if nodo:
            #painter.drawText(x - 15, y + 15, str(nodo.valor))
            painter.drawText(x - 15, y + 15, nodo.valor)

            separacion_horizontal = 80
            separacion_vertical = 50
            dx = separacion_horizontal * (2 ** (nivel + 1))
            dy = separacion_vertical

            if nodo.izquierda:
                x_izquierda = x - dx
                y_izquierda = y + dy
                painter.drawLine(x, y + 20, x_izquierda, y_izquierda + 20)
                self.dibujar_arbol(painter, nodo.izquierda, x_izquierda, y_izquierda, nivel + 1)

            if nodo.derecha:
                x_derecha = x + dx
                y_derecha = y + dy
                painter.drawLine(x, y + 20, x_derecha, y_derecha + 20)
                self.dibujar_arbol(painter, nodo.derecha, x_derecha, y_derecha, nivel + 1)

            self.setMinimumWidth(max(x + dx + 20, self.parent().width()))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindowAVL()
    window.show()
    sys.exit(app.exec())