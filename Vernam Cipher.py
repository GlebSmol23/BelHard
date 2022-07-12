massage = input('Сообщение (Eng): ')
key = input('Ключ (Eng): ')

if len(massage) != len(key):
    raise ValueError('Длина ключа должна совпадать с длиной сообщения')

massage_bin = ""
key_bin = ""
for i in range(len(key)):
    char = bin(ord(massage[i]))[2:]
    char = "0" * (8 - len(char)) + char
    massage_bin +=char
    char = bin(ord(key[i]))[2:]
    char = "0" * (8 - len(char)) + char
    key_bin += char
result = ""
for i in range(len(key_bin)):
    if massage_bin[i] != key_bin[i]:
        result += '1'
    else:
        result += '0'
print(result)
