"use client"
import Dashboard from "@/components/view/Dashboard/Dashboard";
import AlertHistory from "@/components/view/History/AlertHistory"

import { QueryClient, QueryClientProvider } from '@tanstack/react-query';


export default function Home() {
  const queryClient = new QueryClient();

  return (
    <QueryClientProvider client={queryClient}>
      <div className="bg-slate-400 grid xl:grid-cols-6 md:grid-cols-5 md:grid-rows-auto p-4 gap-6">

        <div className="col-span-2">
          <Dashboard />
        </div>

        <div className="xl:col-span-4 md:col-span-4">
          <AlertHistory />
        </div>

      </div>
    </QueryClientProvider>
  )
}