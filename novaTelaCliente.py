from tkinter import *
from tkinter import messagebox
from tkinter import filedialog, Tk
#from tkinter.ttk import Frame, Button, Label, Style
import os
import socket, json
import threading
import logging



class Mensagem(object):
    def __init__(self):
        self.nome = ""
        self.mensagem = ""
        self.lista = list()
        self.tipo = ""

class TelaAplicacao(Frame):
   
    objectEnviar = Mensagem()
    objetoMensagem = Mensagem()
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self,):
        super().__init__()

        self.master.title("Exemplo Sockets TCP - Cliente")
        self.pack(fill=BOTH, expand=True)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        
        self.textMsgRecebida = Text(self)
        self.textMsgRecebida.grid(row=0, column=0, columnspan=3, rowspan=1, padx=5, pady=5, sticky=E+W+S+N)

        self.lbConectados = Listbox(self) 
        # self.lbConectados.insert(1, 'ze') 
        self.lbConectados.grid(row=0, column=4, columnspan=1, rowspan=2, padx=5, pady=5, sticky=E+W+S+N)

        self.entryMsgEnviar = Entry(self)
        self.entryMsgEnviar.grid(row=1, column=0, columnspan=3, rowspan=1, padx=5, pady=5, sticky=E+W+S+N)


        self.buttonConectar = Button(self, text="Conectar")
        self.buttonConectar.grid(row=2, column=0, padx=5, pady=5 )
        self.buttonConectar["command"] = self.conectar

        self.buttonEnviar = Button(self, text="Enviar")
        self.buttonEnviar.grid(row=2, column=1, padx=5, pady=5 )
        self.buttonEnviar["command"] = self.enviarMensagem

        self.buttonEnviarArquivo = Button(self, text="Arquivo")
        self.buttonEnviarArquivo.grid(row=2, column=2, padx=5, pady=5 )
        self.buttonEnviarArquivo["command"] = self.enviarArquivo

        self.buttonConectar = Button(self, text="Desconectar")
        self.buttonConectar.grid(row=2, column=3, padx=5, pady=5 )
        self.buttonConectar["command"] = self.desconectar
        
        messagebox.showinfo("Atenção", "Informe o nome de usuário e clique em conectar")

    def conectar(self):
        host = '127.0.0.1'
        port = 10000
        # define o endereço e porta do servidor de destino
        self.servidorDestino = (host, port)
        
        #realiza a conexao com o servidor
        # cria e dispara a execução da thread para o servidor
        self.mySocket.connect(self.servidorDestino)

        self.username = self.entryMsgEnviar.get()
        self.entryMsgEnviar.delete(0, END)
        self.objectEnviar.nome = self.username
        self.objectEnviar.tipo = "Login"

        #Enviando Nome da Conexão pro Servidor
        data_string = json.dumps(self.objectEnviar.__dict__, indent=0)
        self.mySocket.send( bytes(data_string,encoding="utf-8") )

        messagebox.showinfo("Status", "Conectado")

    def enviarMensagem(self):
        #messagebox.showerror("Enviar Mensagem", "implemente as rotinas para enviar mensagem")
        teste = self.entryMsgEnviar.get()
        self.entryMsgEnviar.delete(0, END)
        self.textMsgRecebida.insert(END, "\n"+": ".join([self.username, teste]))

        self.objectEnviar.mensagem = teste
        self.objectEnviar.tipo = 'Mensagem'

        data_string = json.dumps(self.objectEnviar.__dict__, indent=0)
        self.mySocket.send( bytes(data_string,encoding="utf-8") )

        #mensagemServidor = ": ".join([self.username, teste])
        #self.mySocket.send(mensagemServidor.encode('utf-8'))

        
    def desconectar(self):
        self.objectEnviar.tipo = "Logoff"

        #Enviando Nome da Conexão pro Servidor
        data_string = json.dumps(self.objectEnviar.__dict__, indent=0)
        self.mySocket.send( bytes(data_string,encoding="utf-8") )    

        
    def enviarArquivo(self):
        #messagebox.showwarning("Enviar Arquivo", "implemente as rotinas para enviar arquivo")
        
             #Enviando Nome da Conexão pro Servidor
        data_string = json.dumps(self.objectEnviar.__dict__, indent=0)
        self.mySocket.send( bytes(data_string,encoding="utf-8") )
        
        # abre tela para escolha de um arquivo
        root = Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(
        initialdir="/", title="Escolha um arquivo", filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))
        print(file_path)
        # envia mensagem com o nome do arquivo que vai ser enviado
        self.mySocket.send(os.path.basename(file_path).encode())
        #abre o arquivo escolhido, e vai enviando para o cliente por partes
        with open( file_path , 'rb') as f:
            self.mySocket.sendfile(f, 0)

    def createThreading(self):
        t = threading.Thread(target=self.rodaThread, args=(self.mySocket,))
        t.start()

    def rodaThread(self, mySocket):
        while True:
            try:
                # fica em wait ate que uma mensagem chegue
                # recebe e mostra a mensagem devolvida pelo servidor
                
                mensagemRecebida = mySocket.recv(4096)
                objetoMensagem = json.loads(mensagemRecebida)
                
                self.textMsgRecebida.insert(END, "\n"+objetoMensagem.mensagem)
                
                # Percorrendo array da lista de conexões para atualizar list box
                for i in range (len(self.objetoMensagem.lista)): 
                    self.lbConectados.insert([i], self.objetoMensagem.lista[i])

                print('Recebido do servidor {}: {}'.format( mySocket.getpeername(),objetoMensagem.mensagem.decode()))
            except:
                mySocket.close()
                break


def main():
    root = Tk()
    root.geometry("500x500")
    app = TelaAplicacao()
    root.mainloop()


if __name__ == '__main__':
    main()