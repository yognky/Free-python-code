import telebot
from telebot import types
import requests
from gtts import gTTS
import os
from googletrans import Translator

# Ganti token kamu di sini!
TOKEN = "ISI_TOKEN_KAMU"
bot = telebot.TeleBot(TOKEN)

translator = Translator()

# ===== MENU UTAMA =====
@bot.message_handler(commands=['start', 'menu'])
def kirim_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("🌤 Cuaca", "📱 Teks ke Suara")
    markup.row("🧮 Kalkulator", "🕌 Jadwal Sholat")
    markup.row("🌐 Translate")
    bot.send_message(message.chat.id, "👋 Selamat datang! Pilih menu di bawah:", reply_markup=markup)

# ===== CUACA =====
@bot.message_handler(func=lambda m: m.text == "🌤 Cuaca")
def fitur_cuaca(message):
    msg = bot.send_message(message.chat.id, "Masukkan nama kota:")
    bot.register_next_step_handler(msg, proses_cuaca)

def proses_cuaca(message):
    kota = message.text
    api_key = "ISI_API_KEY_CUACA"  # Dapatkan dari openweathermap.org
    url = f"http://api.openweathermap.org/data/2.5/weather?q={kota}&appid={api_key}&lang=id&units=metric"
    res = requests.get(url).json()
    if res.get("cod") != 200:
        bot.send_message(message.chat.id, "Kota tidak ditemukan.")
        return

    info = res["weather"][0]["description"]
    suhu = res["main"]["temp"]
    bot.send_message(message.chat.id, f"Cuaca di {kota}:\n🌤 {info}\n🌡 {suhu}°C")

# ===== TEKS KE SUARA =====
@bot.message_handler(func=lambda m: m.text == "📱 Teks ke Suara")
def fitur_tts(message):
    msg = bot.send_message(message.chat.id, "Ketik teks yang ingin diubah jadi suara:")
    bot.register_next_step_handler(msg, proses_tts)

def proses_tts(message):
    teks = message.text
    tts = gTTS(teks, lang='id')
    file = "suara.mp3"
    tts.save(file)
    with open(file, 'rb') as audio:
        bot.send_audio(message.chat.id, audio)
    os.remove(file)

# ===== KALKULATOR =====
@bot.message_handler(func=lambda m: m.text == "🧮 Kalkulator")
def fitur_kalkulator(message):
    msg = bot.send_message(message.chat.id, "Masukkan operasi (misal: 12+3*2):")
    bot.register_next_step_handler(msg, proses_kalkulator)

def proses_kalkulator(message):
    try:
        hasil = eval(message.text)
        bot.send_message(message.chat.id, f"Hasil: {hasil}")
    except:
        bot.send_message(message.chat.id, "Operasi tidak valid.")

# ===== JADWAL SHOLAT =====
@bot.message_handler(func=lambda m: m.text == "🕌 Jadwal Sholat")
def fitur_sholat(message):
    msg = bot.send_message(message.chat.id, "Masukkan nama kota:")
    bot.register_next_step_handler(msg, proses_sholat)

def proses_sholat(message):
    kota = message.text
    url = f"https://api.myquran.com/v1/sholat/jadwal/kota/cari/{kota}"
    res = requests.get(url).json()
    if not res["data"]:
        bot.send_message(message.chat.id, "Kota tidak ditemukan.")
        return
    id_kota = res["data"][0]["id"]

    url_jadwal = f"https://api.myquran.com/v1/sholat/jadwal/{id_kota}/today"
    jadwal = requests.get(url_jadwal).json()["data"]["jadwal"]
    teks = (
        f"🕌 Jadwal Sholat - {kota}\n"
        f"Subuh: {jadwal['subuh']}\n"
        f"Zuhur: {jadwal['dzuhur']}\n"
        f"Ashar: {jadwal['ashar']}\n"
        f"Maghrib: {jadwal['maghrib']}\n"
        f"Isya: {jadwal['isya']}"
    )
    bot.send_message(message.chat.id, teks)

# ===== TRANSLATE =====
@bot.message_handler(func=lambda m: m.text == "🌐 Translate")
def fitur_translate(message):
    msg = bot.send_message(message.chat.id, "Ketik kalimat yang ingin diterjemahkan:")
    bot.register_next_step_handler(msg, proses_translate)

def proses_translate(message):
    hasil = translator.translate(message.text, dest='en')
    bot.send_message(message.chat.id, f"🌐 Terjemahan:\n{hasil.text}")

# ===== DEFAULT (JIKA SALAH MENU) =====
@bot.message_handler(func=lambda m: True)
def fallback(message):
    bot.send_message(message.chat.id, "Silakan pilih dari menu atau ketik /menu untuk melihat pilihan.")

# ===== JALANKAN BOT =====
print("🤖 Bot sedang berjalan...")
bot.infinity_polling()
