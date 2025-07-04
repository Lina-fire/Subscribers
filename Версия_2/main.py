import sys
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTableWidget, QTableWidgetItem, 
                            QVBoxLayout, QHBoxLayout, QWidget, QPushButton, 
                            QInputDialog, QMessageBox, QHeaderView, QDialog)
from PyQt5.QtCore import Qt

class ResultWindow(QDialog):
    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setMinimumSize(800, 400)
        
        self.table = QTableWidget()
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        
        layout = QVBoxLayout()
        layout.addWidget(self.table)
        self.setLayout(layout)
    
    def show_data(self, data, headers):
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.setRowCount(len(data))
        
        for row_idx, row_data in enumerate(data):
            for col_idx, field in enumerate(headers):
                item = QTableWidgetItem(str(row_data.get(field, '')))
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                self.table.setItem(row_idx, col_idx, item)
        
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        
        self.exec_()

class MobileNetworkManager(QMainWindow):
    SORT_FIELD = 'Фамилия'  
    
    def __init__(self):
        super().__init__()
        self.filename = 'mobile_data.txt'
        self.data = []
        self.fieldnames = ['Фамилия', 'Инициалы', 'Телефон', 'Тариф', 'ГБ', 'Минуты', 'СМС', 'Платеж (год)', 'Дата']
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Управление мобильной сетью')
        self.setMinimumSize(1500, 600)
        self.table = QTableWidget()
        self.table.setColumnCount(len(self.fieldnames))
        self.table.setHorizontalHeaderLabels(self.fieldnames)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setRowCount(0)
        
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)

        self.load_btn = QPushButton('Загрузить данные')
        self.load_btn.clicked.connect(self.load_data)

        self.add_btn = QPushButton('Добавить данные')
        self.add_btn.clicked.connect(self.add_data)

        self.edit_btn = QPushButton('Изменить данные')
        self.edit_btn.clicked.connect(self.edit_data)

        self.delete_btn = QPushButton('Удалить данные')
        self.delete_btn.clicked.connect(self.delete_data)

        self.delete_all_btn = QPushButton('Удалить ВСЕ данные')
        self.delete_all_btn.clicked.connect(self.delete_all_data)
        self.delete_all_btn.setStyleSheet("background-color: #ff9999;")

        self.save_btn = QPushButton('Сохранить данные')
        self.save_btn.clicked.connect(self.save_data)

        self.sort_btn = QPushButton('Сортировка по фамилии')
        self.sort_btn.clicked.connect(self.sort_data)

        self.search_btn = QPushButton('Поиск по телефону')
        self.search_btn.clicked.connect(self.search_data)

        self.exit_btn = QPushButton('Выход')
        self.exit_btn.clicked.connect(self.close)

        button_layout1 = QHBoxLayout()
        button_layout1.addWidget(self.load_btn)
        button_layout1.addWidget(self.add_btn)
        button_layout1.addWidget(self.edit_btn)
        button_layout1.addWidget(self.delete_btn)
        button_layout1.addWidget(self.delete_all_btn)

        button_layout2 = QHBoxLayout()
        button_layout2.addWidget(self.save_btn)
        button_layout2.addWidget(self.sort_btn)
        button_layout2.addWidget(self.search_btn)
        button_layout2.addWidget(self.exit_btn)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.table)
        main_layout.addLayout(button_layout1)
        main_layout.addLayout(button_layout2)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def load_data(self):
        """Загрузка данных из файла"""
        file = open(self.filename, 'r', encoding='utf-8')
        lines = file.readlines()
        file.close()
        
        self.data = []
        if lines:
            for line in lines[1:]:
                values = line.strip().split(';')
                if len(values) == len(self.fieldnames):
                    self.data.append(dict(zip(self.fieldnames, values)))
        
        self.update_table()
        QMessageBox.information(self, 'Успех', 'Данные успешно загружены!')

    def save_data(self):
        """Сохранение данных в файл"""
        file = open(self.filename, 'w', encoding='utf-8')
        file.write(';'.join(self.fieldnames) + '\n')
        for row in self.data:
            file.write(';'.join(str(row.get(field, '')) for field in self.fieldnames) + '\n')
        file.close()
        
        QMessageBox.information(self, 'Успех', 'Данные успешно сохранены!')

    def update_table(self):
        """Обновление основной таблицы"""
        self.table.setRowCount(len(self.data))
        for row_idx, row_data in enumerate(self.data):
            for col_idx, field in enumerate(self.fieldnames):
                item = QTableWidgetItem(str(row_data.get(field, '')))
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                self.table.setItem(row_idx, col_idx, item)

    def add_data(self):
        """Добавление новой записи"""
        new_entry = {}
        for field in self.fieldnames[:-1]:
            value, ok = QInputDialog.getText(self, 'Добавление', f'Введите {field}:')
            if not ok:
                return
            new_entry[field] = value
        
        new_entry['Дата'] = datetime.now().strftime("%Y-%m-%d")
        self.data.append(new_entry)
        self.update_table()
        QMessageBox.information(self, 'Успех', 'Данные успешно добавлены!')

    def edit_data(self):
        """Редактирование записи"""
        if not self.data:
            QMessageBox.warning(self, 'Ошибка', 'Нет данных для редактирования')
            return
        
        row, ok = QInputDialog.getInt(self, 'Редактирование', 'Введите номер строки:', 1, 1, len(self.data))
        if not ok:
            return
        
        row_idx = row - 1
        edited_data = self.data[row_idx].copy()
        
        for field in self.fieldnames[:-1]:
            value, ok = QInputDialog.getText(self, 'Редактирование', 
                                          f'{field} (текущее: {self.data[row_idx].get(field, "")}):',
                                          text=str(self.data[row_idx].get(field, '')))
            if ok:
                edited_data[field] = value
        
        edited_data['Дата'] = datetime.now().strftime("%Y-%m-%d")
        self.data[row_idx] = edited_data
        self.update_table()
        QMessageBox.information(self, 'Успех', 'Данные успешно изменены!')

    def delete_data(self):
        """Удаление записи"""
        if not self.data:
            QMessageBox.warning(self, 'Ошибка', 'Нет данных для удаления')
            return
        
        row, ok = QInputDialog.getInt(self, 'Удаление', 'Введите номер строки:', 1, 1, len(self.data))
        if not ok:
            return
        
        row_idx = row - 1
        del self.data[row_idx]
        self.update_table()
        QMessageBox.information(self, 'Успех', 'Данные успешно удалены!')

    def delete_all_data(self):
        """Удаление всех данных"""
        if not self.data:
            QMessageBox.warning(self, 'Ошибка', 'Нет данных для удаления')
            return
        
        reply = QMessageBox.question(self, 'Подтверждение', 
                                   'Вы действительно хотите удалить ВСЕ данные?',
                                   QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            self.data = []
            self.update_table()
            QMessageBox.information(self, 'Успех', 'Все данные успешно удалены!')

    def sort_data(self):
        """Сортировка данных по фамилии"""
        if not self.data:
            QMessageBox.warning(self, 'Ошибка', 'Нет данных для сортировки')
            return
        
        reverse = QMessageBox.question(self, 'Сортировка', 'Сортировать по убыванию?', 
                                     QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes
        
        self.data.sort(key=lambda x: x.get(self.SORT_FIELD, ''), reverse=reverse)
        self.update_table()
        QMessageBox.information(self, 'Успех', f'Данные отсортированы по {self.SORT_FIELD}!')

    def search_data(self):
        """Поиск данных по номеру телефона"""
        if not self.data:
            QMessageBox.warning(self, 'Ошибка', 'Нет данных для поиска')
            return
        
        phone, ok = QInputDialog.getText(self, 'Поиск', 'Введите номер телефона:')
        if not ok:
            return
        
        found = [row for row in self.data if row['Телефон'] == phone]
        if not found:
            QMessageBox.information(self, 'Поиск', 'Абонент не найден')
        else:
            result_window = ResultWindow("Результаты поиска", self)
            result_window.show_data(found, self.fieldnames)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MobileNetworkManager()
    window.show()
    sys.exit(app.exec_())
