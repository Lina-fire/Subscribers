from datetime import datetime

class Subscriber:
    def __init__(self, last_name, initials, phone, tariff, gigabytes, minutes, sms, payment, start_date):
        self.last_name = last_name
        self.initials = initials
        self.phone = phone
        self.tariff = tariff
        self.gigabytes = gigabytes
        self.minutes = minutes
        self.sms = sms
        self.payment = payment
        self.start_date = datetime.strptime(start_date, "%d.%m.%Y").date()

    def to_dict(self):
        return {
            'Фамилия': self.last_name,
            'Инициалы': self.initials,
            'Телефон': self.phone,
            'Тариф': self.tariff,
            'ГБ': str(self.gigabytes),
            'Минуты': str(self.minutes),
            'СМС': str(self.sms),
            'Платеж (год)': str(self.payment),
            'Дата': self.start_date.strftime("%Y-%m-%d")
        }

class MobileNetwork:
    SORT_FIELD = 'last_name'
    
    def __init__(self):
        self.subscribers = []
    
    def load_from_file(self, filename):
        self.subscribers = []
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if line:
                    parts = line.split('/')
                    if len(parts) == 9:
                        self.subscribers.append(Subscriber(
                            parts[0].strip(),
                            parts[1].strip(),
                            parts[2].strip(),
                            parts[3].strip(),
                            int(parts[4]),
                            int(parts[5]),
                            int(parts[6]),
                            float(parts[7]),
                            parts[8].strip()
                        ))
        return bool(self.subscribers)
    
    def save_to_file(self, filename):
        with open(filename, 'w', encoding='utf-8') as file:
            for sub in self.subscribers:
                file.write(
                    f"{sub.last_name}/{sub.initials}/{sub.phone}/{sub.tariff}/"
                    f"{sub.gigabytes}/{sub.minutes}/{sub.sms}/{sub.payment}/"
                    f"{sub.start_date.strftime('%d.%m.%Y')}\n"
                )
        return True
    
    def sort_subscribers(self, reverse=False):
        """Сортировка по константному полю"""
        self.subscribers.sort(key=lambda x: getattr(x, self.SORT_FIELD), reverse=reverse)
    
    def add_subscriber(self, subscriber_data):
        new_sub = Subscriber(**subscriber_data)
        self.subscribers.append(new_sub)
        return True
    
    def delete_subscriber(self, phone):
        for i, sub in enumerate(self.subscribers):
            if sub.phone == phone:
                del self.subscribers[i]
                return True
        return False
    
    def find_subscriber(self, phone):
        for sub in self.subscribers:
            if sub.phone == phone:
                return sub
        return None
    
    def edit_subscriber(self, phone, new_data):
        sub = self.find_subscriber(phone)
        if sub:
            for key, value in new_data.items():
                setattr(sub, key, value)
            return True
        return False
    
    def search_by_phone(self, phone):
        result = []
        for sub in self.subscribers:
            if sub.phone == phone:
                result.append(sub.to_dict())
        return result
