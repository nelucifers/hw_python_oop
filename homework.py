import datetime as dt


class Calculator:

    def __init__(self, limit):
        self.limit = limit
        self.records = list()

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        now = dt.date.today()
        today_amount = 0
        for record in self.records:
            if record.date == now:
                today_amount += record.amount
        return today_amount

    def get_week_stats(self):
        week_amount = 0
        today = dt.date.today()
        week_ago = today - dt.timedelta(days=7)

        for record in self.records:
            if week_ago <= record.date <= today:
                week_amount += record.amount
        return week_amount


class Record:

    def __init__(self, amount, comment, date=False):
        self.amount = amount
        self.comment = comment
        if not date:
            date = dt.datetime.now()
        else:
            date_format = '%d.%m.%Y'
            date = dt.datetime.strptime(date, date_format)
        self.date = date.date()


class CashCalculator(Calculator):

    USD_RATE = 54.85
    EURO_RATE = 55.83

    def get_today_cash_remained(self, currency):
        currencies = {
            'rub': ['руб', 1.00],
            'usd': ['USD', self.USD_RATE],
            'eur': ['Euro', self.EURO_RATE]
        }
        currency_title, currency_rate = currencies[currency]

        cash_today_stat = self.get_today_stats()
        remained = self.limit - cash_today_stat
        cash_today = round(remained / currency_rate, 2)

        if remained > 0:
            return f'На сегодня осталось {cash_today} {currency_title}'
        elif remained < 0:
            debt = abs(cash_today)
            return f'Денег нет, держись: твой долг - {debt} {currency_title}'
        else:
            return 'Денег нет, держись'


class CaloriesCalculator(Calculator):

    def get_calories_remained(self):
        calories_today = self.get_today_stats()
        remained = self.limit - calories_today

        if remained > 0:
            return (f'Сегодня можно съесть что-нибудь ещё, '
                    f'но с общей калорийностью не более {remained} кКал')
        else:
            return 'Хватит есть!'
