import os
import time
import vk_api
import pdfminer
import openpyxl
import xlsxwriter
import pandas as pd
from pdfminer.high_level import extract_text

# Библиотеки и функции для VK
from vk_api import VkUpload
from vk_api.keyboard import VkKeyboard
from vk_api.bot_longpoll import VkBotLongPoll
from vk_api.bot_longpoll import VkBotEventType

key = '66ad8c5ffed24d0df68094a8bdc04b96b6868b6df748f1e87d8376188a2335e5b5d139247c530c4d48eb6'

vk_session = vk_api.VkApi(token=key, api_version="5.103")
longpoll = VkBotLongPoll(vk_session, '204198097') # '202793215' - dv # '201237497' - main
vk = vk_session.get_api()
users = vk.users
upload = VkUpload(vk_session)

start = VkKeyboard(one_time=True)

start.add_button(label='Получить сводку', color='positive')

# решионы
region = VkKeyboard(one_time=True)

region.add_button(label='Красноярск.', color='default')
region.add_button(label='Краснодарск.', color='default')
region.add_line()
region.add_button(label='Алтайск.', color='primary')
region.add_button(label='Забайкал.', color='primary')
region.add_line()
region.add_button(label='Все + регрессия', color='positive')

menu = {}
ex = {}
info = []
tag = ['горячие точки']
columns = [{'header': 'дата'}, {'header': "регион"}, {'header': "число"}, {'header': "точки"},
           {'header': "площадь га"}]

def main():
    global ex, info, tag, columns, vk_session, vk, users, upload, longpoll, key, region, menu, start
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            if event.message.peer_id not in menu or event.message.text.lower() == "Получить сводку" or event.message.text.lower() == "Начать" or menu[event.message.peer_id] == "старт":
                menu[event.message.peer_id] = "получение"
                vk.messages.send(
                    peer_id=event.message.peer_id,
                    random_id=time.time(),
                    message="Выберите регион для получения данных",
                    keyboard=region.get_keyboard())

            elif menu[event.message.peer_id] == "получение":
                r = str(event.message.text).replace('.', '')
                vk.messages.send(
                    peer_id=event.message.peer_id,
                    random_id=time.time(),
                    message="Запрос принят, получаю данные")

                for years in range(2020, 2022):
                    if 'Все' in r:
                        document_excel = upload.document_message(
                            f"{'Dataset_all'}.xlsx",
                            title="сводка для РФ",
                            peer_id=event.message.peer_id
                        )['doc']
                        vk.messages.send(
                            peer_id=event.message.peer_id,
                            random_id=time.time(),
                            message='Ваш запрос обработан',
                            attachment=f"doc{document_excel['owner_id']}_{document_excel['id']}",
                            keyboard=start.get_keyboard())
                        break

                    for months in range(4, 12):
                        if months < 10:
                            months = '0' + str(months)
                        else:
                            months = str(months)

                        for days in range(1, 32):
                            years = str(years)
                            if days < 10:
                                days = '0' + str(days)
                            else:
                                days = str(days)
                            try:
                                text = extract_text(f'{years + months + days}.pdf')
                                fin = text.split()
                                if r not in str(fin[fin.index('Максимальное') + 5]) and r != 'все':
                                    a = 12 / 0
                                ex[str(fin[fin.index('на') - 1])] = []
                                if str(fin[fin.index('Максимальное') + 7])[1:-2].isdigit():
                                    ex[str(fin[fin.index('на') - 1])].append(str(fin[fin.index('Максимальное') + 5]) + ' ' +
                                                                             str(fin[fin.index('Максимальное') + 6]))
                                    ex[str(fin[fin.index('на') - 1])].append(int(str(fin[fin.index('Максимальное') + 7])[1:-2]))
                                else:
                                    ex[str(fin[fin.index('на') - 1])].append(str(fin[fin.index('Максимальное') + 5]) + ' ' +
                                                                             str(fin[fin.index('Максимальное') + 6]) + str(
                                        fin[fin.index('Максимальное') + 7]))
                                    ex[str(fin[fin.index('на') - 1])].append(int(str(fin[fin.index('Максимальное') + 8])[1:-2]))
                                ex[str(fin[fin.index('на') - 1])].append(int(str(fin[fin.index('них') + 3])))

                                if str(fin[fin.index('около') + 2]) == 'тыс':
                                    a = fin[fin.index('около') + 1].replace(',', '.')
                                    ex[str(fin[fin.index('на') - 1])].append(int(float(a) * 1000))
                                else:
                                    ex[str(fin[fin.index('на') - 1])].append(int(fin[fin.index('около') + 1]))

                                '''
                                info.append("дата - " + str(fin[fin.index('на') - 1]))
                                info.append("природных пожаров c активным горением - " + str(fin[fin.index('природных') - 1]))
                                info.append("горячие точки - " + str(fin[fin.index('горячие') - 1]))
                                info.append("активных  пожаров - " + str(fin[fin.index('активных') - 1]))
                                info.append("активных  пожаров лесов - " + str(fin[fin.index('точка).') - 2])[1:])
                                info.append("Максимальное число пожаров в - " + str(fin[fin.index('Максимальное') + 5]) + ' ' +
                                            str(fin[fin.index('Максимальное') + 6]) + ' ' + str(fin[fin.index('Максимальное') + 7])[1:-2])
                                info.append("На них было зарегистрировано (горячие точки) - " + str(fin[fin.index('них') + 3]))
                                '''
                            except:
                                continue
                if 'Все' not in r:
                    data1 = [[a, *i] for a, i in ex.items()]
                    if len(data1) < 2:
                        menu[event.message.peer_id] = "старт"
                        vk.messages.send(
                            peer_id=event.message.peer_id,
                            random_id=time.time(),
                            message='Не удалось обработать Ваш запрос',
                            keyboard=start.get_keyboard())

                    workbook = xlsxwriter.Workbook('Dataset.xlsx')
                    worksheet = workbook.add_worksheet()
                    worksheet.add_table(0, 0, len(data1) + 1, 4, {'data': data1, 'columns': columns})
                    workbook.close()
                    document_excel = upload.document_message(
                        f"{'Dataset'}.xlsx",
                        title='сводка_для_' + r,
                        peer_id=event.message.peer_id
                    )['doc']
                    if len(data1) < 2:
                        vk.messages.send(
                            peer_id=event.message.peer_id,
                            random_id=time.time(),
                            message='lol',
                            sticker_id=12,
                            keyboard=start.get_keyboard())
                        continue

                    vk.messages.send(
                        peer_id=event.message.peer_id,
                        random_id=time.time(),
                        message='Ваш запрос обработан',
                        attachment=f"doc{document_excel['owner_id']}_{document_excel['id']}",
                        keyboard=start.get_keyboard())
                menu[event.message.peer_id] = "старт"

            else:
                menu[event.message.peer_id] = "старт"
                vk.messages.send(
                    peer_id=event.message.peer_id,
                    random_id=time.time(),
                    message='У меня нет такой команды',
                    keyboard=start.get_keyboard())
main()

