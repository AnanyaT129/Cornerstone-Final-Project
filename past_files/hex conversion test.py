# Using ast.literal_eval()
from ast import literal_eval
    
def getchar(string, n):
    return str(string)[n - 1]
data = [b'\x03', b'\xd5', b'`', b'\t']

def hex_to_dec(hex):
    try:
        tens_digit = int(getchar(hex,1))
    except:
        if getchar(hex,1) == 'a':
            tens_digit = 10
        if getchar(hex,1) == 'b':
            tens_digit = 11
        if getchar(hex,1) == 'c':
            tens_digit = 12
        if getchar(hex,1) == 'd':
            tens_digit = 13
        if getchar(hex,1) == 'e':
            tens_digit = 14
        if getchar(hex,1) == 'f':
            tens_digit = 15
    
    try:
        ones_digit = int(getchar(hex,2))
    except:
        if getchar(hex,2) == 'a':
            ones_digit = 10
        if getchar(hex,2) == 'b':
            ones_digit = 11
        if getchar(hex,2) == 'c':
            ones_digit = 12
        if getchar(hex,2) == 'd':
            ones_digit = 13
        if getchar(hex,2) == 'e':
            ones_digit = 14
        if getchar(hex,2) == 'f':
            ones_digit = 15
    
    number = 16*tens_digit + ones_digit
    return number

for i in range(len(data)):
    if len(str(data[i])) == 7:
        a=getchar(str(data[i]),3)
        b=getchar(str(data[i]),4)
        c=getchar(str(data[i]),5)
        d=getchar(str(data[i]),6)
        hex=c+d
        # print(hex)
        print(hex_to_dec(hex))
    else:
        print("ERROR")
        # print(len(str(data[i])))
