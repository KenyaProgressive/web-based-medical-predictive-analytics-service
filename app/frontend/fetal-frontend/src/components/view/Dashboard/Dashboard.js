import DashboardCard from "./DashboardCard";
import { useAppState } from "@/components/controller/StateHooks";
import { useState } from "react";
import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogHeader,
    DialogTitle,
    DialogTrigger,
} from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import {
    Card
} from "@/components/view/card"

import { defaultDashboard } from "../DefaultStates";

export default function Dashboard() {
    const [isPolling, setIsPolling] = useState(false)
    const { data, isLoading, isError } = useAppState(isPolling);
    const state = !isLoading && data ? data.state : defaultDashboard;
    const triggerPolling = () => {
        console.log("clicked ", isPolling);
        setIsPolling(!isPolling);
    }
    console.log("from Dashboard ", state);
    return (
        <div className="w-full h-full grid grid-cols-2 grid-rows-4 gap-2">
            {state.card_params.map(param =>
                <DashboardCard key={param.id} param={param} />
            )}

            <Dialog>
                <DialogTrigger>
                    <div variant="outline" className="rounded-sm flex justify-center items-center w-full h-[70px] bg-slate-200 hover:bg-slate-100"><p className="font-bold">Import</p></div>
                </DialogTrigger>
                <DialogContent>
                    <DialogHeader>
                        <DialogTitle>Вставьте ссылку на CSV файл</DialogTitle>
                        <DialogDescription>
                            This action cannot be undone. This will permanently delete your account
                            and remove your data from our servers.
                        </DialogDescription>
                    </DialogHeader>
                </DialogContent>
            </Dialog>

            <Button onClick={() => triggerPolling()} variant="outline" className="font-bold w-full h-[70px] bg-slate-200">
                {isPolling ? "Закончить процедуру" : "Начать процедуру"}
            </Button>
        </div >
    )
}