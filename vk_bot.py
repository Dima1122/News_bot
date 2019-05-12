import bs4 as bs4
import requests
from news_finder import get_news


class VkBot:

    def __init__(self, user_id, auth):
        print("Создан объект бота!")

        self._USER_ID = user_id
        self._USERNAME = self._get_user_name_from_vk_id(user_id)
        self.auth = auth
        self._COMMANDS = ["ki"]

    def _get_user_name_from_vk_id(self, user_id):
        request = requests.get("https://vk.com/id"+str(user_id))
        bs = bs4.BeautifulSoup(request.text, "html.parser")

        user_name = self._clean_all_tag_from_str(bs.findAll("title")[0])

        return user_name.split()[0]

    def new_message(self, message):
        # Привет
        if message.lower() == self._COMMANDS[0]:
            self.auth.add(self._USER_ID)
            global autorized
            autorized = self.auth
            return f"Привет, {self._USERNAME}!"

        # Время
        elif self._USER_ID in self.auth:
            res = get_news(message.lower())
            if len(res) < 4096:
                return res
            else:
                return f"Извини, {self._USERNAME}, попробуй другое слово :/"
            

        else:
            pass

    def _get_time(self):
        request = requests.get("https://my-calend.ru/date-and-time-today")
        b = bs4.BeautifulSoup(request.text, "html.parser")
        return self._clean_all_tag_from_str(str(b.select(".page")[0].findAll("h2")[1])).split()[1]

    @staticmethod
    def _clean_all_tag_from_str(string_line):

        """
        Очистка строки stringLine от тэгов и их содержимых
        :param string_line: Очищаемая строка
        :return: очищенная строка
        """

        result = ""
        not_skip = True
        for i in list(string_line):
            if not_skip:
                if i == "<":
                    not_skip = False
                else:
                    result += i
            else:
                if i == ">":
                    not_skip = True

        return result
