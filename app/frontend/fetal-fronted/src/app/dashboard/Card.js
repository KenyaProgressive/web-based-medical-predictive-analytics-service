import {
    Card,
    CardAction,
    CardContent,
    CardDescription,
    CardFooter,
    CardHeader,
    CardTitle,
} from "@/components/ui/card"

export default function DashboardCard({ param, param_title }) {
    let ok_status = "bg-slate-100"
    let warn_status = "bg-yellow-300"
    let alert_status = "bg-red-400"

    return (
        <Card className={`min-h-[300px] ${param === 2 ? alert_status : param === 1 ? warn_status : ok_status}`}>
            <CardHeader>
                <CardTitle>Data to be loaded:</CardTitle>
                <CardTitle>{param_title}</CardTitle>
            </CardHeader>
        </Card>
    )
}
