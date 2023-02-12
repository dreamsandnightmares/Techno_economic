import matplotlib.pyplot as plt

def grid_price(time):
    price = 0
    if 5 <= int(time/(30*24))<9 or int(time/(30*24)) ==10 :
        if 12<=time%24 <14:
            price =2
            pass
        elif 8<= time%24<12 or 14<=time%24<15 or 18<=time%24<21:
            price =1.3
            pass
        elif 6<= time%24<8 or 15<=time%24<18 or 21<=time%24<22:
            price =0.6
            pass
        elif 0<= time%24<6 or 22<=time%24<24:
            price =0.3
    elif int(time/(30*24))==9 :
        if 8<=time%24 <15 or 18<=time%24 <21 :
            price= 1.3
        elif 6<=time%24 <8 or 15<=time%24 <18 or 21<=time%24 <22:
            price = 0.6
        elif 0<=time%24 <6 or 22<=time%24 <24:
            price = 0.3
    elif int(time/(30*24)) ==12 or int(time/30/24)==1:
        if  19<=time%24 <21:
            price = 2
        elif  8<=time%24 <11 or 18<=time%24 <19:
            price = 1.3
        elif   6<=time%24 <8 or 11<=time%24 <18 or  21<=time%24 <22:
            price = 0.6
        elif 0<=time%24 <6 or 22<=time%24 <24:
            price = 0.3
    else:
        if 8 <= time % 24 < 11 or   18<=time%24 <19:
            price = 1.3
        elif 6 <= time % 24 < 8 or   11<=time%24 <18 or 21<=time%24 <22 :
            price = 0.6
        else:
            price = 0.3
    return price

if __name__ == '__main__':
    price = []
    for i in range(8640):
        if int(i/(30*24)) == 4:

            price.append(grid_price(i))
    dist = list(range(len(price[:25])))
    plt.plot(dist,price[:25])
    plt.title('Typical peak-valley electricity price of a day')
    plt.xlabel('hour [h]')
    plt.ylabel('price [yuan]')
    plt.show()



