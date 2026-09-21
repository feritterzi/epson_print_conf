# epson_print_conf (L3251)

Epson yazıcı yapılandırma aracı (Wi‑Fi / SNMP). Bu kopya özellikle **Epson L3251 / L3250** için sadeleştirilmiştir.

Kaynak proje: [Ircama/epson_print_conf](https://github.com/Ircama/epson_print_conf)

## Kurulum

```powershell
cd epson_print_conf
python -m pip install -r requirements.txt
```

> Windows’ta `pip` bulunamazsa her zaman `python -m pip` kullan.

## L3251 – hızlı kullanım

Yazıcı ve PC aynı Wi‑Fi ağında olmalı (USB desteklenmez).

```powershell
# Yazıcıyı bul
python find_printers.py

# Durum
python reset_l3251_pad.py 192.168.1.16 --status

# Ped (waste ink) – mümkünse geçici sıfırlama
python reset_l3251_pad.py 192.168.1.16

# GUI
python ui.py
```

Kafa temizliği için GUI’de **Clean Nozzles** kullanın (`python ui.py`).

### Önemli (yeni firmware)

Birçok L3251/L3250’de SNMP üzerinden **kalıcı EEPROM ped sıfırlama kapalıdır**.  
Bu araç durum gösterir; ped “full” ise geçici sıfırlama dener. Kalıcı çözüm için USB aracı veya servis gerekir. Ped bakımı yapılmadan sürekli sıfırlamak sızıntı riski yaratır.

Python 3.12+ / 3.14 için event loop düzeltmesi `epson_print_conf.py` içinde vardır.

## Dosyalar

| Dosya | Açıklama |
|-------|----------|
| `epson_print_conf.py` | Ana kütüphane / CLI |
| `ui.py` | Grafik arayüz |
| `find_printers.py` | Ağda yazıcı bulma |
| `reset_l3251_pad.py` | L3251 ped durumu / geçici sıfırlama |
| `parse_devices.py` | Harici yazıcı veritabanı içe aktarma |
| `requirements.txt` | Bağımlılıklar |

## Lisans

Orijinal projenin `LICENSE` dosyasına bakın.
