# Guide de Démarrage Rapide

Ce guide vous permet de reproduire rapidement les résultats de l'article.

## Installation rapide

```bash
# Cloner le dépôt
git clone https://github.com/LordLexAsti/fejer-guasti-analogy.git
cd fejer-guasti-analogy

# Installer les dépendances
pip install -r requirements.txt
```

## Reproduction des résultats (ordre recommandé)

### 1. Test de décroissance spectrale (~5 secondes)

```bash
python scripts/test_decroissance_spectrale.py
```

**Sortie attendue :**
- Tableau de |G_m(12)| pour m = 1, 2, 5, 10, 20, 50
- Graphique `decroissance_spectrale_n12.png`
- Observation de la résonance à m=20

**Résultat clé :** Décroissance globale confirmée avec résonance locale.

### 2. Test sur les nombres premiers (~10 secondes)

```bash
python scripts/test_G2_premiers.py
```

**Sortie attendue :**
- Calculs pour p = 101, 1009, 10007
- Validation de la formule G_2(p) ≈ (2√2/p)·i
- Graphique `comportement_G2_premiers.png`

**Résultat clé :** Loi de puissance α ≈ 1 validée empiriquement.

### 3. Test de convergence des moyennes (~60 secondes)

⚠️ **Attention** : Ce test calcule G_1(n) pour 10000 entiers. Temps estimé : 1 minute.

```bash
python scripts/test_moyennes_M1.py
```

**Sortie attendue :**
- Tableau de M_1(X) pour X = 100, 1000, 10000
- Estimation C_1 ≈ 2.135 ± 0.003
- Graphique `convergence_moyennes_M1.png`
- Fichier de données `donnees_moyennes_M1.npz`

**Résultat clé :** Existence de la moyenne spectrale confirmée.

## Vérification des résultats

Après avoir exécuté les trois scripts, vous devriez avoir :

```
fejer-guasti-analogy/
├── decroissance_spectrale_n12.png     ✓
├── comportement_G2_premiers.png       ✓
├── convergence_moyennes_M1.png        ✓
└── data/
    └── donnees_moyennes_M1.npz        ✓
```

Comparez vos graphiques avec ceux dans `paper/figures/` pour valider.

## Compilation de l'article

```bash
cd paper
pdflatex fejer_guasti_analogy.tex
pdflatex fejer_guasti_analogy.tex  # Seconde passe
```

Le PDF généré doit faire **13 pages** et **~600 KB**.

## Exploration interactive

Pour explorer les résultats du Test 3 :

```python
import numpy as np

# Charger les données sauvegardées
data = np.load('data/donnees_moyennes_M1.npz')
X = data['X']
M = data['M']
modules = data['modules']

# Afficher les valeurs aux points clés
print(f"M_1(100) = {M[99]:.6f}")
print(f"M_1(1000) = {M[999]:.6f}")
print(f"M_1(10000) = {M[9999]:.6f}")

# Trouver l'entier avec le spectre maximal
idx_max = np.argmax(modules)
print(f"Spectre maximal : n = {idx_max+1}, |G_1(n)| = {modules[idx_max]:.6f}")
```

## Troubleshooting

**Problème** : `ModuleNotFoundError: No module named 'tqdm'`  
**Solution** : `pip install tqdm`

**Problème** : Les graphiques ne s'affichent pas  
**Solution** : Les graphiques sont sauvegardés en PNG. Ouvrez-les avec un visualiseur d'images.

**Problème** : Le Test 3 prend trop de temps  
**Solution** : Réduisez X_max dans `test_moyennes_M1.py` (ligne 120) à 1000 au lieu de 10000.

## Questions ?

Ouvrez une [issue sur GitHub](https://github.com/LordLexAsti/fejer-guasti-analogy/issues).
