"""
Motore di calcolo RAL -> netto.

  registro.py   dove stanno i coefficienti e come si leggono
  calcolo.py    le regole di calcolo, come funzioni pure
  inverso.py    dal netto desiderato alla RAL da offrire

I numeri stanno in dati/coefficienti.json, non nel codice: cambiano ogni anno,
il codice no.
"""

from .calcolo import (calcola, Risultato, Voce, valida_ral, valida_giorni,
                      formatta_euro, formatta_percentuale)
from .inverso import ral_per_netto, RisultatoInverso, punti_di_salto

__all__ = [
    "calcola", "Risultato", "Voce", "valida_ral", "valida_giorni",
    "formatta_euro", "formatta_percentuale",
    "ral_per_netto", "RisultatoInverso", "punti_di_salto",
]
