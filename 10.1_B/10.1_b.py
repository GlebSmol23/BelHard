#1. Дан многострочный файл txt
# б) разбить файл на несколько файлов по N строк


N = int(input("N: "))
split_len = N
input1 = open("input.txt", "r", encoding="utf-8")
count: int = 0
start: int = 1
f_out = None
for line in input1:
    if count % split_len == 0:
        if f_out: f_out.close()
        f_out = open("output" + str(start) + ".txt", "w", encoding="utf-8")
        start += 1
    f_out.write(line)
    count += 1

