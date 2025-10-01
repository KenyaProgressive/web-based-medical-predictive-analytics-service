import random
from time import sleep
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

global count
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        # У Реакта свой мини-сервер для быстрой отладки, я говорил.
        # У него порт 3000, поэтому разрешаем подключение с 3000 порта
        "http://localhost:3000",
        # Возможно придется делать то же самое для итоговой версии, но по идее нет.
    ],
    allow_credentials=True,
    allow_methods=["GET"],
)

@app.get("/test")
async def connection_test():
    return {"status": "SUCCESS"}


# Вот тут тебе нужно короче досоставить стейт по образцу и раскидать в него значения из ML-слоя
# Самое сложное будет следить за полем current_notifications

# count = 1 # временная переменная для временного дебага

@app.get("/getNotifications")
async def get_notifications():
    sleep(0.5)

    notifications = [
            {
                'title': "Фактические уведомления",
                'values': [
                    {
                        'title':"Гипоксия",
                        'description':"Ваще пиздец всему",
                        'status':2,
                        'id' : 88
                    },
                    {
                        'title':"Децелерация",
                        'description':"Ну такое",
                        'status':1,
                        'id' : 99
                    }
                ],
            },
            {
                'title': "Предиктивные уведомления",
                'values': [
                    {
                        'title':"Хуепоксия",
                        'description':"Ваще пиздец всему",
                        'status':2,
                        'id' : 81
                    },
                    {
                        'title':"Хулелерация",
                        'description':"Ну такое",
                        'status':1,
                        'id' : 91
                    }],
            }
        ]
    return {'notifications': notifications}
    


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
                        'id' : 88
                    },
                    {
                        'title':"Децелерация",
                        'description':"Ну такое",
                        'status':1,
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



# @app.get("/test/jigle_bell")
# async def connection_test():
    
#     global status_jigle

#     status_jigle = (status_jigle % 3) + 1

#     state = {
#         'card_params': [
#                 {
#                 'value': 1,
#                 'status': (status_jigle % 3)+1,
#                 'title': "ЧСС",
#                 'rows': 1,
#                 'cols': 1,
#                 'id': 1
#                 },
#             {
#                 'value': 1,
#                 'status': status_jigle,
#                 'title': "Сокращения матки",
#                 'rows': 1,
#                 'cols': 1,
#                 'id': 2
#             }

#         ]
#     }
    
#     return {'state': state}