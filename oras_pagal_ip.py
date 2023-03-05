import requests
import json
import csv
from os import environ


def gauti_temperatura(API, miestai):
    nuoroda = "http://api.openweathermap.org/data/2.5/weather"
    miesto_oras = []
    for miestas in miestai:
        uzklausa = {"q": miestas, "appid": API}
        atsakymas = requests.get(nuoroda, params=uzklausa)
        oru_duomenys = atsakymas.json()
        temp_kelvin = oru_duomenys['main']['temp']
        temp_celsijus = temp_kelvin - 273.15
        oru_aprasymas = oru_duomenys['weather'][0]['description']
        miesto_oras.append({
            "miestas": miestas,
            "temp_celsijus": f"{temp_celsijus:.2f}",
            "oru_aprasymas": oru_aprasymas
        })
    return miesto_oras


def gauti_sali_pagal_ip():
    atsakymas = requests.post("http://ip-api.com/batch", json=[
        {"query": "122.35.203.161"},
        {"query": "174.217.10.111"},
        {"query": "187.121.176.91"},
        {"query": "176.114.85.116"},
        {"query": "174.59.204.133"},
        {"query": "54.209.112.174"},
        {"query": "109.185.143.49"},
        {"query": "176.114.253.216"},
        {"query": "210.171.87.76"},
        {"query": "24.169.250.142"}
    ]).text

    data = json.loads(atsakymas)

    with open('miestu_temperaturos.csv', mode='w', newline='') as failas:
        lauku_pavadinimai = ['IP', 'Šalis', 'Miestas', 'Temperatūra', 'Oras']
        writer = csv.DictWriter(failas, fieldnames=lauku_pavadinimai)

        writer.writeheader()

        for i in data:
            ip = i["query"]
            salis = i["country"]
            miestas = i["city"]
            miesto_oras = gauti_temperatura(environ.get('ORAS'), [miestas])
            for oras in miesto_oras:
                writer.writerow({
                    "IP": ip,
                    "Šalis": salis,
                    "Miestas": oras["miestas"],
                    "Temperatūra": oras["temp_celsijus"],
                    "Oras": oras["oru_aprasymas"]
                })


gauti_sali_pagal_ip()
