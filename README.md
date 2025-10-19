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

