from django.urls.converters import StringConverter

class CurrencyConverter(StringConverter):
    """Конвертер для валютных пар (USD-RUB, EUR-USD и т.д.)"""
    regex = r'[A-Z]{3}-[A-Z]{3}'  

    def to_python(self, value):
        """Проверяем поддерживаемые валюты"""
        from_cur, to_cur = value.split('-')
        supported_currencies = {'USD', 'EUR', 'RUB'}
        
        if from_cur not in supported_currencies or to_cur not in supported_currencies:
            raise ValueError(f"Неподдерживаемая валюта. Доступно: {', '.join(supported_currencies)}")
        return value

    def to_url(self, value):
        """Проверяем формат перед использованием в URL"""
        if not isinstance(value, str) or len(value) != 7 or value[3] != '-':
            raise ValueError("Формат валютной пары: XXX-XXX (например USD-RUB)")
        return value
    # converters.py
class FloatConverter:
        regex = r'-?\d+(?:\.\d+)?'  # Соответствует положительным и отрицательным числам с десятичной точкой

        def to_python(self, value):
            try:
                return float(value)
            except ValueError:
                return None  # Или бросить исключение

        def to_url(self, value):
            return str(value)
    
