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
        self.start_date = datetime.strptime(start_date, "%Y-%m-%d").date()

class MobileNetwork:
    def __init__(self):
        self.subscribers = []
    
    def load_from_file(self, filename):
        self.subscribers = []  
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            if not lines or len(lines) < 2:
                return
            
            for line in lines[1:]:
                line = line.strip()
                if line:
                    parts = line.split(';')
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
    
    def save_to_file(self, filename):
        with open(filename, 'w', encoding='utf-8') as file:
            file.write("Фамилия;Инициалы;Телефон;Тариф;ГБ;Минуты;СМС;Платеж (год);Дата\n")
            for sub in self.subscribers:
                file.write(f"{sub.last_name};{sub.initials};{sub.phone};{sub.tariff};"
                          f"{sub.gigabytes};{sub.minutes};{sub.sms};{sub.payment};"
                          f"{sub.start_date.strftime('%Y-%m-%d')}\n")
    
    def add_subscriber(self, subscriber):
        self.subscribers.append(subscriber)
    
    def delete_subscriber(self, phone):
        for i, sub in enumerate(self.subscribers):
            if sub.phone == phone:
                del self.subscribers[i]
                return True
        return False
    
    def edit_subscriber(self, phone, new_data):
        for sub in self.subscribers:
            if sub.phone == phone:
                for key, value in new_data.items():
                    setattr(sub, key, value)
                return True
        return False
