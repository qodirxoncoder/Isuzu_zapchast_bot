from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy import select, or_
from database.db import AsyncSessionLocal
from database.models import Part

router = Router()

back_btn = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="🔙 Ortga")]],
    resize_keyboard=True
)


class SearchPart(StatesGroup):
    searching = State()

class AddPart(StatesGroup):
    nomi = State()
    narx = State()
    kodi = State()
    model = State()
    kategoriya = State()
    dukonda_nechta = State()
    tavsif = State()


# ───── QIDIRISH ─────

@router.message(F.text == "🔍 Zapchast qidirish")
async def search_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Zapchast nomini, kodini yoki modelini yozing:",
        reply_markup=back_btn
    )
    await state.set_state(SearchPart.searching)


@router.message(SearchPart.searching)
async def search_result(message: Message, state: FSMContext):
    if message.text == "🔙 Ortga":
        from handlers.menu import main_menu
        await state.clear()
        await message.answer("Asosiy menyu:", reply_markup=main_menu)
        return

    query = message.text.strip()

    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Part).where(
                or_(
                    Part.nomi.ilike(f"%{query}%"),
                    Part.kodi.ilike(f"%{query}%"),
                    Part.model.ilike(f"%{query}%"),
                )
            )
        )
        parts = result.scalars().all()

    if not parts:
        await message.answer("❌ Hech narsa topilmadi. Boshqa so'z bilan qidiring:")
        return

    for part in parts:
        text = f"📦 <b>{part.nomi}</b>\n"
        text += f"💰 Narx: <b>{part.narx:,.0f} so'm</b>\n"
        if part.kodi:
            text += f"🔢 Kod: {part.kodi}\n"
        if part.model:
            text += f"🚛 Model: {part.model}\n"
        if part.kategoriya:
            text += f"📁 Kategoriya: {part.kategoriya}\n"
        if part.dukonda_nechta is not None:
            text += f"🏪 Dukonda: {part.dukonda_nechta} ta\n"
        if part.tavsif:
            text += f"📝 Tavsif: {part.tavsif}\n"
        text += f"📅 Qo'shilgan: {part.sana.strftime('%d.%m.%Y')}"

        await message.answer(text, parse_mode="HTML")


# ───── QO'SHISH ─────

@router.message(F.text == "➕ Zapchast qo'shish")
async def add_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Zapchast nomini kiriting:",
        reply_markup=back_btn
    )
    await state.set_state(AddPart.nomi)


@router.message(AddPart.nomi)
async def add_nomi(message: Message, state: FSMContext):
    if message.text == "🔙 Ortga":
        from handlers.menu import main_menu
        await state.clear()
        await message.answer("Asosiy menyu:", reply_markup=main_menu)
        return
    await state.update_data(nomi=message.text.strip())
    await message.answer("Narxini kiriting (faqat raqam, so'mda):")
    await state.set_state(AddPart.narx)


@router.message(AddPart.narx)
async def add_narx(message: Message, state: FSMContext):
    if message.text == "🔙 Ortga":
        from handlers.menu import main_menu
        await state.clear()
        await message.answer("Asosiy menyu:", reply_markup=main_menu)
        return
    try:
        narx = float(message.text.strip().replace(" ", "").replace(",", ""))
    except ValueError:
        await message.answer("❌ Faqat raqam kiriting. Masalan: 150000")
        return
    await state.update_data(narx=narx)
    await message.answer("Zapchast kodini kiriting (ixtiyoriy, o'tkazish uchun — kiriting):")
    await state.set_state(AddPart.kodi)


@router.message(AddPart.kodi)
async def add_kodi(message: Message, state: FSMContext):
    if message.text == "🔙 Ortga":
        from handlers.menu import main_menu
        await state.clear()
        await message.answer("Asosiy menyu:", reply_markup=main_menu)
        return
    await state.update_data(kodi=message.text.strip() if message.text.strip() != "-" else None)
    await message.answer("Isuzu modelini kiriting (ixtiyoriy, o'tkazish uchun — kiriting):")
    await state.set_state(AddPart.model)


@router.message(AddPart.model)
async def add_model(message: Message, state: FSMContext):
    if message.text == "🔙 Ortga":
        from handlers.menu import main_menu
        await state.clear()
        await message.answer("Asosiy menyu:", reply_markup=main_menu)
        return
    await state.update_data(model=message.text.strip() if message.text.strip() != "-" else None)
    await message.answer("Kategoriyani kiriting (ixtiyoriy, o'tkazish uchun — kiriting):")
    await state.set_state(AddPart.kategoriya)


@router.message(AddPart.kategoriya)
async def add_kategoriya(message: Message, state: FSMContext):
    if message.text == "🔙 Ortga":
        from handlers.menu import main_menu
        await state.clear()
        await message.answer("Asosiy menyu:", reply_markup=main_menu)
        return
    await state.update_data(kategoriya=message.text.strip() if message.text.strip() != "-" else None)
    await message.answer("Dukonda nechta borligini kiriting (ixtiyoriy, o'tkazish uchun — kiriting):")
    await state.set_state(AddPart.dukonda_nechta)


@router.message(AddPart.dukonda_nechta)
async def add_dukonda(message: Message, state: FSMContext):
    if message.text == "🔙 Ortga":
        from handlers.menu import main_menu
        await state.clear()
        await message.answer("Asosiy menyu:", reply_markup=main_menu)
        return
    val = message.text.strip()
    if val == "-":
        await state.update_data(dukonda_nechta=None)
    else:
        try:
            await state.update_data(dukonda_nechta=int(val))
        except ValueError:
            await message.answer("❌ Faqat raqam kiriting yoki — yozing:")
            return
    await message.answer("Tavsif kiriting (ixtiyoriy, o'tkazish uchun — kiriting):")
    await state.set_state(AddPart.tavsif)


@router.message(AddPart.tavsif)
async def add_tavsif(message: Message, state: FSMContext):
    if message.text == "🔙 Ortga":
        from handlers.menu import main_menu
        await state.clear()
        await message.answer("Asosiy menyu:", reply_markup=main_menu)
        return

    val = message.text.strip()
    await state.update_data(tavsif=val if val != "-" else None)
    data = await state.get_data()

    async with AsyncSessionLocal() as session:
        part = Part(
            nomi=data["nomi"],
            narx=data["narx"],
            kodi=data.get("kodi"),
            model=data.get("model"),
            kategoriya=data.get("kategoriya"),
            dukonda_nechta=data.get("dukonda_nechta"),
            tavsif=data.get("tavsif"),
        )
        session.add(part)
        await session.commit()

    from handlers.menu import main_menu
    await state.clear()
    await message.answer(
        f"✅ <b>{data['nomi']}</b> muvaffaqiyatli qo'shildi!",
        reply_markup=main_menu,
        parse_mode="HTML"
    )



    # ───── BARCHA ZAPCHASTLAR ─────

class ListPart(StatesGroup):
    browsing = State()


@router.message(F.text == "📋 Barcha zapchastlar")
async def list_parts(message: Message, state: FSMContext):
    await state.clear()
    await state.update_data(page=0)
    await show_page(message, 0)
    await state.set_state(ListPart.browsing)


async def show_page(message: Message, page: int):
    limit = 5
    offset = page * limit

    async with AsyncSessionLocal() as session:
        total_result = await session.execute(select(Part))
        total = len(total_result.scalars().all())

        result = await session.execute(
            select(Part).offset(offset).limit(limit)
        )
        parts = result.scalars().all()

    if not parts:
        await message.answer("❌ Bazada hali zapchast yo'q.")
        return

    text = f"📦 <b>{offset + 1}-{min(offset + limit, total)} / {total} ta zapchast</b>\n\n"

    for i, part in enumerate(parts, start=offset + 1):
        text += f"{i}. <b>{part.nomi}</b> — {part.narx:,.0f} so'm"
        if part.model:
            text += f" | {part.model}"
        if part.kodi:
            text += f" | #{part.kodi}"
        text += "\n"

    nav_buttons = []
    if page > 0:
        nav_buttons.append(KeyboardButton(text="⬅️ Oldingi"))
    if offset + limit < total:
        nav_buttons.append(KeyboardButton(text="➡️ Keyingi"))

    keyboard = ReplyKeyboardMarkup(
        keyboard=[nav_buttons, [KeyboardButton(text="🔙 Ortga")]],
        resize_keyboard=True
    ) if nav_buttons else ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="🔙 Ortga")]],
        resize_keyboard=True
    )

    await message.answer(text, reply_markup=keyboard, parse_mode="HTML")


@router.message(ListPart.browsing)
async def browse_parts(message: Message, state: FSMContext):
    if message.text == "🔙 Ortga":
        from handlers.menu import main_menu
        await state.clear()
        await message.answer("Asosiy menyu:", reply_markup=main_menu)
        return

    data = await state.get_data()
    page = data.get("page", 0)

    if message.text == "➡️ Keyingi":
        page += 1
    elif message.text == "⬅️ Oldingi":
        page -= 1

    await state.update_data(page=page)
    await show_page(message, page)