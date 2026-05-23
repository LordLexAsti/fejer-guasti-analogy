#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de convergence des moyennes spectrales
M_1(X) = (1/X) Σ_{n≤X} |G_1(n)|
"""

import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

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

def G_m(n, m):
    """
    Calcule G_m(n) = (1/√τ(n)) · Σ_{d|n} exp(i·m·θ(d,n))
    """
    if n == 1:
        return 1.0 + 0.0j
    
    divs = diviseurs(n)
    tau_n = len(divs)
    
    somme = 0.0 + 0.0j
    for d in divs:
        theta = angle_guasti(d, n)
        somme += np.exp(1j * m * theta)
    
    return somme / np.sqrt(tau_n)

def calcul_moyennes(X_max, m=1):
    """
    Calcule M_m(X) pour X allant de 1 à X_max.
    Retourne les tableaux X et M_m(X).
    """
    print(f"Calcul de M_{m}(X) pour X = 1 à {X_max}...")
    
    # Calcul de |G_m(n)| pour tous les n
    modules = []
    for n in tqdm(range(1, X_max + 1), desc=f"Calcul |G_{m}(n)|"):
        G = G_m(n, m)
        modules.append(np.abs(G))
    
    # Calcul des moyennes cumulatives
    X_vals = []
    M_vals = []
    
    somme_cumulative = 0.0
    for X in tqdm(range(1, X_max + 1), desc="Calcul moyennes"):
        somme_cumulative += modules[X - 1]
        M = somme_cumulative / X
        X_vals.append(X)
        M_vals.append(M)
    
    return np.array(X_vals), np.array(M_vals), np.array(modules)

def analyse_convergence(X_vals, M_vals, titre="M_1(X)"):
    """Analyse la convergence de M(X)."""
    print(f"\n{'=' * 80}")
    print(f"ANALYSE DE CONVERGENCE : {titre}")
    print('=' * 80)
    
    # Valeurs à différentes échelles
    echelles = [10, 50, 100, 500, 1000, 5000, 10000]
    echelles = [e for e in echelles if e <= len(X_vals)]
    
    print(f"\n{'X':>8} | {'M(X)':>15} | {'Variation':>15}")
    print('-' * 45)
    
    M_prev = None
    for X in echelles:
        idx = X - 1
        M = M_vals[idx]
        
        if M_prev is None:
            var = "—"
        else:
            delta = M - M_prev
            var = f"{delta:+.10f}"
        
        print(f"{X:8d} | {M:15.10f} | {var:>15}")
        M_prev = M
    
    # Estimation de la limite
    print()
    print("ESTIMATION DE LA LIMITE :")
    
    # Moyenne des 10% dernières valeurs
    n_fin = len(M_vals) // 10
    M_fin = np.mean(M_vals[-n_fin:])
    std_fin = np.std(M_vals[-n_fin:])
    
    print(f"  Moyenne des {n_fin} dernières valeurs : {M_fin:.10f}")
    print(f"  Écart-type : {std_fin:.10f}")
    print(f"  Estimation C_1 ≈ {M_fin:.10f} ± {std_fin:.10f}")
    
    # Test de stabilité : variation sur les derniers 10%
    variation_fin = np.max(M_vals[-n_fin:]) - np.min(M_vals[-n_fin:])
    print(f"  Variation max sur les {n_fin} dernières valeurs : {variation_fin:.10f}")
    
    # Taux de convergence
    print()
    print("VITESSE DE CONVERGENCE :")
    
    # Différences successives
    diff = np.abs(np.diff(M_vals[-1000:]))
    print(f"  Moyenne de |M(X+1) - M(X)| sur les 1000 derniers : {np.mean(diff):.10e}")
    print(f"  Maximum de |M(X+1) - M(X)| sur les 1000 derniers : {np.max(diff):.10e}")
    
    return M_fin, std_fin

def distribution_modules(modules, titre="|G_1(n)|"):
    """Analyse la distribution des modules."""
    print(f"\n{'=' * 80}")
    print(f"DISTRIBUTION DES MODULES : {titre}")
    print('=' * 80)
    
    print(f"\nStatistiques descriptives :")
    print(f"  Minimum    : {np.min(modules):.10f}")
    print(f"  Maximum    : {np.max(modules):.10f}")
    print(f"  Moyenne    : {np.mean(modules):.10f}")
    print(f"  Médiane    : {np.median(modules):.10f}")
    print(f"  Écart-type : {np.std(modules):.10f}")
    
    # Quartiles
    q25, q75 = np.percentile(modules, [25, 75])
    print(f"  Q1 (25%)   : {q25:.10f}")
    print(f"  Q3 (75%)   : {q75:.10f}")
    print(f"  IQR        : {q75 - q25:.10f}")
    
    # Valeurs remarquables
    print(f"\nValeurs remarquables :")
    idx_min = np.argmin(modules)
    idx_max = np.argmax(modules)
    print(f"  n = {idx_min + 1} : {titre} = {modules[idx_min]:.10f} (minimum)")
    print(f"  n = {idx_max + 1} : {titre} = {modules[idx_max]:.10f} (maximum)")

def test_moyennes():
    """Test principal."""
    X_max = 10000
    
    print("=" * 80)
    print("TEST DE CONVERGENCE DES MOYENNES SPECTRALES")
    print("=" * 80)
    print()
    print(f"Calcul de M_1(X) = (1/X) Σ_{{n≤X}} |G_1(n)|")
    print(f"Pour X allant de 1 à {X_max}")
    print()
    
    # Calcul
    X_vals, M_vals, modules = calcul_moyennes(X_max, m=1)
    
    # Analyse de convergence
    M_fin, std_fin = analyse_convergence(X_vals, M_vals, "M_1(X)")
    
    # Distribution
    distribution_modules(modules, "|G_1(n)|")
    
    # Résultats aux échelles demandées
    print(f"\n{'=' * 80}")
    print("RÉSULTATS AUX ÉCHELLES DEMANDÉES")
    print('=' * 80)
    print()
    
    for X in [100, 1000, 10000]:
        M = M_vals[X - 1]
        print(f"  M_1({X:5d}) = {M:.15f}")
    
    # Visualisations
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Graphique 1 : Convergence de M_1(X)
    ax1 = axes[0, 0]
    ax1.plot(X_vals, M_vals, linewidth=1.5)
    ax1.axhline(y=M_fin, color='red', linestyle='--', linewidth=2, 
                label=f'Limite ≈ {M_fin:.6f}')
    ax1.set_xlabel('X', fontsize=12)
    ax1.set_ylabel('M_1(X)', fontsize=12)
    ax1.set_title('Convergence de M_1(X)', fontsize=14, fontweight='bold')
    ax1.legend(fontsize=10)
    ax1.grid(True, alpha=0.3)
    ax1.set_xscale('log')
    
    # Graphique 2 : Zoom sur la fin
    ax2 = axes[0, 1]
    n_zoom = 1000
    ax2.plot(X_vals[-n_zoom:], M_vals[-n_zoom:], linewidth=2)
    ax2.axhline(y=M_fin, color='red', linestyle='--', linewidth=2)
    ax2.fill_between(X_vals[-n_zoom:], M_fin - std_fin, M_fin + std_fin, 
                      alpha=0.3, color='red', label=f'±σ = ±{std_fin:.6f}')
    ax2.set_xlabel('X', fontsize=12)
    ax2.set_ylabel('M_1(X)', fontsize=12)
    ax2.set_title(f'Zoom sur les {n_zoom} dernières valeurs', fontsize=14, fontweight='bold')
    ax2.legend(fontsize=10)
    ax2.grid(True, alpha=0.3)
    
    # Graphique 3 : Distribution des |G_1(n)|
    ax3 = axes[1, 0]
    ax3.hist(modules, bins=50, density=True, alpha=0.7, edgecolor='black')
    ax3.axvline(x=np.mean(modules), color='red', linestyle='--', linewidth=2, 
                label=f'Moyenne = {np.mean(modules):.4f}')
    ax3.axvline(x=np.median(modules), color='green', linestyle='--', linewidth=2, 
                label=f'Médiane = {np.median(modules):.4f}')
    ax3.set_xlabel('|G_1(n)|', fontsize=12)
    ax3.set_ylabel('Densité', fontsize=12)
    ax3.set_title('Distribution de |G_1(n)|', fontsize=14, fontweight='bold')
    ax3.legend(fontsize=10)
    ax3.grid(True, alpha=0.3)
    
    # Graphique 4 : Stabilité (différences successives)
    ax4 = axes[1, 1]
    diff = np.abs(np.diff(M_vals))
    ax4.semilogy(X_vals[1:], diff, linewidth=1, alpha=0.7)
    ax4.set_xlabel('X', fontsize=12)
    ax4.set_ylabel('|M_1(X+1) - M_1(X)|', fontsize=12)
    ax4.set_title('Stabilité de la convergence', fontsize=14, fontweight='bold')
    ax4.grid(True, alpha=0.3, which='both')
    
    plt.tight_layout()
    plt.savefig('/home/claude/convergence_moyennes_M1.png', dpi=150, bbox_inches='tight')
    print()
    print("Graphique sauvegardé : convergence_moyennes_M1.png")
    
    # Sauvegarde des données
    np.savez('/home/claude/donnees_moyennes_M1.npz',
             X=X_vals, M=M_vals, modules=modules, M_fin=M_fin, std_fin=std_fin)
    print("Données sauvegardées : donnees_moyennes_M1.npz")
    
    return X_vals, M_vals, modules, M_fin, std_fin

if __name__ == "__main__":
    X_vals, M_vals, modules, M_fin, std_fin = test_moyennes()
