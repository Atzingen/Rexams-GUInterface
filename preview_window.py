from PyQt5 import QtWidgets, uic, QtGui, QtCore
from PyQt5.QtWidgets import QMessageBox, QDialog, QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget
from PyQt5.Qt import Qt
import sys, os
from functools import partial
import create_script


class AnotherWindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """
    def __init__(self, self_main):
        super().__init__()
        uic.loadUi('GUI/prova_preview.ui', self)
        self.hide_lineEdits(True)
        self.pushButton_salvar.clicked.connect(self.salvar)
        self.pushButton_apagar.clicked.connect(self.apagar)
        self.pushButton_refresh.clicked.connect(self.refresh)

    def hide_lineEdits(self, state):
        self.lineEdit_fileName.setHidden(state)
        self.lineEdit_fileArea.setHidden(state)
        self.lineEdit_fileSubArea.setHidden(state)
        if state:
            self.pushButton_salvar.setStyleSheet("background-color: grey")
        else:
            self.pushButton_salvar.setStyleSheet("background-color: red")

    def refresh(self):
        create_script.create_html('./CriaRnw/Rnw_question.Rnw')
        with open('html/plain1.html', 'r') as f:
            html = f.read()
            self.webEngineView.setHtml(html)
        
    def salvar(self):
        if self.lineEdit_fileName.isVisible():
            file_name = self.lineEdit_fileName.text()
            if len(file_name) > 0:
                create_script.move_Rnw('./BancoQuestoes/criadas/', file_name + '.Rnw')
                self.hide()
        else:
            self.hide_lineEdits(False)

    def apagar(self):
        self.hide()