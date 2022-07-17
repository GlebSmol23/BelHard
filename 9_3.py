#Создать квадратную матрицу размером N, на диагонали которой находятся тройки, выше диагонали находятся двойки, 
#остальные элементы равна единице.


n =int(input("n: "))

def generate_array_of_numbers(n: int) -> list[list[int]]:
    numbers: list[list[int]] = []

    for j in range(n):
        raw: list[int] = []
        for i in range(n):
            if i == j:
                raw.append(3)
            elif i > j:
                raw.append(2)
            else:
                raw.append(1)
        numbers.append(raw)
    return numbers

for raw in generate_array_of_numbers(n):
    print(raw)
