from telegram import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup


def Button(type=None, ctg=None):
    btn = []
    # Create your views here.

    if type == 'contact':
        btn = [
            [KeyboardButton('Ракамни юбориш 📲', request_contact=True)]
        ]

    elif type == 'menu':
        btn = [
            [KeyboardButton("🎁 ТАНЛОВДА ИШТИРОК ЭТИШ")],
            [KeyboardButton("📊 Рейтинг"), KeyboardButton("📝 Шартлар")],
            [KeyboardButton("Менинг топлаган балларим 💳")]
        ]

    return ReplyKeyboardMarkup(btn, resize_keyboard=True)


def inline_btns(type=None):
    btn = []
    if type == "reklama":
        btn = [
            [InlineKeyboardButton("FinTech Innovation Hub", callback_data="fintechhubuz",
                                  url="https://t.me/fintechhubuz")],
            # [InlineKeyboardButton("qwertyy’s group🗽", callback_data="qwertysgroup", url="https://t.me/qwertysgroup")],
        ]
    elif type == "referal":
        btn = [
            [InlineKeyboardButton("👤 Одам таклиф килиб балл топлаш ", callback_data="refr")]
        ]

    return InlineKeyboardMarkup(btn)


def admin_btn(type=None):
    btn = []
    if type == "admin_menu":
        btn = [
            [KeyboardButton("Reklama yuborish"), KeyboardButton("Users 👤")],
            [KeyboardButton("Botga qaytish 🏘")]
        ]
    elif type == 'conf':
        btn = [
            [KeyboardButton("Ha"), KeyboardButton("Yo'q")]
        ]

    return ReplyKeyboardMarkup(btn, resize_keyboard=True)
