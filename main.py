from PyQt5 import QtWidgets, uic, QtGui, QtCore
from PyQt5.QtWidgets import QMessageBox, QDialog, QApplication, QMainWindow, \
                            QPushButton, QLabel, QVBoxLayout, QWidget, QCompleter
from PyQt5.Qt import Qt
import sys, os
from functools import partial
import create_script
from preview_window import AnotherWindow

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('GUI/main.ui', self)
        self.prova_preview_window = AnotherWindow('teste')
        self.listRnw = create_script.list_all_Rnw()
        completer = QCompleter(self.listRnw)
        completer.setFilterMode(Qt.MatchContains)
        # start window setup
        self.listWidget_solutions.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        self.listWidget_variables.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        self.listWidget_images.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        self.listWidget_atividade.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        self.lineEdit_function.setHidden(True)
        self.lineEdit_busca.setCompleter(completer)
        # Connects 
        self.pushButton_previewQuestion.clicked.connect(self.preview_question_activity)
        self.pushButton_addQuestion.clicked.connect(self.add_to_ativity)
        self.pushButton_addSolution.clicked.connect(self.addSolution)
        self.pushButton_addVar.clicked.connect(self.addVar)
        self.pushButton_addImage.clicked.connect(self.addImage)
        self.pushButton_checkVars.clicked.connect(self.checkVars)
        self.pushButton_preview.clicked.connect(self.preview)
        self.comboBox_Rline.currentIndexChanged.connect(self.Rline_change)
        self.pushButton_moodle.clicked.connect(self.make_moodle)
        self.listWidget_variables.itemDoubleClicked.connect(partial(self.itemClicked_event, 'variables'))
        self.listWidget_solutions.itemDoubleClicked.connect(partial(self.itemClicked_event, 'solutions'))
        self.listWidget_images.itemDoubleClicked.connect(partial(self.itemClicked_event, 'images'))
        self.listWidget_atividade.itemDoubleClicked.connect(partial(self.itemClicked_event, 'atividade'))
        # End of Initialization
        self.show()   

    def make_moodle(self):
        nome_atividade = self.lineEdit_nomeAtividade.text()
        nome_disciplina = self.lineEdit_nomeDisciplina.text()
        nome_arquivo = self.lineEdit_nomeArquivo.text()
        n = self.spinBox_nAtividades.value()
        files =  [str(self.listWidget_atividade.item(i).text()) for i in range(self.listWidget_atividade.count())]
        print(files)
        if n > 0 and nome_atividade and len(files) > 0:
            try:
                create_script.create_xml(list_Rnw=files, n=n, subject=nome_atividade)
            except Exception as e:
                print(f'DEBUG: make_moodle - {e}')
        else:
            self.pop_message('Preencha os campos corretamente', 'campos em branco')

    def preview_question_activity(self):
        Rnw_file = self.lineEdit_busca.text()
        try:
            create_script.create_html(Rnw_file)
            with open('html/plain1.html', 'r', encoding='utf-8') as f:
                html = f.read()
                self.webEngineView_previewAtividade.setHtml(html)
                self.webEngineView_previewAtividade.show()
        except Exception as e:
            print(f'DEBUG: preview_question_activity - {e}')
        
    def add_to_ativity(self):
        self.listWidget_atividade.addItems([self.lineEdit_busca.text()])

    def Rline_change(self):
        if self.comboBox_Rline.currentText() == 'sample':
            state = False
        elif self.comboBox_Rline.currentText() == 'function':
            state = True
        self.lineEdit_function.setHidden(not state)
        self.lineEdit_varMin.setHidden(state)
        self.lineEdit_varMax.setHidden(state)
        self.lineEdit_varStep.setHidden(state)

    def addImage(self):
        fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file',
                                            'c:\\', "Image files (*.jpg *.gif)")
        if fname[0]:
            self.listWidget_images.addItems([fname[0]])

    def pop_message(self, text_main, text_body):
        msg = QMessageBox()
        msg.setText(text_main)
        msg.setInformativeText(text_body)
        msg.setStandardButtons(QMessageBox.Ok)
        retval = msg.exec_()
     
    def checkVars(self):
        cmd_check = ''
        R_vars = []
        try:
            R_lines =  [str(self.listWidget_variables.item(i).text()) for i in range(self.listWidget_variables.count())]
            for line in R_lines:
                R_vars.append(line.split(' -> ')[0])
                cmd_check += line
                cmd_check += '\n'
            for R_var in R_vars:
                cmd_check += f'print({R_var})'
                cmd_check += '\n'
            output_full = create_script.test_R_singleline(cmd_check)
            self.pop_message("R results", output_full)
        except Exception as e:
            print(f'DEBUG: checkVars - {e}')

    def itemClicked_event(self, widget):
        if widget == 'solutions':
            self.listWidget_solutions.takeItem(self.listWidget_solutions.currentRow())
        elif widget == 'variables':
            self.listWidget_variables.takeItem(self.listWidget_variables.currentRow())
        elif widget == 'images':
            self.listWidget_images.takeItem(self.listWidget_images.currentRow())
        elif widget == 'atividade':
            self.listWidget_atividade.takeItem(self.listWidget_atividade.currentRow())

    def addSolution(self):
        ItemText = self.lineEdit_itemText.text()
        SolVar = self.lineEdit_itemSolVar.text()
        SolTex = self.lineEdit_itemSolTex.text()
        if ItemText and SolVar and SolTex:
            self.listWidget_solutions.addItems([f'{ItemText}\n{SolVar}\n{SolTex}\n{180*"-"}'])
            self.lineEdit_itemSolTex.setText("")
            self.lineEdit_itemSolVar.setText("")
            self.lineEdit_itemText.setText("")
        else:
            self.pop_message("Existem campos em branco", "Adicione informações em todos os campos para adicionar")

    def addVar(self):
        if self.comboBox_Rline.currentText() == 'sample':
            VarName = self.lineEdit_varName.text()
            VarMin = self.lineEdit_varMin.text()
            VarMax = self.lineEdit_varMax.text()
            VarStep = self.lineEdit_varStep.text()
            if VarName and VarMin and VarMax and VarStep:
                var_line = create_script.create_R_sample(VarName, VarMin, VarMax, VarStep)
                self.listWidget_variables.addItems([f'{var_line}'])
            else:
                self.pop_message("Existem campos em branco", "Adicione informações em todos os campos para adicionar")
        elif self.comboBox_Rline.currentText() == 'function':
            VarName = self.lineEdit_varName.text()
            VarFunction = self.lineEdit_function.text()
            if VarName and VarFunction:
                self.listWidget_variables.addItems([f'{VarName} <- {VarFunction}'])
            else:
                self.pop_message("Existem campos em branco", "Adicione informações em todos os campos para adicionar")
        else:
            print("ERROR")

    def preview(self):
        if self.prova_preview_window.isVisible():
            self.prova_preview_window.hide()
        else:
            vars_list =  [str(self.listWidget_variables.item(i).text()) for i in range(self.listWidget_variables.count())]
            main_text = self.textEdit_questionText.toPlainText()
            sol_list  =  [str(self.listWidget_solutions.item(i).text()) for i in range(self.listWidget_solutions.count())]
            if vars_list and main_text and sol_list:
                vars_list_front = []
                try:
                    for var_list in vars_list:
                        var, command = var_list.split(' <- ')
                        vars_list_front.append(var)
                        vars_list_front.append(command)
                    var, sol = create_script.vardom_2_varsol(vars_list_front)
                    d0 = create_script.variable_formater(var, sol)

                    solucoes_list_dom = []
                    for itens in sol_list:
                        text, sol_var, sol_text, _ = itens.split('\n')
                        solucoes_list_dom.append(sol_var)
                        solucoes_list_dom.append(text)
                        solucoes_list_dom.append(sol_text)
                    d4_p, d2, d3 = create_script.parse_solucoes_dom(solucoes_list_dom)
                    d2 = create_script.answerlist_formater(d2)
                    d3 = create_script.answerlist_formater(d3)
                    d1 = main_text
                    d4 = create_script.meta_formater(['cloze', d4_p, 'CiclopeEstrábico', '0.1'])  
                    data = [d0, [d1], d2, d3, d4]
                    create_script.create_Rnw(data)
                    create_script.create_html('./CriaRnw/Rnw_question.Rnw')
                    with open('html/plain1.html', 'r', encoding='utf-8') as f:
                        html = f.read()
                        self.prova_preview_window.webEngineView.setHtml(html)
                        self.prova_preview_window.show()
                except Exception as e:
                    print(f'DEBUG: preview - {e}')
            else:
                self.pop_message("Existem campos em branco", "Adicione informações em todos os campos para adicionar")


app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()