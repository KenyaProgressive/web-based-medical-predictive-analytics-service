
import { useAppState } from "@/components/controller/StateHooks";
import {
    Card,
    CardAction,
    CardContent,
    CardDescription,
    CardFooter,
    CardHeader,
    CardTitle,
} from "@/components/view/card"
import { STATUS_STYLES } from "@/components/consts/consts"

export default function AlertHistory() {
    const { data, isLoading, error } = useAppState();
    const state = !isLoading && data ? data.state.notifications : [{ "values": [] }, { "values": [] }];

    return (
        <div className="grid grid-cols-2 bg-slate-400 w-full min-h-[300px] h-full p-0 gap-2">
            {state[0]&&<AlertList notifications={state[0].values} title={"Фактические уведомления"} />}
            {state[1]&&<AlertList notifications={state[1].values} title={"Предиктивные уведомления"} />}
        </div>
    )
}



function AlertList({ notifications, title }) {

    return (
        <Card className={`flex flex-col w-full h-full gap-0 p-2 `}>
            <CardTitle className="flex justify-center p-2 ">{title}</CardTitle>
            <div className="DATA_COLUMNS flex flex-col-reverse h-full">
                <CardContent className="gap-0 p-0">
                    {notifications && notifications.map(notification =>
                        <AlertNotification key={notification.title} title={notification.title} status={notification.status} />
                    )}
                </CardContent>
                {notifications.length === 0 && <h1 className="flex h-full items-center justify-center">Уведомления отсутствуют</h1>}
            </div>
        </Card >
    )
}

function AlertNotification({ status, title }) {
    const statusMask = STATUS_STYLES[status] || STATUS_STYLES[0];
    return (
        <Card className={`min-h-[100px] bg-slate-400 mt-2 ${statusMask}`}>
            <CardHeader><CardTitle>
                {title}
            </CardTitle></CardHeader>
            <CardContent>
                <h1> + характеристики аномалии (Soon)</h1>
            </CardContent>
        </Card>
    )
}