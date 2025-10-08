
This solution provides a local (or "on-premise") web user interface for Ollama models and includes a Python-based proxy server. This server handles CORS (Cross-Origin Resource Sharing) issues and integrates a DuckDuckGo search functionality, allowing the model to work with real-time information.

🚀 SimpleChat for Ollama - Installation and Usage Guide

Prerequisites

Ensure the following components are installed and running on your system:

    Ollama: The necessary tool for running large language models locally.

        Installation: Follow the official Ollama installation guide.

        Running: Make sure Ollama is running in the background, typically at http://localhost:11434.

    Model: Download and run at least one model with Ollama (e.g., ollama run llama3).

    Python 3: Required to run the proxy server.

    Web Browser: To open the user interface.

1. Environment Setup (Proxy Server)

The attached SimpleChat-Proxy.py file is a Python-based Flask server that is essential for communication between the web interface and Ollama.

1.1. Install Python Dependencies

Open a terminal or command prompt and install the required Python packages:
Bash

pip install flask flask-cors requests beautifulsoup4

1.2. Run the Proxy Server

    Save the contents of the attached SimpleChat-Proxy.py into a file with the exact same name.

    Start the server in the terminal:

Bash

python SimpleChat-Proxy.py

You should see the following message in the terminal:

============================================================
🚀 Ollama CORS Proxy szerver indítása...
============================================================
✓ Proxy elérhető: http://localhost:5000
✓ Ollama API: http://localhost:11434
✓ ÚJ útvonal: http://localhost:5000/api/duckduckgo
============================================================
...

IMPORTANT: Keep this terminal running while you use the browser!

2. Using the Web Interface

2.1. Open the Web Page

    Save the contents of the attached SimpleChatForOllama-en.html into a file with the exact same name.

    Open the saved HTML file in your favorite web browser (e.g., Chrome, Firefox).

2.2. Starting a Chat

💬 Chat Tab

This is the main interface for conversations.
Element	Description
✨ New Chat	Start a new, empty conversation. Be sure to click this if you update the settings.
⏹️ Stop	Stops the model's current response generation.
Last Code Only	If checked, the model's response will only show the last code block, hiding the rest of the text. Useful for programming tasks.
Start DuckDuck	IMPORTANT! If checked, the next message sent will initiate a DuckDuckGo search, and the search results will be included as context in the message before sending it to the model.
📎 Attach File	Allows uploading files such as .txt, .py, .json, .csv, .html, or .md. The file content is included in the model's message for analysis.
➡️ Send	Sends the message to the model. (Also works with the Enter key, Shift+Enter inserts a new line.)

⚙️ Settings Tab

Here you can configure the model's operation and personality.
Setting	Default Value	Description
Model Name	deepseek-v3.1:671b-cloud	Enter the name of the model you have installed and want to run locally with Ollama (e.g., llama3, mistral, etc.).
Model Personality	Detailed description	The System Prompt, which defines the model's behavior, tone, and response rules.

Note: The settings (model name, personality) only take effect when you click the ✨ New Chat button!

📚 History Tab

This tab manages previous conversations, which are stored locally in the browser using the SQLite database.
Button	Description
📄 Export All to HTML	Exports all saved conversations into a single HTML file.
📂 Load	Loads the specific conversation into the Chat tab, allowing you to continue it. The model and system prompt settings are also restored.
📄 Export	Exports the specific conversation into an individual HTML file.
🗑️ Delete	Permanently deletes the conversation from the local database.

2.3. Conversation Flow

    Configuration: Go to the ⚙️ Settings tab and ensure the Model Name is set correctly. If you made changes, go back to the Chat tab and click the ✨ New Chat button.

    Enable Search (optional): If you need up-to-date information for the response, check the Start DuckDuck option before sending your message.

    Send Message: Type your question into the bottom text box and click the ➡️ Send button.

    Response: The model's response will be streamed into the chat window.

    Saving: Every user-assistant pair is automatically saved to the local database once the response is complete.

💡 Useful Information

    Offline Operation: The chat interface (HTML) can run without the proxy, but it will not be able to communicate with Ollama or the search engine.

    Database: Conversations are stored in the browser's Local Storage. If you clear your browser data (especially Local Storage), your saved conversations will be lost.











Ez a megoldás egy helyi (lokális) webes felhasználói felületet biztosít az Ollama modellekhez, és tartalmaz egy Python alapú proxy szervert, ami kezeli a CORS (Cross-Origin Resource Sharing) problémákat és egy DuckDuckGo kereső funkcionalitást is beépít, hogy a modell valós idejű információval dolgozhasson.

🚀 SimpleChat for Ollama - Telepítési és Használati Útmutató

Előfeltételek

Győződjön meg róla, hogy az alábbi komponensek telepítve vannak és futnak a rendszerén:

    Ollama: A nagy nyelvi modellek lokális futtatásához szükséges eszköz.

        Telepítés: Kövesse az Ollama hivatalos telepítési útmutatóját.

        Futtatás: Győződjön meg róla, hogy az Ollama háttérben fut, általában a http://localhost:11434 címen.

    Modell: Töltsön le és futtasson legalább egy modellt az Ollama-val (pl. ollama run llama3).

    Python 3: A proxy szerver futtatásához.

    Webböngésző: A felhasználói felület megnyitásához.

1. A Környezet Előkészítése (Proxy Szerver)

A mellékelt SimpleChat-Proxy.py fájl egy Python alapú Flask szerver, ami nélkülözhetetlen a webes felület és az Ollama közötti kommunikációhoz.

1.1. Python Függőségek Telepítése

Nyisson meg egy terminált vagy parancssort, és telepítse a szükséges Python csomagokat:
Bash

pip install flask flask-cors requests beautifulsoup4

1.2. A Proxy Szerver Futtatása

    Mentse el a mellékelt SimpleChat-Proxy.py tartalmát egy fájlba, pontosan ezen a néven.

    Indítsa el a szervert a terminálban:

Bash

python SimpleChat-Proxy.py

A terminálban a következő üzenetet kell látnia:

============================================================
🚀 Ollama CORS Proxy szerver indítása...
============================================================
✓ Proxy elérhető: http://localhost:5000
✓ Ollama API: http://localhost:11434
✓ ÚJ útvonal: http://localhost:5000/api/duckduckgo
============================================================
...

FONTOS: Hagyja futni ezt a terminált a böngésző használata közben!

2. A Webes Felület Használata

2.1. A Weboldal Megnyitása

    Mentse el a mellékelt SimpleChatForOllama-en.html tartalmát egy fájlba, pontosan ezen a néven.

    Nyissa meg a mentett HTML fájlt a kedvenc webböngészőjében (pl. Chrome, Firefox).

2.2. A Chat Kezdése

💬 Chat Fül

Ez a fő felület a beszélgetésekhez.
Elem	Leírás
✨ New Chat	Új, üres beszélgetés indítása. Mindenképp kattintson rá, ha frissíti a beállításokat.
⏹️ Stop	Megállítja a modell folyamatban lévő válaszát.
Last Code Only	Ha bejelöli, a modell válaszában csak az utolsó kód blokkot mutatja meg, a többi szöveg elrejtve marad. Programozási feladatokhoz hasznos.
Start DuckDuck	FONTOS! Ha bejelöli, a következő elküldött üzenet elindít egy DuckDuckGo keresést, és a keresési eredményeket forrásként beilleszti az üzenetbe, mielőtt elküldené a modellnek.
📎 Attach File	Lehetővé teszi .txt, .py, .json, .csv, .html, .md vagy hasonló fájlok feltöltését. A fájl tartalma bekerül a modell üzenetébe elemzésre.
➡️ Send	Elküldi az üzenetet a modellnek. (Enter billentyűvel is működik, Shift+Enter új sort szúr be.)

⚙️ Settings Fül

Itt állíthatja be a modell működését és személyiségét.
Beállítás	Alapértelmezett Érték	Leírás
Model Name	deepseek-v3.1:671b-cloud	Írja be az Ollama-val helyileg telepített és futtatni kívánt modell nevét (pl. llama3, mistral, stb.).
Model Personality	Részletes leírás	A rendszerutasítás (System Prompt), amely megadja a modell viselkedését, hangnemét és válaszadási szabályait.

Megjegyzés: A beállítások (modellnév, személyiség) csak akkor lépnek életbe, ha rákattint a ✨ New Chat gombra!

📚 History Fül

Ez a fül a korábbi beszélgetéseket kezeli, melyeket a böngészőben, helyileg tárol a SQLite adatbázis segítségével.
Gomb	Leírás
📄 Export All to HTML	Exportálja az összes elmentett beszélgetést egyetlen HTML fájlba.
📂 Load	Betölti az adott beszélgetést a Chat fülre, lehetővé téve a folytatást. A modell és a rendszer prompt beállítások is visszaállnak.
📄 Export	Az adott beszélgetést exportálja egyedi HTML fájlba.
🗑️ Delete	Véglegesen törli a beszélgetést a helyi adatbázisból.

2.3. Beszélgetés Folyamata

    Beállítás: Menjen a ⚙️ Settings fülre, és győződjön meg róla, hogy a Model Name helyesen van beállítva. Ha módosított, menjen vissza a Chat fülre, és kattintson a ✨ New Chat gombra.

    Keresés Engedélyezése (opcionális): Ha friss információra van szüksége a válaszadáshoz, jelölje be a Start DuckDuck opciót az üzenet elküldése előtt.

    Üzenet Küldése: Írja be a kérdését az alsó szövegdobozba, és kattintson a ➡️ Send gombra.

    Válasz: A modell válasza streamelve jelenik meg a chat ablakban.

    Mentés: Minden felhasználói-asszisztens pár automatikusan elmentésre kerül a helyi adatbázisba, amint a válasz elkészült.

💡 Hasznos Tudnivalók

    Offline Működés: A chat felület (HTML) fut a proxy nélkül is, de nem tud kommunikálni az Ollamával vagy a keresővel.

    Adatbázis: A beszélgetéseket a böngésző Local Storage területén tárolja. Ha törli a böngésző adatait (különösen a Local Storage-t), az elmentett beszélgetések elvesznek.

    Fájlméret Limit: A feltölthető fájlok maximális mérete 5 MB.
