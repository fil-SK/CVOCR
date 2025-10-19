# Computer Vision OCR Pipeline implementacija

## Uvod

Ovaj dokument napisan je primarno kao izveštaj za projekat iz predmeta Kompjuterske vizije na Elektrotehničkom fakultetu, Univerziteta U beogradu.

Projekat predstavlja ručnu implementaciju pipeline-a za OCR detekciju registrarskih tablica, čija je struktura data na: https://www.geeksforgeeks.org/machine-learning/license-plate-recognition-with-opencv-and-tesseract-ocr/

## Cilj

Cilj projekta jeste da ručno implementira sve delove pipeline-a (do samog OCR poziva) date u priloženom blog postu, kao ilustraciju funkcionisanja konkretnih Computer Vision pristupa i algoritama. 

## Preduslovi za instalaciju

- Python IDE
- Git

## Struktura fajlova

Finalni izgled fajl sistema izgleda ovako:

```
root
|--- image_related_ops
    |--- load_image.py
    |--- grayscale.py
|--- test_images
|--- main.py
|--- README.md
```

### Pojašnjenje:
- `image_related_ops`: Folder u kom su skripte koje vrše opšte operacije sa slikom.
    - `load_image.py`: Učitava sliku preko PIL-a.
    - `grayscale.py`: Konvertuje sliku u crno-beli prikaz.
`test_images`: Folder u kom se nalaze slike korišćene za primenu projekta.
- `main.py`: Početna tačka od koje kreće izvršavanje programa, iz kog se pozivaju sve funkcije.
- `README.md`: Uputstvo / izveštaj

## Instalacija i pokretanje

Klonirati projekat:

```
git clone https://github.com/fil-SK/CVOCR.git
```

Instalirati dependencies:

```
pip install -r requirements.txt
```

## Postupak rada

### 1. Učitavanje slike

Dva najčešća pristupa za učitavanje i rad sa slikama su:
- PIL (Pillow)
- OpenCV (cv2)

Iako je po pitanju performansi `cv2` bolji jer ima optimizovaniji C++ backend, `PIL` se koristi za manipulaciju slikama opšteg tipa, pa je zato odabran za potrebe ovog projekta.

### 2. Konverzija u crno-belo (grayscale)

Nakon učitavanja slike, prvi (stvarni) proces u pipeline-u je konverzija RGB slike u crno-belu. Ovakva konverzija čini sliku jednostavnijom za rad, prostorno je smanjujući (smanjuje broj kanala), što olakšava i ubrzava njeno dalje procesiranje.

Svaka slika se na računaru predstavlja kroz 3 kanala: RGB (Red Green Blue) - intenzitet zastupljenosti crvene, zelene i plave boje. Da bi se slika predstavila kao crno-bela (grayscale), potrebno je da se 3 kanala pretvore u jedan, koji će svaku od boja predstaviti kao neku nijansu sive.

Ova funkcionalnost odrađuje ekvivalentno kao CV biblioteka sa `gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)`

Iako se aproksimacija u sivu može uraditi prostim usrednjavanjem:

$$
gray = \frac{R+G+B}{3}
$$

ovakav pristup ne bi bio dobar jer ljudsko oko nije podjednako osetljivo na ove tri boje. Ljudsko oko je najosetljivije na zelenu, zatim na crvenu i najmanje osetljivo na plavu. Iz tog razloga koristi se formula koja uzima u obzir koeficijente za konkretnu boju.

`ITU-R BT.601` je standard koji se koristi za enkodovanje analognog signala u digitalni oblik. Na [njihovom sajtu](https://www.itu.int/dms_pubrec/itu-r/rec/bt/R-REC-BT.601-7-201103-I!!PDF-E.pdf) moguće je naći konkretne vrednosti koje su preporučene za ovaj vid konverzije:

- Crvena: `0.299 R`
- Zelena: `0.587 G`
- Plava: `0.114 B`

Gde su `R`, `G` i `B` konkretne numeričke vrednosti koje posmatrana slika ima. Numeričke vrednosti su celobrojne, `int8`, pa imaju opseg `[0,255]`.

Dodatni, opcioni resursi:
- https://en.wikipedia.org/wiki/Grayscale
-  https://www.geeksforgeeks.org/python/python-grayscaling-of-images-using-opencv/

