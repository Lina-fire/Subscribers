import sys
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTableWidgetItem, 
                            QMessageBox, QInputDialog, QHeaderView)
from PyQt5 import uic

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

class MobileNetworkApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.network = MobileNetwork()
        self.init_ui()
        self.update_table()

    def init_ui(self):
        uic.loadUi('mobile_form.ui', self)
        self.setWindowTitle('Мобильная сеть')
        self.setMinimumSize(1200, 600)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.btn_load.clicked.connect(self.load_data)
        self.btn_save.clicked.connect(self.save_data)
        self.btn_add.clicked.connect(self.add_data)
        self.btn_edit.clicked.connect(self.edit_data)
        self.btn_delete.clicked.connect(self.delete_data)
        self.btn_delete_all.clicked.connect(self.delete_all_data)

    def load_data(self):
        self.network.load_from_file('mobile_data.txt')
        self.update_table()
        QMessageBox.information(self, 'Успех', 'Данные загружены успешно!')

    def save_data(self):
        if not self.network.subscribers:
            QMessageBox.warning(self, 'Ошибка', 'Нет данных для сохранения')
            return
        self.network.save_to_file('mobile_data.txt')
        QMessageBox.information(self, 'Успех', 'Данные сохранены успешно!')

    def update_table(self):
        self.tableWidget.setRowCount(len(self.network.subscribers))
        for row, sub in enumerate(self.network.subscribers):
            self.tableWidget.setItem(row, 0, QTableWidgetItem(sub.last_name))
            self.tableWidget.setItem(row, 1, QTableWidgetItem(sub.initials))
            self.tableWidget.setItem(row, 2, QTableWidgetItem(sub.phone))
            self.tableWidget.setItem(row, 3, QTableWidgetItem(sub.tariff))
            self.tableWidget.setItem(row, 4, QTableWidgetItem(str(sub.gigabytes)))
            self.tableWidget.setItem(row, 5, QTableWidgetItem(str(sub.minutes)))
            self.tableWidget.setItem(row, 6, QTableWidgetItem(str(sub.sms)))
            self.tableWidget.setItem(row, 7, QTableWidgetItem(str(sub.payment)))
            self.tableWidget.setItem(row, 8, QTableWidgetItem(sub.start_date.strftime('%Y-%m-%d')))

    def add_data(self):
        last_name, ok = QInputDialog.getText(self, 'Добавление', 'Введите фамилию:')
        if not ok: return
        
        initials, ok = QInputDialog.getText(self, 'Добавление', 'Введите инициалы:')
        if not ok: return
        
        phone, ok = QInputDialog.getText(self, 'Добавление', 'Введите телефон:')
        if not ok: return
        
        tariff, ok = QInputDialog.getText(self, 'Добавление', 'Введите тариф:')
        if not ok: return
        
        gigabytes, ok = QInputDialog.getInt(self, 'Добавление', 'Введите количество ГБ:')
        if not ok: return
        
        minutes, ok = QInputDialog.getInt(self, 'Добавление', 'Введите количество минут:')
        if not ok: return
        
        sms, ok = QInputDialog.getInt(self, 'Добавление', 'Введите количество СМС:')
        if not ok: return
        
        payment, ok = QInputDialog.getDouble(self, 'Добавление', 'Введите годовой платеж:')
        if not ok: return
        
        new_sub = Subscriber(
            last_name, initials, phone, tariff, gigabytes,
            minutes, sms, payment, datetime.now().strftime('%Y-%m-%d')
        )
        self.network.add_subscriber(new_sub)
        self.update_table()
        QMessageBox.information(self, 'Успех', 'Абонент добавлен успешно!')

    def edit_data(self):
        if not self.network.subscribers:
            QMessageBox.warning(self, 'Ошибка', 'Нет данных для редактирования')
            return
            
        phone, ok = QInputDialog.getText(self, 'Редактирование', 'Введите телефон абонента:')
        if not ok: return
        
        subscriber = None
        for sub in self.network.subscribers:
            if sub.phone == phone:
                subscriber = sub
                break
        
        if not subscriber:
            QMessageBox.warning(self, 'Ошибка', 'Абонент не найден')
            return
            
        new_data = {}
        
        last_name, ok = QInputDialog.getText(self, 'Редактирование', 'Фамилия:', text=subscriber.last_name)
        if ok: new_data['last_name'] = last_name
        
        initials, ok = QInputDialog.getText(self, 'Редактирование', 'Инициалы:', text=subscriber.initials)
        if ok: new_data['initials'] = initials
        
        tariff, ok = QInputDialog.getText(self, 'Редактирование', 'Тариф:', text=subscriber.tariff)
        if ok: new_data['tariff'] = tariff
        
        gigabytes, ok = QInputDialog.getInt(self, 'Редактирование', 'ГБ:', value=subscriber.gigabytes)
        if ok: new_data['gigabytes'] = gigabytes
        
        minutes, ok = QInputDialog.getInt(self, 'Редактирование', 'Минуты:', value=subscriber.minutes)
        if ok: new_data['minutes'] = minutes
        
        sms, ok = QInputDialog.getInt(self, 'Редактирование', 'СМС:', value=subscriber.sms)
        if ok: new_data['sms'] = sms
        
        payment, ok = QInputDialog.getDouble(self, 'Редактирование', 'Платеж:', value=subscriber.payment)
        if ok: new_data['payment'] = payment
        
        if new_data:
            self.network.edit_subscriber(phone, new_data)
            self.update_table()
            QMessageBox.information(self, 'Успех', 'Данные обновлены успешно!')

    def delete_data(self):
        if not self.network.subscribers:
            QMessageBox.warning(self, 'Ошибка', 'Нет данных для удаления')
            return
            
        phone, ok = QInputDialog.getText(self, 'Удаление', 'Введите телефон абонента:')
        if not ok: return
        
        if self.network.delete_subscriber(phone):
            self.update_table()
            QMessageBox.information(self, 'Успех', 'Абонент удален успешно!')
        else:
            QMessageBox.warning(self, 'Ошибка', 'Абонент не найден')

    def delete_all_data(self):
        if not self.network.subscribers:
            QMessageBox.warning(self, 'Ошибка', 'Нет данных для удаления')
            return
            
        reply = QMessageBox.question(
            self, 'Подтверждение', 
            'Вы действительно хотите удалить ВСЕ данные?', 
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            self.network.subscribers = []
            self.update_table()
            QMessageBox.information(self, 'Успех', 'Все данные удалены!')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MobileNetworkApp()
    window.show()
    sys.exit(app.exec_())
