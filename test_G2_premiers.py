#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test du comportement de G_2(p) pour les grands nombres premiers
Prédiction théorique : |G_2(p)| → 0 quand p → ∞
"""

import numpy as np
import matplotlib.pyplot as plt

def est_premier(n):
    """Test de primalité simple."""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(np.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True

def angle_guasti(d, n):
    """Calcule l'angle de Guasti θ(d,n) = arctan(n/d²)."""
    return np.arctan(n / (d**2))

def G2_premier(p):
    """
    Calcule G_2(p) pour un nombre premier p.
    
    Pour un premier p, τ(p) = 2, diviseurs = {1, p}
    G_2(p) = (1/√2) · [exp(i·2·θ(1,p)) + exp(i·2·θ(p,p))]
    """
    # Vérification
    if not est_premier(p):
        raise ValueError(f"{p} n'est pas premier !")
    
    # Les deux angles
    theta_1_p = angle_guasti(1, p)
    theta_p_p = angle_guasti(p, p)
    
    # G_2(p)
    G2 = (1 / np.sqrt(2)) * (np.exp(2j * theta_1_p) + np.exp(2j * theta_p_p))
    
    return G2, theta_1_p, theta_p_p

def analyse_theorique(p):
    """Analyse théorique de la limite pour grand p."""
    # Valeurs asymptotiques
    theta_1_inf = np.pi / 2  # arctan(∞) = π/2
    theta_p_inf = 0          # arctan(1/∞) = 0
    
    # Limite théorique
    G2_limite = (1 / np.sqrt(2)) * (np.exp(2j * theta_1_inf) + np.exp(2j * theta_p_inf))
    
    # Pour p fini
    theta_1_p = np.arctan(p)
    theta_p_p = np.arctan(1/p)
    
    # Écarts à la limite
    delta_theta_1 = np.pi/2 - theta_1_p
    delta_theta_p = theta_p_p - 0
    
    return {
        'theta_1_limite': theta_1_inf,
        'theta_p_limite': theta_p_inf,
        'G2_limite': G2_limite,
        'delta_theta_1': delta_theta_1,
        'delta_theta_p': delta_theta_p
    }

def test_comportement_premiers():
    """Test pour p = 101, 1009, 10007."""
    premiers = [101, 1009, 10007]
    
    print("=" * 80)
    print("TEST DU COMPORTEMENT DE G_2(p) POUR LES GRANDS NOMBRES PREMIERS")
    print("=" * 80)
    print()
    print("Prédiction théorique :")
    print("  Pour p → ∞ :")
    print("    θ(1,p) = arctan(p) → π/2")
    print("    θ(p,p) = arctan(1/p) → 0")
    print("    G_2(p) → (1/√2) · [exp(iπ) + 1] = (1/√2) · [-1 + 1] = 0")
    print()
    print("  Donc |G_2(p)| devrait tendre vers 0 quand p augmente.")
    print()
    print("=" * 80)
    print()
    
    resultats = []
    
    for p in premiers:
        print(f"\n{'─' * 80}")
        print(f"NOMBRE PREMIER p = {p}")
        print('─' * 80)
        
        # Calcul de G_2(p)
        G2, theta_1, theta_p = G2_premier(p)
        
        # Analyse théorique
        theo = analyse_theorique(p)
        
        # Affichage des angles
        print(f"\nAngles de Guasti :")
        print(f"  θ(1,{p}) = arctan({p}) = {theta_1:.10f} rad = {np.degrees(theta_1):.6f}°")
        print(f"  θ({p},{p}) = arctan(1/{p}) = {theta_p:.10f} rad = {np.degrees(theta_p):.6f}°")
        
        print(f"\nÉcarts à la limite asymptotique :")
        print(f"  π/2 - θ(1,{p}) = {theo['delta_theta_1']:.10e} rad")
        print(f"  θ({p},{p}) - 0   = {theo['delta_theta_p']:.10e} rad")
        
        # Affichage de G_2(p)
        print(f"\nTransformée G_2({p}) :")
        print(f"  Partie réelle     : Re(G_2) = {G2.real:20.15f}")
        print(f"  Partie imaginaire : Im(G_2) = {G2.imag:20.15f}")
        print(f"  Module            : |G_2|   = {np.abs(G2):20.15f}")
        print(f"  Argument          : arg(G_2) = {np.angle(G2):.10f} rad = {np.degrees(np.angle(G2)):.6f}°")
        
        # Décomposition explicite
        print(f"\nDécomposition :")
        term1 = np.exp(2j * theta_1)
        term2 = np.exp(2j * theta_p)
        print(f"  exp(2i·θ(1,{p}))  = {term1.real:15.10f} + {term1.imag:15.10f}i")
        print(f"  exp(2i·θ({p},{p})) = {term2.real:15.10f} + {term2.imag:15.10f}i")
        print(f"  Somme            = {(term1+term2).real:15.10f} + {(term1+term2).imag:15.10f}i")
        print(f"  G_2 = Somme/√2   = {G2.real:15.10f} + {G2.imag:15.10f}i")
        
        resultats.append({
            'p': p,
            'G2': G2,
            'module': np.abs(G2),
            'theta_1': theta_1,
            'theta_p': theta_p
        })
    
    # Résumé comparatif
    print(f"\n{'=' * 80}")
    print("RÉSUMÉ COMPARATIF")
    print('=' * 80)
    print()
    print(f"{'Premier p':>10} | {'|G_2(p)|':>20} | {'Variation':>15} | {'Distance à 0':>15}")
    print('-' * 70)
    
    for i, res in enumerate(resultats):
        p = res['p']
        mod = res['module']
        
        if i == 0:
            var = "—"
        else:
            var_relative = mod / resultats[i-1]['module']
            var = f"×{var_relative:.6f}"
        
        dist = mod
        print(f"{p:10d} | {mod:20.15f} | {var:>15} | {dist:15.10e}")
    
    # Test de convergence
    print()
    print("VÉRIFICATION DE LA CONVERGENCE :")
    print()
    
    # Ratios successifs
    for i in range(len(resultats) - 1):
        p1 = resultats[i]['p']
        p2 = resultats[i+1]['p']
        mod1 = resultats[i]['module']
        mod2 = resultats[i+1]['module']
        ratio = mod2 / mod1
        
        print(f"  |G_2({p2})| / |G_2({p1})| = {ratio:.10f}")
        if ratio < 1:
            print(f"    → ✓ Décroissance confirmée (facteur {1/ratio:.2f})")
        else:
            print(f"    → ✗ Pas de décroissance")
    
    print()
    
    # Estimation de la vitesse de convergence
    print("ESTIMATION DE LA VITESSE DE CONVERGENCE :")
    print()
    
    # Si |G_2(p)| ~ C/p^α, alors log|G_2| ~ log(C) - α·log(p)
    log_p = [np.log(r['p']) for r in resultats]
    log_mod = [np.log(r['module']) for r in resultats]
    
    # Régression linéaire
    coeffs = np.polyfit(log_p, log_mod, 1)
    alpha = -coeffs[0]
    C = np.exp(coeffs[1])
    
    print(f"  Modèle : |G_2(p)| ≈ C / p^α")
    print(f"  Estimation : α ≈ {alpha:.6f}")
    print(f"  Estimation : C ≈ {C:.6f}")
    print()
    
    # Prédictions
    print("  Prédictions du modèle vs valeurs calculées :")
    for res in resultats:
        p = res['p']
        mod_calc = res['module']
        mod_pred = C / (p ** alpha)
        erreur = abs(mod_calc - mod_pred) / mod_calc * 100
        print(f"    p = {p:5d} : calculé = {mod_calc:.10e}, prédit = {mod_pred:.10e}, erreur = {erreur:.2f}%")
    
    # Projection pour p = 100007
    p_proj = 100007
    mod_proj = C / (p_proj ** alpha)
    print()
    print(f"  Projection pour p = {p_proj} : |G_2({p_proj})| ≈ {mod_proj:.10e}")
    
    # Visualisation
    plt.figure(figsize=(14, 5))
    
    # Graphique 1 : |G_2(p)| en fonction de p
    plt.subplot(1, 3, 1)
    p_vals = [r['p'] for r in resultats]
    mod_vals = [r['module'] for r in resultats]
    
    plt.plot(p_vals, mod_vals, 'o-', linewidth=2, markersize=10, label='|G_2(p)| calculé')
    plt.axhline(y=0, color='red', linestyle='--', linewidth=1.5, label='Limite théorique = 0')
    plt.xlabel('Nombre premier p', fontsize=12)
    plt.ylabel('|G_2(p)|', fontsize=12)
    plt.title('Décroissance de |G_2(p)| vers 0', fontsize=14, fontweight='bold')
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.xscale('log')
    plt.yscale('log')
    
    # Graphique 2 : Écarts angulaires
    plt.subplot(1, 3, 2)
    theta_1_vals = [r['theta_1'] for r in resultats]
    theta_p_vals = [r['theta_p'] for r in resultats]
    
    plt.plot(p_vals, [np.pi/2 - t for t in theta_1_vals], 'o-', linewidth=2, markersize=10, 
             label='π/2 - θ(1,p)')
    plt.plot(p_vals, theta_p_vals, 's-', linewidth=2, markersize=10, 
             label='θ(p,p) - 0')
    plt.xlabel('Nombre premier p', fontsize=12)
    plt.ylabel('Écart à la limite (rad)', fontsize=12)
    plt.title('Convergence des angles de Guasti', fontsize=14, fontweight='bold')
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.xscale('log')
    plt.yscale('log')
    
    # Graphique 3 : Modèle de régression
    plt.subplot(1, 3, 3)
    p_fit = np.logspace(2, 4.5, 100)
    mod_fit = C / (p_fit ** alpha)
    
    plt.loglog(p_vals, mod_vals, 'o', markersize=10, label='Données calculées')
    plt.loglog(p_fit, mod_fit, '--', linewidth=2, label=f'Modèle: C/p^{alpha:.3f}')
    plt.xlabel('Nombre premier p', fontsize=12)
    plt.ylabel('|G_2(p)|', fontsize=12)
    plt.title('Loi de puissance', fontsize=14, fontweight='bold')
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3, which='both')
    
    plt.tight_layout()
    plt.savefig('/home/claude/comportement_G2_premiers.png', dpi=150, bbox_inches='tight')
    print()
    print("Graphique sauvegardé : comportement_G2_premiers.png")
    
    return resultats

if __name__ == "__main__":
    resultats = test_comportement_premiers()
