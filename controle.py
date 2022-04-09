from PyQt6 import  uic, QtWidgets #importação e exibição da tabela feita no Qt Designer
import mysql.connector #comunicação com MySQL

#acesso ao banco de dados especifico. 
banco = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="2994",
    database="cadastro_produtos"
)

#função para executar quando apertar o botão "enviar".
def funcao_principal():
    linha1 = formulario.lineEdit.text()
    linha2 = formulario.lineEdit_2.text()   #variaveis que recebem os dados nas caixas de texto
    linha3 = formulario.lineEdit_3.text()   
    categoria = ''
   #condicções para funcionar as opcoes de categoria no formulario
    if formulario.radioButton.isChecked():
        categoria = 'informática'
    elif formulario.radioButton_2.isChecked():
        categoria = 'Alimentos'
    else:
        categoria = 'Eletrônicos'
    #Para salvar dados no banco de dados selecionado(Criei uma variavel pra executar o codigo sql "comando_SQL")
    cursor  =  banco.cursor() #serve para comunicar com o banco de dados 
    comando_SQL  =  "INSERT INTO produtos (codigo, descricao, preco, categoria) VALUE (%s,%s,%s,%s)" 
    dados  = (str(linha1), str(linha2), str(linha3), categoria)
    cursor.execute(comando_SQL, dados) #executa os comandos (colunas, valor)
    banco.commit()#salva no banco
    #limpa as LineEdit após apertar o botão enviar(ainda dentro da função)
    formulario.lineEdit.setText('')
    formulario.lineEdit_2.setText('')
    formulario.lineEdit_3.setText('')
#função que chama segunda tela com lista de produtos apos apertar o botao "visualizar"
def visu_segunda_tela():
    segunda_tela.show()
    cursor = banco.cursor()
    comando_SQL = 'SELECT * FROM produtos'
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()    
    #cria uma tabela de exibição para segunda tela
    segunda_tela.tableWidget.setRowCount(len(dados_lidos))#quantidade de linhas de acordo com a quatidade de dados lidos
    segunda_tela.tableWidget.setColumnCount(5)#quantidade de colunas pré definida
        
    for i in range(0, len(dados_lidos)):
        for j in range(0, 5):
             segunda_tela.tableWidget.setItem(i,j,QtWidgets.QTableWidgetItem(str(dados_lidos[i][j]))) 
             

apl = QtWidgets.QApplication([]) #cria o aplicativo 
formulario = uic.loadUi("cadastroprodutos.ui")#lê e carrega arquivo 'ui' criado pelo Qt Designer
segunda_tela = uic.loadUi("visualizar.ui") #lê e carrega o aquivo 'ui' da segunda tela
formulario.pushButton.clicked.connect(funcao_principal) #chama a funcção quando aperta o botão 'enviar'.
formulario.pushButton_2tela.clicked.connect(visu_segunda_tela) #chama a função quando aperta o botão 'visualizar'


formulario.show() #mostra a primeira tela com o arquivo "ui".
apl.exec() #axecuta o aplicativo