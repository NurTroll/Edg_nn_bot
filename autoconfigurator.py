import csv
from typing import TextIO
import json

MASK = {
    "24": "255.255.255.0",
    "25": "255.255.255.128",
    "26": "255.255.255.192",
    "27": "255.255.255.224",
    "28": "255.255.255.240",
    "29": "255.255.255.248",
    "30": "255.255.255.252"
}


# Функция вычисления шлюза
def gw_define(ip, mask):
    ip2 = int(ip.split('.')[3])
    mask2 = int(mask.split('.')[3])
    gw = ip.rpartition('.')[0] + '.' + str((ip2 & mask2) + 1)
    return gw


# функция проверки ввода маски
def mask_found():
    while True:
        mask1 = input("Введите маску подсети:").strip()
        for key in MASK:
            if mask1 == key:
                return MASK[key]
        print('Вы ввели неверные данные, попробуйте ещё раз')


# Проверка верности вводимых данных ip адреса
def ip_input():
    while True:
        ip = input("Введите ip:").strip()
        ip_split = ip.split('.')
        if (ip.count('.') == 3 and ip_split[0].isdigit() and ip_split[1].isdigit() and ip_split[2].isdigit() and
            len(ip_split[0]) < 4 and len(ip_split[1]) < 4 and len(ip_split[3]) < 4 ) :
            return ip
        print('Вы ввели неверные данные, попробуйте ещё раз')


def uik_vlans_name(uik_vlans):
    vlans = uik_vlans.split(';')
    vlans_name = ''
    for el in range(len(vlans)):
        vlans_name = vlans_name + f'vlan {vlans[el]}\n name IPOE{vlans[el]}\n!\n'
    return vlans_name.strip()

with open("data.json", "r") as read_file:
    data = json.load(read_file)

gw = gw_define(data["IP"], data["MASK"])
print(f'{data["HOSTNAME"]} {data["IP"]} {data["MASK"]} {gw}')
config_ring = open('3750.txt', 'r', encoding='utf-8')
conf_text = config_ring.read()
new_text = conf_text.replace('<hostname>', data["HOSTNAME"])
new_text = new_text.replace('<ip>', data["IP"])
new_text = new_text.replace('<mask>', data["MASK"])
new_text = new_text.replace('<gw>', gw)
new_text = new_text.replace('<managament>', data["MANAGEMENT VLAN"])
new_text = new_text.replace('<uik_vlans>', data["UIK VLANS"])
new_text = new_text.replace('<uik_vlans_names>', uik_vlans_name(data["UIK VLANS"]))
filename = data["HOSTNAME"] + '.conf'
output = open('backup/' + filename, 'w', encoding='utf-8')
print(new_text, file=output)
config_ring.close()
output.close()


