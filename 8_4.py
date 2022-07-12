#Дан список чисел, отсортировать его по возрастанию без использования sort и sorted

a = (input('Введите числа: '))
b = a.split()
A = [int(x) for x in b]
n = 1
while n < len(A):
     for i in range(len(A)-n):
          if A[i] > A[i+1]:
               A[i],A[i+1] = A[i+1],A[i]
     n += 1
print(A)
