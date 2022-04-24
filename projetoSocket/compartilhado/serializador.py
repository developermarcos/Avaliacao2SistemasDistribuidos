import json

class Serial:
    
    def serealizarMensagem(self, objetoMensagem):
        objetoSerealizado = json.dumps(objetoMensagem, indent=0)
        return objetoSerealizado

    def deserializarMensagem(self, objetoMensagem):
        return json.loads(objetoMensagem)

    def serealizarObjeto(self, objetoMensagem):
        objetoSerealizado = json.dumps(objetoMensagem.__dict__, indent=0)
        return objetoSerealizado