import math
def convert_precision(tolerance):
    """
    Преобразует значение точности (tolerance) в порядок (количество знаков после запятой для округления).
    """
    if tolerance <= 0:
        raise ValueError("Tolerance must be positive.")
    return round(abs(round(math.log10(tolerance))))


def calculate(num1, num2, operand, tolerance=1e-6):
    """
    Функция принимает два числа и тип операции. Служит для выполнения операций с числами. Выводит результат или сообщение об ошибке.
    """
    precision = convert_precision(tolerance)

    if operand == '+':
        result = num1 + num2
    elif operand == '-':
        result = num1 - num2
    elif operand == '*':
        result = num1 * num2
    elif operand == '/':
        if num2 == 0:
            return "Error"
        result = num1 / num2
    else:
        return "Error: Invalid operand."

    return round(result, precision)


def main():
    """
    Основная функция, запрашивает у пользователя ввод двух чисел и тип операции. Запускает функцию calculate().
    """
    try:
        num1 = float(input("Введите первое число: "))
        num2 = float(input("Введите второе число: "))
        operand = input("Введите операцию (+, -, *, /): ")

        result = calculate(num1, num2, operand)
        print("Результат:", result)
    except ValueError:
        print("Error: некорректные данные.")

if __name__ == "__main__":
    main()