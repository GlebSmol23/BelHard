#Дан двухмерный массив (список списков) 5×5. Найти сумму модулей отрицательных нечетных элементов.

numbers: list[list[int]] = [
    [1, -2, 3, -4, 5],
    [1, -2, -3, 4, -5],
    [-1, 2, -3, -4, -5],
    [1, -2, 3, -4, 5],
    [-1, -2, -3, -4, -5],
]

def get_abs_sum_negative_num(numbers: list[list[int]]) -> int:
    count: int = 0
    for raw in numbers:
        count += sum(filter(lambda number: number < 0 and number % 2, raw))
    return count
