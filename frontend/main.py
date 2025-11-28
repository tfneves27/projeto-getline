import asyncio
import webbrowser
from kivymd.app import MDApp
from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationItem
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivy.properties import StringProperty, NumericProperty
from kivymd.uix.screen import MDScreen
from kivymd.uix.carousel import MDCarousel
from kivymd.uix.spinner import MDSpinner
from api_service import ApiService
from kivymd.uix.textfield import MDTextField
from carrinho import Carrinho
from kivymd.uix.list import TwoLineAvatarListItem, ImageLeftWidget, OneLineIconListItem, IconLeftWidget, TwoLineAvatarIconListItem, IconRightWidget

# --- 1. COMPONENTES ---
class ProdutoCard(MDCard):
    nome = StringProperty()
    preco = NumericProperty()
    imagem_url = StringProperty()

    def adicionar_ao_carrinho(self):
        app = MDApp.get_running_app()
        novo_item = {
            "nome": self.nome,
            "preco": self.preco,
            "imagem_url": self.imagem_url
        }
        app.carrinho.adicionar_item(novo_item)
        print(f"Comprado: {self.nome}")

class ItemCarrinho(TwoLineAvatarIconListItem):
    def __init__(self, produto_original, remover_callback, **kwargs):
        super().__init__(**kwargs)
        self.produto_original = produto_original
        self.remover_callback = remover_callback

    def remover_clicado(self):
        print(f"Lixeira clicada para: {self.produto_original['nome']}")
        self.remover_callback(self.produto_original, self)

class RootWidget(FloatLayout):
    pass

# --- 2. TELAS ---
class HomeScreen(MDBottomNavigationItem):
    def on_enter(self):
        app = MDApp.get_running_app()
        # Verifica se a aba Categorias encomendou uma busca
        termo = app.termo_pendente
        
        # Se tem encomenda, busca ela. Se não, busca tudo (destaques).
        asyncio.create_task(self.fetch_products(termo=termo))
        
        # Limpa a encomenda
        app.termo_pendente = None

    def realizar_busca(self, texto_digitado):
        # Busca manual pela barra de pesquisa
        asyncio.create_task(self.fetch_products(termo=texto_digitado))

    async def fetch_products(self, termo=None):
        app = MDApp.get_running_app()
        spinner = app.root.ids.loading_spinner
        content = app.root.ids.main_layout_content
        grid = app.root.ids.product_grid
        
        spinner.active = True 
        content.opacity = 0
        
        service = ApiService()
        # Busca dados da API
        lista_de_produtos = await service.buscar_produtos_destaque(termo=termo)

        grid.clear_widgets()
        for produto in lista_de_produtos:
            novo_card = ProdutoCard(
                nome=produto['nome'],
                preco=produto['preco'],
                imagem_url=produto['imagem_url']
            )
            grid.add_widget(novo_card)
            
        spinner.active = False 
        content.opacity = 1 

class CartScreen(MDBottomNavigationItem):
    def on_enter(self):
        app = MDApp.get_running_app()
        self.carrinho = app.carrinho
        lista_visual = self.ids.cart_list
        lista_visual.clear_widgets()
        
        for item in self.carrinho.itens:
            list_item = ItemCarrinho(
                text=item['nome'],
                secondary_text=f"R$ {item['preco']}",
                produto_original=item,
                remover_callback=self.remover_item_da_lista
            )
            imagem = ImageLeftWidget(source=item['imagem_url'])
            list_item.add_widget(imagem)
            
            lixeira = IconRightWidget(
                icon="trash-can",
                on_release=lambda x, i=list_item: i.remover_clicado()
            )
            list_item.add_widget(lixeira)
            lista_visual.add_widget(list_item)

    def remover_item_da_lista(self, produto, widget_da_lista):
        try:
            print("Tentando remover item...")
            self.carrinho.remover_item(produto)
            self.ids.cart_list.remove_widget(widget_da_lista)
            print("Item removido com sucesso!")

        except Exception as e:
            print(f"ERRO AO REMOVER (Mas o app não fechou!): {e}")
            
    def finalizar_pedido(self):
        nome = self.ids.campo_nome.text
        observacao = self.ids.campo_observacao.text
        
        if nome == "":
            print("Preencha seu nome!")
            return

        app = MDApp.get_running_app()
        carrinho = app.carrinho
        
        if not carrinho.itens:
            print("Carrinho vazio")
            return

        mensagem = f"Olá! Sou *{nome}* e gostaria de finalizar o pedido:\n\n"
        for item in carrinho.itens:
            mensagem += f"• {item['nome']} - R$ {item['preco']}\n"
        
        total = carrinho.get_total()
        mensagem += f"\n*Total: R$ {total:.2f}*"
        
        if observacao:
            mensagem += f"\n\n*Obs:* {observacao}"

        from urllib.parse import quote
        mensagem_codificada = quote(mensagem)
        numero_loja = "551193198031"
        link_whatsapp = f"https://wa.me/{numero_loja}?text={mensagem_codificada}"

        webbrowser.open(link_whatsapp)
        
        carrinho.limpar()
        self.ids.cart_list.clear_widgets()
        self.ids.campo_nome.text = ""
        self.ids.campo_observacao.text = ""

# --- 3. APP ---
class GetlineApp(MDApp):
    def build(self):
        self.carrinho = Carrinho()
        self.termo_pendente = None # Variável para controlar a busca das categorias
        return RootWidget()
    
    def definir_busca(self, termo):
        self.termo_pendente = termo

if __name__ == '__main__':
    asyncio.run(GetlineApp().async_run())