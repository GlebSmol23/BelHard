#Написать функцию перевода десятичного числа в двоичное и обратно, без
#использования функции int

def convert_to_bin (number: int) -> str:
    bin_number: str = ""
    while number // 2 > 0:
        bin_number += str(number % 2)
        number //= 2
    bin_number += str(number)
    bin_number = bin_number[::-1]
    return bin_number
