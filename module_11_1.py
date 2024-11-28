import pprint

# Сторонняя библиотека requests используется для выполнения HTTP-запросов на Python.
# Основные методы: get, post, delete, put, patch.
import requests

# PIL (Python Imaging Library) - это бесплатная Python-библиотека для открытия, работы и сохранения различных
# форматов изображений. К сожалению, ее разработка окончательно остановилась, а последнее обновление вышло в 2009.
# К счастью, есть Pillow — активно развивающийся форк PIL с простой установкой.
from PIL import Image, ImageTk
import tkinter as tk

def show_imge(path):
    image_window = tk.Tk()
    img = ImageTk.PhotoImage(Image.open(path))
    panel = tk.Label(image_window, image=img)
    panel.pack(side="bottom", fill="both")#, expand="yes")
    image_window.mainloop()

# большинство значений этих констант получено при регистрации на сайте https://genius.com
ACCESS_TOKEN = "SYFqU09mZuxpRIDm3FZ-2z2eHhs6ntcFIIG7Dko8ldo-4DJO6sLbPsPBeLXp-U0M"
RANDOM_GENRE_API_URL = "https://binaryjazz.us/wp-json/genrenator/v1/genre"
GENIUS_API_URL = "https://api.genius.com/search"
GENIUS_URL = "https://genius.com"
# "https://genius.com/songs/3297075/apple_music_player" - можно послушать отрезок песни

# Когда используется метод get, все данные формы кодируются в URL-адрес и добавляются к URL-адресу действия
# в качестве параметров строки запроса.
# Имеются ограничения на объем данных, которые могут быть отправлены, поскольку данные отправляются по URL.
# Этот метод извлекает данные с сервера по указанному URL-адресу и возвращает их обратно в локальную среду Python.
# Обычно используется для доступа к веб-страницам, загрузки файлов или использования данных из API.
genre = requests.get(RANDOM_GENRE_API_URL)

# проверка,что ответ сервера действительно содержит JSON-данные.
if genre.ok and 'application/json' in genre.headers.get('Content-Type', ''):
    try:
        # JSON (JavaScript Object Notation) - это текстовый формат обмена данными.
        # Формат JSON похож на словари в Python
        # Метод json() преобразует полученные от сервера данные в формат JSON
        genre_json_data = genre.json()
    except:
        genre_json_data = None  # Обрабатываем ситуацию некорректного JSON.
        print(f"Не обработать данные, полученные от {RANDOM_GENRE_API_URL}. Попробуйте её раз запустить программу.")
        exit(1)
data = requests.get(GENIUS_API_URL, params={"access_token": ACCESS_TOKEN, 'q': genre_json_data})
pprint.pprint(data.json())
data = data.json()
try:
    image_url = data["response"]['hits'][0]['result']['header_image_url']#'api_path']
except:# IndexError:
    image_url = ''  # Обрабатываем ситуацию некорректного JSON.
    print(f"Не удалось получить путь к изображению. Попробуйте её раз запустить программу.")
    exit(1)

print(f"{image_url}")

image_data = requests.get(image_url, stream=True)
image_data.raise_for_status()
with open("image.jpg", 'wb') as fd:
    # Некоторые файлы, которые вы загружаемые из Интернета с помощью модуля Requests,
    # могут иметь огромный размер. В таких случаях неразумно загружать весь ответ или
    # файл в память сразу. Вы можете загрузить файл по кускам или фрагментам, используя метод iter_content().
    for chunk in image_data.iter_content(chunk_size=50000):
        print('Получен кусок данных')
        fd.write(chunk)

# открываем сохранённый файл с изображением
with Image.open("image.jpg") as image:
    print(f"image.format: {image.format}")
    print(f"image.size: {image.size}")
    print(f"image.mode: {image.mode}")

    # показываем полученное изображение
    show_imge("image.jpg")

    # изменяем размер изображения
    image = image.resize((400, 300))
    print(f"После изменения размеров image.size: {image.size}")

    # делаем изображение черно-белым
    image = image.convert('L')

    # поворачиваем изображение на 45 градусов
    image = image.rotate(45)

    # сохраняем полученное изображение
    image.save("new_image.jpg")

    # показываем изменённое изображение
    show_imge("new_image.jpg")




