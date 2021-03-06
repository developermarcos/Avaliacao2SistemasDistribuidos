from faulthandler import disable
import socket, json
import threading
from typing import Any
from compartilhado import serializador


from tkinter import *
from tkinter import messagebox, filedialog, Tk

from compartilhado.mensagem import Mensagem
#from tkinter.ttk import Frame, Button, Label, Style

import os


class TelaAplicacao(Frame):
   
    def __init__(self, molduraTela):
        super().__init__()
        self.molduraTela = molduraTela
        self.master.title("Exemplo Sockets TCP - Cliente")
        self.pack(fill=BOTH, expand=True)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        
        self.textMsgRecebida = Text(self)
        self.textMsgRecebida.grid(row=0, column=0, columnspan=3, rowspan=1, padx=5, pady=5, sticky=E+W+S+N)

        self.lbConectados = Listbox(self) 
        self.lbConectados.grid(row=0, column=4, columnspan=1, rowspan=2, padx=5, pady=5, sticky=E+W+S+N)
        self.lbConectados.bind('<Double-1>', self.setDestinatario)

        self.entryMsgEnviar = Entry(self)
        self.entryMsgEnviar.grid(row=1, column=0, columnspan=3, rowspan=1, padx=5, pady=5, sticky=E+W+S+N)


        self.buttonConectar = Button(self, text="Conectar")
        self.buttonConectar.grid(row=2, column=0, padx=5, pady=5 )
        self.buttonConectar["command"] = self.conectar

        self.buttonEnviar = Button(self, text="Enviar")
        self.buttonEnviar.grid(row=2, column=1, padx=5, pady=5 )
        self.buttonEnviar["command"] = self.enviarMensagem
        self.buttonEnviar["state"] = DISABLED

        self.buttonEnviarArquivo = Button(self, text="Arquivo")
        self.buttonEnviarArquivo.grid(row=2, column=2, padx=5, pady=5 )
        self.buttonEnviarArquivo["command"] = self.enviarArquivo
        self.buttonEnviarArquivo["state"] = DISABLED

        self.buttonDesconectar = Button(self, text="Desconectar e Sair")
        self.buttonDesconectar.grid(row=2, column=4, padx=5, pady=5 )
        self.buttonDesconectar["command"] = self.desconectar
        self.buttonDesconectar["state"] = DISABLED

        self.serializador = serializador.Serial()
        self.destinatario = ''
        
        messagebox.showinfo("Aten????o", "Informe o nome de usu??rio e clique em conectar")

    def setDestinatario(self, e):
        self.destinatario = self.lbConectados.get(self.lbConectados.curselection())
        

    def conectar(self):
        # Captura nome na tela
        nome = self.entryMsgEnviar.get()

        if nome != '':

            # Guarda o nome do cliente
            self.nome = nome
            
            # Cria mensagem de conexao
            mensagemConexao = Mensagem(nome, '', 'conectar', '','')
            
            # Serealiza objeto mensagem
            novaMensagemSerealizada =  self.serializador.serealizarObjeto(mensagemConexao)

            # Cria conex??o com o servidor
            self.__createConection()

            # Envia mensagem para o servidor
            self.__EnviarMensagemSerealizadaServidor(novaMensagemSerealizada)

            #Limpa o campo de digita????o
            self.entryMsgEnviar.delete(0, END)
            # Popula campo de conectador
            self.lbConectados.insert(0, self.nome) 
            
            # Nome cliente na tela
            self.master.title("Exemplo Sockets TCP - Cliente - "+self.nome)

            #muda estado dos bot??es
            self.buttonConectar["state"] = DISABLED
            self.buttonEnviar["state"] = NORMAL
            self.buttonEnviarArquivo["state"] = NORMAL 
            self.buttonDesconectar["state"] = NORMAL
        else:
            messagebox.showinfo("Aviso", "Nenhum nome informado, tente novamente.")

    def enviarMensagem(self):
        #messagebox.showinfo("Status", "Mensagem enviada")
        message = self.entryMsgEnviar.get()
        
        if message != '' and self.destinatario != self.nome:
            #Cria instancia do nome do destinatario como vazio
            nomeDestinatario = 'Todos os clientes'
            tipo = 'mensagem'

            #Verifica se a mensagem ser?? para um usu??rio espec??fico e seta o nome
            if self.destinatario != '':
                nomeDestinatario = self.destinatario
                tipo = 'mensagemDestinatario'

            # Monta mensagem para o servidor
            mensagem = Mensagem(self.nome,message,tipo,'',nomeDestinatario)
            
            # Serealiza o objeto
            mensagemSerealizada = self.serializador.serealizarObjeto(mensagem)

            # Envia mensagem para o servidor
            self.__EnviarMensagemSerealizadaServidor(mensagemSerealizada)
            
            # Limpa o campo de digita????o
            self.entryMsgEnviar.delete(0, END)

            mensagemFormatada = "\nEu: "+message
            # Popula mensagem cliente
            self.textMsgRecebida.insert(END, mensagemFormatada)

            # Limpa nome do destinat??rio
            self.destinatario = ''
        else:
            if message == '':
                messagebox.showwarning("Aviso", "Nenhuma mensagem informada.")
            else:
                messagebox.showwarning("Aviso", "Remetente e destinat??rio s??o iguais.")
                self.destinatario = ''

    def enviarArquivo(self):
        nomeDestinatario = ''
        tipo = 'arquivo'
        if self.destinatario != '':
                nomeDestinatario = self.destinatario

        mensagemArquivo = Mensagem(self.nome,"",tipo,'',nomeDestinatario)

        mensagemSerializada = self.serializador.serealizarObjeto(mensagemArquivo)

        self.__EnviarMensagemSerealizadaServidor(mensagemSerializada)
        # abre tela para escolha de um arquivo
        root = Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(initialdir="/", title="Escolha um arquivo", filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))
        
        # envia mensagem com o nome do arquivo que vai ser enviado
        self.Conection.send(os.path.basename(file_path).encode())

        messagebox.showinfo("Aten????o", "Aperte OK quando todos os clientes selecionarem uma pasta")

        #abre o arquivo escolhido, e vai enviando para o cliente por partes
        with open( file_path , 'rb') as f:
            self.Conection.sendfile(f, 0)
            
        print('Arquivo enviado.')

    def receiveMesages(self):
        try:
            while True:
                #Recebe a resposta do servidor
                data = self.Conection.recv(4096)
                
                if not data:
                    break
                
                # Deserealiza objeto mensagem
                mensagemRecebida = self.serializador.deserializarMensagem(data)

                try:
                    tipo = mensagemRecebida.get("tipo")
                    # Verifica o tipo da mensagem recebida do servidor
                    
                    if tipo == 'mensagem':
                        self.__populaTxtMsgRecebida(mensagemRecebida)
                    
                    elif tipo == 'conectar' or tipo == 'desconectar':
                        print(tipo)
                        conectados = self.serializador.deserializarMensagem(mensagemRecebida.get("conectados"))
                        # Popular campo com todos clientes conectados
                        self.__popularLabelConectados(conectados)
                        mensagem = 'Novo usu??rio conectado' if tipo == 'conectar' else 'Usu??rio desconectado'
                        messagebox.showinfo("Aten????o", mensagem)

                    elif tipo == 'arquivo':
                        print('Arquivo')

                        # recebe mensagem com o nome do arquivo que vai receber
                        nomeArquivo = self.Conection.recv(1024)
                        
                        # cria um novo arquivo bin??rio, vazio, para receber o arquivo enviado
                        caminhoNomeArquivo = os.path.abspath(os.path.dirname(__file__))
                        print(caminhoNomeArquivo)
                        file = open(caminhoNomeArquivo+'/arquivos/new_'+nomeArquivo.decode(), "wb")
                        # Receba as partes do arquivo e monta o arquivo
                        RecvData = self.Conection.recv(1024)
                        while RecvData:
                            file.write(RecvData)
                            RecvData = self.Conection.recv(1024)
                        # Feche o arquivo aberto no lado do servidor uma vez que a c??pia seja conclu??da
                        file.close()
                        print("\n O arquivo foi copiado com sucesso \n")
                except:
                    break
        except:
            print('Conex??o encerrada')
                
    def desconectar(self):
        # Cria mensagem de conexao
        mensagemDesconexao = Mensagem(self.nome, '', 'desconectar', '','')
        
        # Serealiza objeto mensagem
        novaMensagemSerealizada =  self.serializador.serealizarObjeto(mensagemDesconexao)

        # Envia mensagem para o servidor
        self.__EnviarMensagemSerealizadaServidor(novaMensagemSerealizada)
        self.Conection.close()
        messagebox.showwarning("Status", "Usu??rio desconectado.")

        #self.molduraTela.destroy()

        # Muda estado dos bot??es
        self.buttonConectar["state"] = NORMAL
        self.buttonEnviar["state"] = DISABLED
        self.buttonEnviarArquivo["state"] = DISABLED 
        self.buttonDesconectar["state"] = DISABLED

        # Limpa conex??es dos campos
        self.lbConectados.delete(0, END)
        self.textMsgRecebida.delete('1.0', END) 
         


    # m??todos privados

    def __createConection(self):
        # cria o socket TCP do cliente, abrindo uma porta alta
        self.Conection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        #Define o endere??o e a porta
        self.ConectParameter = ('127.0.0.1', 10000)

        #realiza a conexao com o servidor
        self.Conection.connect(self.ConectParameter)

        # Define uma thread para aguardar as respostas
        self.Threading = threading.Thread(target=self.receiveMesages, args=())
        # Inicia a thread
        self.Threading.start()

    def __EnviarMensagemSerealizadaServidor(self, objetoMensagemSerealizada):
        # Enviar mensagem para o servidor
        self.Conection.send( bytes(objetoMensagemSerealizada,encoding="utf-8") )
    
    def __popularLabelConectados(self, objetoRecebidoServidor):
        #Limpar listbox de conex??o de clientes
        self.lbConectados.delete(0, END)

        # Status da conex??o que ser?? conectado ou desconectado ao final do m??todo
        status = ''

        # La??o de repeti????o que lista todos os usu??rios conectados
        for conexao in objetoRecebidoServidor:
            # Popula campo de usu??rios conectados
            self.lbConectados.insert(0, conexao.get("nome")) 
            # Captura tipo da conex??o
            status = conexao.get('tipo')

        # Verifica o status para apresentar mensagem na tela
        if status == 'conectar':
            self.textMsgRecebida.insert(END, "\nNovo usu??rio conectado")
        else:
            self.textMsgRecebida.insert(END, "\nUsu??rio desconectado")

    def __populaTxtMsgRecebida(self, objetoRecebidoServidor):
        # Insere mensagem recebida no campo de mensagens
        self.textMsgRecebida.insert(END, "\n"+": ".join([objetoRecebidoServidor.get("nome"), objetoRecebidoServidor.get("mensagem")]))
        
    #m??todos privados        

def main():
    root = Tk()
    root.geometry("500x500")
    app = TelaAplicacao(root)
    root.mainloop()
    


if __name__ == '__main__':
    main()