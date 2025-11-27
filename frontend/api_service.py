import httpx

class ApiService:
    async def buscar_produtos_destaque(self, termo=None):
        async with httpx.AsyncClient() as client:
            if termo:
                url = f"http://127.0.0.1:8000/produtos/busca?termo={termo}"
            else:
                url = "http://127.0.0.1:8000/produtos"
            
            response = await client.get(url)
            return response.json()
        
    async def buscar_promocoes(self):
        async with httpx.AsyncClient() as client:
            response = await client.get("http://127.0.0.1:8000/promocoes")
            return response.json()