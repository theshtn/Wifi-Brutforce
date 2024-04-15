from os import system
from libs.TFormat import tcolors
import platform
import pywifi
from prettytable import PrettyTable
from time import sleep
from tqdm import trange

wifi = pywifi.PyWiFi()
iface = wifi.interfaces()[0] # Для внешней сетевой карты использовать значение 1

def clear (): # Очистка терминала
    if platform.system().startswith("Win" or "win"):
        system("cls")
    else:
        system("clear")

def netcheck(): # Проверка сетевой карты
    global iface

    iface.disconnect()

    print(tcolors.PROC + '[~] Проверка состояния сетевой карты....' + tcolors.END)
    sleep(0.3)
    if iface.status() not in [pywifi.const.IFACE_DISCONNECTED, pywifi.const.IFACE_INACTIVE]:
        print(tcolors.ERROR + "Что-то пошло не так. Проверьте работоспособность сетевой карты" + \
              tcolors.END)
        exit()
    else: print(tcolors.SUCCESS + "[+] Сетевая карта работает корректно" + tcolors.END)

def netscan():
    global iface

    clear()
    iface.scan()
    for prog in trange(5, dynamic_ncols=True, desc="[~] Сканирование сетей....", \
                    bar_format=(tcolors.PROC + '{l_bar}{bar}' + tcolors.END)):
        sleep(1)

    clear()

    print(tcolors.SUCCESS + "[+] Сканирование завершено успешно! Список доступных сетей:" +\
        tcolors.END)
    net_list = iface.scan_results()
    net_list = tableout(net_list)

    return iface, net_list

def tableout(network_list): # Вывод сетей в таблицу
    table = PrettyTable(['№', 'MAC Address', 'SSID', 'Signal', 'Security'])
    table.align = 'l'
    t_data = []
    num = 0

    for i in network_list:
        if i.ssid != "" and i.ssid not in t_data:
            match i.akm[0]:
                case 0: i.akm = "OPEN"
                case 1: i.akm = "WPA/WPA2 Enterprise"
                case 2: i.akm = "WPA/WPA2 Personal"
                case 3: i.akm = "WPA/WPA2 Enterprise"
                case 4: i.akm = "WPA/WPA2 Personal"
                case 5: i.akm = "UNKNOWN"

            t_data.append(i.ssid)
            table.add_row([num, i.bssid, i.ssid, str(100 + i.signal), i.akm])
            num += 1

    print(table)
    return t_data