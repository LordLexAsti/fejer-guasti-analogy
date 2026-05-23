#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de décroissance spectrale pour la Transformée de Guasti
Cas test : n = 12 (6 diviseurs)
"""

import numpy as np
import matplotlib.pyplot as plt

def diviseurs(n):
    """Retourne la liste des diviseurs de n."""
    divs = []
    for i in range(1, int(np.sqrt(n)) + 1):
        if n % i == 0:
            divs.append(i)
            if i != n // i:
                divs.append(n // i)
    return sorted(divs)

def angle_guasti(d, n):
    """Calcule l'angle de Guasti θ(d,n) = arctan(n/d²)."""
    return np.arctan(n / (d**2))

def transformee_guasti(n, m):
    """
    Calcule G_m(n) = (1/√τ(n)) · Σ_{d|n} exp(i·m·θ(d,n))
    
    Retourne un nombre complexe.
    """
    divs = diviseurs(n)
    tau_n = len(divs)
    
    somme = 0.0 + 0.0j
    for d in divs:
        theta = angle_guasti(d, n)
        somme += np.exp(1j * m * theta)
    
    G_m = somme / np.sqrt(tau_n)
    return G_m

def test_decroissance_n12():
    """Test de décroissance pour n = 12."""
    n = 12
    modes = [1, 2, 5, 10, 20, 50]
    
    print(f"Test de décroissance spectrale pour n = {n}")
    print(f"Diviseurs de {n} : {diviseurs(n)}")
    print(f"τ({n}) = {len(diviseurs(n))}")
    print()
    
    # Affichage des angles
    print("Angles de Guasti θ(d,n) pour chaque diviseur :")
    for d in diviseurs(n):
        theta = angle_guasti(d, n)
        theta_deg = np.degrees(theta)
        print(f"  d = {d:2d} : θ({d},{n}) = {theta:.6f} rad = {theta_deg:.2f}°")
    print()
    
    # Calcul de G_m(12) pour différents modes
    print("Calcul de G_m(12) pour différents modes m :")
    print(f"{'Mode m':>8} | {'Re(G_m)':>12} | {'Im(G_m)':>12} | {'|G_m|':>12} | {'Théorie 1/√m':>15}")
    print("-" * 75)
    
    resultats = []
    for m in modes:
        G_m = transformee_guasti(n, m)
        module = np.abs(G_m)
        
        # Prédiction théorique O(1/√m) normalisée par |G_1|
        if m == 1:
            G_1_ref = module
        prediction = G_1_ref / np.sqrt(m)
        
        resultats.append((m, G_m.real, G_m.imag, module, prediction))
        print(f"{m:8d} | {G_m.real:12.6f} | {G_m.imag:12.6f} | {module:12.6f} | {prediction:15.6f}")
    
    print()
    
    # Vérification de la décroissance
    print("Vérification de la décroissance :")
    for i in range(len(resultats) - 1):
        m1, _, _, mod1, _ = resultats[i]
        m2, _, _, mod2, _ = resultats[i+1]
        ratio = mod2 / mod1
        print(f"  |G_{m2}| / |G_{m1}| = {ratio:.6f} {'✓ décroit' if ratio < 1 else '✗ ne décroit pas'}")
    
    print()
    
    # Compatibilité avec O(1/√m)
    print("Compatibilité avec la loi O(1/√m) :")
    print("Si |G_m| ~ C/√m, alors |G_m| · √m devrait être approximativement constant.")
    print(f"{'Mode m':>8} | {'|G_m| · √m':>15} | {'Écart relatif':>15}")
    print("-" * 45)
    
    produits = [mod * np.sqrt(m) for m, _, _, mod, _ in resultats]
    moyenne = np.mean(produits)
    
    for (m, _, _, mod, _), prod in zip(resultats, produits):
        ecart = abs(prod - moyenne) / moyenne * 100
        print(f"{m:8d} | {prod:15.6f} | {ecart:14.2f}%")
    
    print()
    print(f"Moyenne de |G_m| · √m = {moyenne:.6f}")
    print(f"Écart-type = {np.std(produits):.6f}")
    
    # Visualisation
    plt.figure(figsize=(12, 5))
    
    # Graphique 1 : Décroissance de |G_m|
    plt.subplot(1, 2, 1)
    modes_array = np.array(modes)
    modules = np.array([mod for _, _, _, mod, _ in resultats])
    predictions = np.array([pred for _, _, _, _, pred in resultats])
    
    plt.plot(modes_array, modules, 'o-', label='|G_m(12)| calculé', linewidth=2, markersize=8)
    plt.plot(modes_array, predictions, 's--', label='Prédiction 1/√m', linewidth=1.5, markersize=6, alpha=0.7)
    plt.xlabel('Mode m', fontsize=12)
    plt.ylabel('|G_m(12)|', fontsize=12)
    plt.title('Décroissance spectrale pour n = 12', fontsize=14, fontweight='bold')
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.xscale('log')
    plt.yscale('log')
    
    # Graphique 2 : Test |G_m| · √m = constante
    plt.subplot(1, 2, 2)
    plt.plot(modes_array, produits, 'o-', linewidth=2, markersize=8, color='green')
    plt.axhline(y=moyenne, color='red', linestyle='--', linewidth=1.5, label=f'Moyenne = {moyenne:.3f}')
    plt.xlabel('Mode m', fontsize=12)
    plt.ylabel('|G_m(12)| · √m', fontsize=12)
    plt.title('Test de la loi O(1/√m)', fontsize=14, fontweight='bold')
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('/home/claude/decroissance_spectrale_n12.png', dpi=150, bbox_inches='tight')
    print("\nGraphique sauvegardé : decroissance_spectrale_n12.png")
    
    return resultats

if __name__ == "__main__":
    resultats = test_decroissance_n12()
