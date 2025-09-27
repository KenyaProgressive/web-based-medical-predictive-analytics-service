// import Card from "@/app/dashboard/Card";
import DashboardCard from "./Card";

import {
    Card,
    CardAction,
    CardContent,
    CardDescription,
    CardFooter,
    CardHeader,
    CardTitle,
} from "@/components/ui/card"

export default function Dashboard() {

    let hypoxy = {
        'status': 1,
        'title': "Гипоксия"
    };

    let state = {
        'hypoxy': hypoxy
    };

    let ok_status = "bg-slate-100"
    let warn_status = "bg-yellow-300"
    let alert_status = "bg-red-400"

    return (
        <div className="w-full h-full grid grid-cols-3 grid-rows-3s gap-4">

            <DashboardCard param={state.hypoxy.status} param_title={state.hypoxy.title} />
            <DashboardCard param={state.hypoxy.status} param_title={state.hypoxy.title} />
            <DashboardCard param={state.hypoxy.status} param_title={state.hypoxy.title} />
            {/* <DashboardCard param={state.hypoxy.status} param_title={state.hypoxy.title} /> */}
            {/* <DashboardCard param={state.hypoxy.status} param_title={state.hypoxy.title} /> */}
            {/* <DashboardCard param={state.hypoxy.status} param_title={state.hypoxy.title} /> */}
            <DashboardCard param={state.hypoxy.status} param_title={state.hypoxy.title} />
            <DashboardCard param={state.hypoxy.status} param_title={state.hypoxy.title} />
            <DashboardCard param={state.hypoxy.status} param_title={state.hypoxy.title} />

        </div >
    )
}
