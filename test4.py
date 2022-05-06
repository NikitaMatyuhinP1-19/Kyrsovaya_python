# pip install pycoingecko
# pip install python-telegram-bot
# pip install pyTelegramBotAPI
# pip install selenium

import time
import telebot
from telebot import types
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import os

bot = telebot.TeleBot('TOKEN')

@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item4 = types.KeyboardButton("/book")
    item5 = types.KeyboardButton("/site_list")
    markup.add(item5, item4)
    bot.send_message(message.chat.id,
                     'Привет, я помогу найти интерисующую тебя книгу')
    time.sleep(1)
    bot.send_message(message.chat.id,
                     'Что я умею:')
    time.sleep(1)
    bot.send_message(message.chat.id,
                     'С помощью команды "/book" я найду тебе книгу по названию и автору')
    time.sleep(1)
    bot.send_message(message.chat.id,
                     'Команда "/site_list" выведет список сайтов на которых ты сможешь сам поискать нужную тебе '
                     'литературу')
    time.sleep(1)
    bot.send_message(message.chat.id,
                     'Для удобства можешь использовать кнопки для отправление мне команд')
    time.sleep(1)
    bot.send_sticker(message.chat.id,
                     "CAACAgIAAxkBAAEEopVidBuO5Cqk1hxVRA_qblnv0xBSNAACXAADJ_awAy4dgZhApomhJAQ", reply_markup=markup)

@bot.message_handler(commands=['book'])
def book(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item4 = types.KeyboardButton("/book")
    item5 = types.KeyboardButton("/site_list")
    markup.add(item5, item4)
    bot.send_message(message.chat.id,
                     'Какую книгу ты хочешь найти?', reply_markup=markup)

    @bot.message_handler(content_types=["text"])
    def book_search(message):
        global book_name
        book_name = message.text
        try:
            driver = webdriver.Chrome()  # открываем браузер
            driver.get('https://libgen.li/index.php')  # переходим на указанный сайт
            xpath_site = \
                '/html/body/form/div[1]/input'  # по Xpatch находим строку поиска на сайте
            driver.find_element_by_xpath(xpath_site).send_keys(book_name)   # в book_name записанно название
            # запрошенной книги , происходит ввод в строку поиска на сайте
            xpath_search = \
                '/html/body/form/div[1]/div[1]/button'   # кнопка поиска
            driver.find_element_by_xpath(xpath_search).click()   # нажатие на кнопку поиска
            xpath_select_book = \
                '/html/body/table/tbody/tr[1]/td[9]/a[1]/span'   # кнопка перехода на книгу
            driver.find_element_by_xpath(xpath_select_book).click()   # нажатие
            xpath_download_book = \
                '/html/body/table/tbody/tr[1]/td[2]/a/h2'   # кнопка скачивание
            driver.find_element_by_xpath(xpath_download_book).click()   # нажатие
            time.sleep(2)
            driver.quit()  # выход из браузера
            bot.send_message(message.chat.id, 'Ща отправлю')
            directory = 'C:/Users/Никита/Downloads'   # скаченная книга оказывается тут
            i = 0
            filelist = os.listdir(directory)  # Все файлы в этой папке (включая папки)
            for files in filelist:  # Обойти все файлы
                i = i + 1
                Olddir = os.path.join(directory, files)  # Первоначальный путь к файлу
                if os.path.isdir(Olddir):  # Пропустить, если это папка
                    continue
                filename = 'Book'  # имя файла
                filetype = '.fb2'  # Расширение файла
                Newdir = os.path.join(directory, filename + str(i) + filetype)  # Новый путь к файлу
                os.rename(Olddir, Newdir)  # Rename
                bot.send_document(message.chat.id, open(f"C:/Users/Никита/Downloads/Book{str(i)}.fb2", 'rb'))
                # отправка переименнованного файла
                os.remove(f"C:/Users/Никита/Downloads/Book{str(i)}.fb2")   # удаление файла с пк
                time.sleep(1)
                bot.send_message(message.chat.id,
                                 'Вот книга которую ты просил')
                time.sleep(1)
                bot.send_sticker(message.chat.id,
                                 "CAACAgIAAxkBAAEEortidC7EtAvepsmBz15B7oTjrtwXGgACDgADJ_awA8CX9YBBpBEWJAQ")
                time.sleep(1)
                bot.send_message(message.chat.id,
                                 'Для лучшего времяпровождения рекоментую воспользоватся услугами моего собрата:')
                time.sleep(1)
                bot.send_message(message.chat.id,
                                 '@circle_friends_bot , Здесь вы сможете утешить свои вкусовые сосочки🥃🔞',
                                 reply_markup=markup)

        except NoSuchElementException:
            try:
                bot.send_message(message.chat.id, 'Еще ищу , секунду...')
                driver = webdriver.Chrome()
                driver.get('https://booksee.org/')  # сайт
                xpath_site = \
                    '/html/body/table/tbody/tr[2]/td/center/div/form/div[1]/div/div[1]/input'  # строка поиска
                driver.find_element_by_xpath(xpath_site).send_keys(book_name)
                xpath_search = \
                    '/html/body/table/tbody/tr[2]/td/center/div/form/div[1]/div/div[2]/div/input'  # кнопка поиска
                driver.find_element_by_xpath(xpath_search).click()
                xpath_select_book = \
                    '/html/body/table/tbody/tr[2]/td/center/div/div[2]/div/div[2]/div[1]/div[1]/a[1]/h3'  # выбор книги
                driver.find_element_by_xpath(xpath_select_book).click()
                xpath_download_book = \
                    '/html/body/table/tbody/tr[2]/td/center/div/div[3]/div[1]/div[2]/div[2]/div/div/a[1]'  # кнопка скачать
                driver.find_element_by_xpath(xpath_download_book).click()
                time.sleep(2)
                driver.quit()
                bot.send_message(message.chat.id, 'Ща отправлю')
                directory = 'C:/Users/Никита/Downloads'
                i = 0
                filelist = os.listdir(directory)  # Все файлы в этой папке (включая папки)
                for files in filelist:  # Обойти все файлы
                    i = i + 1
                    Olddir = os.path.join(directory, files)  # Первоначальный путь к файлу
                    if os.path.isdir(Olddir):  # Пропустить, если это папка
                        continue
                    filename = 'Book'  # имя файла
                    filetype = '.zip'  # Расширение файла
                    Newdir = os.path.join(directory, filename + str(i) + filetype)  # Новый путь к файлу
                    os.rename(Olddir, Newdir)  # Rename
                    bot.send_document(message.chat.id, open(f"C:/Users/Никита/Downloads/Book{str(i)}.zip", 'rb'))
                    os.remove(f"C:/Users/Никита/Downloads/Book{str(i)}.zip")
                    time.sleep(1)
                    bot.send_message(message.chat.id,
                                     'Вот книга которую ты просил')
                    time.sleep(1)
                    bot.send_sticker(message.chat.id,
                                     "CAACAgIAAxkBAAEEortidC7EtAvepsmBz15B7oTjrtwXGgACDgADJ_awA8CX9YBBpBEWJAQ")
                    time.sleep(1)
                    bot.send_message(message.chat.id,
                                     'Для лучшего времяпровождения рекоментую воспользоватся услугами моего собрата:')
                    time.sleep(1)
                    bot.send_message(message.chat.id,
                                     '@circle_friends_bot , Здесь вы сможете утешить свои вкусовые сосочки🥃🔞',
                                     reply_markup=markup)

            except NoSuchElementException:
                try:
                    bot.send_message(message.chat.id,
                                     'Тут посмотрю... *_*')
                    driver = webdriver.Chrome()
                    driver.get('https://obuchalka.org/')  # сайт
                    xpath_site = \
                        '/html/body/div[1]/div/div[2]/div/form/input[1]'  # строка поиска
                    driver.find_element_by_xpath(xpath_site).send_keys(book_name)
                    xpath_search = \
                        '/html/body/div[1]/div/div[2]/div/form/input[6]'  # кнопка поиска
                    driver.find_element_by_xpath(xpath_search).click()
                    xpath_select_book = \
                        '/html/body/div[3]/div[1]/div[1]/div[2]/div[2]/div/div/div/div[5]/div[2]/div/div/div[1]/div[' \
                        '1]/div[1]/div[1]/div '
                    driver.find_element_by_xpath(xpath_select_book).click()
                    xpath_select_book_1 = \
                        '/html/body/div[3]/div[1]/div[1]/div[2]/div/div[2]/a[1]'
                    driver.find_element_by_xpath(xpath_select_book_1).click()
                    xpath_download_book = \
                        '/html/body/div[1]/div[1]/section[1]/div[2]/a[1]'
                    driver.find_element_by_xpath(xpath_download_book).click()
                    time.sleep(3)
                    driver.quit()
                    bot.send_message(message.chat.id,
                                     'Ща отправлю')
                    directory = 'C:/Users/Никита/Downloads'
                    i = 0
                    filelist = os.listdir(directory)  # Все файлы в этой папке (включая папки)
                    for files in filelist:  # Обойти все файлы
                        i = i + 1
                        Olddir = os.path.join(directory, files)  # Первоначальный путь к файлу
                        if os.path.isdir(Olddir):  # Пропустить, если это папка
                            continue
                        filename = 'Book'  # имя файла
                        filetype = '.pdf'  # Расширение файла
                        Newdir = os.path.join(directory, filename + str(i) + filetype)  # Новый путь к файлу
                        os.rename(Olddir, Newdir)  # Rename
                        bot.send_document(message.chat.id,
                                          open(f"C:/Users/Никита/Downloads/Book{str(i)}.pdf", 'rb'))
                        os.remove(f"C:/Users/Никита/Downloads/Book{str(i)}.pdf")
                        time.sleep(1)
                        bot.send_message(message.chat.id,
                                         'Вот книга которую ты просил')
                        time.sleep(1)
                        bot.send_sticker(message.chat.id,
                                         "CAACAgIAAxkBAAEEortidC7EtAvepsmBz15B7oTjrtwXGgACDgADJ_awA8CX9YBBpBEWJAQ")
                        time.sleep(1)
                        bot.send_message(message.chat.id,
                                         'Для лучшего времяпровождения рекоментую воспользоватся услугами моего '
                                         'собрата:')
                        time.sleep(1)
                        bot.send_message(message.chat.id,
                                         '@circle_friends_bot , Здесь вы сможете утешить свои вкусовые сосочки🥃🔞',
                                         reply_markup=markup)

                except NoSuchElementException:
                    bot.send_message(message.chat.id,
                                     'Я не смог найти такой книги, попробуй ввести название по другому, или попробуй '
                                     'найти сам')
                    time.sleep(1)
                    bot.send_sticker(message.chat.id,
                                     "CAACAgIAAxkBAAEEoq9idCjXS2uwusD46737qDdsoISvjAACdgADJ_awAx3lZYmct2GoJAQ",
                                     reply_markup=markup)

@bot.message_handler(commands=['site_list'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item4 = types.KeyboardButton("/book")
    item5 = types.KeyboardButton("/site_list")
    markup.add(item5, item4)
    bot.send_message(message.chat.id, "\n".join(['http://libgen.is/ - Художественная литература',
                                                 '',
                                                 'https://www.studmed.ru/ - Учебно-методическая литература',
                                                 '',
                                                 'https://w41.torlook.info/  Есть книги в .mp3',
                                                 '',
                                                 'https://booksee.org/   Художественная литература',
                                                 '',
                                                 'https://archive.org/  Иностранная литература',
                                                 '',
                                                 'https://bookskeeper.ru/  Тут определенно что-то связанное с книгами ',
                                                 '',
                                                 'https://www.gutenberg.org/  Тоже иностранная литература',
                                                 '',
                                                 'https://obuchalka.org/  ГДЗ и чтото связанное со школой *_*']),
                     reply_markup=markup)

bot.polling()
