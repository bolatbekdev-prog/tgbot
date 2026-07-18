import asyncio
import datetime
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, F, types
from aiogram.types import BufferedInputFile
from aiogram.filters import Command, StateFilter
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from telethon import TelegramClient
from openpyxl import Workbook

# Load environment variables
load_dotenv()

# --- SOZLAMALAR ---
SESSION_PATH = os.getenv('SESSION_PATH', 'bot_session')
TOKEN = os.getenv('TOKEN')
API_ID = int(os.getenv('API_ID'))
API_HASH = os.getenv('API_HASH')

# Parse multiple admin IDs (comma-separated)
admin_ids_str = os.getenv('ADMIN_ID', '0')
ADMIN_IDS = []
if admin_ids_str and admin_ids_str != 'your_admin_id_here':
    try:
        ADMIN_IDS = [int(id.strip()) for id in admin_ids_str.split(',') if id.strip().isdigit()]
    except:
        ADMIN_IDS = []

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())
client = TelegramClient(SESSION_PATH, API_ID, API_HASH)

# BAZA
KOTIBIYAT_DB = {
    "Nukus shahri": ["https://t.me/nokisdeputat"],
    "Amudaryo": ["https://t.me/AmudaryoKengash"],
    "Beruniy": ["https://t.me/kengashberuniy"],
    "Bo'zatov": ["https://t.me/BozatawrayonliqKenesi"],
    "Kegayli": ["@kegeylideputat"],
    "Qorao'zak": ["https://t.me/xdrk_qaraozek"],
    "Qanliko'l": ["https://t.me/kanlikul_deputatlar_kenesi_2019"],
    "Qo'ng'irot": ["https://t.me/Kungraddeputat"],
    "Mo'ynoq": ["https://t.me/moynaqdeputatlarikenesi"],
    "Nukus tumani": ["https://t.me/Nukus_tuman_Kengashi"],
    "Taxtako'pir": ["https://t.me/taxta_kengash"],
    "Taxiatosh": ["https://t.me/TaxiatoshtumanKengashi"],
    "To'rtko'l": ["https://t.me/kotibiyat_turtkul"],
    "Xo'jayli": ["https://t.me/kotibiyat_xodjeyli"],
    "Chimboy": ["https://t.me/Sh_sekretariat"],
    "Shumanay": ["https://t.me/ShumanaytumaniKengashi"],
    "Ellikqal'a": ["https://t.me/ellikqala_Kengashi"]
}

HOKIMIYAT_DB = {
    "Shumanay tumani": ["https://t.me/Shomanay_rayon"],
    "To'rtko'l tumani": ["https://t.me/turtkulhokim_uz"],
    "Qo'ng'irot tumani": ["https://t.me/qongiratrkuz"],
    "Taxiatosh tumani": ["https://t.me/pressTaqiyatas"],
    "Beruniy tumani": ["https://t.me/beruniy_news"],
    "Qorao'zak tumani": ["https://t.me/QaraozekHakimligi"],
    "Bo'zatov tumani": ["https://t.me/bozataw_uz"],
    "Taxtako'pir tumani": ["https://t.me/Taxtakopir_press"],
    "Qanliko'l tumani": ["https://t.me/kanlikulnews"],
    "Nukus tumani (Oqmang'it)": ["https://t.me/Aqmangituz"],
    "Kegeyli tumani": ["https://t.me/kegeylirkuzofficial"],
    "Chimboy tumani": ["https://t.me/shimbayrk"],
    "Ellikqal'a tumani": ["https://t.me/ellikqala1977"],
    "Xo'jayli tumani": ["https://t.me/xodjeyli_rk"],
    "Amudaryo tumani": ["https://t.me/press_Amuwdarya"],
    "Mo'ynoq tumani": ["https://t.me/MuynakPress"],
    "Nukus shahri": ["https://t.me/nukus_pressa"]
}

# --- HANDLERLAR ---
def is_admin(user_id):
    """Check if user is admin"""
    if not ADMIN_IDS:
        return False  # Deny all if no admins are set
    return user_id in ADMIN_IDS

def extract_context(text, query, max_length=300):
    """Extract the context around the found query word"""
    query_lower = query.lower()
    text_lower = text.lower()
    
    # Find the position of the query
    pos = text_lower.find(query_lower)
    if pos == -1:
        return text[:max_length]
    
    # Calculate start and end positions to extract context
    start = max(0, pos - 100)
    end = min(len(text), pos + len(query) + 100)
    
    context = text[start:end]
    
    # Add ellipsis if we cut from beginning or end
    if start > 0:
        context = "..." + context
    if end < len(text):
        context = context + "..."
    
    return context

def create_excel_report(results, query, district, ch_type, days):
    wb = Workbook()
    ws = wb.active
    ws.title = "Hisobot"
    
    # Headers
    ws.append(['Sana', 'Kanal', 'Matn (so\'z qatnashgan qismi)', 'Link'])
    
    for result in results:
        date_str = result['date'].strftime('%d.%m.%Y %H:%M')
        channel = result['channel']
        text = extract_context(result['text'], query)
        link = f"https://t.me/{channel[1:]}/{result['id']}"
        ws.append([date_str, channel, text, link])
    
    filename = f"hisobot_{query}_{district}_{ch_type}_{days}kun.xlsx"
    wb.save(filename)
    return filename

def get_main_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏢 Kotibiyat", callback_data="select_kotibiyat")],
        [InlineKeyboardButton(text="🏛 Hokimiyat", callback_data="select_hokimiyat")],
        [InlineKeyboardButton(text="➕ Yangi kanal qo'shish", callback_data="add_ch")]
    ])

@dp.message(Command("start"))
async def start(msg: types.Message):
    if not is_admin(msg.from_user.id):
        await msg.answer("❌ Sizda bu botdan foydalanish huquqi yo'q!")
        return
    await msg.answer("👋 Monitoring tizimiga xush kelibsiz!", reply_markup=get_main_menu())

@dp.callback_query(F.data == "back_to_menu")
async def back_menu(call: types.CallbackQuery, state: FSMContext):
    if not is_admin(call.from_user.id):
        await call.answer("❌ Sizda bu botdan foydalanish huquqi yo'q!")
        return
    await state.clear()
    await call.message.edit_text("👋 Asosiy menyu:", reply_markup=get_main_menu())

@dp.callback_query(F.data == "select_kotibiyat")
async def select_kotibiyat(call: types.CallbackQuery, state: FSMContext):
    if not is_admin(call.from_user.id):
        await call.answer("❌ Sizda bu botdan foydalanish huquqi yo'q!")
        return
    await state.update_data(db_type="kotibiyat")
    kb = [[InlineKeyboardButton(text=t, callback_data=f"dist_{t}")] for t in KOTIBIYAT_DB.keys()]
    kb.append([InlineKeyboardButton(text="🏠 Menu", callback_data="back_to_menu")])
    await call.message.edit_text("📍 Tumanni tanlang (Kotibiyat):", reply_markup=InlineKeyboardMarkup(inline_keyboard=kb))

@dp.callback_query(F.data == "select_hokimiyat")
async def select_hokimiyat(call: types.CallbackQuery, state: FSMContext):
    if not is_admin(call.from_user.id):
        await call.answer("❌ Sizda bu botdan foydalanish huquqi yo'q!")
        return
    await state.update_data(db_type="hokimiyat")
    kb = [[InlineKeyboardButton(text=t, callback_data=f"dist_{t}")] for t in HOKIMIYAT_DB.keys()]
    kb.append([InlineKeyboardButton(text="🏠 Menu", callback_data="back_to_menu")])
    await call.message.edit_text("📍 Tumanni tanlang (Hokimiyat):", reply_markup=InlineKeyboardMarkup(inline_keyboard=kb))

@dp.callback_query(F.data.startswith("dist_"))
async def choose_duration(call: types.CallbackQuery, state: FSMContext):
    if not is_admin(call.from_user.id):
        await call.answer("❌ Sizda bu botdan foydalanish huquqi yo'q!")
        return
    district = call.data.replace("dist_", "")
    data = await state.get_data()
    db_type = data.get('db_type', 'kotibiyat')
    
    # Select appropriate database
    db = KOTIBIYAT_DB if db_type == "kotibiyat" else HOKIMIYAT_DB
    
    # Check if district exists in database
    if district not in db:
        await call.answer("❌ Tuman topilmadi!")
        return
    
    # Get channel link
    channel_link = db[district][0]
    
    # Convert https://t.me/username to @username format if needed
    if channel_link.startswith("https://t.me/"):
        channel_link = "@" + channel_link.replace("https://t.me/", "")
    
    ch_type = "Kotibiyat" if db_type == "kotibiyat" else "Hokimiyat"
    await state.update_data(district=district, channel=channel_link, ch_type=ch_type)
    await call.message.edit_text(f"✅ {district} ({ch_type}) tanlandi. Qidiruv muddatini tanlang:", reply_markup=InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⏳ 24 soat", callback_data="dur_1")],
        [InlineKeyboardButton(text="⏳ 7 kun", callback_data="dur_7")],
        [InlineKeyboardButton(text="🏠 Menu", callback_data="back_to_menu")]
    ]))

@dp.callback_query(F.data.startswith("dur_"))
async def set_duration(call: types.CallbackQuery, state: FSMContext):
    if not is_admin(call.from_user.id):
        await call.answer("❌ Sizda bu botdan foydalanish huquqi yo'q!")
        return
    days = int(call.data.split("_")[1])
    await state.update_data(days=days)
    await state.set_state("waiting_for_query")
    await call.message.edit_text(f"✅ {days} kunlik rejim. Qidiruv so'zini yozing:")

@dp.message(StateFilter("waiting_for_query"))
async def execute_search(msg: types.Message, state: FSMContext):
    if not is_admin(msg.from_user.id):
        await msg.answer("❌ Sizda bu botdan foydalanish huquqi yo'q!")
        await state.clear()
        return
    data = await state.get_data()
    ch_link = data['channel']
    days = data.get('days', 1)
    district = data.get('district', '')
    ch_type = data.get('ch_type', 'Noma\'lum')
    query = msg.text
    
    await msg.answer(f"⏳ Qidirilmoqda...")
    limit_date = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=days)
    
    try:
        results = []
        async for m in client.iter_messages(ch_link, limit=100):
            if m.date < limit_date: break
            if m.text and query.lower() in m.text.lower():
                results.append({
                    'date': m.date,
                    'channel': ch_link,
                    'text': m.text,
                    'id': m.id
                })
        
        if results:
            await msg.answer(f"✅ {len(results)} ta natija topildi. Excel hisobot tayyorlanmoqda...")
            
            # Create Excel report
            filename = create_excel_report(results, query, district, ch_type, days)
            
            # Send Excel report
            try:
                with open(filename, 'rb') as f:
                    file_content = f.read()
                buffered_file = BufferedInputFile(file_content, filename=f"hisobot_{query}_{district}_{ch_type}_{days}kun.xlsx")
                caption = f"📊 Hisobot: {query} - {district} ({ch_type}) - {days} kun\nTopilgan: {len(results)} ta"
                
                # Send to all admins
                for admin_id in ADMIN_IDS:
                    try:
                        await bot.send_document(admin_id, buffered_file, caption=caption)
                    except Exception as e:
                        print(f"Failed to send to admin {admin_id}: {e}")
                
                await msg.answer("✅ Hisobot adminga yuborildi!")
            except Exception as e:
                await msg.answer(f"❌ Hisobot yuborishda xatolik: {e}")
            
            # Clean up
            os.remove(filename)
        else:
            await msg.answer("❌ Natija topilmadi.")
    except Exception as e:
        await msg.answer(f"❌ Kanalga ulanishda xatolik yoki so'z topilmadi: {str(e)}")
    
    await msg.answer("🏠 Keyingi amal:", reply_markup=get_main_menu())
    await state.clear()

@dp.callback_query(F.data == "add_ch")
async def add_channel_start(call: types.CallbackQuery, state: FSMContext):
    if not is_admin(call.from_user.id):
        await call.answer("❌ Sizda bu botdan foydalanish huquqi yo'q!")
        return
    await call.message.edit_text("Yangi kanal nomini yozing:")
    await state.set_state("waiting_for_new_name")

@dp.message(StateFilter("waiting_for_new_name"))
async def add_channel_link(msg: types.Message, state: FSMContext):
    if not is_admin(msg.from_user.id):
        await msg.answer("❌ Sizda bu botdan foydalanish huquqi yo'q!")
        await state.clear()
        return
    await state.update_data(new_name=msg.text)
    await msg.answer("Kanal linkini (@...) yozing:")
    await state.set_state("waiting_for_new_link")

@dp.message(StateFilter("waiting_for_new_link"))
async def save_channel(msg: types.Message, state: FSMContext):
    if not is_admin(msg.from_user.id):
        await msg.answer("❌ Sizda bu botdan foydalanish huquqi yo'q!")
        await state.clear()
        return
    data = await state.get_data()
    # Add to both databases for simplicity (can be customized)
    KOTIBIYAT_DB[data['new_name']] = [msg.text]
    await msg.answer("✅ Kanal qo'shildi!", reply_markup=get_main_menu())
    await state.clear()

async def main():
    await client.start()
    print("✅ Bot muvaffaqiyatli ishga tushdi!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
