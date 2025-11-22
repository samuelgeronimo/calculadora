import asyncio
from app import ProductExtractor

async def main():
    extractor = ProductExtractor()
    await extractor.iniciar()
    try:
        result = await extractor.extrair_ofertas('https://www.comprasparaguai.com.br/busca/?q=ps5')
        print('SUGESTOES:', result.get('sugestoes'))
    finally:
        await extractor.fechar()

if __name__ == '__main__':
    asyncio.run(main())
