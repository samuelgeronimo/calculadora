import requests
import json

BASE_URL = 'http://localhost:5000'

def test_category_extraction():
    print("\nTesting Category Extraction...")
    url = f"{BASE_URL}/api/extrair"
    
    # Example category URL (common pattern)
    category_url = "https://www.comprasparaguai.com.br/celular/?q=iphone"
    
    payload = {"url": category_url}
    try:
        print(f"Sending POST with URL: {category_url}")
        response = requests.post(url, json=payload)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Success: {data.get('success')}")
            print(f"Type: {data.get('tipo')}")
            
            if data.get('tipo') == 'ofertas':
                ofertas = data.get('ofertas', [])
                print(f"Found {len(ofertas)} offers.")
                if ofertas:
                    first = ofertas[0]
                    print("First offer sample:")
                    print(f"  Name: {first.get('nome')}")
                    print(f"  Store: {first.get('loja')}")
                    print(f"  Price: {first.get('preco')}")
            elif data.get('tipo') == 'detalhes':
                print("Returned as 'detalhes' (Single Product).")
                produto = data.get('produto', {})
                print(f"  Name: {produto.get('nome')}")
        else:
            print(f"Request failed: {response.text}")
            
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    test_category_extraction()
