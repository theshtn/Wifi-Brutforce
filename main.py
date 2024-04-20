import libs.func
from libs.TFormat import tcolors
from libs.brutforce import brutforce
from time import sleep

libs.func.clear()
libs.func.netcheck()
sleep(0.3)

iface, net_list = libs.func.netscan()

while True:
    usr_sel = input(tcolors.USER + '\n[*] Введите номер сети ' + tcolors.END +\
                    '(Для повторного сканирования введите [S]): ')
    if usr_sel.upper() == ('S' or '[S]'):
        iface, net_list = libs.func.netscan()
        continue
    elif int(usr_sel) not in range(len(net_list)):
        print(tcolors.ERROR + '[-] Введено неверное значение. Попробуйте еще раз' + tcolors.END)
        continue
    else:
        print(tcolors.SUCCESS + '\n[+] Выбрана сеть: ' + tcolors.ITALIC + net_list[int(usr_sel)] + \
              tcolors.END)
        break

sleep(0.3)
brutforce(iface, net_list[int(usr_sel)])