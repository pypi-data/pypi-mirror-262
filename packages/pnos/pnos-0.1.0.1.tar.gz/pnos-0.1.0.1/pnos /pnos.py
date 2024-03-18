import os

def OPM_BOOT_INITD0():
    print("INIT D0 BOOT")
    print("0x0000000001")
    os.system("PMI --init --visr --bootOS='PNOS, entry1, disk=0;part=1' --AANSI")

def pnos_bootloader() :
    print("PNOS OPENBOOT")
    print("SOURCE AVAILABLE AT 'https://github.com/StNiosem/pnos-packages/'")
    