from itertools import groupby

with open('good_numbers.txt', 'r') as inp_file:
    good_numbers = set(inp_file.read().split('\n'))

a = set('023567')
for number in good_numbers:
    if number[17] == number[14] and len(set(number[9:12] + number[13] + number[16]) | a) == 6:
        with open('great_numbers.txt', 'a') as output_file:
            print(number, file=output_file)
