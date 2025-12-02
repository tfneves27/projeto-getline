import httpx

class ApiService:
    async def buscar_produtos_destaque(self, termo=None):
        async with httpx.AsyncClient() as client:
            base_url = "https://getline-api.onrender.com"
            if termo:
                url = f"{base_url}/produtos/busca?termo={termo}"
            else:
                url = f"{base_url}/produtos"
            
            response = await client.get(url)
            return response.json()
        
    async def buscar_banners(self):
        async with httpx.AsyncClient() as client:
            base_url = "https://getline-api.onrender.com"
        try:
            response = await client.get(f"{base_url}/banners")
            return response.json()
        except Exception as e:
            print(f"Erro ao buscar banners: {e}")
            return[]