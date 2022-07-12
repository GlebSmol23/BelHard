#Дан многострочный файл txt
# а) Разбить файл на N (вводится с клавиатуры) файлов построчно.


N: int = int(input("N: "))
with open("input.txt", "r", encoding="utf-8") as f_in:
    lines = f_in.readlines()

end = 0
for i in range(1, N+1):
    if i == 1:
        start = 0
    inc = int(len(lines) / N)
    end += inc
    with open("output" + str(i) + ".txt", "w", encoding="utf-8") as f_out:
        for line in lines[start:end]:
            f_out.write(line)
    start = end
