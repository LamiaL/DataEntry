import webbrowser
import threading
from app import create_app

app = create_app()

# Open the app in a browser
def open_browser():
    webbrowser.open_new("http://localhost:5500")

if __name__ == "__main__":
    threading.Timer(1.5, open_browser).start()
    app.run(host="0.0.0.0", port=5500, debug=True)