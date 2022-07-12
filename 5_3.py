#Вывести четные числа от 2 до N по 5 в строку

n = int(input())

count = 0
for i in range(2, n+1, 2):
    if count < 5:
        print(i, end=' ')
        count += 1
    else:
        print()
        print(i, end=' ')
        count = 1
