import DashboardCard from "./DashboardCard";
import { useAppState } from "@/components/controller/StateHooks";

import {
    Card
} from "@/components/view/card"

import { defaultDashboard } from "../DefaultStates";

export default function Dashboard() {

    const { data, isLoading, isError } = useAppState();
    const state = !isLoading ? data.state : defaultDashboard;

    return (
        <div className="w-full h-full grid grid-cols-2 grid-rows-4 gap-2">
            {state.card_params.map(param =>
                <DashboardCard key={param.id} param={param} />
            )}

            <Card className="col-span-2 items-center bg-pink-300" >
                Панель управления (soon)
            </Card>

        </div >
    )
}