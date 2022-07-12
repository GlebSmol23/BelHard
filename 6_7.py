#Дан список чисел, необходимо для каждого элемента посчитать сумму его
#соседей, для крайних чисел одним из соседей является число с противоположной
#стороны списка

inp = list(map(int, input('Введите числа: ').split()))
out = []

for i in range(len(inp) - 1):
    out.append(inp[i - 1] + inp[i + 1])
else:
    out.append(inp[i] + inp[0])
print(out)
