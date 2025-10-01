import { useQuery } from '@tanstack/react-query';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

const fetchAllData = async () => {
    const response = await fetch('http://localhost:8080/getState');
    if (!response.ok) {
        throw new Error('Ошибка сети');
    }
    return response.json();
};

export const useAppState = (isEnabled = false) => {
    return useQuery({
        queryKey: ['allState'],
        queryFn: fetchAllData,
        refetchInterval: 500,
        enabled: isEnabled,
    });
};