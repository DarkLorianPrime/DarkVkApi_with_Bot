import sqlite3
import re

import requests
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import vk_api
import ConfigForFactory as CFF

conn = sqlite3.connect('need_test.db')
cur = conn.cursor()
vk_session = vk_api.VkApi(token=str(CFF.token))
vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, str(CFF.group_id))

conn.execute('CREATE TABLE IF NOT EXISTS ROLES(name_roles str, is_addRole str, is_adminAccept str)')
conn.execute('CREATE TABLE IF NOT EXISTS ROLES_USERS(name_roles str, USERS str)')
cur.execute('select * from ROLES where name_roles is ?', ('TECH_ADMIN',))
v = cur.fetchone()
if v is None:
    values = ('TECH_ADMIN', True, True)
    valuesTwo = ('standart', False, False)
    cur.execute('insert into ROLES values(?, ?, ?)', values)
    cur.execute('select * from ROLES where name_roles is ?', ('TECH_ADMIN',))
    values_user = ('TECH_ADMIN', '404016892')
    cur.execute('insert into ROLES_USERS values(?, ?)', values_user)
    conn.commit()
    vk.messages.send(chat_id=14, message='<Role TECH_ADMIN pass id404016892>', random_id=0)
vk.messages.send(chat_id=14, message='MODULE CONNECTED', random_id=0)

while True:
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            text = event.object.text
            user_id = event.object.from_id

            if re.search('addRole', text):
                cur.execute('select * from ROLES_USERS where USERS is ?', (user_id,))
                v = cur.fetchone()
                if v is not None:
                    cur.execute('select * from ROLES where name_roles is ?', (v[0],))
                    s = cur.fetchone()
                    if s is not None:
                        if s[1] == 1:
                            query = text.split(' ')
                            if len(query) == 4:
                                values = (query[1], query[2], query[3])
                                cur.execute('insert into ROLES values(?, ?, ?)', values)
                                conn.commit()
                                vk.messages.send(chat_id=14, message=f'Добавлена новая роль - {query[1]}.', random_id=0)
                            else:
                                vk.messages.send(chat_id=14,
                                                 message=f'Ошибка ввода. addRole [name] [addRoleGive] [AdminCommands]',
                                                 random_id=0)
                        else:
                            vk.messages.send(chat_id=14,
                                             message=f'У роли {s[0]} не хватает прав для выполнения данной команды.',
                                             random_id=0)
                else:
                    vk.messages.send(chat_id=14,
                                     message=f'Твоя роль не найдена. Обратись к администрации..',
                                     random_id=0)

            if re.search('RolePerm', text):
                returns = {}
                query = text.split(' ')
                if len(query) == 2:
                    cur.execute('select * from ROLES where name_roles is ?', (query[1],))
                    row = cur.fetchone()
                    if row is not None:
                        print(row)
                        if row[1] == 1:
                            returns['addRoles'] = 'Может давать роли\nМожет создавать роли'
                        if row[2] == 1:
                            returns['adminCommands'] = 'Может использовать команды администрации'
                        if row[1] == 0:
                            returns['addRoles'] = 'Не может давать роли'
                        if row[2] == 0:
                            returns['adminCommands'] = 'Не может использовать команды администрации'
                        vk.messages.send(chat_id=14,
                                         message=f'Роль {row[0]}:\n {returns["adminCommands"]}\n {returns["addRoles"]}',
                                         random_id=0)
                    else:
                        vk.messages.send(chat_id=14, message=f'Роль {query[1]} не найдена.', random_id=0)

            if text == 'giveCommand':
                print(2)

            if text == 'allCommands':
                print(1)

            if text == 'removeCommand':
                print(1)

            if text == 'deleteRole':
                print(1)

            if text == 'allRoles':
                users = []
                users_roles = []
                w = []
                cur.execute('select * from ROLES')
                v = cur.fetchall()
                for i in v:
                    cur.execute('select * from ROLES_USERS where name_roles is ?', (i[0],))
                    f = cur.fetchall()
                    w.clear()
                    if f:
                        for v in f:
                            ids = vk.users.get(user_ids=f"id{v[1]}")[0]
                            if f is not []:
                                w.append(f'@id{v[1]} ({ids["first_name"]} {ids["last_name"]})')
                        users.append(f'\n{v[0]} - {w}')
                vk.messages.send(chat_id=14, message=users, random_id=0, disable_mentions=1)

            if re.search('removeRole', text):
                query = text.split(' ')
                query_name = query[1].replace('[id', '')
                var = query_name.split('|')[0]
                cur.execute('select * from ROLES_USERS where USERS is ?', (user_id,))
                user_accept = cur.fetchone()
                cur.execute('select * from ROLES_USERS where USERS is ?', (var,))
                rem_id = cur.fetchone()
                if rem_id is not None:
                    if user_accept is not None:
                        cur.execute('select * from ROLES where name_roles is ?', (user_accept[0],))
                        s = cur.fetchone()
                        if s is not None:
                            if s[1] == 1:
                                query = text.split(' ')
                                cur.execute('delete from ROLES_USERS where USERS=?', (var,))
                                cur.execute('insert into ROLES_USERS values(?,?)', (var, 'standart'))
                                nick = f'{vk.users.get(user_ids=var)[0]["first_name"]} {vk.users.get(user_ids=var)[0]["last_name"]}'
                                conn.commit()
                                vk.messages.send(chat_id=14,
                                                 message=f'У пользователя @id{user_id} ({nick}) была удалена роль.',
                                                 random_id=0, disable_mentions=1)
                            else:
                                vk.messages.send(chat_id=14,
                                                 message=f'У роли {s[0]} не хватает прав для выполнения данной команды.',
                                                 random_id=0)
                        else:
                            vk.messages.send(chat_id=14, message=f'Твоя роль не найдена, обратись к администрации. ',
                                             random_id=0)
                else:
                    vk.messages.send(chat_id=14, message=f'У пользователя нет роли.', random_id=0)

            if re.search('giveRole', text):
                query = text.split(' ')
                if len(query) == 3:
                    query_name = query[1].replace('[id', '')
                    var = query_name.split('|')[0]
                    cur.execute('select * from ROLES_USERS where USERS is ?', (var,))
                    v = cur.fetchone()
                    cur.execute('select * from ROLES_USERS where USERS is ?', (user_id,))
                    user_accept = cur.fetchone()
                    if user_accept is not None:
                        cur.execute('select * from ROLES where name_roles is ?', (user_accept[0],))
                        s = cur.fetchone()
                        if s is not None:
                            if s[1] == 1:
                                query = text.split(' ')
                                if v is None:
                                    cur.execute('select * from ROLES where name_roles is ?', (query[2],))
                                    v = cur.fetchone()
                                    if v is not None:
                                        if v[0] != 'TECH_ADMIN':
                                            values = query[2], var
                                            cur.execute('insert into ROLES_USERS values(?, ?)', values)
                                            par = {
                                                'user_ids': var, 'access_token': str(CFF.token), 'v': 5.85}
                                            ids = requests.get('https://api.vk.com/method/users.get', params=par)
                                            if ids.json().get('error') is not None:
                                                vk.messages.send(chat_id=14,
                                                                 message=f'Такого пользователя не существует.',
                                                                 random_id=0, disable_mentions=1)
                                                break
                                            nick = f'{ids.json()["response"][0]["first_name"]} {ids.json()["response"][0]["last_name"]}'
                                            vk.messages.send(chat_id=14,
                                                             message=f'Теперь пользователь @id{var} ({nick}) имеет роль - {query[2]}.',
                                                             random_id=0, disable_mentions=1)
                                            conn.commit()
                                        else:
                                            vk.messages.send(chat_id=14,
                                                             message='Выдача данной роли недоступна для смертных.',
                                                             random_id=0)
                                    else:
                                        vk.messages.send(chat_id=14, message='Вы ошиблись названием роли', random_id=0)
                                else:
                                    vk.messages.send(chat_id=14,
                                                     message='Данный пользователь уже имеет роль. \nПеред выдачей новой - удалите старую',
                                                     random_id=0)
                            else:
                                vk.messages.send(chat_id=14,
                                                 message=f'У роли {s[0]} не хватает прав для выполнения данной команды. ',
                                                 random_id=0)
                    else:
                        vk.messages.send(chat_id=14,
                                         message=f'Твоя роль не найдена, обратись к администрации. ',
                                         random_id=0)
