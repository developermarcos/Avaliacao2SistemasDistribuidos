from tkinter import *
from tkinter import messagebox
#from tkinter.ttk import Frame, Button, Label, Style

class TelaAplicacao(Frame):

    def __init__(self):
        super().__init__()

        self.master.title("Exemplo Sockets TCP - Cliente")
        self.pack(fill=BOTH, expand=True)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        
        self.textMsgRecebida = Text(self)
        self.textMsgRecebida.grid(row=0, column=0, columnspan=3, rowspan=1, padx=5, pady=5, sticky=E+W+S+N)

        self.lbConectados = Listbox(self) 
        self.lbConectados.insert(1, 'ze') 
        self.lbConectados.insert(2, 'maria') 
        self.lbConectados.insert(3, 'joão') 
        self.lbConectados.insert(4, 'abc Bolinhas') 
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


    def conectar(self):
        messagebox.showinfo("Conectar", "implemente as rotinas para conectar")

    def enviarMensagem(self):
        messagebox.showerror("Enviar Mensagem", "implemente as rotinas para enviar mensagem")
        
        teste = self.entryMsgEnviar.get()
        self.entryMsgEnviar.delete(0, END)
        self.textMsgRecebida.insert(END, "\n"+teste)
       
    def enviarArquivo(self):
        messagebox.showwarning("Enviar Arquivo", "implemente as rotinas para enviar arquivo")


def main():
    
    root = Tk()
    root.geometry("500x500")
    app = TelaAplicacao()
    root.mainloop()


if __name__ == '__main__':
    main()
