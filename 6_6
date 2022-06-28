#Дан список рандомных чисел, необходимо отсортировать его в виде, сначала
#четные, потом нечётные

def main(l):
    a = list( i for i in l if l.index(i) % 2 == 0) + list(i for i in l if l.index(i) % 2 != 0)
    return a
lst = input('Введите числа: ').split()
print(*main(lst))
