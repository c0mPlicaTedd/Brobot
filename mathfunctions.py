import math

def basic(voice_data): #basic math functions +-*/^
    voice_data = voice_data.replace("what is","")
    voice_data = voice_data.replace("plus","+")
    voice_data = voice_data.replace("minus","-")
    voice_data = voice_data.replace("multiply","*")
    voice_data = voice_data.replace("x","*")
    voice_data = voice_data.replace("into","*")
    voice_data = voice_data.replace("times","*")
    voice_data = voice_data.replace("multiplied by","*")
    voice_data = voice_data.replace(" divided by ","/")
    voice_data = voice_data.replace("to the power of","**")
    voice_data = voice_data.replace("raise to","**")
    voice_data = voice_data.replace("raised to","**")
    voice_data = voice_data.replace(" ","")
    final = eval(voice_data)
    return round(final,2)

def factorial(n): #for factorials
    
    n = int(n)
    if (n==0 or n==1):
        return 1
    else:
        return n*factorial(n-1)

def roots(voice_data): #for nth root
    print("in roots")
    voice_data=voice_data.replace("what is","")
    voice_data=voice_data.replace("of","")
    voice_data=voice_data.replace(" ","")
    exp = voice_data.split('root')[0]
    rexp = float(1/float(exp))
    base = voice_data.split('root')[1]
    result = round((float(base)**rexp),2)
    return (result)
