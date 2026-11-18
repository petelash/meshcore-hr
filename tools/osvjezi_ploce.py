# -*- coding: utf-8 -*-
"""Povlaci katalog uredaja s flasher.meshcore.io i izvlaci tablicu ploca.

Daje ploce.json: oznaka ploce -> puni naziv, proizvodac, slika i prikovana
OTAFIX verzija. Wizard to cita s raw.githubusercontent.com (koji ima CORS),
pa se nazivi i prikivanje osvjezavaju bez diranja HTML-a.

Samo standardna biblioteka. Pokrece se iz korijena repozitorija.
"""
import json
import os
import re
import sys
import urllib.request

KATALOG = 'https://flasher.meshcore.io/config.json'
IZLAZ = 'ploce.json'

# uloge koje se pojavljuju iza oznake ploce u imenima firmwarea
ULOGE = (r'kiss_modem|repeater|room_server|companion_radio_ble|companion_radio_usb|'
         r'companion_radio|sensor|terminal_chat')


def oznaka(ime):
    m = re.match(r'^(.+?)_(?:' + ULOGE + r')-', ime)
    return m.group(1) if m else None


def bootloader(dev):
    """Flasher prikiva OTAFIX verziju po ploci. Vraca (verzija, [oznake])."""
    b = dev.get('bootloader')
    if not b:
        return None, []
    lst = b if isinstance(b, list) else [b]
    ver, oznake = None, []
    for x in lst:
        m = re.match(r'(.+?)_bootloader-[\d.]+-OTAFIX([\d.]+?)\.?(?:uf2|zip|hex)$', str(x))
        if not m:
            continue
        ver = ver or m.group(2)
        if m.group(1) not in oznake:
            oznake.append(m.group(1))
    return ver, oznake


def main():
    req = urllib.request.Request(KATALOG, headers={'User-Agent': 'meshcore-hr-regije'})
    kat = json.load(urllib.request.urlopen(req, timeout=60))

    uredaji = kat.get('device') or []
    if len(uredaji) < 20:
        print('Katalog ima samo %d uredaja - sumnjivo malo, ne diram nista.' % len(uredaji))
        return 1

    tablica = {}
    for dev in uredaji:
        slike = re.findall(r"src='([^']+)'", dev.get('tooltip', '') or '')
        slika = slike[0] if slike else (dev.get('icon') or '')
        ver, bploce = bootloader(dev)

        def unos():
            u = {'n': dev.get('name', ''), 'm': dev.get('maker', ''), 's': slika}
            if ver:
                u['ov'] = ver
                u['ob'] = bploce
            return u

        nasao = False
        for fw in dev.get('firmware', []):
            for v in (fw.get('version') or {}).values():
                for f in v.get('files', []):
                    o = oznaka(f.get('name', ''))
                    if not o:
                        continue
                    nasao = True
                    tablica.setdefault(o, unos())

        # uredaji bez ijedne firmware datoteke (npr. Heltec T096) hvataju se
        # preko imena bootloadera, koje se poklapa s oznakom iz MeshCore izdanja
        if not nasao:
            for b in bploce:
                tablica.setdefault(b, unos())

    if len(tablica) < 20:
        print('Izvuceno samo %d ploca - sumnjivo malo, ne diram nista.' % len(tablica))
        return 1

    novi = json.dumps(tablica, ensure_ascii=False, separators=(',', ':'), sort_keys=True)

    staro = None
    if os.path.exists(IZLAZ):
        with open(IZLAZ, encoding='utf-8') as f:
            staro = f.read()

    if staro == novi:
        print('Bez promjena (%d ploca, %d s OTAFIX-om).'
              % (len(tablica), sum(1 for v in tablica.values() if v.get('ov'))))
        return 0

    with open(IZLAZ, 'w', encoding='utf-8') as f:
        f.write(novi)
    print('Osvjezeno: %d ploca, %d s prikovanim OTAFIX-om.'
          % (len(tablica), sum(1 for v in tablica.values() if v.get('ov'))))
    return 0


if __name__ == '__main__':
    sys.exit(main())
