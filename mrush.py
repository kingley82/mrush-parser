#Передаю спасибо и привет https://github.com/Wilidon, если бы не он я бы не разобрался как обойти анти-бот систему

#Связь со мной: @a352642 (telegram)

import os
import time
try:
    import requests
    from bs4 import BeautifulSoup as BS
except:
    print("Installing module 'requests'")
    os.system("pip3 install requests -q")
    print("Installing module 'beautifulsoup4'")
    os.system("pip3 install beautifulsoup4 -q")

class Client:
    def __init__(self, name: str, password: str):
        self.session = requests.Session()
        self.url = "https://mrush.mobi/" #URL нашей игры
        self.name = name #Ваше имя в игре
        self.password = password #Ваш пароль в игре
        self.headers = { 
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0"
        }
        self.login()


    def login(self): #Вход в аккаунт
        response = self.session.get(self.url+"welcome", headers=self.headers) #Отправка GET запроса на сервер
        html = response.text #Получаем HTML код страницы
        if "я не робот" in html: #Если есть защита от ботов
            soup = BS(html, "html.parser")
            elems = soup.findAll("style") #Получаем все элементы системы
            for elem in elems:
                if "margin-left:" not in str(elem) and "display: none;" not in str(elem) and "overflow: hidden" not in str(elem): #Если этот элемент не спрятан то он нам нужен
                    correct_elem = str(elem).split(".")[1].split("{")[0] #Отделяем его от кода
                    correct_elem = soup.find("div", class_=correct_elem).find("input")["name"] #Находим по нему другой нужный нам элемент
                    request = self.session.post(self.url+"login", headers=self.headers, data={ #Посылаем POST запрос
                        "name": self.name,
                        "password": self.password,
                        correct_elem: "" #Элемент который мы нашли
                    })
                    if "Неправильное Имя или Пароль" in request.text: #Проверка на валидность данных
                        return "Incorrect name or password at 'login'"
                    if "заблокирован" in request.text: #Проверка на блокировку
                        return "You have been banned"
                    return "Succesfull"
        elif "Вы кликаете слишком быстро" in html:
            time.sleep(2)
            self.login()
        else: #Если нет защиты
            request = self.session.post(self.url+"login", headers=self.headers, data={ #Посылаем POST запрос
                "name": self.name,
                "password": self.password
            })
    

    #=================================================================
    #=======================GET ЗАПРОСЫ===============================
    #=================================================================


    def profile(self, id: str = None): #Информация из своего или чужого профиля
        if id == None: #Если ID не указано то узнаем информацию из своего профиля
            response = self.session.get(self.url+"profile", headers=self.headers) #Посылаем GET запрос
        else: #Если ID указано то узнаем информацию человека с этим ID
            response = self.session.get(self.url+"view_profile?player_id="+id, headers=self.headers) #Посылаем GET запрос
        html = response.text #Получаем HTML код страницы
        if "Вы кликаете слишком быстро" in html:
            time.sleep(2)
            self.profile(id)
        soup = BS(html, "html.parser")
        elems = soup.findAll("span") #Получаем данные
        data = {} #Сюда будут сохранятся обработанные данные
        for elem in elems:
            if "visibility: hidden" not in str(elem): #Если элемент показан
                elem = elem.text.replace("\t", "").replace("\n", "") #Убираем все лишнее
                if "уровень" in elem: #Узнаем уровень и имя
                    data["name"] = elem.split(",")[0].strip()
                    data["level"] = elem.split(",")[1].split("уровень")[0].replace(" ", "")
                if "Статус" in elem: #Узнаем статус
                    data["status"] = " ".join(elem.split(":")[1:])
                if "Опыт" in elem: #Узнаем текущий опыт и опыт необходимый для перехода на следующий уровень
                    data["exp"] = elem.split(":")[1].split("/")[0].replace(" ", "")
                    data["exp_max"] = elem.split(":")[1].split("/")[1].replace(" ", "")
                if "Доблесть" in elem: #Узнаем текущий уровень доблести
                    data["valor_level"] = elem.split(":")[1].split("у")[0].replace(" ", "")
                if "Сила" in elem: #Узнаем текущую силу
                    data["strength"] = elem.split(":")[1].replace(" ", "")
                if "Здоровье" in elem: #Узнаем текущее здоровье
                    data["health"] = elem.split(":")[1].replace(" ", "")
                if "Броня" in elem: #Узнаем текущую броню
                    data["defense"] = elem.split(":")[1].replace(" ", "")
                if "Золото" in elem: #Узнаем текущее кол-во золота
                    data["gold"] = elem.split(":")[1].replace(" ", "")
                if "Серебро" in elem: #Узнаем текущее кол-во серебра
                    data["silver"] = elem.split(":")[1].replace(" ", "")
        if "valor_level" not in data: #Если не удалось узнать доблесть
            if id == None: #В своем профиле
                response = self.session.get(self.url+"valor_info", headers=self.headers) #Посылаем GET запрос
                html = response.text
                soup = BS(html, "html.parser")
                elems = soup.findAll("div", class_="mlr10")
                for elem in elems:
                    if "уровень" in str(elem):
                        data["valor_level"] = elem.text.split(":")[1].split("Ваши")[0].replace(" ", "").replace("\n", "")
            else: #В чужом
                response = self.session.get(self.url+"valor_info?player_id="+id, headers=self.headers) #Посылаем GET запрос
                html = response.text
                soup = BS(html, "html.parser")
                elems = soup.findAll("div", class_="mt10")
                for elem in elems:
                    elem = elem.text.replace("\n", "").replace("\t", "")
                    if "За" in elem:
                        data["valor_level"] = elem.split("й")[1].split("у")[0].replace(" ", "")
        links = soup.findAll("a")
        for link in links:
            if "player_id" in link["href"]:
                data["player_id"] = link["href"].split("=")[1].split("&")[0]
        return data
    

    def best(self, pages: int = 1, category: int = 1): #Список лучших
        if pages > 500: pages = 500 #Проверка на максимальное кол-во страниц
        data = {} #Возвращаемый словарь
        for i in range(1, pages+1): 
            player_list = {} #Нужная вещь
            a = [] #Нужная вещь x2
            i = str(i)
            urls = ["?pvp=0&page="+i, "/clans&page="+i, "?pvp=1&page="+i, "?pvp=2&page="+i, "/fightValor?page="+i, "/invasionValor?page="+i, "/tourneyValor?page="+i, "/towerValor?page="+i, "/throneValor?page="+i, "/clanTourneyValor?page="+i, "/armyValor?page="+i, "/clanSurvivalValor?page="+i]
            response = self.session.get(self.url+"best"+urls[category-1], headers=self.headers) #Посылаем GET запрос
            html = response.text #Получаем HTML код страницы
            if "Вы кликаете слишком быстро" in html:
                time.sleep(2)
                self.best(pages, category)
            if "Рейтинг лучших" or "Боевая доблесть" in html: #Проверяем, нужную ли страницу нашли
                soup = BS(html, "html.parser")
                rating_ = soup.find("table", class_="wa").findAll("td", class_="yell") #Находим позиции и рейтинг игроков
                names = soup.find("table", class_="wa").findAll("a") #Находим имена игроков
                position = [] #Нужная вещь x3
                rating = [] #Нужная вещь x4
                for j in range(0, len(rating_)):
                    if j % 2 == 0: #Если индекс элемента четный то это позиция игрока
                        position.append(rating_[j].text)
                    else: #Иначе его рейтинг
                        rating.append(rating_[j].text)
                for j in range(0, 16 if category != 2 else 15):
                    if position[j] != "10000": #Условие чтобы ваш профиль не отображался
                        player_list["position"] = position[j]
                        player_list["name"] = names[j].text
                        player_list["rating"] = rating[j]
                        a.append(player_list)
                        player_list = {}
                data[i] = a
        return data
    

    def train(self): #Узнать наш уровень тренировки
        data = { #Заготовка на вывод
            "strength": {},
            "health": {},
            "defense": {}
        }
        response = self.session.get(self.url+"train", headers=self.headers) #Посылаем GET запрос
        html = response.text #Получаем HTML код страницы
        if "Вы кликаете слишком быстро" in html:
            time.sleep(2)
            self.train()
        soup = BS(html, "html.parser")
        elems = soup.findAll("span", class_="darkgreen_link font_15") #Находим прибавки к аттрибутам
        data["strength"]["bonus"] = elems[0].text
        data["health"]["bonus"] = elems[1].text
        data["defense"]["bonus"] = elems[2].text
        elems = soup.findAll("div", class_="ml68") #Находим уровни тренировок
        levels = []
        for elem in elems:
            levels.append(elem.text.split(":")[1].split("из")[0].replace(" ", "")) #Обрабатываем их
        data["strength"]["level"] = levels[0]
        data["health"]["level"] = levels[1]
        data["defense"]["level"] = levels[2]
        elems = soup.findAll("span", class_="ur") #Находим цену и валюту следующего улучшения
        cost = []
        currency = []
        for elem in elems: #Обрабатываем их
            cost.append(elem.text.split("за ")[1])
            currency_ = elem.find_next("img")["src"].split("/")[-1]
            if currency_ == "gold.png":
                currency.append("gold")
            else:
                currency.append("silver")
        data["strength"]["cost"] = cost[0]
        data["health"]["cost"] = cost[1]
        data["defense"]["cost"] = cost[2]
        data["strength"]["currency"] = currency[0]
        data["health"]["currency"] = currency[1]
        data["defense"]["currency"] = currency[2]
        return data
    

    def task(self, category: int = 1): #Узнать сюжетные/ежедневные задания
        data = {} #Заготовка на выход
        task = {} #Нужная вещь
        categories = ["task", "task/daily"]
        response = self.session.get(self.url+categories[category-1], headers=self.headers) #Посылаем GET запрос
        html = response.text #Получаем HTML код страницы
        if "Вы кликаете слишком быстро" in html:
            time.sleep(2)
            self.task(category)
        soup = BS(html, "html.parser")
        elems = soup.findAll("div", class_="wr8") #Находим нужные элементы
        result = [] #Будем сохранять необработанные данные сюда
        task_ = [] #Список для текстов заданий
        level = [] #Текущий прогресс на задании
        level_required = [] #Нужный уровень для выполнения
        for elem in elems:
            result.append(elem.text.replace("\n", "").replace("\t", "")) #Обрабатываем каждый элемент и сохраняем его
        result = result[1:] #Обрезаем заголовок
        for i in result: #Обрабатываем каждый пункт и сохраняем их
            task_.append(i.split(":")[0].split("Прогресс")[0].strip())
            level.append(i.split(":")[1].split("из")[0].replace(" ", ""))
            level_required.append(i.split("из ")[1].replace(" ", ""))
        for i in range(0, len(task_)): #Записываем их в словарь data
            task["task"] = task_[i]
            task["level"] = level[i]
            task["level_required"] = level_required[i]
            data[str(i)] = task
            task = {}
        return data
    

    def clan(self, id: str): #Узнаем информацию о клане (ВАЖНО! Может работать некорректно с некоторыми кланами. У всех разный HTML код, в будущем возможно эта проблема решится)
        data = {} #Заготовка на вывод
        response = self.session.get(self.url+"clan?id="+str(id), headers=self.headers) #Посылаем GET запрос
        html = response.text #Получаем HTML код страницы
        if "Вы кликаете слишком быстро" in html: #Проверка на нужную страницу
            time.sleep(2)
            self.clan(id)
        if "Хочу в клан!" in html: #Проверка что данный клан существует
            return "Incorect clan id at 'clan'"
        if "О клане" in html: #Проверка на нужную страницу x2
            soup = BS(html, "html.parser")
            try:
                data["name"] = soup.find("div", class_="rr").text.replace("\n", "").replace("\t", "")
            except AttributeError:
                data["name"] = soup.find("div", class_="bold").text.replace("\n", "").replace("\t", "") #Получаем название клана
            data["description"] = soup.find("span", class_="green_dark").text.replace("\n", "").replace("\t", "")[2:]
            elems = soup.find("div", class_="mlr10").text.split("\n")
            for elem in elems: #Получаем информацию клана
                if elem != "":
                    if "О клане" not in elem:
                        if "Основан" in elem:
                            data["founded"] = elem.split(":")[1].strip()
                        elif "Уровень" in elem:
                            data["level"] = elem.split(":")[1].strip()
                        elif "Опыт" in elem:
                            data["exp"] = elem.split(":")[1].split("из")[0].replace(" ", "")
                            try:
                                data["exp_required"] = elem.split(":")[1].split("из")[1].replace(" ", "")
                            except:
                                pass
            elem = soup.findAll("a", class_="mb2")[2]
            data["buildings_percent"] = elem.text.split("(")[1].split(")")[0]
        time.sleep(0.5)
        response = self.session.get(self.url+"builds?id="+str(id), headers=self.headers) #Посылаем GET запрос
        html = response.text #Получаем HTML код страницы
        if "строения" in html: #Получаем информацию о строениях
            soup = BS(html, "html.parser")
            elems = soup.findAll("a", class_="lwhite")
            for elem in elems:
                elem = elem.text
                if "из" in elem:
                    if "Академия" in elem:
                        data["academy_level"] = elem.split("(")[1].split("из")[0].replace(" ", "")
                    elif "Архивы" in elem:
                        data["archives_level"] = elem.split("(")[1].split("из")[0].replace(" ", "")
                    elif "лавка" in elem:
                        data["magical_shop_level"] = elem.split("(")[1].split("из")[0].replace(" ", "")
                    elif "зал" in elem:
                        data["trophy_room_level"] = elem.split("(")[1].split("из")[0].replace(" ", "")
                    elif "Оружейная" in elem:
                        data["armory_level"] = elem.split("(")[1].split("из")[0].replace(" ", "")
                    elif "Обелиск" in elem:
                        data["obelisk_of_valor_level"] = elem.split("(")[1].split("из")[0].replace(" ", "")
                    elif "Дом" in elem:
                        data["house_of_herolds_level"] = elem.split("(")[1].split("из")[0].replace(" ", "")
                    elif "совет" in elem:
                        data["military_council_level"] = elem.split("(")[1].split("из")[0].replace(" ", "")
        return data

    
    def chest(self): #Узнать содержимое сумки
        data = {} #Заготовка на вывод
        item = {} #Нужная вещь
        response = self.session.get(self.url+"chest", headers=self.headers) #Посылаем GET запрос
        html = response.text #Получаем HTML код страницы
        soup = BS(html, "html.parser")
        elems = soup.findAll("div", class_="wr8") #Находим нужные нам элементы
        j = 0 #Нужная вещь x2
        for elem in elems:
            j += 1
            elem = elem.text.replace("\t", "").split("\n") #Обработка элемента
            item_ = [] #Нужная вещь x3
            for i in elem:
                if i != "":
                    item_.append(i)
            item["item"] = item_[0]
            item["rarity"] = item_[1].split("[")[0].replace(" ", "")
            item["level"] = item_[1].split("[")[1].split("/")[0]
            item["level_max"] = item_[1].split("/")[1].split("]")[0]
            data[j] = item
            item = {}
        return data
    

    def gear(self, id: str = None): #Узнать снаряжения игрока
        data = {} #Заготовка на вывод
        if id == None: #Узнаем у себя если id не указан
            response = self.session.get(self.url+"gear", headers=self.headers) #Посылаем GET запрос
        else: #Узнаем снаряжение у другого игрока
            response = self.session.get(self.url+"view_gear?player_id="+str(id), headers=self.headers) #Посылаем GET запрос
        html = response.text #Получаем HTML код страницы
        if "Вы кликаете слишком быстро" in html: #Проверка на нужную страницу
            time.sleep(2)
            self.gear(id)
        if "Снаряжение" in html: #Проверка на нужную страницу x2
            names = []
            rarities = []
            levels = []
            levels_max = []
            runes = [""] * 10
            gems = [""] * 10
            differences = [""] * 10
            sharpenings = [""] * 10
            output = {}
            i = 0
            soup = BS(html, "html.parser")
            elems = soup.findAll("div", class_="wr8") #Получаем все элементы
            for elem in elems:
                i += 1
                for link in elem.findAll("a"):
                    if link.text != "" and link.text != "В сумку":
                        names.append(link.text) #Находим название
                for span in elem.findAll("span"):
                    if span.has_attr("class") and len(span["class"][0]) == 2:
                        rarities.append(span.text.split('[')[0][:-1]) #Находим редкость
                        levels.append(span.text.split("[")[1].split("/")[0]) #Находим текущий уровень
                        levels_max.append(span.text.split("/")[1].split("]")[0]) #Находим максимальный уровень
                    if span.has_attr("class") and len(span["class"][0]) != 2:
                        runes[i-1] = span.text #Проверка на наличие руны
                    if span.has_attr("class") and span["class"][0] == "win":
                        differences[i-1] = span.text.replace("\n", "").replace("\t", "").replace(" ", "") #Отличие от нашей вещи (работает только на других пользователях и только если у них есть вещь лучше вашей)
                for gem in elem.findAll("div", class_="mt5"):
                    img = gem.find("img")
                    if img != None and img.has_attr("class") and len(img["class"]) == 2:
                        gems[i-1] = gem.text.replace("\n", "").replace("\t", "").replace(" ", "") #Проверка на наличие самоцвета
                    link = gem.find("a")
                    if link != None and link["href"].startswith("/view"):
                        res = gem.text.replace("\n", "").replace("\t", "").replace(" ", "").split("+")[-1] #Находим заточку
                        if res.isdigit():
                            sharpenings[i-1] = res
            for i in range(0, len(names)):
                output["name"] = names[i]
                output["rarity"] = rarities[i]
                output["level"] = levels[i]
                output["level_max"] = levels_max[i]
                output["rune"] = runes[i]
                output["gem"] = gems[i]
                output["difference"] = differences[i]
                output["sharpening"] = sharpenings[i]
                data[str(i+1)] = output
                output = {}
        return data
    

    def schedule(self): #Узнать расписание битв
        data = {} #Заготовка на вывод
        response = self.session.get(self.url+"schedule", headers=self.headers) #Посылаем GET запрос
        html = response.text #Получаем HTML код страницы
        if "Вы кликаете слишком быстро" in html: #Проверка на нужную страницу
            time.sleep(2)
            self.schedule()
        if "Расписание" in html: #Проверка на нужную страницу x2
            soup = BS(html, "html.parser")
            data["current_time"] = ":".join(soup.find("div", class_="lblue").text.replace("\t", "").replace("\n", "").replace(" ", "").split(":")[1:]).strip()[:-3] #Находим текущее время
            times = soup.findAll("li", class_="mb10")
            for time_ in times: #Находим оставшееся время до битв
                time_ = time_.text.replace("\t", "").replace("\n", "").strip()
                if "Турнир героев" in time_:
                    data["tournament"] = time_.split("через")[1].replace("ч", "h").replace("м", "m").replace("д", "d").strip()
                elif "Вторжение" in time_:
                    data["invasion"] = time_.split("через")[1].replace("ч", "h").replace("м", "m").replace("д", "d").strip()
                elif "Турнир кланов" in time_:
                    data["clanTourney"] = time_.split("через")[1].replace("ч", "h").replace("м", "m").replace("д", "d").strip()
                elif "Войны кланов" in time_:
                    data["army"] = time_.split("через")[1].replace("ч", "h").replace("м", "m").replace("д", "d").strip()
                elif "Остров сокровищ" in time_:
                    data["clanSurvival"] = time_.split("через")[1].replace("ч", "h").replace("м", "m").replace("д", "d").strip()
                elif "Осада башен" in time_:
                    data["tower"] = time_.split("через")[1].replace("ч", "h").replace("м", "m").replace("д", "d").strip()
                elif "Битва за престол" in time_:
                    data["throne"] = time_.split("через")[1].replace("ч", "h").replace("м", "m").replace("д", "d").strip()
        return data
    

    def coliseum(self): #Узнать информацию о колизее
        data = {} #Заготовка на вывод
        response = self.session.get(self.url+"pvp", headers=self.headers) #Посылаем GET запрос
        html = response.text #Получаем HTML код страницы
        if "Вы кликаете слишком быстро" in html: #Проверка на нужную страницу
            time.sleep(2)
            self.coliseum()
        if "Ваш рейтинг" in html: #Проверка на нужную страницу x2
            soup = BS(html, "html.parser")
            elem = soup.find("div", class_="wr8") #Находим информацию
            txts = []
            for i in elem.text.replace("\t", "").split("\n"):
                if i != "":
                    txts.append(i.strip())
            data["rating"] = txts[0].split(":")[1] #Находим рейтинг
            data["league"] = txts[1][1:] #Находим лигу
            data["season_end"] = " ".join(txts[2].split(" ")[3:]).replace("ч", "h").replace("м", "m").replace("д", "d") #Находим время, оставшееся до конца сезона
        return data
    

    def chat(self, id: str = "0", pages: int = 1): #Получить сообщения из чата
        data = {} #Заготовка на вывод
        message = {} #Нужная вещь
        i = 0 #Нужная вещь x2
        for page in range(1, pages+1):
            response = self.session.get(self.url+"chat?id="+str(id)+"?page="+str(page), headers=self.headers) #Посылаем GET запрос
            html = response.text #Получаем HTML код страницы
            if "Вы кликаете слишком быстро" in html: #Проверка на нужную страницу
                time.sleep(2)
                self.chat()
            if "Отправить" in html: #Проверка на нужную страницу x2
                soup = BS(html, "html.parser")
                elems = soup.findAll("div", class_="mb5") #Получаем все элементы с сообщениями
                for elem in elems: #Проходимся по каждому из них
                    if len(elem["class"]) == 1:
                        i += 1
                        elem = elem.text
                        message["nickname"] = elem.split("(»):")[0].strip() #Узнаем никнейм
                        message["text"] = elem.split("(»):")[1].strip() #Узнаем текст
                        data[str(i)] = message
                        message = {}
        return data
    

    def amulet(self, id: str = None): #Узнать информацию об амулете
        data = {} #Заготовка на вывод
        if id == None: #Если узнаем у себя
            response = self.session.get(self.url+"amulet", headers=self.headers) #Посылаем GET запрос
        else: #Если узнаем у человека с указанным ID
            response = self.session.get(self.url+"view_amulet?player_id="+str(id), headers=self.headers) #Посылаем GET запрос
        html = response.text #Получаем HTML код страницы
        if "Вы кликаете слишком быстро" in html: #Проверка на нужную страницу
            time.sleep(2)
            self.amulet(id)
        if "Амулет" in html: #Проверка на нужную страницу
            soup = BS(html, "html.parser")
            elem = soup.find("div", class_="wr8")
            if id != None:
                try:
                    data["difference"] = elem.find("div", class_="win").text.split(":")[1].strip() #Находим различие, если амулет чужой
                except:
                    pass
            data["level"] = elem.find("span", class_="lblue").text.split(":")[1].split("из")[0].strip() #Находим качество амулета
            a = [] #Нужная вещь
            for i in elem.text.replace("\t", "").split("\n"): #Обработка данных
                if i != "":
                    a.append(i)
            a = a[2:] #Обработка данных x2
            data["parametrs_bonus"] = a[0].split("к")[0].strip() #Находим бонус к параметрам
            data["exp_bonus"] = a[1].split("к")[0].strip() #Находим бонус к опыту
            data["silver_bonus"] = a[2].split("к")[0].strip() #Находим бонус к серебру
            if id == None: #Если парсим свой амулет
                btn = soup.find("span", class_="ur")
                data["upgrade_cost"] = btn.text.split("за")[1].strip() #Находим стоимость улучшения
                img = btn.find("img")
                if "silver" in img["src"]: #Находим валюту
                    data["upgrade_currency"] = "silver"
                elif "gold" in img["src"]:
                    data["upgrade_currency"] = "gold"
        return data
    

    def abilities(self, id: str = None): #Узнать умения игрока
        data = {} #Заготовка на вывод
        obj = {} #Нужная вещь
        if id == None: #Если узнаем у себя
            response = self.session.get(self.url+"ability", headers=self.headers) #Посылаем GET запрос
        else: #Или если узнаем у игрока с данным ID
            response = self.session.get(self.url+"view_abilities?player_id="+str(id), headers=self.headers) #Посылаем GET запрос
        html = response.text #Получаем HTML код страницы
        if "Вы кликаете слишком быстро" in html: #Проверка на нужную страницу
            time.sleep(2)
            self.abilities(id)
        if "Умения" in html: #Проверка на нужную страницу x2
            soup = BS(html, "html.parser")
            elems = soup.findAll("div", class_="wr8") #Находим все элементы
            a = [] #Нужная вещь x2
            for elem in elems:
                for i in elem.text.replace("\t", "").split("\n"):
                    if i != "" and i != "Активное" and i != " ":
                        a.append(i)
                if "Уворот" in a[0]: #Отдельная обработка для уворота
                    obj["percents"] = "".join(a[0].split(" ")[1]).strip() #Находим шанс/кулдаун/прибавку
                else:
                    obj["percents"] = "".join(a[0].split(" ")[-1]).strip()
                obj["bonus"] = a[1].split(":")[1].strip() #Находим бонус
                obj["level"] = a[2].split(":")[1].split("из")[0].strip() #Находим уровень прокачки
                names = {"Ярость": "rage", "Пробивание": "punch", "Круговой": "round_hit", "Блок": "block", "Защита": "protect", "Парирование": "parry", "Уворот": "dodge", "Лечение": "health", "Уклонение": "evasion"}
                data[names[a[0].split(" ")[0].strip()]] = obj
                obj = {}
                a = []
        return data


    def trophies(self, id: str = None): #Узнать трофеи игрока
        data = {"trophies": []} #Заготовка на вывод
        if id == None: #Если узнаем у себя
            response = self.session.get(self.url+"trophies", headers=self.headers) #Посылаем GET запрос
        else: #Если узнаем у игрока с этим ID
            response = self.session.get(self.url+"view_trophies?player_id="+str(id), headers=self.headers) #Посылаем GET запрос
        html = response.text #Получаем HTML код страницы
        if "Вы кликаете слишком быстро" in html: #Проверка на нужную страницу
            time.sleep(2)
            self.trophies(id)
        if "Трофеи" in html: #Проверка на нужную страницу x2
            soup = BS(html, "html.parser")
            elems = soup.findAll("a", class_="medium") #Находим все элементы
            for elem in elems:
                if elem.text != "":
                    data["trophies"].append(elem.text) #Заносим их в список
        return data


    def oracle_quests(self, category: int = 0): #Узнать задания оракула (для кольца/печати)
        data = {} #Заготовка на вывод
        obj = {} #Нужная вещь
        categories = ["ring", "seal"] #Вместо if
        response = self.session.get(self.url+"oracle/quests?category="+categories[category], headers=self.headers) #Посылаем GET запрос
        html = response.text #Получаем HTML код страницы
        if "Вы кликаете слишком быстро" in html: #Проверка на нужную страницу
            time.sleep(2)
            self.oracle_quests(category)
        if "Кольца" in html or "Печати" in html: #Проверка на нужную страницу
            soup = BS(html, "html.parser")
            names = [] #Список для заданий
            levels = [] #Список для их прогресса
            levels_max = [] #Список для уровней, которые надо пройти
            for name in soup.findAll("span", class_="lwhite"):
                if not "bold" in name["class"]:
                    names.append(name.text.replace("\t", "").strip()) #Ищем все задания
            for level in soup.findAll("span"):
                if level.has_attr("class") and ("green2" in level["class"] or "succes" in level["class"]):
                    levels.append(level.text.split(":")[1].split("из")[0].strip() if not "Завершено" in level.text.strip() else "completed") #Ищем прогресс
                    levels_max.append(level.text.split("из")[1].strip() if not "Завершено" in level.text.strip() else None) #Ищем чтото_нейм (см. levels_max)
                if level.has_attr("class") and level["class"] == "small lorange tdn".split():
                    data["completed"] = level.text.replace("\t", "").split("Выполнено")[1].split("из")[0].strip() + "/" + level.text.replace("\t", "").split("из")[1].strip() #Ищем сколько заданий выполнено
            for i in range(len(names)):
                obj["name"] = names[i]
                obj["level"] = levels[i]
                obj["level_max"] = levels_max[i]
                data[str(i+1)] = obj
                obj = {}
        return data


    def rarity_shop(self): #Узнаем вещи из лавки редкостей
        data = {} #Заготовка на вывод
        obj = {} #Нужная вещь
        response = self.session.get(self.url+"rarityShop", headers=self.headers) #Посылаем GET запрос
        html = response.text #Получаем HTML код страницы
        if "Вы кликаете слишком быстро" in html: #Проверка на нужную страницу
            time.sleep(2)
            self.rarity_shop()
        if "Лавка редкостей" in html: #Проверка на нужную страницу x2
            soup = BS(html, "html.parser")
            names = [] #Список для названий предметов
            counts = [] #Список для кол-ва/уровня вещей
            prices = [] #Список для цены вещей
            currencies = [] #Список для валюты вещей
            for name in soup.findAll("a", class_="white"):
                names.append(name.text) #Находим названия вещей
            for count in soup.findAll("span", class_="lblue"):
                if count.text != " | ":
                    if count.text == "":
                        counts.append("1") #Находим их кол-во/уровень
                    else:
                        counts.append(count.text.replace("шт.", "").replace("ур.", "lvl.").strip()) #Находим их кол-во/уровень x2
            for price in soup.findAll("span", class_="cntr"):
                prices.append(price.text) #Находим их цену
                currencies.append(price.find("img")["src"].split("/")[-1].split(".")[0]) #Находим их валюты
            data["time_left"] = " ".join(soup.find("span", id="rarity_shop_timer").text.split()[1:]).replace("м", "m").replace("с", "c") #Находим сколько времени осталось но нового предмета
            for i in range(len(names)):
                obj["item"] = names[i]
                obj["count"] = counts[i]
                obj["price"] = prices[i]
                obj["currency"] = currencies[i]
                data[str(i+1)] = obj
                obj = {}
        return data


    def talisman(self, id: str = None):
        data = {} #Заготовка на вывод
        if id == None: #Если узнаем у себя
            response = self.session.get(self.url+"talisman", headers=self.headers) #Посылаем GET 
        else:
            response = self.session.get(self.url+"talisman?player_id="+id, headers=self.headers)
        html = response.text
        if "Вы кликаете слишком быстро" in html: #Проверка на нужную страницу
            time.sleep(2)
            self.talisman(id)
        if "Талисман" in html: #Проверка на нужную страницу x2
            soup = BS(html, "html.parser")
            elem = soup.find("div", class_="wr8")
            data["level"] = elem.find("div", class_="mb5").text.replace("\t", "").replace("\n", "").split(":")[1].split("из")[0].strip()
            bonuses = elem.findAll("div", class_="lorange")
            data["strength"] = bonuses[0].text.replace("\t", "").replace("\n", "").split()[0]
            data["health"] = bonuses[1].text.replace("\t", "").replace("\n", "").split()[0]
            data["defense"] = bonuses[2].text.replace("\t", "").replace("\n", "").split()[0]
            if id != None:
                try:
                    data["difference"] = bonuses[3].text.replace("\t", "").replace("\n", "").split()[1]
                except:
                    pass
        return data


    #=================================================================
    #========================POST ЗАПРОСЫ=============================
    #=================================================================


    def send_message(self, id: str = "0", message: str = "hi"): #Функция отправки сообщения в чат
        if len(message) < 2 or len(message) > 500: #Проверка на длину сообщения
            return f"Invalid length: {len(message)} at '{message}'"
        request = self.session.post(self.url+"chat_message", data={
            "message_text": message, #Текст сообщения
            "answer_id": "0",
            "page": "1", #Сам не знаю что это
            "clan_id": str(id) #Если ID - 0, то пишем в глобал чат, или в клан с этим ID
        }, headers=self.headers) #Посылаем POST запрос
        return f"Sended: '{message}' to {id}" if str(request) == "<Response [200]>" else request #Выводим сообщение об успехе если код состояния 200, или выводим