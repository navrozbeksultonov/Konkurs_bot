from django.shortcuts import render
from referer.Buttons import Button, inline_btns
from referer.models import *
from referer.tgadmin import TGAdmin, rek_rasm, rek_video


def my_decorator_func(func):
    def wrapper_func(update, context):
        user_id = update.message.from_user.id
        my_channel_id = ['@fintechhubuz']
        statuss = ['creator', 'administrator', 'member']
        referer_id = None
        start_com = update.message.text
        try:
            a = start_com.split()
        except:
            a = []
        if len(a) > 1:
            referer_id = a[1]
        for j in my_channel_id:
            for i in statuss:
                if i == context.bot.get_chat_member(chat_id=j, user_id=user_id).status:
                    break
            else:
                s = f"<a href='https://t.me/texnakonkurs_bot?start={referer_id}'>/start</a>" if referer_id else "/start"
                context.bot.send_message(user_id,
                                         f"Assalomu Alaykum FintechHub 👨🏻‍💻\n\nQuydagi kanalarga obuna bo'ling va 👉 {s} bosing",
                                         reply_markup=inline_btns("reklama"),
                                         parse_mode="HTML",

                                         )
                return False
        func(update, context)

    return wrapper_func


@my_decorator_func
def start(update, context):
    start_com = update.message.text

    a = start_com.split()

    user = update.message.from_user
    tglog = Log.objects.filter(user_id=user.id).first()
    tg_user = TgUser.objects.filter(user_id=user.id).first()
    referer_id = None
    if len(a) > 1:
        referer_id = a[1]
    if not tglog:
        tglog = Log()
        tglog.user_id = user.id

        tglog.save()
    log = tglog.message
    print(log, f"a{referer_id}a", type(referer_id))

    if not tg_user:
        tg_user = TgUser()
        tg_user.user_id = user.id
        tg_user.user_name = user.username
        tg_user.first_name = user.first_name
        tg_user.refer_id = referer_id
        tg_user.save()
        log['state'] = 1
        update.message.reply_text('Ассалому алейкум исмингизни киритинг 😃')

        if referer_id:
            ref_friend = TgUser.objects.get(user_id=int(referer_id))
            ref_friend.odam = ref_friend.odam + 1
            ref_friend.ball = ref_friend.ball + 5
            ref_friend.save()
            context.bot.send_message(text=f"Sizga yangi odam qo'shildi {user.first_name}", chat_id=ref_friend.user_id)

            log['refer_id'] = referer_id
            tg_user.refer_id = referer_id

        tglog.message = log
        tglog.save()

        return 0

    print(log)
    update.message.reply_text('Куйидаги  менюдан керакли бўлимни танланг 👇', reply_markup=Button('menu'))

    if tg_user.menu == 1:
        log.clear()
        log['admin_state'] = 1
        tglog.messages = log
        tglog.save()
        TGAdmin(update, context)
        return 0

    tg_user.menu_log = 0
    tg_user.save()
    log.clear()
    log['state'] = 0
    tglog.messages = log
    tglog.save()

    tglog.message = log
    tglog.save()


@my_decorator_func
def photo_handler(update, context):
    user = update.message.from_user
    tg_user = TgUser.objects.filter(user_id=user.id).first()
    tglog = Log.objects.filter(user_id=user.id).first()
    log = tglog.message
    state = log.get('state', 0)
    astate = log.get('admin_state', 0)
    if astate == 100:
        rek_rasm(update, context)
        return 0


@my_decorator_func
def video_handler(update, context):
    user = update.message.from_user
    video = update.message.video
    tg_user = TgUser.objects.filter(user_id=user.id).first()
    print(update.message.message_id, user.id)
    tglog = Log.objects.filter(user_id=user.id).first()
    log = tglog.message
    state = log.get('state', 0)
    astate = log.get('admin_state', 0)
    if astate == 100:
        rek_video(update, context)
        return 0


@my_decorator_func
def message_handler(update, context, ball=0, odam=None):
    user = update.message.from_user
    msg = update.message.text
    referer_id = None
    tglog = Log.objects.filter(user_id=user.id).first()
    tguser = TgUser.objects.filter(user_id=user.id).first()
    log = tglog.message

    if tguser.menu == 1:
        TGAdmin(update, context)
        return 0

    if msg == "/adm1NF1nTech6000":
        update.message.reply_text('Parolni kiriting')
        log['admin_state'] = 0
        tglog.message = log
        tglog.save()
        return 0

    if log.get('admin_state') == 0:
        if msg == "enigma6000":
            tguser.menu = 1
            tguser.save()
            log.clear()
            log['admin_state'] = 1
            tglog.message = log
            tglog.save()
            # update.message.reply_text("Admin bo'limiga xush kelibsiz")
            TGAdmin(update, context)
            return 0
        else:
            update.message.reply_text("Parolni notog'ri kiridingiz")
            return 0

    if log['state'] == 1:
        log['state'] = 3
        log['name'] = msg
        update.message.reply_text("Телефон ракамингизни юбориш учун пастдаги 'Ракамни юбориш 📲' тугмасини босинг",
                                  reply_markup=Button(type='contact'))

    if msg == "🎁 ТАНЛОВДА ИШТИРОК ЭТИШ":
        update.message.reply_text("Балл тўплаш учун сизга бериладиган реферал (махсус) линк орқали одам таклиф "
                                  "қилишингиз керак бўлади. Таклиф этилган ҳар бир одам учун 5 балл берилади",
                                  reply_markup=inline_btns("referal"))

    if msg == "📝 Шартлар":
        update.message.reply_text("ТАНЛОВ ШАРТЛАРИ:\n\n"
                                  "❗️Ушбу танловда 10та ғолиблар тўплаган балларига қараб аниқланади.\n\n"
                                  "Баллар қандай тўпланади?\n\nБОТда келтирилган 2 та каналга обуна бўлгач,"
                                  "Аъзо бўлдим тугмасини босишингиз билан, сизга махсус реферал линк (ҳавола) берилади."
                                  " Ўша линк орқали обуна бўлган ҳар бир инсон учун сизга 5 баллдан бериб борилади. Қанча кўп балл йиғсангиз,"
                                  " ғолиб бўлиш имкониятингиз шунча ортиб боради.\n\n"
                                  "⌛️ Танлов 31 декабрь куни 23:59да якунланади.\n\n"
                                  "❗️Диққат! Сунъий (ўлик аккаунтлар қўшган) накрутка ва х.к. лардан фойдаланганлар танловдан четлаштирилади!\n\n"
                                  "🚚 Танлов сўнгида совринлар Ўзбекисто бўйича почта орқали БЕПУЛ етказиб берилади.\n\n"
                                  "😀 Фаол бўлинг ва совринлардан бирини ютиб олинг. Барчага омад!\n\n")

    elif msg == "Менинг топлаган балларим 💳":
        odam = TgUser.objects.get(user_id=user.id)
        update.message.reply_text(f"Сиз {odam.odam} та одам чакиргансиз🗣\nУмумий балингиз {odam.ball} 💸")

        tglog.message = log
        tglog.save()
        return 0

    elif msg == "📊 Рейтинг":
        s = "📊 Ботимизга энг кўп дўстини таклиф қилиб балл тўплаганлар рўйҳати:\n\n"
        top10 = TgUser.objects.all().order_by('-ball')[:10]
        for i, j in zip(range(1, len(top10)), top10):
            s += f"{i} - {j.first_name} - {j.ball} балл💸\n"

        s += "‼Накрутка қилганлар, пуллик спамлардан, 🔞 ахлоқсиз каналлларда спам тарқатганлар конкурсдан четлаштирилади. ‼️"

        update.message.reply_text(s)
    tglog.message = log
    tglog.save()


@my_decorator_func
def contact_handler(update, context):
    contact = update.message.contact
    user = update.message.from_user
    tg_user = TgUser.objects.filter(user_id=user.id).first()
    tglog = Log.objects.filter(user_id=user.id).first()
    log = tglog.message
    if log['state'] == 3:
        log['phone'] = contact.phone_number
        tg_user.name = log['name']

        tg_user.phone_number = log['phone']
        tg_user.save()
        log.clear()
        log['state'] = 9
        print('g')
        update.message.reply_text('"IT Masters" ҳамда "Excel Hacks"\n'
                                  'хамкорлигида ташкил этилган техно\n'
                                  'конкурсда иштирок этинг ва қуйидаги\n'
                                  'совринлардан бирини ютиб олинг!\n\n'
                                  '🥇 1-ўрин: RGB Gaming Combo 4 in 1\n'
                                  ' (Клавиатура, сичқонча, қулоқчинлар ва коврик)\n'
                                  '🥈 2-ўрин: UzBrand ноутбук сумкаси ва клавиатура.\n'
                                  '🥉 3-ўрин: Freemotion B525 Wireless қулоқчинлари.\n\n'
                                  '4-ўрин: Game коврик 30X80 ва К200 колонкалар.\n'
                                  '5-ўрин: К200 колонкалар ва сичқонча.\n'
                                  '6-ўрин: 16 Gb USB 3.0 флешка ва сичқонча\n'
                                  '7-ўрин: USB hub ва сичқонча.\n'
                                  '8-ўрин: 8 Gb ли флешка ва сичқонча\n'
                                  '9-ўрин: Gaming Mouse M160.\n'
                                  '10-ўрин: 16 Gb ли Hikvision M200S USB 3.0 флешка.\n\n'
                                  '⏱ Танлов 31 Декабрь 23:59 гача давом этади.')

        update.message.reply_text(
            "Табриклаймиз сиз муваффакийатли ройхатдан отдингиз 🫶\n"
            "Куйидаги «Танловда иштирок этиш» бўлимини танланг 👇 👇", reply_markup=Button("menu"))

    tglog.message = log
    tglog.save()


def callback_handler(update, context, kwargs=None):
    query = update.callback_query
    data = query.data
    user = query.from_user
    tglog = Log.objects.filter(user_id=user.id).first()
    tg_user = TgUser.objects.filter(user_id=user.id).first()
    log = tglog.message

    if data == "refr":
        log['state'] = 20
        query.message.reply_text("Энг сара 10 та совринлардан бирини ютиб олишни истайсизми?\nУнда «IT Masters» ҳамда "
                                 "«Excel Hacks» ҳамкорлигида ташкил этилган танловда қатнашиб, омадингизни синаб кўринг!\n\n"
                                 f"Танловда иштирок этиш учун 👇\nhttps://t.me/texnakonkurs_bot?start={user.id}")

        tglog.message = log
        tglog.save()
