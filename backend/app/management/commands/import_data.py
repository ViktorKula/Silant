import os
import pandas as pd
from django.core.management.base import BaseCommand
from app.models import Maintenance

class Command(BaseCommand):
    help = 'Импорт данных из Excel'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Путь к Excel-файлу')
        parser.add_argument('--sheet_name', type=str, help='Имя листа для импорта', default=None)

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']
        sheet_name = kwargs['sheet_name'].strip()  # Удаление лишних пробелов

        # Проверка на существование файла
        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f'Файл не найден: {file_path}'))
            return

        # Получение списка листов
        xls = pd.ExcelFile(file_path)
        self.stdout.write(self.style.SUCCESS(f'Доступные листы: {", ".join(xls.sheet_names)}'))

        # Проверка наличия листа
        if sheet_name not in xls.sheet_names:
            self.stdout.write(self.style.ERROR(f'Лист "{sheet_name}" не найден в файле.'))
            return

        data = pd.read_excel(file_path, engine='openpyxl', sheet_name=sheet_name)

        # Вывод заголовков столбцов
        print(data.columns)

        # Удаление пробелов из заголовков
        data.columns = data.columns.str.strip()

        # Проверка наличия необходимых столбцов
        required_columns = ['Машина', 'Вид ТО', 'Дата проведения ТО', 'Наработка', 'Номер заказ-наряда', 'Дата заказ-наряда', 'Сервисная компания']
        for col in required_columns:
            if col not in data.columns:
                self.stdout.write(self.style.ERROR(f'Столбец "{col}" не найден в данных.'))
                return

        for index, row in data.iterrows():
            try:
                maintenance = Maintenance(
                    machine=row['Машина'],
                    type_of_maintenance=row['Вид ТО'],
                    date_of_maintenance=row['Дата проведения ТО'],
                    maintenance_development=row['Наработка'],
                    order_number=row['Номер заказ-наряда'],
                    order_date=row['Дата заказ-наряда'],
                    service_company=row['Сервисная компания'],
                )
                maintenance.save()
                self.stdout.write(self.style.SUCCESS(f'Импортирована запись: {maintenance}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Ошибка при импорте записи: {e}'))

        self.stdout.write(self.style.SUCCESS('Данные успешно импортированы!'))