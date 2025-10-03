
import random
from time import sleep
from fastapi import FastAPI
from app.config import BackendLogger
from fastapi.middleware.cors import CORSMiddleware
import os


from app.emulator.datahandler import DataHandler

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.backend import funcs
from app.backend.funcs import PriorityList

app = FastAPI()

# Монтируем статические файлы (CSS, JS, изображения)
# app.mount("/_next", StaticFiles(directory=os.path.join(OUT_PATH, "_next")), name="_next")
# app.mount("/static", StaticFiles(directory=os.path.join(OUT_PATH, "_next","static")), name="static")

out_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../frontend/fetal-frontend/out'))
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
        "http://127.0.0.1:8080"
        # Возможно придется делать то же самое для итоговой версии, но по идее нет.
    ],
    allow_credentials=True,
    allow_methods=["GET"],
)

predict_notifications = PriorityList()
fact_notifications = PriorityList()


@app.get("/getState")
async def get_state():

    global priority_list

    ctg_data = DataHandler.result

    BackendLogger.debug(ctg_data)

    if "decelerations_per_30_min" in list(ctg_data.keys()):
        BackendLogger.debug(ctg_data["decelerations_per_30_min"])
        fact_notifications.add_items(ctg_data["decelerations_per_30_min"])

    state = {
        'card_params': [
                {
                'title': "ЧСС (уд/мин)",
                'value': int(ctg_data["baseline"]),
                'status': funcs.status_bpm(ctg_data["baseline"]),
                'rows': 2,
                'cols': 2,
                'id': 1
                },
            {
                'title': "Кратковременная вариабельность",
                'value': round(ctg_data["short_term_variability"], 2),
                'status': funcs.status_variable(ctg_data),
                'rows': 1,
                'cols': 1,
                'id': 2
            },
            {
                'title': "Долговременная вариабельность",
                'value': round(ctg_data["long_term_variability"], 2),
                'status': funcs.status_variable(ctg_data),
                'rows': 1,
                'cols': 1,
                'id': 3
            },
            {
                'title': "Акцелерации",
                'value': len(ctg_data['accelerations_per_30_min']) or "Нет данных",
                'status': funcs.status_acceleration(ctg_data['accelerations_per_30_min'] or "Нет данных"),
                'rows': 1,
                'cols': 2,
                'id': 4
            }
        ],

        'notifications' : [
            {
                'values': []
            },
            {
                'values': []
            }
        ]
    }
    
    return {'state': state}

# Все остальные запросы отправляем на index.html
@app.get("/{full_path:path}")
async def serve_react_app(full_path: str):
    return FileResponse(os.path.join(out_path, "index.html"))
