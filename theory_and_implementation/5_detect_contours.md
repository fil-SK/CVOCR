# Detekcija kontura

## Uvod

Nakon određivanja ivica i filtriranja slike od smetnji i nerelevantnih piksela, prelazimo na korak određivanja kontura.
- Ovaj korak predstavlja osnovu za dalji rad. Želimo da detektujemo konture koje će, između ostalog, predstavljati tablicu, iz koje će se ekstraktovati tekst.

Ovaj deo projekta treba da ručno implementira sledeći kod referisanog blog posta:

```python
contours = sorted(contours, key=cv2.contourArea, reverse=True)
    plate_contour = None
    for contour in contours:
        epsilon = 0.02 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)
        
        if len(approx) == 4:
            plate_contour = approx
            break
```

Implementacija će se sastojati iz dva koraka:
- Detekcija kontura, iz formiranih ivica
- Pojednostavljenje kontura

## Detekcija kontura

Izlaz Keni algoritma čine jaki pikseli, čija vrednost je postavljena na `255` - belu boju, i "prazni" pikseli, odnosno oni s vrednošću `0`. Algoritam detekcije kontura treba da prođe kroz sve jake piksele i analizira da li, počevši od nekog piksela `i`, možemo da prolazimo kroz piksele tako da na kraju formiramo zatvoren ciklus - konturu.

Algoritam:

- Za svaki piksel koji je jak piksel, pratimo da li je već posećen ili ne. Ukoliko nije, onda njim započinjemo novu konturu.
- Za taj piksel, proveravamo njegove susedne piksele. Ako svaki piksel potencijalno može biti kontura, onda tu konturu čine susedi tok piksela.
    - U ovom koraku algoritma primenjujemo DFS pretragu.
    - Krećemo od neproverenog piksela, on sada postaje proveren. Zatim, proveravamo njegove susede, tako da svaki neprovereni piksel dodajemo u listu piksela koje treba proveriti.
    - Ovaj korak se radi rekurzivno, dok za "originalni" neposećen piksel naiđemo na prvi piksel u toj obradi koji je posećen - to je piksel koji zatvara trenutno posmatranu konturu.