// import CARD_STATUSES from "../consts/consts"

import {
    Card,
    CardAction,
    CardContent,
    CardDescription,
    CardFooter,
    CardHeader,
    CardTitle,
} from "@/components/ui/card"

export default function DashboardCard({ param }) {
    let ok_status = "bg-slate-100"
    let warn_status = "bg-yellow-300"
    let alert_status = "bg-red-400"

    return (
        <Card className={`min-h-[100px] h-full ${param.status === 2 ? alert_status : param.status === 1 ? warn_status : ok_status} col-span-` + param.cols + ` row-span-` + param.rows}>
            <CardHeader>
                <CardTitle>Получение данных:</CardTitle>
                <CardTitle>{param.title}</CardTitle>
            </CardHeader>
        </Card>
    )
}