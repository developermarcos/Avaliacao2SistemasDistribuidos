from tkinter import *
from tkinter import messagebox
#from tkinter.ttk import Frame, Button, Label, Style

import socket, json
import threading

class Mensagem(object):
    def __init__(self):
        self.nome = ""
        self.mensagem = ""
        self.lista = list()
        self.tipo = ""

class TelaAplicacao(Frame):
   
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

        
        messagebox.showinfo("Atenção", "Informe o nome de usuário e clique em conectar")

    def conectar(self):
        # cria o socket TCP do cliente, abrindo uma porta alta
        self.mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #print('Cliente Python UDP: {}'.format( mySocket.getsockname ) )
        
        # define o endereço e porta do servidor de destino
        self.servidorDestino = ('127.0.0.1', 10000)
        
        #realiza a conexao com o servidor
        # cria e dispara a execução da thread para o servidor
        self.mySocket.connect(self.servidorDestino)
        self.t = threading.Thread(target=self.rodaThread, args=())
        self.t.start()
        self.username = self.entryMsgEnviar.get()
        self.entryMsgEnviar.delete(0, END)
        messagebox.showinfo("Status", "Conectado")

    def enviarMensagem(self):
        #messagebox.showerror("Enviar Mensagem", "implemente as rotinas para enviar mensagem")
        teste = self.entryMsgEnviar.get()
        self.entryMsgEnviar.delete(0, END)
        self.textMsgRecebida.insert(END, "\n"+": ".join([self.username, teste]))

        objectEnviar = Mensagem()
        objectEnviar.nome = self.username
        objectEnviar.mensagem = teste
        objectEnviar.tipo = 'Mensagem'

        data_string = json.dumps(objectEnviar.__dict__, indent=0)
        self.mySocket.send( bytes(data_string,encoding="utf-8") )

        #mensagemServidor = ": ".join([self.username, teste])
        #self.mySocket.send(mensagemServidor.encode('utf-8'))

        


        
    def enviarArquivo(self):
        messagebox.showwarning("Enviar Arquivo", "implemente as rotinas para enviar arquivo")

    def createThreading(self):
        self.Threading = threading.Thread(target=self.receiveMesages, args=())
        self.Threading.start()

    def rodaThread(self):
        while True:
            try:
                # fica em wait ate que uma mensagem chegue
                # recebe e mostra a mensagem devolvida pelo servidor
                
                mensagemRecebida = self.mySocket.recv(4096)
                objetoMensagem = json.loads(mensagemRecebida)
                
                self.textMsgRecebida.insert(END, "\n"+objetoMensagem.mensagem.decode())
                print('Recebido do servidor {}: {}'.format( self.mySocket.getpeername(),objetoMensagem.mensagem.decode()))
            except:
                self.mySocket.close()
                break


def main():
    root = Tk()
    root.geometry("500x500")
    app = TelaAplicacao()
    root.mainloop()


if __name__ == '__main__':
    main()