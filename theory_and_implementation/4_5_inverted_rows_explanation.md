# Pojašnjenje za obrnute redove 1 i 3 Sobel operatora

Koordinate (x, y) označavaju, standardno, u matematici, Dekartov koordinatni sistem gde:
- x raste sleva nadesno
- y raste odozdo nagore

Samim tim, veća y vrednost znači da je pozicionirana "na većoj visini".

U računarstvu, konkretno obradi slike, koordinate (x,y) su takve da:
- x raste sleva nadesno
- y raste odozgo NADOLE

Ako posmatramo kernel:

$$
Sobel_Y = \left[
\begin{matrix}
1 & 2 & 1 \\
0 & 0 & 0 \\
-1 & -2 & -1 \\
\end{matrix}
\right]
$$

Prvi red, `[1, 2, 1]` primenjuje se na piksele iznad trenutno posmatranog. Treći red, `[-1, -2, -1]`, primenjuje se na piksele ispod posmatranog. Pošto je "iznad" posmatranog piksela, u računarima, sa manjom y vrednošću, tada y ne raste onako kako je u matematici. Zato se ova dva reda obrću, kako bi se te vrednosti primenile baš na ono što treba.