from bs4 import BeautifulSoup
import requests
import time


# Курс и разница
cur, variance = 0, ''


def chasing_course():
    # Http запрос bank.uz
    respond = requests.get('https://bank.uz/currency').text

    bs = BeautifulSoup(respond, 'lxml')

    # Отслежка курса
    course = bs.find('div', class_='tabs-a')
    course = course.find_all('span', class_='medium-text')[1].text.split(' ')
    course = float(''.join(course))

    global cur, variance

    # Разница старого и нового курса
    if cur != course and cur - course > 0 and cur != 0:
        variance = f'Курс увеличился на {cur - course}uzs.'
        # Новый курс
        cur = course
        return cur, variance
    elif cur != course and cur - course < 0 and cur != 0:
        variance = f'Курс уменьшился на {course - cur}uzs.'
        # Новый курс
        cur = course
        return cur, variance
    else:
        pass

    time.sleep(3)

    # Рекурсия
    chasing_course()


def main():
    # Вызов функции
    chasing_course()

    api_bot = 'https://api.telegram.org/bot<ТОКЕН БОТА>'
    user_id = 'ВАШ ТЕЛЕГРАМ ID'

    # Http запрос для отправки сообщения через телеграм бот
    requests.get(api_bot + f'/sendMessage?chat_id={user_id}&text={variance}\nТекущий курс 1$ = {cur}uzs')

    # Рекурсия
    main()


if __name__ == '__main__':
    main()
