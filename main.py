import libs.func
from libs.termFormat import TColors
from libs.brutforce import brutforce
from time import sleep

libs.func.clear()
libs.func.netcheck()
sleep(0.3)

iface, net_list = libs.func.netscan()

while True:
    usr_sel = input(TColors.USER + '\n[*] Введите номер сети ' + TColors.END +\
                    '(Для повторного сканирования введите [S]): ')
    if usr_sel.upper() == ('S' or '[S]'):
        iface, net_list = libs.func.netscan()
        continue
    elif int(usr_sel) not in range(len(net_list)):
        print(TColors.ERROR + '[-] Введено неверное значение. Попробуйте еще раз' + TColors.END)
        continue
    else:
        print(TColors.SUCCESS + '\n[+] Выбрана сеть: ' + TColors.ITALIC + net_list[int(usr_sel)] +\
              TColors.END)
        break

sleep(0.3)
brutforce(iface, net_list[int(usr_sel)])