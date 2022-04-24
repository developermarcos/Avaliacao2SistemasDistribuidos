import socket, json
class Mensagem:
    def __init__(self, nome, mensagem, tipo, lista, destinatario):
        self.nome = nome
        self.mensagem = mensagem
        self.tipo = tipo
        self.conexoes = lista
        self.destinatario = destinatario
