import datetime
import os
import re
import sqlite3
import sys
import time
import ConfigForFactory as CFF
import requests
import vk_api
from bs4 import BeautifulSoup
from googletrans import Translator
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import json

chat_id, peer_id, user_id = None, None, 0000
conn = sqlite3.connect('Factory.db')
cur = conn.cursor()
vk_session = vk_api.VkApi(token=str(CFF.token))
vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, str(CFF.group_id))
vk.messages.send(chat_id=14, message='Я родился', random_id=0)
method_course, v = 'https://api.vk.com/method', 5.126


def main():
    global chat_id
    global peer_id
    global user_id
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            text = event.object.text
            lower = text.lower()
            peer_id = event.object.peer_id
            user_id = event.object.from_id
            chat_id = peer_id - 2000000000
            if event.object.peer_id != event.object.from_id:
                print(f'Текст: {event.object.text} ')
                if peer_id != event.object.from_id:
                    event_entry = {'погода': weather, 'коды': cods_for_zoom, 'расписание': rasp,
                                   'команды': send_command, 'каникулы': Kan, 'список': textlist,
                                   'alllang': alllang, 'allrep': allrep}
                    event_entry_admin = {'restart': exit_bot}
                    event_entry_arg = {'delrep': delrep, 'report': report, 'переведи': translate,
                                       'объясни': give_name_word, 'addlang': addlang, 'dellang,': dellang,
                                       'findlang,': findlang}
                    event_entry_gdz = {'англ': eng_parse, 'геометрия': geom_parse, 'русский': rus_parse,
                                       'алгебра': alg_parse, 'немецкий': deu_parse}
                    if lower in event_entry:
                        event_entry[lower]()
                    if lower in event_entry_admin:
                        if isAdmin(user_id):
                            event_entry_admin[lower]()
                    else:
                        text_split = lower.split(' ')
                        text_split_doub = lower.split(': ')
                        if text_split[0] in event_entry_gdz:
                            event_entry_gdz[text_split[0]](lower)
                        if text_split_doub[0] in event_entry_arg:
                            event_entry_arg[text_split_doub[0]](lower)
                    if re.search('сб ', lower):
                        score_counter(lower)

                    if re.search("переведи,", lower):
                        translate(text)

                    if re.search('добавь,', lower):
                        add(lower)

                    if re.search('убери,', lower):
                        rem(lower)

                    if re.search('удали,', lower):
                        kickfull(lower)

                        action = event.obj.get('action', {}).get('type')
                        if action == "chat_invite_user":
                            removelef(event)

                        attachn = event.obj.get('attachments')
                        if attachn:
                            deshifration(event, attachn)
                        else:
                            attachn = event.obj.get('fwd_messages')
                        if attachn:
                            deshifration(event, attachn)


def weather():
    responses = requests.get(f'https://api.gismeteo.net/v2/weather/current/4407/', headers=CFF.headers)
    responsestwoday = requests.get(
        f'https://api.gismeteo.net/v2/weather/forecast/4407/?lang=ru&days=2', headers=CFF.headers)
    Speedwind = responses.json()['response']['wind']['speed']['m_s']
    pressu = responses.json()['response']['pressure']['mm_hg_atm']
    humid = responses.json()['response']['humidity']['percent']
    precip = responses.json()['response']['precipitation']['type']
    temp = responses.json()['response']['temperature']['comfort']['C']
    temptommorn = responsestwoday.json()['response'][12]['temperature']['comfort']['C']
    temptomday = responsestwoday.json()['response'][14]['temperature']['comfort']['C']
    temptomeven = responsestwoday.json()['response'][15]['temperature']['comfort']['C']
    full = responses.json()['response']['description']['full']
    if precip == 0:
        sender(dis_ment=0,
               message=f'Коротко о погоде:\nСкорость ветра - {Speedwind} м/с,\nДавление - {pressu} мм,'
                       f'\nВлажность - {humid}%,\nОсадки - Отсутствуют,\nТемпература: '
                       f'{temp}\nТемпература завтра утром: {temptommorn},\nТемпература завтра днем: '
                       f'{temptomday},\nТемпература завтра вечером: {temptomeven},\n{full}.\nпо данным '
                       f'Gismeteo.')
    elif precip == 1:
        sender(dis_ment=0,
               message=f'Коротко о погоде:\nСкорость ветра - {Speedwind} м/с,\nДавление - {pressu} мм,'
                       f'\nВлажность - {humid}%,\nОсадки - Дождь,\nТемпература: {temp},\nТемпература '
                       f'завтра утром: {temptommorn},\nТемпература завтра днем: {temptomday},'
                       f'\nТемпература завтра вечером: {temptomeven},\n{full}.\nпо данным Gismeteo.')
    elif precip == 2:
        sender(dis_ment=0,
               message=f'Коротко о погоде:\nСкорость ветра - {Speedwind} м/с,\nДавление - {pressu} мм,'
                       f'\nВлажность - {humid}%,\nОсадки - Снег,\nТемпература: {temp},\nТемпература '
                       f'завтра утром: {temptommorn},\nТемпература завтра днем: {temptomday},'
                       f'\nТемпература завтра вечером: {temptomeven},\n{full}.\nпо данным Gismeteo.')

    elif precip == 3:
        sender(dis_ment=0,
               message=f'Коротко о погоде:\nСкорость ветра - {Speedwind} м/с,\nДавление - {pressu} мм,'
                       f'\nВлажность - {humid}%,\nОсадки - Смешанные Осадки,\nТемпература: {temp},'
                       f'\n{full}.\nпо данным Gismeteo.')


def geom_parse(lower):
    d = lower.split(' ')
    if len(d) > 1:
        if d[1].isnumeric():
            if 1 <= int(d[1]) <= 86:
                parse(num=d, intn=2, url=f'https://gdz.ru/class-7/geometria/atanasyan-7-9/1-chapter-{int(d[1])}/')
            elif 87 <= int(d[1]) <= 185:
                parse(num=d, intn=2, url=f'https://gdz.ru/class-7/geometria/atanasyan-7-9/2-chapter-{int(d[1])}/')
            elif 186 <= int(d[1]) <= 222:
                parse(num=d, intn=2, url=f'https://gdz.ru/class-7/geometria/atanasyan-7-9/3-chapter-{int(d[1])}/')
            elif 223 <= int(d[1]) <= 362:
                parse(num=d, intn=2, url=f'https://gdz.ru/class-7/geometria/atanasyan-7-9/4-chapter-{int(d[1])}/')
            elif 363 <= int(d[1]) <= 444:
                parse(num=d, intn=2, url=f'https://gdz.ru/class-7/geometria/atanasyan-7-9/5-chapter-{int(d[1])}/')
            elif 445 <= int(d[1]) <= 532:
                parse(num=d, intn=2, url=f'https://gdz.ru/class-7/geometria/atanasyan-7-9/6-chapter-{int(d[1])}/')
            elif 533 <= int(d[1]) <= 630:
                parse(num=d, intn=2, url=f'https://gdz.ru/class-7/geometria/atanasyan-7-9/7-chapter-{int(d[1])}/')
            elif 631 <= int(d[1]) <= 737:
                parse(num=d, intn=2, url=f'https://gdz.ru/class-7/geometria/atanasyan-7-9/8-chapter-{int(d[1])}/')
            elif 738 <= int(d[1]) <= 910:
                parse(num=d, intn=2, url=f'https://gdz.ru/class-7/geometria/atanasyan-7-9/9-chapter-{int(d[1])}/')
            elif 911 <= int(d[1]) <= 1010:
                parse(num=d, intn=2, url=f'https://gdz.ru/class-7/geometria/atanasyan-7-9/10-chapter-{int(d[1])}/')
            elif 1011 <= int(d[1]) <= 1077:
                parse(num=d, intn=2, url=f'https://gdz.ru/class-7/geometria/atanasyan-7-9/11-chapter-{int(d[1])}/')
            elif 1078 <= int(d[1]) <= 1147:
                parse(num=d, intn=2, url=f'https://gdz.ru/class-7/geometria/atanasyan-7-9/12-chapter-{int(d[1])}/')
            elif 1148 <= int(d[1]) <= 1183:
                parse(num=d, intn=2, url=f'https://gdz.ru/class-7/geometria/atanasyan-7-9/13-chapter-{int(d[1])}/')
            elif 1184 <= int(d[1]) <= 1310:
                parse(num=d, intn=2, url=f'https://gdz.ru/class-7/geometria/atanasyan-7-9/14-chapter-{int(d[1])}/')
            elif int(d[1]) > 1310:
                sender(dis_ment=0, message='Такого номера не существует!')


# Перевод #
def translate(text):
    per = text.split(' | ')
    translator = Translator()
    if len(per) == 4:
        cur.execute('select * from Lang where Lang is ?', (per[1],))
        row = cur.fetchall()
        if row is not None:
            cur.execute('select * from Lang where Lang is ?', (per[2],))
            if row is not None:
                result = translator.translate(per[3], src=per[1], dest=per[2])
                sender(dis_ment=0, message=result.text)
            else:
                sender(dis_ment=0, message='Доступные языки - alllang')
        else:
            sender(dis_ment=0, message='Доступные языки - alllang')
    else:
        sender(message='Указаны не все аргументы \n Введи: переведи, | язык с которого переводишь | на который | текст')


# Добавление языка в базу #
def addlang(lower):
    if isAdmin(user_id):
        text = lower.split(', ')
        if len(text) == 3:
            texts = (text[1], text[2])
            cur.execute('insert into Lang values(?, ?)', texts)
            conn.commit()
            sender(message=f'В базу добавлен язык {text[2]} с кратким названием {text[1]}')


# База языков #
def alllang():
    cur.execute("select * from Lang")
    row = cur.fetchall()
    mess = bool(row)
    i = 0
    if mess:
        cur.execute("select * from Lang")
        mess = []
        while i < len(row):
            rows = cur.fetchone()
            mess.append(f'\n[{rows[0]}] {rows[1]}')
            i = i + 1
        sender(dis_ment=0, message='Список языков:')
        sender(dis_ment=0, message=mess)
    else:
        sender(dis_ment=0, message='Языки не обнаружены.')


# Удаление языка из базы #
def dellang(lower):
    if isAdmin(user_id):
        text = lower.split(', ')
        if len(text) == 2:
            cur.execute('DELETE FROM Lang WHERE Lang is ?', (text[1],))
            conn.commit()
            sender(dis_ment=0, message=f'Язык {text[1]} был удален')
        else:
            sender(dis_ment=0, message='Введи: dellang, [короткое название языка]')


# Поиск языка по аргументу #
def findlang(lower):
    i = 0
    text = lower.split(', ')
    if len(text) == 2:
        cur.execute('select * from Lang where Fulllang is ?', (text[1],))
        row = cur.fetchone()
        if row is not None:
            sender(dis_ment=0, message=f'Был найден язык {row[1]} с коротким названием [{row[0]}].')
        else:
            cur.execute('select * from Lang where Lang is ?', (text[1],))
            row = cur.fetchone()
            if row is not None:
                sender(message=f'Был найден язык {row[1]} с коротким названием [{row[0]}].')
            else:
                cur.execute('select * from Lang where Fulllang like ?', (f'{text[1]}%',))
                row = cur.fetchall()
                alllanguage = []
                if row is not None:
                    while i < len(row):
                        alllanguage.append(f'\nБыл найден язык {row[i][1]} с коротким названием [{row[i][0]}]')
                        i = i + 1
                    if alllanguage:
                        sender(dis_ment=0, message=alllanguage)
                    else:
                        sender(dis_ment=0, message='Ничего нигде нет... Я все проверил.. Что поделать?')


# Отправка нового репорта #
def report(lower):
    pers = lower[8:]
    cur.execute("SELECT Id from Report order by Id desc limit 1")
    res = cur.fetchall()
    if not res:
        Id = 0
    else:
        Id = res[0][0] + 1
    cur.execute('select * from Report where report is ?', (pers[1],))
    ros = cur.fetchone()
    if ros is None:
        if pers is not None and pers != '':
            lost = (Id, chatname_and_username(0), pers)
            cur.execute('insert into Report values(?, ?, ?)', lost)
            conn.commit()
            sender(
                message=f'{chatname_and_username(0)} отправил репорт:\n{pers} c Id {Id}\n@animanshnik (Тебе там репорт кинули)')
        else:
            sender(dis_ment=0, message='Пустое поле.')
    else:
        sender(dis_ment=0, message='Запись уже есть.')


# Все репорты #
def allrep():
    cur.execute("select * from Report")
    row = cur.fetchall()
    mess = bool(row)
    if mess:
        mess = []
        for i in row:
            print(i)
            mess.append(f'\n[{i[0]}] {i[2]} (от {i[1]})')
        sender(dis_ment=0, message='Список репортов:' + ' '.join(mess))
    else:
        sender(dis_ment=0, message='Репорты не обнаружены. Я идеален.')


# Удаление репорта #
def delrep(lower):
    pers = lower.split(': ')
    if len(pers) == 2:
        if pers[1].isnumeric():
            pers[1] = int(pers[1])
            print(pers[1])
            cur.execute('select * from Report where Id is ?', (pers[1],))
            ros = cur.fetchone()
            if ros is not None:
                cur.execute('DELETE FROM Report WHERE Id is ?', (pers[1],))
                conn.commit()
                sender(dis_ment=0, message=f'Репорт {pers[1]} удален.', bool_hi=1)
            else:
                sender(dis_ment=0, message='Такого репорта не существует.', bool_hi=1)
        else:
            sender(dis_ment=0, message='Такого репорта не существует.', bool_hi=1)
    elif pers[1] == 'all':
        cur.execute('select * from Report')
        ros = cur.fetchall()
        sender(dis_ment=0, message='Ожидайте, удаляю.')
        for i in ros:
            cur.execute('DELETE FROM Report WHERE Id is ?', (i[0],))
        sender(dis_ment=0, message='Список репортов очищен.', bool_hi=1)
        conn.commit()
    else:
        sender(dis_ment=0, message='delrep: [id, all]]', bool_hi=1)


# Проверка на админа #
def isAdmin(ids):
    d = vk.messages.getConversationMembers(peer_id=peer_id)
    if ids == 404016892:
        return True
    else:
        for VIND in d['items']:
            if VIND['member_id'] == ids:
                itemsfor = VIND.get('is_admin')
                if itemsfor:
                    return True
                else:
                    sender(message='Вы не администратор и не имеете доступ к этой команде.', bool_hi=1)


# Коды для зума #
def cods_for_zoom():
    sender(dis_ment=0, message=CFF.textsend[1])


def send_command():
    sender(dis_ment=0, message=CFF.textsend[0])


# Список пользователей #
def textlist():
    cur.execute("select * from USERS")
    row = cur.fetchall()
    mess = bool(row)
    i = 0
    if mess:
        cur.execute("select * from USERS")
        mess = []
        while i < len(row):
            rows = cur.fetchone()
            mess.append(f' @id{rows[2]} ({rows[0]} {rows[1]} )')
            i = i + 1
        sender(dis_ment=0, message='Список участников:')
        sender(dis_ment=0, message=mess)
    else:
        sender(dis_ment=0, message='Это все из списка', bool_hi=1)


# Удаление из списка #
def rem(lower):
    if isAdmin(user_id):
        need = lower.split(', ')
        if len(need) == 2:
            if re.search('@', need[1]):
                Id = need[1].replace('id', '')
                Final = Id.replace('[', '')
                FinalSplit = Final.split('|')
                Fin = FinalSplit[0]
                cur.execute("select * from USERS where id is ?", (Fin,))
                row = cur.fetchone()
                if row is not None:
                    cur.execute('DELETE FROM USERS WHERE id = ?', (Fin,))
                    conn.commit()
                    sender(message='Все ок. База данных потеряла еще одного человека.', bool_hi=1)
                else:
                    sender(message='Ты или ошибся ID, или этого человека не существует...', bool_hi=1)
            elif re.search('id', need[1]):
                Id = need[1].replace('id', '')
                cur.execute("select * from USERS where id is ?", (Id,))
                row = cur.fetchone()
                if row is not None:
                    cur.execute('DELETE FROM USERS WHERE id = ?', (Id,))
                    conn.commit()
                    sender(message='Все ок. База данных потеряла еще одного человека.', bool_hi=1)
                else:
                    sender(message='Ты или ошибся ID, или этого человека не существует...', bool_hi=1)
            else:
                idis = str(vk.users.get(user_ids=need[1])[0]["id"])
                cur.execute("select * from USERS where id is ?", (idis,))
                row = cur.fetchone()
                if row is not None:
                    cur.execute('DELETE FROM USERS WHERE id = ?', (idis,))
                    conn.commit()
                    sender(message='Все ок. База данных потеряла еще одного человека.', bool_hi=1)
                else:
                    sender(message='Ты или ошибся ID, или этого человека не существует...', bool_hi=1)
        else:
            sender(dis_ment=0, message='Было забыто несколько аргументов.', bool_hi=1)


# Рестарт бота #
def exit_bot():
    sender(dis_ment=0, message='Произвожу рестарт всех своих систем.', bool_hi=1)
    sys.exit()


# Добавление в список #
# UPDATE FOR NEW METHODS#
def add(lower):
    if isAdmin(user_id):
        ids = lower.split(', ')
        if len(ids) == 2:
            if ids[1] != '':
                if re.search('@', ids[1]):
                    Id = ids[1].replace('id', '')
                    Final = Id.replace('[', '')
                    FinalSplit = Final.split('|')
                    fin = FinalSplit[0]
                    cur.execute("select * from USERS where(id is ?)", (fin,))
                    row = cur.fetchone()
                    if row is None:
                        foll = requests.get(
                            f'{method_course}/users.get?user_ids={fin}&v=5.126&access_token={CFF.token}').json()
                        sdd = foll.get('error')
                        if sdd is not None:
                            if sdd[0].get('error_code') == 113:
                                sender(message='Такого пользователя не существует', bool_hi=1)
                        else:
                            name = foll.get('response', {})[0]['first_name']
                            fam = foll.get('response', {})[0]['last_name']
                            massive = (name, fam, fin)
                            cur.execute('insert into USERS values(?,?,?)', massive)
                            conn.commit()
                            d = f'Команда выполнена. Был добавлен юзер @id{fin} ({name} {fam})'
                            sender(dis_ment=0, message=d, bool_hi=1)
                    else:
                        sender(dis_ment=0, message='Этот аккаунт уже зарегестрирован.')
                elif re.search('id', ids[1]):
                    fin = ids[1].replace('id', '')
                    cur.execute("select * from USERS where(id is ?)", (fin,))
                    row = cur.fetchone()
                    if row is None:
                        foll = requests.get(
                            f'{method_course}/users.get?user_ids={fin}&v=5.126&access_token={CFF.token}').json()
                        sdd = foll.get('error', {})
                        if sdd.get('error_code') == 113:
                            sender(message='Такого пользователя не существует', bool_hi=1)
                        else:
                            name = foll.get('response', {})[0]['first_name']
                            fam = foll.get('response', {})[0]['last_name']
                            massive = (name, fam, fin)
                            cur.execute('insert into USERS values(?,?,?)', massive)
                            conn.commit()
                            d = f'Команда выполнена. Был добавлен юзер @id{fin} ({name} {fam})'
                            sender(dis_ment=0, message=d, bool_hi=1)
                    else:
                        sender(dis_ment=0, message='Этот аккаунт уже зарегестрирован.', bool_hi=1)

                else:
                    idis = requests.get(
                        f'{method_course}/users.get?user_ids={ids[1]}&v=5.126&access_token={CFF.token}').json()
                    idis.get('id')
                    idis = idis.get('error', {})
                    if idis != {}:
                        if idis.get('error_code') == 113:
                            sender(message='Такого пользователя не существует, или ты указал группу.', bool_hi=1)
                        else:
                            cur.execute("select * from USERS where(id is ?)", (idis,))
                            row = cur.fetchone()
                            if row is None:
                                foll = requests.get(
                                    f'{method_course}/users.get?user_ids={idis}&v=5.126&access_token={CFF.token}').json()
                                sdd = foll.get('error', {})
                                if sdd.get('error_code') == 113:
                                    sender(message='Такого пользователя не существует', bool_hi=1)
                                else:
                                    name = foll.get('response', {})[0]['first_name']
                                    fam = foll.get('response', {})[0]['last_name']
                                    massive = (name, fam, idis)
                                    cur.execute('insert into USERS values(?,?,?)', massive)
                                    conn.commit()
                                    d = f'Команда выполнена. Был добавлен юзер @id{idis} ({name} {fam})'
                                    sender(dis_ment=0, message=d, bool_hi=1)
                            else:
                                sender(message='Этот аккаунт уже зарегестрирован.', bool_hi=1)
            else:
                sender(dis_ment=0, message='Пусто. Ты видимо забыл айди ввести..', bool_hi=1)
        else:
            sender(dis_ment=0, message='Пусто. Ты видимо забыл айди ввести..', bool_hi=1)


# Проверка чтобы не положить бота #
def check(d, num):
    if len(d) == int(num):
        if d[1].isnumeric():
            return True
        else:
            sender(dis_ment=0, message='Это не число.', bool_hi=1)


def score_counter(lower):
    elsef = lower.split(', ')
    if len(elsef) > 1:
        elfsule = elsef[1].split(' ')
        elfsulelen = len(elsef[1].split(' '))
        elfus = []
        i = 0
        while len(elfsule) != 1 or len(elfsule) != 0:
            if len(elfsule) == 0:
                break
            if int(elfsule[i]) > 5:
                elfsule.remove(elfsule[i])
                elfsulelen = elfsulelen - 1
            if len(elfsule) > 1:
                if int(elfsule[i + 1]) > 5:
                    elfsule.remove(elfsule[i + 1])
                    elfsulelen = elfsulelen - 1
            if len(elfsule) > 1 and int(elfsule[i]) <= 5 and int(elfsule[i + 1]) <= 5:
                elfus.append(int(elfsule[i]) + int(elfsule[i + 1]))
                elfsule.remove(elfsule[i + 1])
                elfsule.remove(elfsule[i])
            elif len(elfsule) == 1 and int(elfsule[i]) <= 5:
                elfus.append(int(elfsule[i]))
                break
            else:
                continue
        if len(elfus) > 1:
            while len(elfus) != 1:
                if len(elfus) > 1:
                    elfus.append(int(elfus[i]) + int(elfus[i + 1]))
                    elfus.remove(elfus[i + 1])
                    elfus.remove(elfus[i])
                else:
                    continue
        if elfus:
            returned = int(elfus[0]) / int(elfsulelen)
            sender(dis_ment=0, message=f'Твой средний балл {returned}', bool_hi=1)
        else:
            sender(dis_ment=0, message='Ты видимо ввёл числа больше пяти..', bool_hi=1)
    else:
        sender(dis_ment=0, message='Ты не ввел числа.', bool_hi=1)


# Удалить из беседы и списка #
# UPDATE FOR NEW METHODS#
def kickfull(lower):
    if isAdmin(user_id):
        need = lower.split(', ')
        if len(need) == 2:
            if need != '':
                if re.search('@', need[1]):
                    FinalSplit = need[1].split('|')
                    Final = FinalSplit[0].replace('[', '')
                    Id = Final.replace('id', '')
                    sd = requests.get(
                        f'{method_course}/messages.removeChatUser?chat_id={chat_id}&member_id={Id}&v=5.126&access_token={CFF.token}').json()
                    sdd = sd.get('error', {})
                    if sdd.get('error_code') == 15:
                        sender(dis_ment=0, message='Этот пользователь администратор')
                    elif sdd.get('error_code') == 935:
                        sender(dis_ment=0, message='Пользователя нет в чате.')
                    elif Id == 'club145807659':
                        sender(dis_ment=0, message='Это я... Ребята, вы чево..')
                    else:
                        cur.execute('DELETE FROM USERS WHERE id = ?', (Id,))
                        sender(message='Пользователь удален из списка. Он не сможет войти в беседу')
                        conn.commit()

                elif re.search('id', need[1]):
                    Id = need[1].replace('id', '')
                    sd = requests.get(
                        f'{method_course}/messages.removeChatUser?chat_id={chat_id}&member_id={Id}&v=5.126&access_token={CFF.token}').json()
                    sdd = sd.get('error', {})
                    if sdd.get('error_code') == 15:
                        sender(dis_ment=0, message='Этот пользователь администратор')
                    elif sdd.get('error_code') == 935:
                        sender(dis_ment=0, message='Пользователя нет в чате.')
                    else:
                        cur.execute('DELETE FROM USERS WHERE id = ?', (Id,))
                        sender(message='Пользователь удален из списка. Он не сможет войти в беседу')
                        conn.commit()

                else:
                    if need[1].isnumeric() is False:
                        fullid = requests.get(
                            f'{method_course}/utils.resolveScreenName?screen_name={need[1]}&v=5.126&access_token={CFF.token}')
                        if fullid.json()['response']:
                            idis = requests.get(
                                f'{method_course}/users.get?user_id={fullid.json()["response"]["object_id"]}&v=5.126&access_token={CFF.token}').json()
                            sd = requests.get(
                                f'{method_course}messages.removeChatUser?chat_id={chat_id}&member_id={idis["response"][0]["id"]}&v=5.126&access_token={CFF.token}').json()
                            sdd = sd.get('error', {})
                            if sdd.get('error_code') == 15:
                                sender(dis_ment=0, message='Пользователь админ.')
                            elif sdd.get('error_code') == 935:
                                sender(dis_ment=0, message='Пользователя нет в чате.')
                            else:
                                cur.execute('DELETE FROM USERS WHERE id = ?', (idis['response'][0]['id'],))
                                sender(message='Пользователь удален из списка. Он не сможет войти в беседу')
                                conn.commit()
                        else:
                            sender(dis_ment=0, message='Айди неверно.')
                    else:
                        sender(message='Это должно быть буквенное айди. Например @animanshnik')
            else:
                sender(dis_ment=0, message='Ты забыл ввести ID')
        else:
            sender(dis_ment=0, message='Эта команда кикает участника без права повторного входа.')


# Проверка чтобы не положить бота, только для слов #
def checkstr(d):
    if len(d) == 2:
        if d[1].isnumeric() is False:
            return True
        else:
            sender(dis_ment=0, message='Это не слово.')


# Проверка, есть ли человек в списке #
def islist(idss):
    cur.execute("select * from USERS where(id is ?)", (idss,))
    row = cur.fetchone()
    if row is None:
        return False
    else:
        return True


# Удаление из беседы при входе, если человек не в списке #
def removelef(event):
    action = event.obj.get('action', {})
    Id = action.get('member_id')
    if islist(Id) is False:
        sender(dis_ment=0, message='Ты в сделку не входил')
        requests.get(
            f'{method_course}/messages.removeChatUser?chat_id={chat_id}&member_id={Id}&v=5.126&access_token={CFF.token}').json()
    else:
        sender(dis_ment=0,
               message=f'Приветик, {vk.users.get(user_ids=Id)[0]["first_name"]} {vk.users.get(user_ids=Id)[0]["last_name"]}')
        sender(dis_ment=0, message='Доступ разрешен.')


def sender(dis_ment=0, message=None, attach=None, bool_hi=0):
    params = {'v': v, 'chat_id': chat_id, 'access_token': CFF.token, 'message': None,
              'random_id': 0, 'disable_mentions': dis_ment, 'attachment': attach}
    if bool_hi == 0:
        params['message'] = message
    else:
        params['message'] = f'{message}\nС уважением, Цербер :P.'
    print(f'Отправляю сообщение:\n {message} в {chat_id}. {dis_ment}')
    requests.post(f'{method_course}/messages.send', params=params)


# Получение названия чата, или имени юзера #
def chatname_and_username(boolean):
    if boolean == 1:
        return vk.messages.getConversationsById(peer_ids=peer_id)['items'][0]['chat_settings']['title']
    else:
        return f'{vk.users.get(user_ids=user_id)[0]["first_name"]} {vk.users.get(user_ids=user_id)[0]["last_name"]}'


# Парсинг любого указанного сайта (только гдз, ибо там проверка по DIV) #
def parse(num, intn, url):
    if check(num, intn):
        sender(message='Ожидайте. Я собираю информацию. Это может занять какое-то время.')
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        quotes = soup.find_all('div', class_="with-overtask")
        attachments, comps = [], []
        for item in quotes:
            comps.append(item.find('img').get('src'))
        for i in comps:
            upload = vk_api.VkUpload(vk)
            p = requests.get(f'http:{i}')
            out = open(f"fall.jpg", "wb+")
            out.write(p.content)
            out.close()
            photo = upload.photo_messages(f'fall.jpg')
            owner_id = photo[0]['owner_id']
            photo_id = photo[0]['id']
            access_key = photo[0]['access_key']
            attachment = f'photo{owner_id}_{photo_id}_{access_key}'
            attachments.append(attachment)
            os.remove(f'fall.jpg')
        sender(dis_ment=1, message=url, attach=','.join(attachments), bool_hi=1)


def eng_parse(lower):
    d = lower.split(' ')
    if len(d) > 1:
        if int(d[1]) <= 152:
            parse(num=d, intn=2, url=f'https://gdz.ru/class-9/english/reshebnik-spotlight-9-vaulina-yu-e/{d[1]}-s/')
        else:
            sender(dis_ment=0, message='Такой страницы нет.')


def rus_parse(lower):
    d = lower.split(' ')
    if len(d) > 1:
        parse(num=d, intn=2, url=f'https://gdz.ru/class-9/russkii_yazik/trostnecova-9/{d[1]}-nom/')


def alg_parse(lower):
    d = lower.split(' ')
    if len(d) > 1:
        parse(num=d, intn=2, url=f'https://gdz.ru/class-9/algebra/makarichev-14/{d[1]}-nom/')


def deu_parse(lower):
    d = lower.split(' ')
    if len(d) > 1:
        parse(num=d, intn=2, url=f'https://gdz.ru/class-6/nemeckiy_yazik/averin/{d[1]}-s/')


# Расписание #
def rasp():
    week = datetime.datetime.weekday(datetime.datetime.today())
    today = datetime.datetime.date(datetime.datetime.today())
    if week == 0:
        sender(
            message=f'Сегодня понедельник, {today} число:\n1. 8:50-9:30 - Физкультура \n2. 9:45-10:25 - Физика \n3. '
                    f'10:40-11:20 - история\n4. 11:35-12:15 - Русский\n5. 12:25-13:05 - Литература\n6. 13:15-13:55 - Англ. '
                    f'яз/Информатика \n\n'
                    f'Завтра вторник:\n1. 8:50-9:30 - география \n2. 9:45-10:25 - алгебра \n3. 10:40-11:20 - физика\n4. '
                    f'11:35-12:15 - родная лит-ра\n5. 12:25-13:05 - Обществознание\n6. 13:15-13:55 - Немецкий\n7. 14:05-14:45 '
                    f'- ОБЖ\n Внеурочка по обществу ')
    if week == 1:
        sender(
            message=f'Сегодня вторник, {today} число:\n1. 8:50-9:30 - география \n2. 9:45-10:25 - алгебра \n3. 10:40-11:20 - '
                    f'физика\n4. 11:35-12:15 - родная лит-ра\n5. 12:25-13:05 - Обществознание\n6. 13:15-13:55 - Немецкий\n7. '
                    f'14:05-14:45 - ОБЖ\n Внеурочка по обществу \n\n'
                    f'Завтра среда:\n1. 8:50-9:30 - Английский \n2. 9:45-10:25 - Лит-ра \n3. 10:40-11:20 - физика\n4. '
                    f'11:35-12:15 - география\n5. 12:25-13:05 - русский\n6. 13:15-13:55 - химия\n7. 14:05-14:45 - физ-ра\n '
                    f'Классный час')
    if week == 2:
        sender(
            message=f'Сегодня среда, {today} число:\n1. 8:50-9:30 - Английский \n2. 9:45-10:25 - Лит-ра \n3. 10:40-11:20 - '
                    f'физика\n4. 11:35-12:15 - география\n5. 12:25-13:05 - русский\n6. 13:15-13:55 - химия\n7. 14:05-14:45 - '
                    f'физ-ра\nКлассный час\n\nЗавтра четверг:\n1. 8:50-9:30 - Алгебра \n2. 9:45-10:25 - англ.яз \n3. 10:40-11:20'
                    f' - геометрия\n4. 11:35-12:15 - Биология\n5. 12:25-13:05 - Русский\n6. 13:15-13:55 - Химия\n Внеурочка по алгебре и '
                    f'информатике')
    if week == 3:
        sender(
            message=f'Сегодня четверг, {today} число:\n1. 8:50-9:30 - алгебра \n2. 9:45-10:25 - англ.яз \n3. 10:40-11:20 - '
                    f'Геометрия\n4. 11:35-12:15 - Биология\n5. 12:25-13:05 - Русский\n6. 13:15-13:55 - Химия\n Внеурочка по '
                    f'алгебре и информатике \n\n'
                    f'Завтра пятница\n1. 8:50-9:30 - информатика|английский 2. 9:45-10:25 - геометрия 3. 10:40-11:20 - '
                    f'история\n4. 11:35-12:15 - литература\n5. 12:25-13:05 - Биология\n6. 13:15-13:55 - Алгебра\n7. '
                    f'14:05-14:45 - Физ-ра\n Внеурочка по русскому')
    elif week == 4:
        sender(
            message=f'Сегодня пятница, {today} число: \n1. 8:50-9:30 - информатика|английский \n2. 9:45-10:25 - геометрия \n3.'
                    f' 10:40-11:20 - история\n4. 11:35-12:15 - литература\n5. 12:25-13:05 - Биология\n6. 13:15-13:55 - '
                    f'Алгебра\n7. 14:05-14:45 - Физ-ра\n Внеурочка по русскому')
    elif week == 5:
        sender(message=f'Скоро понедельник\n1. 8:50-9:30 - Физкультура \n2. 9:45-10:25 - Физика \n3. '
                       f'10:40-11:20 - история\n4. 11:35-12:15 - Русский\n5. 12:25-13:05 - Литература\n6. 13:15-13:55 - Англ.яз ')
    elif week == 6:
        sender(
            message=f'Завтра понедельник\n1. 8:50-9:30 - Физкультура \n2. 9:45-10:25 - Физика \n3.10:40-11:20 - история\n'
                    f'4. 11:35-12:15 - Русский\n5. 12:25-13:05 - Литература\n6. 13:15-13:55 - Англ.яз|Информатика ')


def give_name_word(lower):
    d = lower.split(' ')
    var = 'Null'
    if checkstr(d):
        s = f'https://kartaslov.ru/значение-слова/{d[1]}'
        response = requests.get(s)
        soup = BeautifulSoup(response.text, 'lxml').find_all('li', class_="v2-dict-entry-text")
        for div in soup:
            var = ''.join(div.text.strip())
        sender(dis_ment=0, message=var)


def deshifration(event, attachn):
    fulltext = event.obj.get('conversation_message_id')
    payload = {'peer_id': event.object.peer_id, 'conversation_message_ids': fulltext, 'v': v, 'access_token': CFF.token}
    if event.from_user:
        attachn = attachn[0]['attachments']
        if attachn[0].get('type') == "audio_message":
            while True:
                foll = requests.get(f'{method_course}/messages.getByConversationMessageId', params=payload).json()
                response_text = foll['response']['items'][0]['fwd_messages'][0]['attachments'][0]['audio_message']
                if response_text.get('transcript_state') == 'done':
                    vk.messages.send(user_id=user_id, message=response_text.get('transcript'), random_id=0)
                    break
    else:
        if attachn[0].get('type') == "audio_message":
            while True:
                foll = requests.get(f'{method_course}/messages.getByConversationMessageId', params=payload).json()
                if foll['response']['items'][0]['attachments'][0]['audio_message'].get('transcript_state') == "done":
                    sender(message=f"{foll['response']['items'][0]['attachments'][0]['audio_message']['transcript']}")
                    break


# Каникулы #
def Kan():
    today_and_day = {}
    today = 150 - (int(time.strftime('%j')))
    ctoday = divmod(today, 7)
    today_and_day['date'] = today, ctoday[0], ctoday[1]
    if ctoday[1] == 1:
        today_and_day['format_day'] = 'день'
    elif 5 <= ctoday[1]:
        today_and_day['format_day'] = 'дней'
    else:
        today_and_day['format_day'] = 'дня'
    if ctoday[0] == 1:
        today_and_day['format_week'] = 'неделя'
    elif 5 <= ctoday[0]:
        today_and_day['format_week'] = 'недель'
    else:
        today_and_day['format_week'] = 'недели'
    sender(
        message=f'До каникул осталось: {today_and_day["date"][0]} дней, или {today_and_day["date"][2]} {today_and_day["format_day"]} и {today_and_day["date"][1]} {today_and_day["format_week"]}')


if __name__ == '__main__':
    main()
