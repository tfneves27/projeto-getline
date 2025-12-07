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
from kivymd.uix.fitimage import FitImage
from kivy.core.window import Window
from kivy.clock import Clock
from kivymd.uix.snackbar import MDSnackbar
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton

# --- 1. COMPONENTES ---
class ProdutoCard(MDCard):
    nome = StringProperty()
    preco = NumericProperty()
    preco_original = NumericProperty() 
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
        self.remover_callback(self.produto_original, self)

class RootWidget(FloatLayout):
    pass

# --- 2. TELAS ---
class HomeScreen(MDBottomNavigationItem):
    def on_enter(self):
        app = MDApp.get_running_app()
        termo = app.termo_pendente
        asyncio.create_task(self.fetch_products(termo=termo))
        asyncio.create_task(self.fetch_banners())
        
        app.termo_pendente = None

    def realizar_busca(self, texto_digitado):
        asyncio.create_task(self.fetch_products(termo=texto_digitado))

    async def fetch_banners(self):
        try:
            service = ApiService()
            lista_banners = await service.buscar_banners()
            
            carrossel = self.ids.banner_carousel
            if lista_banners:
                carrossel.clear_widgets()
                for banner in lista_banners:
                    card = MDCard(
                        radius=[15,],
                        elevation=2,
                        size_hint=(None, None),
                        size=(self.ids.main_layout_content.width - 30, "140dp")
                    )
                    imagem = AsyncImage(
                        source=banner['imagem_url'], 
                        allow_stretch=True,
                        keep_ratio=False
                    )
                    card.add_widget(imagem)
                    carrossel.add_widget(card)
        except Exception as e:
            print(f"Erro Banners (Ignorado): {e}")

    async def fetch_products(self, termo=None):
        app = MDApp.get_running_app()
        spinner = app.root.ids.loading_spinner
        content = app.root.ids.main_layout_content
        grid = app.root.ids.product_grid
        
        spinner.active = True 
        content.opacity = 0
        
        try:
            service = ApiService()
            lista_de_produtos = await service.buscar_produtos_destaque(termo=termo)

            grid.clear_widgets()

            if not lista_de_produtos:
                from kivymd.uix.label import MDLabel
                from kivymd.uix.boxlayout import MDBoxLayout
                from kivymd.uix.button import MDIconButton

                aviso = MDBoxLayout(orientation="vertical", size_hint_y=None, height="200dp")
                icone = MDIconButton(
                    icon="emoticon-sad-outline", 
                    pos_hint={"center_x": .5},
                    font_size="64sp",  
                    theme_text_color="Hint"
                )
                texto = MDLabel(
                    text="Produto não encontrado...", 
                    halign="center", 
                    theme_text_color="Hint"
                )
                
                aviso.add_widget(icone)
                aviso.add_widget(texto)
                grid.add_widget(aviso)

            else:
                for produto in lista_de_produtos:
                    p_preco = produto.get('preco', 0)
                    p_original = produto.get('preco_original', p_preco)
                    
                    novo_card = ProdutoCard(
                        nome=produto.get('nome', 'Sem Nome'),
                        preco=p_preco,
                        preco_original=p_original,
                        imagem_url=produto.get('imagem_url', '')
                    )
                    grid.add_widget(novo_card)
                
            content.opacity = 1

        except Exception as e:
            app = MDApp.get_running_app()
            app.mostrar_erro_internet()
        
        finally:
            spinner.active = False

class CartScreen(MDBottomNavigationItem):
    def on_enter(self):
        self.atualizar_lista()

    def atualizar_lista(self):
        app = MDApp.get_running_app()
        self.carrinho = app.carrinho
        
        lista_visual = self.ids.cart_list
        lista_visual.clear_widgets()
        
        for item in self.carrinho.itens:
            list_item = ItemCarrinho(
                text=item['nome'],
                secondary_text=f"R$ {item['preco']:.2f}",
                produto_original=item,
                remover_callback=self.remover_item_da_lista
            )
            imagem = ImageLeftWidget(source=item['imagem_url'])
            list_item.add_widget(imagem)
            
            lixeira = IconRightWidget(
                icon="trash-can",
                theme_text_color="Custom",
                text_color="red",
                on_release=lambda x, i=list_item: i.remover_clicado()
            )
            list_item.add_widget(lixeira)
            lista_visual.add_widget(list_item)

        total = self.carrinho.get_total()
        if total > 0:
            self.ids.lbl_total.text = f"Total: R$ {total:.2f}"
        else:
            self.ids.lbl_total.text = "Seu carrinho está vazio"

    def remover_item_da_lista(self, produto, widget_da_lista):
        try:
            self.carrinho.remover_item(produto)
            self.ids.cart_list.remove_widget(widget_da_lista)
            self.atualizar_lista()
        except Exception as e:
            print(f"Erro ao remover: {e}")

    def finalizar_pedido(self):
        nome = self.ids.campo_nome.text
        observacao = self.ids.campo_observacao.text
        
        # Validação de Nome
        if nome == "":
            self.ids.campo_nome.error = True
            self.ids.campo_nome.helper_text = "O nome é obrigatório!"
            self.ids.campo_nome.helper_text_mode = "on_error"
            return
        
        self.ids.campo_nome.error = False

        app = MDApp.get_running_app()
        carrinho = app.carrinho
        
        if not carrinho.itens:
            self.ids.lbl_total.text = "Adicione itens primeiro!"
            return

        mensagem = f"Olá! Sou *{nome}* e gostaria de finalizar o pedido:\n\n"
        for item in carrinho.itens:
            mensagem += f"• {item['nome']} - R$ {item['preco']:.2f}\n"
        
        total = carrinho.get_total()
        mensagem += f"\n*Total: R$ {total:.2f}*"
        
        if observacao:
            mensagem += f"\n\n*Obs:* {observacao}"

        from urllib.parse import quote
        mensagem_codificada = quote(mensagem)
        numero_loja = "00000000000"
        link_whatsapp = f"https://wa.me/{numero_loja}?text={mensagem_codificada}"

        import webbrowser
        webbrowser.open(link_whatsapp)
        
        carrinho.limpar()
        self.atualizar_lista()
        self.ids.campo_nome.text = ""
        self.ids.campo_observacao.text = ""

# --- 3. APP ---
class GetlineApp(MDApp):
    dialogo_internet = None

    def build(self):
        self.carrinho = Carrinho()
        self.termo_pendente = None 
        return RootWidget()
    
    def events(self, instance, keyboard, keycode, text, modifiers):
        if keyboard == 27:
            if self.exit_count == 0:
                MDSnackbar(
                    text="Pressione novamente para sair",
                    pos_hint={"center_x": .5, "center_y": .1},
                    size_hint_x=.6,
                    bg_color="#333333"
                ).open()
                
                self.exit_count += 1
                Clock.schedule_once(self.reset_exit, 2)
                return True
            
            elif self.exit_count > 0:
                return False
    
    def reset_exit(self, *args):
        self.exit_count = 0

    def mostrar_erro_internet(self):
        if not self.dialogo_internet:
            self.dialogo_internet = MDDialog(
                title="Sem Conexão",
                text="Verifique seu Wi-Fi ou Dados Móveis.",
                type="alert",
                buttons=[
                    MDFlatButton(
                        text="TENTAR NOVAMENTE",
                        theme_text_color="Custom",
                        text_color="#283593",
                        on_release=lambda x: self.tentar_reconectar()
                    ),
                ],
            )
        self.dialogo_internet.open()

    def tentar_reconectar(self):
        self.dialogo_internet.dismiss()
        home = self.root.ids.home_screen_id
        home.on_enter()

    def on_start(self):
        Window.bind(on_keyboard=self.events)
        self.exit_count = 0

    def definir_busca(self, termo):
        self.termo_pendente = termo

    def abrir_suporte(self):
        numero_loja = "00000000000" 
        texto = "Olá! Estou no app Getline e gostaria de tirar uma dúvida."
        
        from urllib.parse import quote
        texto_codificado = quote(texto)
        
        link = f"https://wa.me/{numero_loja}?text={texto_codificado}"
        
        import webbrowser
        webbrowser.open(link)

if __name__ == '__main__':
    asyncio.run(GetlineApp().async_run())