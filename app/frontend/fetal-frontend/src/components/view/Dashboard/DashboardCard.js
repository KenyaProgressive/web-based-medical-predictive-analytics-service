import { STATUS_STYLES, DASHBOARD_ANIMATION } from "@/components/consts/consts"

import {
    Card,
    CardAction,
    CardContent,
    CardDescription,
    CardFooter,
    CardHeader,
    CardTitle,
} from "@/components/view/card"

export default function DashboardCard({ param }) {
    const statusMask = STATUS_STYLES[param.status] || STATUS_STYLES[0];

    return (
        <Card className={`min-h-[100px] h-full ${statusMask} ${DASHBOARD_ANIMATION} col-span-` + param.cols + ` row-span-` + param.rows}>
            <CardHeader>
                <CardTitle>{param.title}</CardTitle>
            </CardHeader>
        </Card>
    )
}