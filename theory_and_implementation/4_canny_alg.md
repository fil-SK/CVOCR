# Keni algoritam za detekciju ivica

## Detekcija ivica

Fantastičan uvod u ovo je Edge Detection Using Gradients | Edge Detection, First Principles of Computer Vision YouTube snimak: https://www.youtube.com/watch?v=lOEBsQodtEQ
- U nastavku dat je kratak pregled izloženog iz izvora.

### Šta je ivica?

Ivica je nagla promena intenziteta slike, na posmatranom malom regionu. Znamo da je izvod funkcije količina promene te funkcije. Tamo gde je funkcija konstantna, izvod će biti nula, dok se na promenama dobija neka vrednost izvoda. Lokalni ekstremumi funkcije označavaju ivice.
- Pozicija vrhova govori nam gde se ivica nalazi.
- Vrednost vrha govori nam koja je jačina ivice.

<img src="../report_images/detect_edges_1st_der.png" width="600px" />

Izvor slike: *Edge Detection Using Gradients | Edge Detection, First Principles of Computer Vision YouTube snimak: https://www.youtube.com/watch?v=lOEBsQodtEQ*

U slučaju 2D slike, parcijalnim izvodima možemo da odredimo promenu intenziteta, po konkretnoj dimenziji. Za te potrebe koristimo operator gradijenta. Gradijent slike, po njenim koordinatama x i y, jeste parcijalni izvod slike po te dve promenljive:

$$
\nabla Slika=[\frac{\partial Slika}{\partial x}, \frac{\partial Slika}{\partial y}]
$$

U zavisnosti od konkretnog tipa ivice, možemo da imamo različite vrednosti gradijenta:

<img src="../report_images/partial_derivatives.png" />

Koristeći ova dva parcijalna izvoda, po promenljivama, odnosno širini i visini, možemo da dobijemo dva krucijalna podatka:

**Snagu (jačinu) ivice - Gradient Magnitude**:

$$
Snaga = \left\| \nabla Slika \right\| = \sqrt{(\frac{\partial Slika}{\partial x})^2 + (\frac{\partial Slika}{\partial y})^2}
$$

**Orijentaciju ivice**:

$$
Orijentacija = arctg(\frac{\partial Slika}{\partial x} / \frac{\partial Slika}{\partial y})
$$

Parcijalni izvodi mogu se implementirati preko konvolucije, uz pažljivo odabrane vrednosti kernela. Detaljnije o ovome u priloženom izvoru. Kao primena u Keni algoritmu, koristiće se Sobel operator koji, za x i y vrednosti, ima različite kernele:

$$
Sobel_X = \left[
\begin{matrix}
-1 & 0 & 1 \\
-2 & 0 & 2 \\
-1 & 0 & 1 \\
\end{matrix}
\right]
$$

$$
Sobel_Y = \left[
\begin{matrix}
1 & 2 & 1 \\
0 & 0 & 0 \\
-1 & -2 & -1 \\
\end{matrix}
\right]
$$

Napomena: U kodu su korišćene vrednosti matrica sa invertovanim prvim i trećim redom. Intuitivnija, ali jako primitivna, analiza: [Invertovani redovi analiza](./4_5_inverted_rows_explanation.md)
- *Wikipedia: "He also assumed the vertical axis increasing upwards instead of downwards as is common in image processing nowadays, and hence the vertical kernel is flipped."*
- Izvor: https://en.wikipedia.org/wiki/Sobel_operator#Formulation

## Implementacija

Želimo da implementiramo OpenCV implementaciju:

```
edges = cv2.Canny(blurred, 100, 200)
```

Prema [Canny OpenCV dokumentaciji](https://docs.opencv.org/4.x/da/d22/tutorial_py_canny.html), ova funkcija realizovana je kroz sledeće korake:
- 1. Redukcija smetnji (Noise reduction): Gaussian Blur sa 5x5 kernelom
- 2. Izračunavanje intenziteta gradijenta slike
- 3. Non-Maximum Suppression
- 3.5. U određenim resursima (npr. [Wikipedia](https://en.wikipedia.org/wiki/Canny_edge_detector#Double_threshold)) postoji međukorak između NMS-a i histerezisa, gde se vrši Double Tresholding.
- 4. Hysteresis Thresholding

### Implementacija: Redukcija smetnji

Ovaj korak je već ispunjen, budući da kao input u našoj Keni implementaciji imamo sliku na kojoj je primenjeno Gausovo zamućivanje.

### Implementacija: Izračunavanje intenziteta gradijenta slike

Kao što je rečeno u uvodu, da bismo došli do ovog dela, neophodno je da imamo parcijalne izvode po x i y. Za to:
- Formiramo Sobel kernele.
- Vršimo konvoluciju sa input Gaussian blur slikom, i konkretnim Sobel kernelom, za x i y. Konvolucija je standardno ručno implementirana.

Nakon ovoga možemo da računamo magnitudu (snagu) ivice i njenu orijentaciju.

Izvor: OpenCV docs: 

U određ

TODO objašnjenje, kroz ove izvore što sam video

Za double threshold:
After application of non-maximum suppression, the remaining edge pixels provide a more accurate representation of real edges in an image. However, some edge pixels remain that are caused by noise and color variation. To account for these spurious responses, it is essential to filter out edge pixels with a weak gradient value and preserve edge pixels with a high gradient value

After you compute:

Gradient magnitude (how strong the edge is), and

Non-Maximum Suppression (to thin it to one pixel wide),

you end up with an image where strong edges have high magnitudes, and weak edges or noise have low magnitudes.

| Category         | Range                           | Interpretation                    |
| ---------------- | ------------------------------- | --------------------------------- |
| **Strong edges** | `G >= high_thresh`              | Confidently part of an edge       |
| **Weak edges**   | `low_thresh <= G < high_thresh` | Maybe an edge, needs confirmation |
| **Non-edges**    | `G < low_thresh`                | Definitely noise, discard         |


## Izvori

- Edge Detection Using Gradients | Edge Detection, First Principles of Computer Vision YouTube snimak: https://www.youtube.com/watch?v=lOEBsQodtEQ
- Sobel operator, Wikipedia članak: https://en.wikipedia.org/wiki/Sobel_operator
- Canny Edge Detector | Edge Detection, First Principles of Computer Vision YouTube snimak: https://www.youtube.com/watch?v=hUC1uoigH6s
- Canny Edge Detector, Wikipedia članak: https://en.wikipedia.org/wiki/Canny_edge_detector
  - Dobar izvor za korake koje treba sprovesti
- RO-1.0X104: Non-Maximal Suppression in Canny Edge Detection Algorithm, Deep Eigen, YouTube snimak: https://www.youtube.com/watch?v=9cpTmJCsI0M