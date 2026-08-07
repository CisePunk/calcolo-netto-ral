# Esportazioni da Figma

Qui dentro va ciò che rende la presentazione leggibile **senza Figma**.

| File | Da dove viene |
|---|---|
| `riquadri/NN.M — titolo.png` | selezione dei riquadri in Figma → esporta PNG a 2× |
| `presentazione.pdf` | esporta tutti i riquadri, un file solo |
| `progetto.fig` | *File → Salva copia locale* |

I nomi dei PNG arrivano già giusti da Figma: sono i nomi dei riquadri, nella
forma `NN.M — titolo breve`. Non rinominarli — sono quelli che decidono
l'ordine e i titoli in `PRESENTAZIONE.md`.

Dopo ogni esportazione:

```
python3 strumenti/genera_presentazione.py
```

Il perché di tutto questo — e cosa succede se ci si affida al solo link — sta
in [COSTRUZIONE_FIGMA.md](COSTRUZIONE_FIGMA.md), sezione 7.
