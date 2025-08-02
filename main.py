import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp

TOKEN = os.getenv("8243519661:AAHEuJUoQL0ZqsZJEeMKxVadKKdtwKar5a8")  # Token diambil dari environment variable

# Command /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Halo! 👋\n"
        "Kirim link YouTube ke saya dan saya akan unduh videonya untukmu (max 50MB)."
    )

# Fungsi untuk download video
async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()

    if "youtube.com" not in url and "youtu.be" not in url:
        await update.message.reply_text("❌ Link tidak valid. Kirim link YouTube yang benar.")
        return

    await update.message.reply_text("⏳ Sedang mengunduh video, mohon tunggu...")

    try:
        ydl_opts = {
            'format': 'best[filesize<50M]',  # Format terbaik di bawah 50MB
            'outtmpl': 'video.%(ext)s',
            'noplaylist': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)

        # Cek ukuran file
        size_mb = os.path.getsize(file_path) / 1024 / 1024
        if size_mb > 49:
            await update.message.reply_text("❗ Ukuran video melebihi batas upload Telegram (50MB).")
            os.remove(file_path)
            return

        await update.message.reply_video(video=open(file_path, 'rb'))
        os.remove(file_path)

    except Exception as e:
        await update.message.reply_text(f"⚠️ Gagal mengunduh: {str(e)}")

# Jalankan bot
def main():
    if not TOKEN:
        print("❌ BOT_TOKEN belum diatur di environment variable.")
        return

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))
    app.run_polling()

if __name__ == '__main__':
    main()