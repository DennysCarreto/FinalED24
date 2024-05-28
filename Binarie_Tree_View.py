import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, \
    QLineEdit, QTextEdit, QComboBox, QFileDialog, QScrollArea
from PyQt6.QtGui import QPainter, QPaintEvent
from PyQt6.QtCore import Qt, QFile, QTextStream


class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izquierda = None
        self.derecha = None


class ArbolBinario:
    def __init__(self):
        self.raiz = None

    def insertar(self, valor, padre=None, direccion=None):
        if self.raiz is None:
            self.raiz = Nodo(valor)
        else:
            if padre is None:
                padre = self.raiz
            if direccion == "izquierda":
                if padre.izquierda is None:
                    padre.izquierda = Nodo(valor)
                else:
                    self.insertar(valor, padre=padre.izquierda, direccion=direccion)
            elif direccion == "derecha":
                if padre.derecha is None:
                    padre.derecha = Nodo(valor)
                else:
                    self.insertar(valor, padre=padre.derecha, direccion=direccion)
            else:
                print("Dirección inválida, intenta de nuevo.")

    def buscar_nodo(self, nodo, valor):
        if nodo is None:
            return None
        if nodo.valor == valor:
            return nodo
        nodo_izquierda = self.buscar_nodo(nodo.izquierda, valor)
        nodo_derecha = self.buscar_nodo(nodo.derecha, valor)
        return nodo_izquierda if nodo_izquierda else nodo_derecha

    def eliminar(self, valor):
        self.raiz = self._eliminar_recursivo(self.raiz, valor)

    def _eliminar_recursivo(self, nodo, valor):
        if nodo is None:
            return None

        if valor < nodo.valor:
            nodo.izquierda = self._eliminar_recursivo(nodo.izquierda, valor)
        elif valor > nodo.valor:
            nodo.derecha = self._eliminar_recursivo(nodo.derecha, valor)
        else:
            if nodo.izquierda is None:
                return nodo.derecha
            elif nodo.derecha is None:
                return nodo.izquierda

            nodo.valor = self._encontrar_minimo(nodo.derecha).valor
            nodo.derecha = self._eliminar_recursivo(nodo.derecha, nodo.valor)

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

    def obtener_info(self):
        info = {
            "Tamaño": self.obtener_tamanio(),
            "Altura": self.obtener_altura(),
        }
        return info

    def obtener_tamanio(self):
        return self._obtener_tamanio_recursivo(self.raiz)

    def _obtener_tamanio_recursivo(self, nodo):
        if nodo is None:
            return 0
        return 1 + self._obtener_tamanio_recursivo(nodo.izquierda) + self._obtener_tamanio_recursivo(nodo.derecha)

    def obtener_altura(self):
        return self._obtener_altura_recursivo(self.raiz)

    def _obtener_altura_recursivo(self, nodo):
        if nodo is None:
            return 0
        return 1 + max(self._obtener_altura_recursivo(nodo.izquierda), self._obtener_altura_recursivo(nodo.derecha))


class MainWindowAB(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Árbol Binario")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.arbol = ArbolBinario()

        self.label_valor = QLabel("Valor:")
        self.input_valor = QLineEdit()
        self.layout.addWidget(self.label_valor)
        self.layout.addWidget(self.input_valor)

        self.label_padre = QLabel("Padre:")
        self.input_padre = QLineEdit()
        self.layout.addWidget(self.label_padre)
        self.layout.addWidget(self.input_padre)

        self.label_direccion = QLabel("Dirección:")
        self.combo_direccion = QComboBox()
        self.combo_direccion.addItems(['Izquierda', 'Derecha'])
        self.layout.addWidget(self.label_direccion)
        self.layout.addWidget(self.combo_direccion)

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

        # Fijar el tamaño mínimo de la ventana
        self.setMinimumSize(800, 600)

        self.guardar_button = QPushButton("Guardar")
        self.guardar_button.clicked.connect(self.guardar_archivo)
        self.layout.addWidget(self.guardar_button)

        self.cargar_button = QPushButton("Cargar")
        self.cargar_button.clicked.connect(self.cargar_archivo)
        self.layout.addWidget(self.cargar_button)

    def insertar_valor(self):
        valor = self.input_valor.text()
        padre_texto = self.input_padre.text()
        direccion = self.combo_direccion.currentText().lower()

        try:
            valor = valor  # Convertir a entero

            if padre_texto:
                # Verificar si el nodo padre proporcionado existe en el árbol
                #padre = self.arbol.buscar_nodo(self.arbol.raiz, int(padre_texto))
                padre = self.arbol.buscar_nodo(self.arbol.raiz, padre_texto)
                if padre is not None:
                    # Si el nodo padre existe, insertar el nuevo nodo como su hijo
                    self.arbol.insertar(valor, padre, direccion)
                    self.actualizar_info()
                    self.visualizacion_widget.actualizar_arbol(self.arbol.raiz)  # Actualizar visualización del árbol
                else:
                    print("Padre no encontrado en el árbol.")
            else:
                # Si no se proporciona un valor para el padre, insertar el nodo como raíz del árbol
                self.arbol.insertar(valor)
                self.actualizar_info()
                self.visualizacion_widget.actualizar_arbol(self.arbol.raiz)  # Actualizar visualización del árbol
        except ValueError:
            self.info_text.append("Ingrese un valor entero válido.")

    def eliminar_valor(self):
        valor = self.input_valor.text()
        #valor = int(self.input_valor.text())
        self.arbol.eliminar(valor)
        self.actualizar_info()
        self.actualizar_visualizacion()  # Actualizar visualización del árbol

    def buscar_valor(self):
        #valor = int(self.input_valor.text())
        valor = self.input_valor.text()
        encontrado = self.arbol.buscar(valor)
        mensaje = f"El valor {valor} {'fue encontrado' if encontrado else 'no fue encontrado'} en el árbol."
        self.info_text.append(mensaje)

    def actualizar_info(self):
        info = self.arbol.obtener_info()
        self.info_text.clear()
        for clave, valor in info.items():
            self.info_text.append(f"{clave}: {valor}")

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

    def actualizar_visualizacion(self):
        self.visualizacion_widget.actualizar_arbol(self.arbol.raiz)


class VisualizacionWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(400, 300)
        self.arbol = None

    def actualizar_arbol(self, raiz):
        self.arbol = raiz
        self.update()

    def paintEvent(self, event: QPaintEvent):
        if self.arbol:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            self.dibujar_arbol(painter, self.arbol, 200, 50, 0)

    def dibujar_arbol(self, painter, nodo, x, y, nivel):
        if nodo:
            painter.drawText(x - 15, y + 15, nodo.valor)
            #painter.drawText(x - 15, y + 15, str(nodo.valor))

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
    window = MainWindowAB()
    window.show()
    sys.exit(app.exec())
