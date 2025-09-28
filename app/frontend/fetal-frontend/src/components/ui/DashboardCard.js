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

export default function DashboardCard({ color, param_title, rows, cols }) {
    let ok_status = "bg-slate-100"
    let warn_status = "bg-yellow-300"
    let alert_status = "bg-red-400"

    return (
        <Card className={`min-h-[100px] h-full ${color} col-span-` + cols + ` row-span-` + rows}>
            <CardHeader>
                <CardTitle>Получение данных:</CardTitle>
                <CardTitle>{param_title}</CardTitle>
            </CardHeader>
        </Card>
    )
}