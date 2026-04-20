# TableTalk

TableTalk je web aplikacija za pregled restorana i analizu komentara korisnika.

Dvije vrste korisnika:
- visitor – može pregledavati restorane i ostavljati komentare
- owner – može dodati restoran i vidjeti statistiku

Komentari se šalju na ML model (Microsoft Azure) koji određuje je li komentar pozitivan ili negativan.

---

## Pokretanje

1. Klonirati repozitorij:

```
git clone <link_na_repo>  
cd TableTalk  
```

2. Pokrenuti projekt:

```
python -m venv venv  
source venv/Scripts/activate  
pip install -r requirements.txt  
python manage.py runserver 
``` 

3. Otvoriti u browseru: 
``` 
http://127.0.0.1:8000/
```

---

## Napomena

Kako bi procjena sentimenta radila, potrebno je napraviti `.env` datoteku u rootu projekta:

AZURE_ENDPOINT_URL = ...
AZURE_ENDPOINT_KEY = ...

---

## Primjeri kreiranih korisnika

Visitor:  
username: jamesh
password: asdfasdf.1 

Owner:  
username: turner1
password: asdfasdf.1

Admin:  
username: admin1  
password: admin 

---

## Korištenje aplikacije

1. Kao visitor:
- pregled restorana  
- otvaranje detalja  
- dodavanje komentara  

2. Kao owner:
- dodavanje restorana  
- pregled statistike (grafovi)  

3. Kao admin:
- ručno uređivanje podataka na Admin panelu

---

## Ostalo

- baza (`db.sqlite3`) je uključena s primjerima podataka  
- slike restorana su u `media/` folderu  