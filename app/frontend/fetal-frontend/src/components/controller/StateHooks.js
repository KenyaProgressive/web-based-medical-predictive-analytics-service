import { useQuery } from '@tanstack/react-query';

const fetchAllData = async () => {
    const response = await fetch('http://localhost:8080/getState');
    if (!response.ok) {
        console.log("from error ");
        throw new Error('Ошибка сети');

    }
    // console.log("from fetchAllData ", response.json());
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