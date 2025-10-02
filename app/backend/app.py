import random
from time import sleep
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI()

out_path = os.path.join(os.path.dirname( __file__ ), '../frontend/fetal-frontend/out')

# Монтируем статические файлы (CSS, JS, изображения)
app.mount("/_next", StaticFiles(directory=os.path.join(out_path, "_next")), name="_next")
app.mount("/static", StaticFiles(directory=os.path.join(out_path, "_next","static")), name="static")


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        # У Реакта свой мини-сервер для быстрой отладки, я говорил.
        # У него порт 3000, поэтому разрешаем подключение с 3000 порта
        "http://localhost:3000",
        "http://localhost:8080",
        # Возможно придется делать то же самое для итоговой версии, но по идее нет.
    ],
    allow_credentials=True,
    allow_methods=["GET"],
)

# @app.get("/")
# async def connection_test():
#     return {"status": "SUCCESS"}


# Вот тут тебе нужно короче досоставить стейт по образцу и раскидать в него значения из ML-слоя
# Самое сложное будет следить за полем current_notifications


# STATUSES: 0 = OK (green), 1 = WARN (yellow), 2 = ALERT (red) 
# МАКСИМАЛЬНЫЙ РАЗМЕР СПИСКА УВЕДОМЛЕНИЙ = 8

# if it.priority > priority then delete and push
# if it.priotiy == priority then if it.time > it.time then delete and push

# запись в файл сразу как получил с ML

@app.get("/getState")
async def connection_test():
    # sleep(0.5)

    rand_status = random.randint(1,3)

    state = {
        'card_params': [
                {
                'title': "ЧСС",
                'value': random.randint(1,180),
                'status': rand_status % 3+1,
                'rows': 2,
                'cols': 2,
                'id': 1
                },
            {
                'title': "Сокращения матки",
                'value': random.randint(1,180),
                'status': rand_status % 3+2,
                'rows': 1,
                'cols': 1,
                'id': 2
            },
            {
                'title': "Акцелерации",
                'value': random.randint(1,180),
                'status': rand_status % 3-1,
                'rows': 1,
                'cols': 1,
                'id': 3
            },
            {
                'title': "Вариабельность (?)",
                'value': random.randint(1,180),
                'status': rand_status,
                'rows': 1,
                'cols': 2,
                'id': 4
            }

        ],
        'notifications' : [
            {
                'title': "Фактические уведомления",
                'values': [
                    {
                        'title':"Высокий риск гипоксии",
                        'description':"Ваще пиздец всему",
                        'status':2,
                        'priority':2,
                        'id' : 88
                    },
                    {
                        'title':"Децелерация",
                        'description':"Ну такое",
                        'status':1,
                        'priority':2,
                        'id' : 99
                    }
                ],
            },
            {
                'title': "Предиктивные уведомления",
                'values': [
                    # {
                    #     'title':"Хуепоксия",
                    #     'description':"Ваще пиздец всему",
                    #     'status':2,
                    #     'id' : 81
                    # },
                    # {
                    #     'title':"Хулелерация",
                    #     'description':"Ну такое",
                    #     'status':1,
                    #     'id' : 91
                    # }
                    ],
            }
        ]
    }
    
    return {'state': state}

# Все остальные запросы отправляем на index.html
@app.get("/{full_path:path}")
async def serve_react_app(full_path: str):
    return FileResponse(os.path.join(out_path, "index.html"))
