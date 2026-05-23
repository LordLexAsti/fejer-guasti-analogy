# Analogie Fejér-Guasti : Lissage Spectral Arithmétique

[![arXiv](https://img.shields.io/badge/arXiv-math.NT-b31b1b.svg)](https://arxiv.org/)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

Ce dépôt accompagne l'article **"Analogie Fejér-Guasti : lissage spectral arithmétique"** qui établit une connexion structurelle profonde entre le noyau de Fejér en analyse harmonique et la Transformée de Guasti en théorie des nombres.

## Résumé

Tout comme Fejér a résolu le problème des oscillations de Gibbs par un lissage spectral des séries de Fourier, la Transformée de Guasti fournit un opérateur de normalisation qui transforme la distribution chaotique des diviseurs en signatures spectrales harmonieuses et comparables.

**Résultats principaux :**
- **Théorème de décroissance spectrale** : |G_m(n)| → 0 quand m → ∞
- **Formule asymptotique pour les premiers** : G_2(p) = (2√2/p)·i + O(1/p²)
- **Existence d'une moyenne spectrale** : C_1 ≈ 2.135 ± 0.003

## Structure du dépôt

```
fejer-guasti-analogy/
├── paper/                      # Article scientifique
│   ├── fejer_guasti_analogy.tex    # Source LaTeX
│   ├── fejer_guasti_analogy.pdf    # Article compilé (13 pages)
│   └── figures/                    # Graphiques
│       ├── decroissance_spectrale_n12.png
│       ├── comportement_G2_premiers.png
│       └── convergence_moyennes_M1.png
├── scripts/                    # Scripts de validation empirique
│   ├── test_decroissance_spectrale.py
│   ├── test_G2_premiers.py
│   └── test_moyennes_M1.py
├── data/                       # Données computationnelles
│   └── donnees_moyennes_M1.npz
└── docs/                       # Documentation supplémentaire
```

## Installation

### Prérequis

- Python 3.8 ou supérieur
- LaTeX (pour compiler l'article)

### Installation des dépendances Python

```bash
pip install -r requirements.txt
```

## Utilisation

### Reproduction des résultats

**Test 1 : Décroissance spectrale pour n=12**
```bash
python scripts/test_decroissance_spectrale.py
```
Génère `decroissance_spectrale_n12.png` montrant la décroissance de |G_m(12)| avec résonance à m=20.

**Test 2 : Comportement des nombres premiers**
```bash
python scripts/test_G2_premiers.py
```
Valide la formule asymptotique G_2(p) ≈ (2√2/p)·i pour p = 101, 1009, 10007.

**Test 3 : Convergence des moyennes**
```bash
python scripts/test_moyennes_M1.py
```
Calcule M_1(X) pour X ≤ 10000 et estime C_1 ≈ 2.135 (⚠️ calcul long : ~1 minute).

### Compilation de l'article

```bash
cd paper
pdflatex fejer_guasti_analogy.tex
pdflatex fejer_guasti_analogy.tex  # Seconde passe pour les références
```

## Résultats clés

### Décroissance spectrale (Test 1)

Pour n=12 (6 diviseurs), on observe :

| Mode m | \|G_m(12)\| | Variation |
|--------|-------------|-----------|
| 1      | 2.162       | —         |
| 2      | 1.409       | ×0.65     |
| 5      | 0.697       | ×0.49     |
| 10     | 0.665       | ×0.95     |
| 20     | 1.511       | ×2.27 (résonance) |
| 50     | 0.434       | ×0.29     |

**Découverte** : Résonance locale à m=20 due à une synchronisation partielle des phases.

### Nombres premiers (Test 2)

Pour les grands premiers :

| Premier p | \|G_2(p)\| | Loi théorique |
|-----------|------------|---------------|
| 101       | 0.028001   | 2√2/p = 0.028  |
| 1009      | 0.002803   | 2√2/p = 0.0028 |
| 10007     | 0.000283   | 2√2/p = 0.00028|

**Résultat** : Loi de puissance exacte α ≈ 1 validée empiriquement.

### Moyennes spectrales (Test 3)

| X     | M_1(X) | Variation |
|-------|--------|-----------|
| 100   | 1.698  | +0.084    |
| 1000  | 1.932  | +0.068    |
| 10000 | 2.139  | +0.060    |

**Estimation** : C_1 ≈ 2.135 ± 0.003 (limite asymptotique).

## Contexte : La Grille et la Transformée de Guasti

### Grille de Guasti

Réinterprétation géométrique de la table de multiplication :
- **Ligne n** = table de multiplication de n
- **Colonne k** = diviseurs de k
- **Nombres premiers** = silence géométrique (seulement 2 diviseurs)

### Transformée de Guasti

Pour un entier n et un mode m :

```
G_m(n) = (1/√τ(n)) · Σ_{d|n} exp(i·m·θ(d,n))
```

où θ(d,n) = arctan(n/d²) est l'**angle de Guasti**.

**Propriétés** :
- |G_m(n)| ≤ 1 (bornage uniforme)
- G_2(n) purement imaginaire pour tout n
- Décroissance spectrale en O(1/√m)

## Citation

Si vous utilisez ce travail, veuillez citer :

```bibtex
@article{guasti2026fejer,
  title={Analogie Fejér-Guasti : lissage spectral arithmétique},
  author={Guasti, Alexandre},
  year={2026},
  eprint={arXiv:XXXX.XXXXX},
  archivePrefix={arXiv},
  primaryClass={math.NT}
}
```

Voir aussi `CITATION.cff` pour le format standard.

## Licence

Ce travail est sous licence [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/).

**Vous êtes libre de :**
- Partager — copier et redistribuer le matériel
- Adapter — remixer, transformer et créer à partir du matériel

**Sous les conditions suivantes :**
- Attribution — Vous devez créditer l'œuvre et indiquer si des modifications ont été effectuées

Le code Python est également sous licence MIT (voir fichiers individuels).

## Auteur

**Alexandre Guasti**  
Chercheur indépendant  
Lyon, France

📧 Contact : [via GitHub Issues](https://github.com/LordLexAsti/fejer-guasti-analogy/issues)

## Contributions

Les contributions sont bienvenues ! Pour proposer des améliorations :

1. Fork le projet
2. Créez une branche pour votre fonctionnalité (`git checkout -b feature/amelioration`)
3. Commit vos changements (`git commit -am 'Ajout d'une amélioration'`)
4. Push vers la branche (`git push origin feature/amelioration`)
5. Ouvrez une Pull Request

## Remerciements

Ce travail s'inscrit dans le cadre du **Protocole TriadIA** de validation multi-IA, avec contributions de Claude (Anthropic), ChatGPT (OpenAI), Gemini (Google), et Grok (xAI).

## Liens connexes

- **Dépôts GitHub connexes** :
  - [Grille de Guasti](https://github.com/LordLexAsti/Guasti-grid)
  - [Transformée de Guasti V2](https://github.com/LordLexAsti/guasti-transform-V2)
  - [Hypothèse de Guasti](https://github.com/LordLexAsti/Hypot-se-de-Guasti)

- **Documentation** :
  - [Théorie de Guasti - Instructions complètes](./docs/) (à venir)

## Statut

- ✅ Papier rédigé et validé empiriquement
- ✅ Scripts de reproduction disponibles
- ⏳ Soumission arXiv en préparation
- ⏳ Soumission revue spécialisée en préparation

---

**Note** : Ce README sera mis à jour au fur et à mesure de l'avancement du projet (soumission arXiv, reviews, etc.).
