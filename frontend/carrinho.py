class Carrinho():
    def __init__(self):
        self.itens = []

    def adicionar_item(self, produto):
        self.itens.append(produto)
        print(f"Item adicionado: {produto['nome']}")

    def get_total(self):
        return sum(item['preco'] for item in self.itens)
    
    def remover_item(self, produto):
        if produto in self.itens:
            self.itens.remove(produto)
            print(f"Item removido do carrinho: {produto['nome']}")

    def limpar(self):
        self.itens = []
        print("Carrinho esvaziado.")