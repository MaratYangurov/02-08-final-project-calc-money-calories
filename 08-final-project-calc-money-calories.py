import datetime as dt
# import urllib.request
# import json
# import requests
# from bs4 import BeautifulSoup as BS
# import lxml
from typing import Optional
DATE_FORMAT = '%d.%m.%Y'

# Класс, содержащий в себе описание структуры данных для записей
# калькулятора калорий/денег.
class Record:
    amount: float
    comment: str
    date: Optional[str]
    def __init__(self, amount, comment, date=None) -> None:
        self.amount = amount
        if date is not None:
            self.date = dt.datetime.strptime(date, DATE_FORMAT).date()
        else:
            self.date = dt.date.today()
        self.comment = comment

# Класс, содержащий общие методы для добавления новых записей и вычисления данных
# для калькулятора денег/калькулятора ккал.
class Calculator:
    def __init__(self, limit: int) -> None:
        # Список записей дневных лимитов трат/калорий, который задал пользователь
        self.records = []
        self.limit = limit

    def add_record(self, record): # Метод, добавляющий новые записи для калькуляторов ккал/денег.
        self.records.append(record)

    def get_today_stats(self): # Метод для вывода данных о ккал/деньгах за день.
        today_stats = 0
        date_today = dt.date.today()
        today_stats = sum(r.amount for r in self.records
                          if r.date == date_today)
        return today_stats

    def get_week_stats(self): # Метод для вывода данных о ккал/деньгах за неделю.
        week_stats = 0
        today = dt.datetime.now().date()
        week_ago = today - dt.timedelta(weeks=1)
        week_stats = sum(r.amount for r in self.records
                         if today >= r.date > week_ago)
        return week_stats

    def get_remained_balance(self): # Метод для получения остатка калорий или денег.
        return self.limit - self.get_today_stats()

# Дочерний класс Кальулятора - Калькулятор калорий.
class CaloriesCalculator(Calculator):
    def get_calories_remained(self) -> str: # Метод, вычисляющий остаток калорий, доступных для употребления.
        remained_balance = self.get_remained_balance()
        if remained_balance > 0:
            return ("Сегодня можно съесть что-нибудь ещё, "
                    "но с общей калорийностью не более "
                    f"{remained_balance} кКал")
        return "Хватит есть!"


# Дочерний класс Калькулятора - Калькулятор денег.
class CashCalculator(Calculator):
    USD_RATE: float = 92.00
    USD_RATE: float = 98.00
    RUB_RATE: float = 1.00

    def get_today_cash_remained(self, currency) -> str: # Метод, вычисляющий остаток денежных средств, доступных для трат, в заданной валюте.
        cash_remained = self.remained()
        currencies = {
            'eur': ('Euro', self.EURO_RATE),
            'usd': ('USD', self.USD_RATE),
            'rub': ('руб', self.RUB_RATE),
        }
        if currency not in currencies:
            return 'Неизвестная валюта.'
        sign, rate = currencies.get(currency)
        cash_remained = round(cash_remained / rate, 2)
        if cash_remained == 0:
            return 'Денег нет, держись!'
        elif cash_remained > 0:
            return f'На сегодня осталось {cash_remained} {sign}'
        else:
            cash_remained = abs(cash_remained)
            return f'Денег нет, держись: твой долг - {cash_remained} {sign}'
"""
#Создадим калькулятор денег с дневным лимитом 1000
cash_calculator = CashCalculator(1000)
# дата в параметрах не указана,
# так что по умолчанию к записи
# должна автоматически добавиться сегодняшняя дата
cash_calculator.add_record(Record(amount=145, comment='кофе'))
# и к этой записи тоже дата должна добавиться автоматически
cash_calculator.add_record(Record(amount=300, comment='Серега за обед'))
# а тут пользователь указал дату, сохраняем ее
cash_calculator.add_record(Record(amount=3000,
                                  comment='бар в Танин др', date='08.11.2019'))

print(cash_calculator.get_today_cash_remained('rub'))
# должно напечататься
# На сегодня осталось 555 руб
"""

