import os
import threading
import asyncio
from http.server import BaseHTTPRequestHandler, HTTPServer
from bot import start_bot  # 👈 Импортируем функцию запуска из bot.py

# Поток для запуска Telegram-бота
def run_bot():
    asyncio.run(start_bot())

# HTTP-сервер для Render
def fake_web_server():
    class PingHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Bot is running!")

    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), PingHandler)
    server.serve_forever()

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    fake_web_server()
