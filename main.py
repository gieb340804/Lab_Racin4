import os
from fractions import Fraction
import decimal
from decimal import Decimal

decimal.getcontext().prec=100

def word_str(str_):
    text = []
    arr =[]
    # tmp_str = ""
    # for i in str_:
    #     if i == "\n":
    #
    #         text.append(arr)
    #         arr =[]
    #         continue
    #     if i == " ":
    #         arr.append(tmp_str)
    #         tmp_str = ""
    #         continue
    #     tmp_str += i
    s = str_.split("\n")
    for i in s:
        t = list(i.split(" "))
        if '' in t:
            t.remove('')
        text.append(t)
    return text
def bin_to_dec(digit):
    dlina =len(digit)
    chislo_dec =0
    for i in range(0, dlina):
        chislo_dec =chislo_dec +int(digit[i] ) *( 2**(dlina - i -1))
    return chislo_dec

def _to_Bytes(data):

    a = []
    for i in range(0, len(data), 8):
        a.append(bin_to_dec(data[i:i + 8]))
    b = bytearray(a)
    return bytes(b)
def decimal_from_fraction(frac):
    return frac.numerator / decimal.Decimal(frac.denominator)





def decode(encoded, alph, strlen, every):
    decoded_str = ""

    count = dict.fromkeys(alph, 1)
    cdf_range = dict.fromkeys(alph)
    pdf = dict.fromkeys(alph)

    low = 0
    high = Decimal(1)/Decimal(len(alph))

    for key, value in sorted(cdf_range.items()):
        cdf_range[key] = [low, high]
        low = high
        high += Decimal(1)/Decimal(len(alph))

    for key, value in sorted(pdf.items()):
        pdf[key] = Decimal(1)/Decimal(len(alph))


    lower_bound = 0                                                                     # upper bound
    upper_bound = 1                                                                     # lower bound

    k = 0

    while (strlen != len(decoded_str)):
        for key, value in sorted(pdf.items()):

            curr_range = upper_bound - lower_bound                                      # current range
            upper_cand = lower_bound + (curr_range * cdf_range[key][1])                 # upper_bound
            lower_cand = lower_bound + (curr_range * cdf_range[key][0])                 # lower bound

            if (lower_cand <= encoded < upper_cand):
                k += 1
                decoded_str += key

                if (strlen == len(decoded_str)):
                    break

                upper_bound = upper_cand
                lower_bound = lower_cand

                count[key] += 1

                if (k == every):
                    k = 0
                    for key, value in sorted(pdf.items()):
                        pdf[key] = Decimal(count[key])/Decimal(len(alph)+len(decoded_str))

                    low = 0
                    for key, value in sorted(cdf_range.items()):
                        high = pdf[key] + low
                        cdf_range[key] = [low, high]
                        low = high

    return decoded_str

def binary_s(n):  # функция которая преобразует
    b = ''
    while n > 0:
        b = str(n % 2) + b
        n = n // 2
    return b
def binary(n):  # функция которая преобразует
    b = ''
    for i in range(0, 8):
        b = str(n % 2) + b
        n = n // 2
    return b


def ecode(encode_str, N):

    alph = list(set(encode_str))
    count = dict.fromkeys(alph, 1)
    cdf_range = dict.fromkeys(alph)
    pdf = dict.fromkeys(alph)

    low = 0
    high = Decimal(1)/Decimal(len(alph))

    for key, value in sorted(cdf_range.items()):
        cdf_range[key] = [low, high]
        low = high
        high += Decimal(1)/Decimal(len(alph))

    for key, value in sorted(pdf.items()):
        pdf[key] = Decimal(1)/Decimal(len(alph))


    i = len(alph)

    lower_bound = 0                                                                     # upper bound
    upper_bound = 1                                                                     # lower bound
    u = 0

    # go thru every symbol in the string
    for sym in encode_str:
        i += 1
        u += 1
        count[sym] += 1

        curr_range = upper_bound - lower_bound                                          # current range
        upper_bound = lower_bound + (curr_range * cdf_range[sym][1])                    # upper_bound
        lower_bound = lower_bound + (curr_range * cdf_range[sym][0])                    # lower bound

        # update cdf_range after N symbols have been read
        if (u == N):
            u = 0

            for key, value in sorted(pdf.items()):
                pdf[key] = Decimal(count[key])/Decimal(i)

            low = 0
            for key, value in sorted(cdf_range.items()):
                high = pdf[key] + low
                cdf_range[key] = [low, high]
                low = high
    b = (upper_bound - lower_bound) / 2
    while b < 1:
        lower_bound*=10
        b*=10

    # while True:
    #     upper_bound *=10
    #     lower_bound *=10
    #     print(lower_bound, upper_bound)
    #     # if(int(upper_bound) % 10 -  int(lower_bound) % 10 == 1):
    #     #     print(lower_bound, upper_bound)
    #     #     upper_bound *= 10
    #     #     lower_bound *= 10
    #     #     lower_bound = int(lower_bound) * 10 +(((int(upper_bound * 10)% 100) - (int(lower_bound * 10)% 100)) // 2)
    #     #     break
    #     if (int(upper_bound) % 10 - int(lower_bound) % 10 > 1):
    #         lower_bound = int(lower_bound)  + (((int(upper_bound) % 10) - (int(lower_bound) % 10)) // 2)
    #         break
    # # for _ in range(100):
    # #     lower_bound*=Decimal(10)
    # print(lower_bound, upper_bound)
    return alph, Fraction(int(lower_bound+ b) )


def main():
    with open("book.txt", encoding="utf-8") as f1:  # вводим текст
        text = f1.read()
    f1.close()
    text = word_str(text)
    alph_code = []
    code_text =""
    for i in text:
        tmp = []
        for j in i:
            alph_map_code, coded = ecode(j, 1)  # кодирование символов, возвращает текст и алфавит

            tmp.append(alph_map_code)
            code_text += binary(len(binary_s(coded))) + binary_s(coded)
            while coded > 1:
                coded *= Fraction(1, 10)
        alph_code.append(tmp)

        tmp = []
    ss = 8 - (len(code_text) % 8)
    code_text = ("0" * ss) + code_text
    with open('test.bin', 'wb') as f:
        f.write(_to_Bytes(code_text))
    f3 = open('test.bin', 'rb')
    s = f3.read()
    int_values = [x for x in s]
    code_text = ""
    for i in int_values:
        code_text += binary(i)
    code_text = code_text[ss:]
    text_dd =""

    for i in range(len(alph_code)):
        for j in range(len(alph_code[i])):
            m = bin_to_dec(code_text[:8])
            code_text = code_text[8:]
            code = code_text[:m]

            code_text = code_text[m:]
            code = bin_to_dec(code)

            while code > 1:
                code *= Fraction(1, 10)

            decode_text = decode(code, alph_code[i][j], len(text[i][j]), 1)  # преобразование сжатого в обычный текст
            text_dd+=decode_text + " "
        text_dd += "\n"
    f3 = open("decode_text1.txt", 'w', encoding="utf-8")  # вывод преобразованного текста
    f3.write(text_dd)
    f3.close()
    _o = os.path.getsize('book.txt')
    _c = os.path.getsize('test.bin')
    print(f'Исходный файл: {_o} bytes')
    print(f'Сжатый файл: {_c} bytes')

    print('Процент сжатия {}% '.format(round((((_c) / _o) * 100), 3)))
    
    # encode_str = "eorgnieunbivnfbddfbdwkvjnwinvribiwertbiwrivnerinvijwbtbnwrtvfjb kfg  jrgfji "
    # strlen = len(encode_str)
    # every = 3
    # alph, encoded = encode(encode_str, every)
    # print(encoded)
    # while encoded > 1:
    #     encoded *= Fraction(1, 10)
    #
    # print(decimal_from_fraction(encoded))
    # decoded = decode(encoded,alph, strlen, every)
    # print(decoded)
if __name__ == '__main__':
    main()