from sqlite3 import Cursor
from MySQLdb import apilevel
from PyQt6 import  uic, QtWidgets
import mysql.connector

banco = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="2994",
    database="cadastro_produtos"
)

def funcao_principal():
    linha1 = formulario.lineEdit.text()
    linha2 = formulario.lineEdit_2.text()
    linha3 = formulario.lineEdit_3.text()
    categoria = ''
    print('teste')
    print(linha1, linha2, linha3)

    if formulario.radioButton.isChecked():
        print('Categoria: informática')
        categoria = 'informática'
    elif formulario.radioButton_2.isChecked():
        print('Categoria: Alimentos')
        categoria = 'Alimentos'
    else:
        print('Categoria: Eletrônicos')
        categoria = 'Eletrônicos'

    cursor  =  banco.cursor ()
    comando_SQL  =  "INSERT INTO produtos (codigo, descricao, preco, categoria) VALUE (%s,%s,%s,%s)"
    dados  = (str(linha1), str(linha2), str(linha3), categoria)
    cursor.execute(comando_SQL, dados)
    banco.commit()
    formulario.lineEdit.setText('')
    formulario.lineEdit_2.setText('')
    formulario.lineEdit_3.setText('')

def visu_segunda_tela():
    segunda_tela.show()
    cursor = banco.cursor()
    comando_SQL = 'SELECT * FROM produtos'
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()
    print(dados_lidos)

    segunda_tela.tableWidget.setRowCount(len(dados_lidos))
    segunda_tela.tableWidget.setColumnCount(5)
        
    for i in range(0, len(dados_lidos)):
        for j in range(0, 5):
             segunda_tela.tableWidget.setItem(i,j,QtWidgets.QTableWidgetItem(str(dados_lidos[i][j]))) 
             

apl = QtWidgets.QApplication([])
formulario = uic.loadUi("cadastroprodutos.ui")
segunda_tela = uic.loadUi("visualizar.ui")
formulario.pushButton.clicked.connect(funcao_principal)
formulario.pushButton_2tela.clicked.connect(visu_segunda_tela)


formulario.show()
apl.exec()