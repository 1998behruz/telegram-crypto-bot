import asyncio
import requests
import schedule
import time
from telegram import Bot

# ✅ TOKEN ва ID-и каналатонро гузоред
TOKEN = "7921330837:AAHMiuINHSJADbNXcJm2DrN1kUgKbq_zGEk"
CHANNEL_ID = "@behruz_invest"
  # ID ё username-и канали Telegram

# ✅ API-ключи Binance-и худро дар ин ҷо гузоред
API_KEY = "50brSZidvxOdFpDwpDKebb9MNmzgl8d1cvLfkFa4aklhqjANWJ2Nc51mL6VaqYs8"

bot = Bot(token=TOKEN)

# ✅ Функсия барои гирифтани нархи крипто аз Binance бо API-ключ
def get_crypto_prices_binance():
    headers = {
        "X-MBX-APIKEY": API_KEY
    }
    url = "https://api.binance.com/api/v3/ticker/price"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()

        # Гирифтани нархи криптовалютҳои лозимӣ
        btc_price = next(item for item in data if item["symbol"] == "BTCUSDT")["price"]
        eth_price = next(item for item in data if item["symbol"] == "ETHUSDT")["price"]
        sol_price = next(item for item in data if item["symbol"] == "SOLUSDT")["price"]

        # Форматкунии паём
        message = "📊 Нархи криптовалютҳо аз Binance:\n\n"
        message += f"🔹 *Bitcoin (BTC)*: ${float(btc_price):,.2f}\n"
        message += f"🔹 *Ethereum (ETH)*: ${float(eth_price):,.2f}\n"
        message += f"🔹 *Solana (SOL)*: ${float(sol_price):,.2f}\n"

        return message
    else:
        return "❌ Хато ҳангоми гирифтани нархи криптовалютҳо аз Binance!"

# ✅ Функсия барои ирсоли нархҳо
async def send_crypto_prices():
    try:
        message = get_crypto_prices_binance()
        await bot.send_message(chat_id=CHANNEL_ID, text=message, parse_mode="Markdown")
        print("✅ Нархи криптовалютҳо ба канал фиристода шуд!")
    except Exception as e:
        print(f"❌ Хато ҳангоми фиристодани нархи криптовалютҳо: {e}")

# ✅ Танзими ирсоли автоматӣ
schedule.every().day.at("08:00").do(lambda: asyncio.run(send_crypto_prices()))

# ✅ Функсияи идоракунӣ
def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(60)  # Ҳар 60 сония санҷиш мекунад

if __name__ == "__main__":
    print("🚀 Бот оғоз шуд...")
    run_scheduler()
