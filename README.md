# GETLINE ACESSÓRIOS - VITRINE VIRTUAL

> **Projeto de Extensão Universitária | Desenvolvimento Mobile**

Este é um aplicativo mobile nativo (Android) desenvolvido para a transformação digital do comércio local. O app funciona como uma vitrine virtual para a loja **Getline Acessórios** (Zabelê - PB), conectando clientes diretamente ao estoque local e simplificando o processo de compra via WhatsApp.

![Status](https://img.shields.io/badge/Status-Concluído-green)
![Python](https://img.shields.io/badge/Python-3.10-blue)
![KivyMD](https://img.shields.io/badge/Frontend-KivyMD-purple)
![FastAPI](https://img.shields.io/badge/Backend-FastAPI-teal)

---

## IMAGENS DO PROJETO

---

## FUNCIONALIDADES

* **VITRINE DINÂMICA:** Visualização de produtos atualizados em tempo real via API na nuvem.
* **BUSCA INTELIGENTE:** Pesquisa de produtos por nome ou através de atalhos de categorias (Ex: Fones, Cabos).
* **CARRINHO DE COMPRAS:** Adição e remoção de itens, com cálculo automático do valor total.
* **CHECKOUT VIA WHATSAPP:** Ao finalizar o pedido, o app formata a lista de compras e envia diretamente para o WhatsApp do vendedor (*Deep Linking*), eliminando burocracias de cadastro.
* **BANNERS PROMOCIONAIS:** Carrossel de ofertas gerenciado remotamente.
* **OFFLINE FIRST:** O app avisa amigavelmente caso o usuário esteja sem internet.

---

## COMO BAIXAR E INSTALAR (PARA USUÁRIOS)

1. Baixe o arquivo **`Getline_Vitrine_v1.0.apk`** da seção "Releases" deste repositório.
2. Transfira o arquivo para o seu celular Android.
3. Clique no arquivo para instalar.
   * *Obs: Se o Android pedir permissão para "Instalar de fontes desconhecidas", habilite a opção nas configurações.*
4. Abra o aplicativo **Getline** e aproveite!

---

## COMO EXECUTAR O PROJETO (PARA DESENVOLVEDORES)

Este projeto é dividido em **Frontend** (App) e **Backend** (API).

### PRÉ-REQUISITOS
* Python 3.10+
* Git instalado

### 1. CLONAR O REPOSITÓRIO
```bash
git clone [https://github.com/tfneves27/projeto-getline.git](https://github.com/tfneves27/projeto-getline.git)
cd projeto-getline
```

2. CONFIGURAR E RODAR (FRONTEND)
Navegue até a pasta do aplicativo:

```bash

cd frontend
```
Crie e ative um ambiente virtual:

```Bash

python -m venv venv
# No Windows:
.\venv\Scripts\activate
# No Linux/Mac:
source venv/bin/activate
```
Instale as dependências:

```Bash

pip install -r requirements.txt
```
Execute o aplicativo no PC:

```Bash

python main.py
```
### 3. BACKEND (OPCIONAL)
O aplicativo já está configurado para consumir a API oficial hospedada na nuvem (Render). Caso queira rodar o servidor localmente:

```Bash

cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```
## TECNOLOGIAS UTILIZADAS
* PYTHON 3.10+
* KIVY & KIVYMD (Interface Gráfica Mobile e Material Design)
* FASTAPI (Backend/API REST de alta performance)
* HTTPX & ASYNCIO (Comunicação assíncrona com a API)
* BUILDOZER (Empacotamento para Android APK)
* RENDER (Hospedagem em Nuvem)

## AUTOR
### Tiago Félix Neves

Desenvolvido como Projeto de Extensão Universitária.
