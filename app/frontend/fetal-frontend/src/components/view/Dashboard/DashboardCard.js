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
    const size = param.id === 1 ? "text-[12vw]" : "text-[3vw]";
    // console.log(param.rows, param.title);
    return (
        <Card className={`min-h-[100px] h-full ${statusMask} ${DASHBOARD_ANIMATION} col-span-` + param.cols + ` row-span-` + param.rows}>
            <CardHeader>
                <CardTitle>{param.title}</CardTitle>
            </CardHeader>
            <CardContent className="h-full flex justify-center items-center">
                {param && <p className={size}>{param.value}</p>}
            </CardContent>
        </Card>
    )
}