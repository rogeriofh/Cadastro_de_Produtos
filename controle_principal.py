from PyQt6 import  uic, QtWidgets #importação e exibição da tabela feita no Qt Designer
import mysql.connector #comunicação com MySQL
from reportlab.pdfgen import canvas

#variavel global iniciada em 0 
numero_id = 0

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
   
   #condicções para funcionar as opcoes de 'categoria' no formulario
    if formulario.radioButton.isChecked():
        categoria = 'informática'
    elif formulario.radioButton_2.isChecked():
        categoria = 'Alimentos'
    else:
        categoria = 'Eletrônicos'
    
    #Para salvar dados no banco de dados selecionado(Criei uma variavel pra executar o codigo sql "comando_SQL")
    cursor  =  banco.cursor() #serve para comunicar com o banco de dados (sempre fazer)
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
    #preenchimento da tabela    
    for i in range(0, len(dados_lidos)):
        for j in range(0, 5):
             segunda_tela.tableWidget.setItem(i,j,QtWidgets.QTableWidgetItem(str(dados_lidos[i][j]))) 

#função pra gerar o aquivo pdf
def gerar_pdf():
    cursor = banco.cursor()
    comando_SQL = "SELECT * FROM produtos"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()
 #comando pra pegar base de dados do Mysql ^^^^^^  
    y = 0 #variael pra escrever no pdf, iniciamos o objeto com 0
    pdf = canvas.Canvas("cadastro_produtos.pdf")#variavel que cria o arquivo
    pdf.setFont("Times-Bold", 25)#fonte(tipo, tamanho)
    pdf.drawString(200,800, "Produtos cadastrados:")#titulo (posição x-y, "texto")
    
    pdf.setFont("Times-Bold", 18)
#Definição da posição e titulo das colunas 
    pdf.drawString(10,750, "ID")
    pdf.drawString(110,750, "Codigo")
    pdf.drawString(210,750, "Produto")
    pdf.drawString(310,750, "Preço")
    pdf.drawString(410,750, "Categoria")

    for i in range(0, len(dados_lidos)):
        y = y + 50
        pdf.drawString(10,750 - y, str(dados_lidos[i][0]))
        pdf.drawString(110,750 - y, str(dados_lidos[i][1]))
        pdf.drawString(210,750 - y, str(dados_lidos[i][2]))
        pdf.drawString(310,750 - y, str(dados_lidos[i][3]))
        pdf.drawString(410,750 - y, str(dados_lidos[i][4]))

    pdf.save()

def excluir_dados():
    linha = segunda_tela.tableWidget.currentRow()# metodo 'currentRow' diz qual é a linha a ser excluida
    segunda_tela.tableWidget.removeRow(linha)#metodo removeRow Exclui a linha na segunda tela
    
    cursor = banco.cursor()
    cursor.execute('SELECT id FROM produtos')#pegou só a coluna id
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[linha][0]#igualou o id do produto com o numero de identificação da linha 
    cursor.execute('DELETE FROM produtos WHERE id='+str (valor_id))#deletou no banco de daods 

def tela_editar():
    global numero_id
    linha = segunda_tela.tableWidget.currentRow()# metodo 'currentRow' diz qual é a linha a ser excluida
    
    cursor = banco.cursor()
    cursor.execute('SELECT id FROM produtos')#pegou só a coluna id
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[linha][0] 
    cursor.execute('SELECT * FROM produtos WHERE id='+str (valor_id))
    produto = cursor.fetchall()
    numero_id = valor_id

    terceira_tela.lineEdit.setText(str(produto[0][0]))
    terceira_tela.lineEdit_2.setText(str(produto[0][1]))
    terceira_tela.lineEdit_3.setText(str(produto[0][2]))
    terceira_tela.lineEdit_4.setText(str(produto[0][3]))
    terceira_tela.lineEdit_5.setText(str(produto[0][4]))
    terceira_tela.show()

def salvar_editados():

    global numero_id
    codigo = terceira_tela.lineEdit_2.text()
    descricao = terceira_tela.lineEdit_3.text()
    preco = terceira_tela.lineEdit_4.text()
    categoria = terceira_tela.lineEdit_5.text()
    #atualizar no banco de dados
    cursor = banco.cursor()
    cursor.execute("UPDATE produtos SET codigo = '{}', descricao = '{}', preco = '{}', categoria ='{}' WHERE id = {}".format(codigo,descricao,preco,categoria,numero_id))
    banco.commit()
    terceira_tela.close()
    segunda_tela.close()
    visu_segunda_tela()


apl = QtWidgets.QApplication([]) #cria o aplicativo 
formulario = uic.loadUi("cadastroprodutos.ui")#lê e carrega arquivo 'ui' criado pelo Qt Designer
segunda_tela = uic.loadUi("visualizar.ui") #lê e carrega o aquivo 'ui' da segunda tela
terceira_tela = uic.loadUi("editar_produto.ui")

#botões
formulario.pushButton.clicked.connect(funcao_principal) #chama a funcção quando aperta o botão 'enviar'.
formulario.pushButton_2tela.clicked.connect(visu_segunda_tela) #chama a função quando aperta o botão 'visualizar'
segunda_tela.pushButton.clicked.connect(gerar_pdf)#chama a funcção que gera o pdf
segunda_tela.pushButton_2.clicked.connect(excluir_dados)
segunda_tela.pushButton_3.clicked.connect(tela_editar)
terceira_tela.pushButton.clicked.connect(salvar_editados)

formulario.show() #mostra a primeira tela com o arquivo "ui".
apl.exec() #executa o aplicativo