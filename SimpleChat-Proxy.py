from flask import Flask, request, Response, stream_with_context, jsonify
from flask_cors import CORS
import requests
import urllib.parse
from bs4 import BeautifulSoup
import random
import time
import re

app = Flask(__name__)
CORS(app)  # Engedélyezi a CORS-t minden domain számára

OLLAMA_URL = "http://localhost:11434"

# ==============================================================================
# DUCKDUCKGO KERESŐ FUNKCIÓK
# ==============================================================================

def _extract_final_url(link_element):
    """URL kinyerése a link elemből (DDG redirect kezelése)."""
    try:
        href = link_element.get("href")
        if not href:
            return None
            
        if '/l/?uddg=' in href or 'duckduckgo.com/l/' in href:
            if href.startswith('//'):
                href = 'https:' + href
                
            parsed_url = urllib.parse.urlparse(href)
            query_params = urllib.parse.parse_qs(parsed_url.query)
            
            if 'uddg' in query_params and query_params['uddg']:
                target_url_encoded = query_params['uddg'][0]
                return urllib.parse.unquote(target_url_encoded)
        
        if href.startswith('http'):
            return href
            
        return None
        
    except Exception:
        return None

def is_relevant_url(url, query):
   
    """Ellenőrzi, hogy egy URL releváns-e a keresési lekérdezéshez és nem egy triviális kizárt formátum."""
    if not url or not isinstance(url, str):
        return False
        
    # Kizárt minták (zajforrások)
    excluded_patterns = [
       'duckduckgo.com', 'google.com/search', 'bing.com/search', 
       '/Special:', '/Category:', 'translate.google', 'youtube.com',
       '.pdf', '.jpg', '.png', '.gif', '.zip', '.rar' # Fájltípusok
    ]
    
    for pattern in excluded_patterns:
        if pattern in url.lower():
            return False
    
    try:
        parsed = urllib.parse.urlparse(url)
        if not parsed.netloc:
            return False
    except:
        return False
        
    return True

def search_duckduckgo_links(query, max_results=15):
    """Javított DuckDuckGo keresés több fallback opcióval, csak linkeket ad vissza."""
    links = []
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    })

    # 1. API próbálkozás (ha elérhető, gyorsabb és stabilabb)
    try:
        api_url = "https://api.duckduckgo.com/"
        params = {
            'q': query,
            'format': 'json',
            'no_html': '1',
            'skip_disambig': '1'
        }
        
        response = session.get(api_url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        for topic in data.get('RelatedTopics', []):
            if isinstance(topic, dict) and 'FirstURL' in topic:
                url = topic['FirstURL']
                if is_relevant_url(url, query):
                    links.append(url)
                    if len(links) >= max_results:
                        break
        
    except Exception:
       pass
    
    # 2. HTML scraping (ha az API nem adott elegendő találatot)
    if len(links) < max_results:
        try:
            encoded_query = urllib.parse.quote_plus(query)
            ddg_url = f"https://duckduckgo.com/html/?q={encoded_query}"
            
            # Késleltetés a robot detektálás elkerülése érdekében
            time.sleep(random.uniform(1, 3))
            
            response = session.get(ddg_url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, "html.parser")
            selectors = ["a.result__a", ".result .result__title a"]
            
            for selector in selectors:
                results = soup.select(selector)
                if results:
                    for r in results[:max_results - len(links)]:
                        final_url = _extract_final_url(r)
                        if final_url and is_relevant_url(final_url, query):
                            if final_url not in links:
                                links.append(final_url)
                                if len(links) >= max_results:
                                    break
                    break
                    
        except Exception:
           pass
    
    return list(dict.fromkeys(links))  # Duplikátumok eltávolítása

def fetch_content_snippet(url):
    """
    Javított funkció: Letölti a tartalom egy részletét a megadott URL-ről, 
    a fő tartalomra fókuszálva (pl. article, main).
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; OllamaAIAgent/1.0; +https://example.com)',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'hu-HU,hu;q=0.8,en-US;q=0.5,en;q=0.3',
        }
        
        # Módosítás: Szigorúbb timeout a letöltési hibák csökkentésére
        response = requests.get(url, headers=headers, timeout=5) 
        response.raise_for_status()
        
        # Módosítás: Kódolás kezelése
        response.encoding = response.apparent_encoding
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Cím kinyerése
        title = soup.title.string if soup.title else url
        
        # ÚJ LOGIKA: Fő tartalom kinyerése, a zaj csökkentésére.
        # Megpróbáljuk megtalálni a legrelevánsabb HTML elemeket.
        content_selectors = [
            'article', 
            'main', 
            'div[role="main"]',
            '.post-content', # Gyakori blog elem
            '#content',
            '#main'
        ]
        
        main_content_element = None
        for selector in content_selectors:
            main_content_element = soup.select_one(selector)
            if main_content_element:
                break
        
        # Ha nem találtunk specifikus elemet, visszatérünk a body-hoz.
        if not main_content_element:
            main_content_element = soup.body
            
        page_text = main_content_element.get_text() if main_content_element else soup.get_text()
        
        # Tisztítás és korlátozás
        # Eltávolítjuk a felesleges szóközöket/új sorokat
        cleaned_content = ' '.join(page_text.split()).strip()
        
        # Módosítás: TARTALOM HOSSZÁNAK NÖVELÉSE 3000 -> 5000 karakterre
        content_limit = 5000 
        
        return {
            "url": url,
            "title": title.strip() if title else url,
            "content": cleaned_content[:content_limit] 
        }

    except requests.exceptions.Timeout:
         return {
            "url": url,
            "title": url,
            "content": "Tartalom letöltése sikertelen: Időtúllépés."
        }
    except requests.exceptions.RequestException as e:
         return {
            "url": url,
            "title": url,
            "content": f"Tartalom letöltése sikertelen: HTTP hiba ({e.response.status_code if e.response else 'ismeretlen'})."
        }
    except Exception:
        # Általános hiba
        return {
            "url": url,
            "title": url,
            "content": "Tartalom letöltése sikertelen: Ismeretlen hiba."
        }


# ==============================================================================
# ÚJ PROXY ÚTVONAL a DuckDuckGo-hoz
# ==============================================================================

@app.route('/api/duckduckgo', methods=['POST'])
def duckduckgo_search_endpoint():
    """Kezeli a kliens DuckDuckGo keresési kérését, letölti a linkeket és a tartalmukat."""
    try:
        data = request.get_json()
        query = data.get('query')
        # A kliens kérheti, hogy csak az első 3 találatot töltse le
        max_results = int(data.get('max_results', 3))
        
        if not query:
            return jsonify({"error": "Hiányzó 'query' paraméter."}), 400

        # 1. Releváns linkek keresése
        links = search_duckduckgo_links(query, max_results=15) 
        
        results_with_content = []
        
        # 2. Az első 'max_results' link tartalmának letöltése
        for url in links[:max_results]:
            # Késleltetés a weboldalak letöltése között, hogy ne legyünk túl agresszívak
            time.sleep(random.uniform(0.5, 1.5))
            content_data = fetch_content_snippet(url)
            results_with_content.append(content_data)

        return jsonify(results_with_content), 200

    except Exception as e:
        # Általános hiba
        return jsonify({"error": f"Belső szerver hiba a DDG keresés során: {str(e)}"}), 500


# ==============================================================================
# Eredeti Ollama Proxy Útvonalak
# ==============================================================================

@app.route('/api/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy(path):
    """Proxy az Ollama API felé"""
    url = f"{OLLAMA_URL}/api/{path}"
    
    if request.method == 'POST':
        def generate():
            with requests.post(
                url, 
                json=request.get_json(),
                stream=True,
                headers={'Content-Type': 'application/json'}
            ) as resp:
                for chunk in resp.iter_content(chunk_size=1024):
                    if chunk:
                        yield chunk
        
        return Response(
            stream_with_context(generate()),
            content_type='application/x-ndjson'
        )
    
    elif request.method == 'GET':
        resp = requests.get(url)
        return Response(resp.content, content_type=resp.headers.get('content-type'))
    
    return Response("Method not allowed", status=405)

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 Ollama CORS Proxy szerver indítása...")
    print("=" * 60)
    print("✓ Proxy elérhető: http://localhost:5000")
    print("✓ Ollama API: http://localhost:11434")
    print("✓ ÚJ útvonal: http://localhost:5000/api/duckduckgo")
    print("=" * 60)
    print("Kötelező csomagok: pip install flask flask-cors requests beautifulsoup4")
    print("=" * 60)
    app.run(host='0.0.0.0', port=5000, debug=False)
