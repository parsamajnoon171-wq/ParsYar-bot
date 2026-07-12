import os
import jdatetime
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# ========== تاریخ شمسی ==========
async def today(update: Update, context: ContextTypes.DEFAULT_TYPE):
    now = jdatetime.datetime.now()
    days = ["شنبه", "یکشنبه", "دوشنبه", "سه‌شنبه", "چهارشنبه", "پنجشنبه", "جمعه"]
    months = ["فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور", "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"]
    
    msg = (
        f"📆 {days[now.weekday()]} {now.day} {months[now.month-1]} {now.year}\n"
        f"🕐 ساعت: {now.hour:02d}:{now.minute:02d}"
    )
    await update.message.reply_text(msg)

# ========== آب و هوا ==========
async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        city = " ".join(context.args)
    else:
        city = "تهران"
    
    await update.message.reply_text(f"🔄 در حال دریافت آب و هوای {city}...")
    
    try:
        url = f"https://wttr.in/{city}?format=%C+%t+%w+%h&lang=fa"
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url, headers=headers, timeout=10)
        
        if res.status_code == 200 and res.text:
            data = res.text.strip()
            temp_parts = data.split()
            condition = temp_parts[0] if len(temp_parts) > 0 else "نامشخص"
            temp = temp_parts[1] if len(temp_parts) > 1 else "نامشخص"
            wind = temp_parts[2] if len(temp_parts) > 2 else "نامشخص"
            humidity = temp_parts[3] if len(temp_parts) > 3 else "نامشخص"
            
            msg = (
                f"🌤 **آب و هوای {city}**\n\n"
                f"☁️ وضعیت: {condition}\n"
                f"🌡 دما: {temp}\n"
                f"💨 باد: {wind}\n"
                f"💧 رطوبت: {humidity}%\n\n"
                "📌 برای شهر دیگه: /weather [نام شهر]"
            )
        else:
            msg = "❌ شهری با این نام پیدا نشد."
            
    except Exception as e:
        msg = "❌ نتونستم آب و هوا رو دریافت کنم."
    
    await update.message.reply_text(msg)

# ========== قیمت طلا و سکه و دلار ==========
async def prices(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔄 در حال دریافت قیمت‌ها...")
    
    try:
        url = "https://www.tala.ir/"
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url, headers=headers, timeout=10)
        res.encoding = "utf-8"
        
        dollar_url = "https://www.tgju.org/"
        dollar_res = requests.get(dollar_url, headers=headers, timeout=10)
        dollar_res.encoding = "utf-8"
        
        from bs4 import BeautifulSoup
        
        soup = BeautifulSoup(res.text, "html.parser")
        dollar_soup = BeautifulSoup(dollar_res.text, "html.parser")
        
        gold_price = "نامشخص"
        coin_price = "نامشخص"
        dollar_price = "نامشخص"
        
        gold_spans = soup.find_all("span", class_="price")
        if gold_spans and len(gold_spans) > 0:
            gold_price = gold_spans[0].text.strip()
        if gold_spans and len(gold_spans) > 1:
            coin_price = gold_spans[1].text.strip()
        
        dollar_spans = dollar_soup.find_all("span", class_="price")
        if dollar_spans and len(dollar_spans) > 0:
            dollar_price = dollar_spans[0].text.strip()
        
        msg = (
            "💰 **قیمت‌های امروز - پارس‌یار**\n\n"
            f"🇺🇸 دلار: {dollar_price} تومان\n"
            f"🥇 طلا ۱۸ عیار: {gold_price} تومان\n"
            f"🪙 سکه امامی: {coin_price} تومان\n\n"
            "⚠️ قیمت‌ها لحظه‌ای و تقریبی هستن"
        )
        
    except Exception as e:
        msg = "❌ نتونستم قیمت‌ها رو دریافت کنم."
    
    await update.message.reply_text(msg)

# ========== اخبار روز ==========
async def news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔄 در حال دریافت آخرین اخبار...")
    
    try:
        url = "https://www.varzesh3.com/"
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url, headers=headers, timeout=10)
        res.encoding = "utf-8"
        
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(res.text, "html.parser")
        
        news_items = soup.find_all("h2", class_="title")
        
        msg = "📰 **آخرین اخبار - پارس‌یار**\n\n"
        count = 0
        for item in news_items:
            if count >= 5:
                break
            title = item.text.strip()
            if title:
                msg += f"🔹 {title}\n\n"
                count += 1
        
        if count == 0:
            msg = "❌ خبری پیدا نشد."
        
    except Exception as e:
        msg = "❌ نتونستم اخبار رو دریافت کنم."
    
    await update.message.reply_text(msg)

# ========== همه اطلاعات یکجا ==========
async def all_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔄 در حال دریافت همه اطلاعات...")
    
    now = jdatetime.datetime.now()
    days = ["شنبه", "یکشنبه", "دوشنبه", "سه‌شنبه", "چهارشنبه", "پنجشنبه", "جمعه"]
    months = ["فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور", "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"]
    
    date_msg = f"📆 {days[now.weekday()]} {now.day} {months[now.month-1]} {now.year}\n🕐 {now.hour:02d}:{now.minute:02d}"
    
    try:
        url = "https://www.tala.ir/"
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url, headers=headers, timeout=10)
        res.encoding = "utf-8"
        
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(res.text, "html.parser")
        gold_spans = soup.find_all("span", class_="price")
        
        gold_price = gold_spans[0].text.strip() if gold_spans and len(gold_spans) > 0 else "نامشخص"
        coin_price = gold_spans[1].text.strip() if gold_spans and len(gold_spans) > 1 else "نامشخص"
        
        price_msg = f"🥇 طلا: {gold_price}\n🪙 سکه: {coin_price}"
    except:
        price_msg = "❌ قیمت‌ها در دسترس نیست"
    
    final_msg = (
        f"🦁 **پارس‌یار** - همه اطلاعات\n\n"
        f"{date_msg}\n\n"
        f"💰 {price_msg}\n\n"
        "برای اطلاعات بیشتر:\n"
        "/today - تاریخ\n"
        "/weather - آب و هوا\n"
        "/prices - قیمت‌ها\n"
        "/news - اخبار"
    )
    
    await update.message.reply_text(final_msg)

# ========== استارت ==========
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🦁 **به ربات پارس‌یار خوش اومدی!**\n\n"
        "دستورات:\n"
        "📆 /today - تاریخ امروز\n"
        "🌤 /weather [شهر] - آب و هوا\n"
        "💰 /prices - قیمت دلار، طلا و سکه\n"
        "📰 /news - آخرین اخبار\n"
        "📊 /all - همه اطلاعات یکجا\n"
        "❓ /help - راهنما"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🦁 **راهنمای پارس‌یار**\n\n"
        "/today - تاریخ و ساعت امروز\n"
        "/weather [نام شهر] - آب و هوای شهر مورد نظر\n"
        "/prices - قیمت لحظه‌ای طلا، سکه و دلار\n"
        "/news - ۵ خبر آخر\n"
        "/all - همه اطلاعات یکجا\n\n"
        "🌤 مثال آب و هوا: /weather شیراز\n"
        "⚠️ قیمت‌ها تقریبی و از سایت‌های عمومی گرفته می‌شن"
    )

def main():
    TOKEN = os.environ.get("BOT_TOKEN")
    
    if not TOKEN:
        print("❌ توکن ربات تنظیم نشده!")
        return
    
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("today", today))
    app.add_handler(CommandHandler("weather", weather))
    app.add_handler(CommandHandler("prices", prices))
    app.add_handler(CommandHandler("news", news))
    app.add_handler(CommandHandler("all", all_info))
    
    print("🦁 ربات پارس‌یار روشن شد ✅")
    app.run_polling()

if __name__ == "__main__":
    main()
