#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Epson L3251 / L3250 waste ink pad helper (Wi-Fi / SNMP).

Yeni firmware'li L3251'lerde kalici EEPROM sifirlama genelde mumkun degil
(SNMP EEPROM erisimi kapali). Bu script durumu gosterir ve mumkunse
gecici sifirlama dener.

Ornek:
  python reset_l3251_pad.py 192.168.1.16 --status
  python reset_l3251_pad.py 192.168.1.16
"""

from __future__ import annotations

import argparse
import asyncio
import logging
import sys

from epson_print_conf import EpsonPrinter

MODEL = "L3251"


def _ensure_event_loop() -> None:
    try:
        asyncio.get_event_loop()
    except RuntimeError:
        asyncio.set_event_loop(asyncio.new_event_loop())


def _print_status(printer: EpsonPrinter) -> dict:
    levels = printer.get_waste_ink_levels()
    if levels:
        print("Ped seviyeleri (EEPROM):")
        for name, value in levels.items():
            print(f"  {name}: %{value}")
    else:
        print(
            "EEPROM ped seviyeleri okunamadi "
            "(yeni firmware'de normal; SNMP EEPROM kilitli)."
        )

    try:
        st = printer.get_printer_status() or {}
    except Exception:
        st = {}
    if st:
        serial = st.get("serial_number_info")
        if serial:
            print(f"Seri no: {serial}")
        for key in (
            "maintenance_box_1",
            "maintenance_box_2",
            "maintenance_box_reset_count_1",
            "maintenance_box_reset_count_2",
            "status",
            "ready",
        ):
            if key in st:
                print(f"  {key}: {st[key]}")
    return st


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Epson L3251 ped durumu / gecici sifirlama"
    )
    parser.add_argument("ip", help="Yazici IP (or. 192.168.1.16)")
    parser.add_argument(
        "--status",
        action="store_true",
        help="Sadece durum goster",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=10.0,
        help="SNMP timeout saniye",
    )
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.WARNING
    )
    _ensure_event_loop()

    printer = EpsonPrinter(
        model=MODEL,
        hostname=args.ip,
        timeout=args.timeout,
    )
    if not printer.parm:
        print(f"Model yapilandirmasi yok: {MODEL}", file=sys.stderr)
        return 1

    try:
        info = printer.get_snmp_info("Epson Printer Name") or {}
        name = info.get("Epson Printer Name") or "?"
        print(f"Baglandi: {name} @ {args.ip}")

        st = _print_status(printer)
        if args.status:
            return 0

        def _box_is_full(value) -> bool:
            text = str(value or "").lower()
            return "full" in text and "not full" not in text

        ready = st.get("ready")
        if ready and not _box_is_full(st.get("maintenance_box_1")) and not _box_is_full(
            st.get("maintenance_box_2")
        ):
            print()
            print(
                "Yazici su an hazir (Idle) ve maintenance box 'full' degil."
            )
            print(
                "Ped hatasi ekranda yoksa sifirlamaya gerek yok; baski deneyebilirsin."
            )
            return 0

        print()
        print("Gecici ped sifirlama deneniyor...")
        ok = printer.temporary_reset_waste()
        if ok:
            print("Gecici ped sifirlama tamam.")
            print(
                "Not: Yazici kapaninca geri gelebilir; ped bakimi planlanmali."
            )
            return 0

        print("Gecici sifirlama basarisiz (yazici rw:NG veya NA dondurdu).")
        print(
            "Bu modelde kalici SNMP/EEPROM sifirlama genelde firmware "
            "yuzunden kapali."
        )
        print(
            "Kalici cozum icin USB uzerinden ped reset araci (or. ez-reset) "
            "veya servis gerekir."
        )
        return 1
    except Exception as exc:
        print(f"Hata: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
