#Написать функцию, которая определяет, является ли список симметричным

a = (input('Введите числа: '))
b = a.split()
lst = [int(x) for x in b]


def norm(lst: list) -> str:
    for i in range(len(lst) // 2):
        if lst[i] != lst[-i - 1]:
            print("Список не симметричный")
            return lst
    else:
        print("Список симметричный")
        return lst

print(norm(lst))
