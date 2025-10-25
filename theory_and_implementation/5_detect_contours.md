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

## Pojednostavljenje kontura

cv2 implementacija: `cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)` dodatno radi i pojednostavljenje detektovanih kontura - `cv2.CHAIN_APPROX_SIMPLE`.

Prema [OpenCV dokumentaciji o konturama](https://docs.opencv.org/4.x/d4/d73/tutorial_py_contours_begin.html):

*But actually do we need all the points? For eg, you found the contour of a straight line. Do you need all the points on the line to represent that line? No, we need just two end points of that line. This is what cv.CHAIN_APPROX_SIMPLE does. It removes all redundant points and compresses the contour, thereby saving memory.*

Ovo je pokušano u manuelnoj implementaciji:
- Kao argument prihvatamo listu kontura, gde je jedan element te liste jedna kontura, koja je zapravo lista svih tačaka odnosno piksela (x,y) koji postoje u toj konturi.
- Ideja algoritma, kao što je gore objašnjeno, jeste da ne čuvamo sve tačke te konture, već samo neophodne tačke, koje nam govore gde su, efektivno, uglovi posmatrane konture.
- Sve konture koje imaju manje od 4 tačke se odbacuju - ovo je zbog pretpostavke da ovde detektujemo tablicu, koja je pravougaonik, pa su nam potrebne minimalno 4 tačke unutar konture.
- U algoritmu, prva i poslednja tačka konture se uvek zadržavaju, a unutrašnje tačke želimo da isfiltriramo tj. očistimo što više možemo.
- Za posmatranu konturu, gledamo prethodnu i sledeću tačku u odnosu na posmatranu trenutnu. 
    - Putanja preth-trenutna je putanja1, putanja trenutna-sled je putanja2.
- Proveravamo da li postoji obična promena smera:

```
putanja1(x,y) != putanja2(x,y)
```

- Ako postoji promena putanje, onda smatramo da je u pitanju ugao, pa tu trenutnu tačku zadržavamo.
- Ako nema promene putanje, onda smo "na ravnoj liniji" unutar konture, pa je to tačka koju možemo da zanemarimo tj. obrišemo iz konture.

### Rezultat

Ovo nije dalo dobre performanse, jer su mnoge konture obrisane na ovaj način. Najverovatniji razlog za to je primitivna implementacija njihovog algoritma koja, primenjena na stvarnu sliku, nije adekvatna, iako idejno deluje kao da jeste.

Ovakva provera proverava promenu smera **na nivou piksela**, što se u praksi verovatno nikada neće desiti.

## Pojednostavljenje kontura - uz aproksimaciju ugla

Aproksimacija ugla uvodi neku vrstu tolerancije. Recimo da posmatramo tablicu, ali da je slika iskošena. Tada, na nivou piksela, ako analiziramo "ravnu" liniju, ona je kosa, pa se ta promena može detektovati kao ivica u prethodnoj implementaciji, iako ona to nije. Zato uvodimo toleranciju da ćemo promenu detektovati kao ivicu samo ako je većeg ugla od nekog ugla datog kao poređenje.
- Npr. ako je dat ugao 30 stepeni, tada, tek ako se detektuje promena u pikselima veća od tog ugla, to ostavljamo kao relevantnu tačku ivice.

Ovakav pristup, takođe, nije dao dobre performanse.

## Aproksimacija konture na mnogougao - DP algoritam

