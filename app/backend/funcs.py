from app.const import STATUS_OK, STATUS_WARN, STATUS_ALERT
from app.ml.bpm_signal_analyzer import HeartRateChange

def status_bpm(bpm: float) -> int:
    if bpm >= 120.0 and bpm <= 160.0:
        return STATUS_OK
    elif (bpm >= 100.0 and bpm <= 120.0) or (bpm >= 160.0 and bpm <= 180.0):
        return STATUS_WARN
    elif bpm < 100.0 or bpm > 180.0:
        return STATUS_ALERT


def status_variable(variables: dict) -> int:
    
    short_variable, long_variable = variables["short_term_variability"], variables["long_term_variability"]

    if (short_variable >= 6.0 and short_variable <= 25.0) or (long_variable >= 17.0):
        return STATUS_OK
    elif (short_variable >= 3.0 and short_variable <= 5.0) or (long_variable >= 10.0 and long_variable <= 16.0):
        return STATUS_WARN
    elif (short_variable < 3.0) or (long_variable < 10.0):
        return STATUS_ALERT

def status_acceleration(accelerations: list) -> int:
    value = len(accelerations)
    if value > 5:
        return STATUS_OK
    elif value >= 1 and value <= 4:
        return STATUS_WARN
    elif value == 0:
        return STATUS_ALERT
    

def status_decelarations(decelartions: list[HeartRateChange]) -> int:

    dec_status = set()

    for deceleration in decelartions:
        dec_status.add(deceleration["type"])
    
    if "prolongued" in dec_status or "variable" in dec_status:
        return STATUS_ALERT
    
    elif "moderate" in dec_status or "late" in dec_status:
        return STATUS_WARN
    
    elif "light" in dec_status or "early" in dec_status:
        pass
    


class PriorityItem:
    def __init__(self, priority, timestamp, data):
        self.priority = priority
        self.timestamp = timestamp
        self.data = data

class PriorityList:
    MAX_SIZE = 8

    def __init__(self):
        self.items = []

    def __add_item(self, new_item):
        # Если список не заполнен, просто добавить новый элемент
        if len(self.items) < self.MAX_SIZE:
            self.items.append(new_item)
            return

        # Поиск кандидата на замену: объекта с приоритетом МЕНЬШЕ, чем у нового
        candidate_index = None
        for i, item in enumerate(self.items):
            if item.priority < new_item.priority:
                candidate_index = i
                break

        # Если нашли кандидата с низким приоритетом - заменить его
        if candidate_index is not None:
            removed_item = self.items.pop(candidate_index)
            self.items.append(new_item)
            print(f"Заменен объект с низким приоритетом: {removed_item}")
            return

        # Иначе ищем самый старый объект с ТАКИМ ЖЕ приоритетом, как у нового
        candidate_index = None
        for i, item in enumerate(self.items):
            if item.priority == new_item.priority:
                if candidate_index is None or item.timestamp < self.items[candidate_index].timestamp:
                    candidate_index = i

        # Если нашли кандидата для замены по timestamp - заменить его
        if candidate_index is not None:
            removed_item = self.items.pop(candidate_index)
            self.items.append(new_item)
            print(f"Заменен самый старый объект с таким же приоритетом: {removed_item}")
            return

        # Если не нашли кандидата для замены - новый объект не добавляется
        print("Новый объект не добавлен: нет подходящего кандидата для замены")

    def add_items(self, new_list):
        for item in new_list:
            self.__add_item(PriorityItem(item["priority"], item["duration"], item))