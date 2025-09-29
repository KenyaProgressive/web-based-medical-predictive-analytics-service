// import Card from "@/app/dashboard/Card";
import DashboardCard from "./DashboardCard";
import CARD_STATUSES from "../consts/consts"

import {
    Card,
    CardAction,
    CardContent,
    CardDescription,
    CardFooter,
    CardHeader,
    CardTitle,
} from "@/components/ui/card"

export default function Dashboard({ card_params, notify_params }) {

    // card priority = columns by a card

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


    let ok_color = "bg-slate-100"
    let warn_color = "bg-yellow-300"
    let alert_color = "bg-red-400"
    return (
        <div className="w-full h-full grid grid-cols-6 grid-rows-4 gap-4">
            {state.card_params.map(param =>
                < DashboardCard color={param.status === 2 ? alert_color : param.status === 1 ? warn_color : ok_color} key={param.title} param={param.status} param_title={param.title} rows={param.rows} cols={param.cols} />
            )}
        </div >
    )
}