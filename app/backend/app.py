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

count = 1 # временная переменная для временного дебага

@app.get("/getState")
async def connection_test():

    global count

    count = (count % 3) + 1

    state = {
        'card_params': [
                {
                'value': 1,
                'status': count+1,
                'title': "ЧСС",
                'rows': 1,
                'cols': 1,
                'id': 1
                },
            {
                'value': 1,
                'status': count,
                'title': "Сокращения матки",
                'rows': 1,
                'cols': 1,
                'id': 2
            }

        ]
    }
    
    return {'state': state}