# Konverzija RGB slike u crno-belo

## Ideja

Svaka slika se na računaru predstavlja kroz 3 kanala: RGB (Red Green Blue) - intenzitet zastupljenosti crvene, zelene i plave boje. Da bi se slika predstavila kao crno-bela (grayscale), potrebno je da se 3 kanala pretvore u jedan, koji će svaku od boja predstaviti kao neku nijansu sive. Kod crno-bele (grayscale) slike, numerička vrednost slike predstavlja osvetljenost nijanse sive (brightness, luminance).

Ova funkcionalnost odrađuje ekvivalentno kao CV biblioteka sa `gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)`

Iako se aproksimacija u sivu može uraditi prostim usrednjavanjem:

$$
gray = \frac{R+G+B}{3}
$$

ovakav pristup ne bi bio dobar jer ljudsko oko nije podjednako osetljivo na ove tri boje. Ljudsko oko je najosetljivije na zelenu, zatim na crvenu i najmanje osetljivo na plavu. Iz tog razloga koristi se formula koja uzima u obzir koeficijente za konkretnu boju.

## Koeficijenti

`ITU-R BT.601` je standard koji se koristi za enkodovanje analognog signala u digitalni oblik. Na [njihovom sajtu](https://www.itu.int/dms_pubrec/itu-r/rec/bt/R-REC-BT.601-7-201103-I!!PDF-E.pdf) moguće je naći konkretne vrednosti koje su preporučene za ovaj vid konverzije:

- Crvena: `0.299 R`
- Zelena: `0.587 G`
- Plava: `0.114 B`

Gde su `R`, `G` i `B` konkretne numeričke vrednosti koje posmatrana slika ima. Numeričke vrednosti su celobrojne, `int8`, pa imaju opseg `[0,255]`.

## OpenCV i PIL implementacija

Možemo se uveriti da i PIL i OpenCV koriste baš ove vrednosti u svojoj grayscale implementaciji:

PIL: 

```
#define L(rgb) ((INT32)(rgb)[0] * 299 + (INT32)(rgb)[1] * 587 + (INT32)(rgb)[2] * 114)
```

Izvor:
- Pillow Imaging Library, Official GitHub repo, linija 43: https://github.com/python-pillow/Pillow/blob/main/src/libImaging/Convert.c#L43

OpenCV:

```
Transformations within RGB space like adding/removing the alpha channel, reversing the channel order, conversion to/from 16-bit RGB color (R5:G6:B5 or R5:G5:B5), as well as conversion to/from grayscale using:
RGB[A] to Gray: Y <- 0.299 R + 0.587 G + 0.114 B
```

## Izvori i resursi

Izvor:
- Open CV dokumentacija: https://docs.opencv.org/4.x/de/d25/imgproc_color_conversions.html

Dodatni, opcioni resursi:
- Grayscale, Wikipedija članak: https://en.wikipedia.org/wiki/Grayscale
- Python grayscaling of images using OpenCV, GeeksForGeeks blog: https://www.geeksforgeeks.org/python/python-grayscaling-of-images-using-opencv/
- OpenCV Python Grayscale, Kevin Wood | Robotics & AI YouTube snimak: https://www.youtube.com/watch?v=gm2Bnfhq2Rw