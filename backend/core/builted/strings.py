from decimal import Decimal


async def number_with_spaces_str(number: float | Decimal) -> str:
    """
    Форматирует число с разделителями тысяч и убирает нули после запятой, если число целое.

    Аргументы:
    number (float | Decimal): Число, которое нужно отформатировать.

    Возвращает:
    str: Число в виде строки с пробелами в качестве разделителей тысяч и без десятичных знаков, если они равны нулю.
    """
    formatted_number = f"{number:,.2f}".replace(",", " ").replace(".00", "")
    return formatted_number
