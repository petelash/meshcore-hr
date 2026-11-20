# MeshCore HR — čarobnjak za čvorove

Web alat koji flasha i podesi MeshCore čvor po standardu hrvatske zajednice.
Radi iz preglednika, bez instalacije, bez servera.

**→ [petelash.github.io/meshcore-hr](https://petelash.github.io/meshcore-hr/)**

Neslužbeni alat zajednice. Firmware dolazi iz službenih izdanja
[meshcore-dev/MeshCore](https://github.com/meshcore-dev/MeshCore).

---

## Što radi

Četiri načina, biraju se na prvom ekranu:

| Način | Za što | Izravno |
|---|---|---|
| **Nova ploča** | ploča koja MeshCore još nema: izbor ploče, firmware, flashanje, pa postavke | — |
| **Nadogradnja** | čvor koji radi dobiva noviji firmware, a zadržava ime, ključeve i postavke | `?nadogradnja` |
| **Podešavanje** | čvor na kojem MeshCore već radi — samo mu se upišu hrvatske postavke | `?podesi` |
| **Provjera postavki** | ništa ne upisuje: pročita čvor i javi što odudara od standarda | `?provjera` |

Uz to, `?admin` otvara uređivanje stabla regija.

## Što upisuje na repetitor

Radio je **EU Narrow** — 869.618 MHz, 62.5 kHz, SF8. Coding rate predlaže savjetnik
od tri pitanja (zadano CR8).

| Naredba | Vrijednost |
|---|---|
| `set tx` | 22 |
| `set dutycycle` | 10 |
| `set advert.interval` | 240 |
| `set flood.advert.interval` | 24 |
| `set flood.max.advert` | 8 |
| `set flood.max` | 32 |
| `set path.hash.mode` | 1 |
| `set loop.detect` | moderate |
| `powersaving` | on (samo repetitor) |
| `set lat` / `set lon` | iz karte |
| `region put` / `region home` | lanac regija do mjesta gdje čvor stoji |

Ime repetitora dobiva prefiks `HR `. Namjerno se **ne diraju**: `txdelay`,
`direct.txdelay`, `rxdelay`, `int.thresh`, `agc.reset.interval`, `multi.acks`,
`radio.rxgain`, `adc.multiplier`, `bridge.*`, `setperm`.

Nakon upisa wizard svaku postavku pročita natrag i pokaže je li stvarno zapisana.

## Regije

Stablo je `#eu → #hr` pa četiri regije — `#slavonija`, `#sredisnja`, `#istralika`,
`#dalmacija` — a ispod njih podregije koje dodaje administrator.

Regija se **ne bira ručno**: izlazi iz pribadače na karti, pa su svi čvorovi na
istom mjestu u istoj regiji. Klikom na razinu u lancu bira se samo `region home`,
razina na kojoj se čvor najavljuje. Granice su službene, iz Državne geodetske
uprave (INSPIRE).

Stablo i dodjele stoje u [`regije.json`](regije.json) i uređuju se u `?admin`.
Spremanje traži GitHub token s pravom pisanja po ovom repozitoriju; token ostaje
u kartici preglednika i šalje se jedino na `api.github.com`.

## Što ti treba

- **Chrome, Edge ili Opera na računalu** — flashanje i upis idu kroz Web Serial,
  koji Firefox i Safari nemaju, kao ni preglednici na mobitelu
- USB kabel
- nRF52 ploče se flashaju prevlačenjem `.uf2` datoteke, ESP32 kroz preglednik

Ništa se ne šalje nikome: firmware ide s GitHuba izravno na tvoje računalo, a
naredbe iz preglednika kabelom na ploču. Nema servera koji bi išta vidio.

## Kad GitHub nije dohvatljiv

Popis ploča i izdanja povlači se uživo s GitHub API-ja. Ako to ne uspije — nema
mreže, iscrpljeno je ograničenje od 60 zahtjeva na sat — alat pada na ugrađenu
snimku izdanja i radi dalje, uz žutu napomenu s uzrokom.

## Što je u repozitoriju

| | |
|---|---|
| `index.html` | cijeli alat u jednoj datoteci (karta, podaci, Leaflet — sve ugrađeno) |
| `regije.json` | stablo regija i dodjele općina |
| `ploce.json` | nazivi, slike i OTAFIX inačice ploča |
| `tools/osvjezi_ploce.py` | dnevno osvježava `ploce.json` iz kataloga flashera |

`index.html` se ne uređuje ručno — sklapa se iz izvora skriptom za izgradnju.

---

Slike uređaja: [flasher.meshcore.io](https://flasher.meshcore.io) ·
Granice: DGU (INSPIRE) · Podloga: OpenStreetMap

Created by [petelash](https://github.com/petelash)
