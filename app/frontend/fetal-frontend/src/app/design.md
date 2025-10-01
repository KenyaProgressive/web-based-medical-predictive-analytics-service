Дешборд:
1. Карточка абсолютного значения ЧСС. Если тахикардия или брадикардия - цвет карточки отображает статус того или другого + мб надпись
2. Карточка вариабильности ритма (Зеленый если 5-25, Желтый/Красный если <5)

3. Журнал: уведомления с приоритетом. Заполнен стек - достаем с наименьшей приоритетностью. Если все приоритетности одинаковые - смотрим по таймштампу.

4. Уведомление: если децелерация, то с указанием их количества за последние 10 мин


CONFIG:
- Приотетность уведомлений


<h1>json`ы</h1>

Уведомления (предикт):
- Время
- Приоритетность (из конфига)
- Название

Уведомления (факт):
- Время
- Приоритетность (из конфига)











    let dec_early = {
        'value': 1,
        'status': CARD_STATUSES.OK,
        'title': "Ранние децелерации",
        'rows': 1,
        'cols': 1
    }

    let dec_late = {
        'value': 1,
        'status': 1,
        'title': "Поздние децелерации",
        'rows': 1,
        'cols': 1
    }


    let decelarations = {
        'dec_early': dec_early,
        'dec_late': dec_late
    }

    let hr_variability = {
        'value': 1,
        'status': CARD_STATUSES.OK,
        'title': "Вариабильность",
        'rows': 1,
        'cols': 1
    }

    let accelerations = {
        'value': 1,
        'status': 2,
        'title': "Акцелерации",
        'rows': 1,
        'cols': 1
    }

    let heart_rate = {
        'value': 1,
        'status': 1,
        'title': "ЧСС",
        'rows': 1,
        'cols': 1
    }

    let hypoxy = {
        'status': CARD_STATUSES.warn_status,
        'title': "Гипоксия",
        'priority': "4"
    };

    let tachycardia = {
        'status': CARD_STATUSES.OK,
        'title': "Тахикардия",
    }

    let bradycardia = {
        'status': CARD_STATUSES.OK,
        'title': "Брадикардия",
    }

    let state = {
        'card_params': [heart_rate, accelerations, hr_variability, decelarations.dec_early, decelarations.dec_late],
        'notify_params': [hypoxy, tachycardia, bradycardia],
        'decelarations': [],
        'events': []
    };

    let decelerations_per_30_min = [
        {
            'apmlitude': 30,
            'duration': 15,
            // всякая прочая хуйня
            'type': "late"
        },
        {
            'apmlitude': 30,
            'duration': 15,
            // всякая прочая хуйня
            'type': "early"
        },
        {
            'apmlitude': 30,
            'duration': 15,
            // всякая прочая хуйня
            'type': "huy"
        }
    ];
