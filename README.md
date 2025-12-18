# ECDSA Implementation & PS3 Attack Simulation 🔐

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)
![Security](https://img.shields.io/badge/Security-Cryptography-red?style=for-the-badge&logo=lock)
![Status](https://img.shields.io/badge/Status-Educational-orange?style=for-the-badge)

## 📋 À propos du projet

Ce projet est une implémentation pure en **Python** de l'algorithme de signature numérique **ECDSA** (Elliptic Curve Digital Signature Algorithm) sur la courbe **secp256k1**.

L'objectif principal est pédagogique : démontrer l'importance critique de l'aléatoire en cryptographie à travers la simulation de la célèbre vulnérabilité qui a touché la **Sony PlayStation 3** en 2010.

> **Le contexte historique :** Sony utilisait un nombre aléatoire (le nonce $k$) qui était statique au lieu d'être généré aléatoirement à chaque signature. Cette erreur d'implémentation a permis aux hackers de retrouver la clé privée maîtresse de la console par simple calcul arithmétique.

## 🛠 Fonctionnalités

* **Implémentation Mathématique :** Opérations sur les courbes elliptiques (Addition de points, Multiplication scalaire) sans librairies externes lourdes.
* **Génération de Clés :** Création de paires de clés (Privée / Publique).
* **Signature & Vérification :** Processus complet de signature de messages.
* **Attack Simulation (Sony Hack) :** Script démontrant comment retrouver une clé privée à partir de deux messages signés avec le même nonce $k$.

## 🧮 La Vulnérabilité (Théorie)

Dans l'algorithme ECDSA, la signature est composée de deux valeurs $(r, s)$. La sécurité repose sur un nombre aléatoire secret $k$.

L'équation de la signature est :
$$s = k^{-1} (z + r \cdot d_A) \mod n$$

Où :
* $z$ est le hash du message.
* $d_A$ est la clé privée.

Si le même $k$ est utilisé pour deux messages différents ($z_1$ et $z_2$), nous obtenons deux signatures avec le même $r$. Il devient alors trivial d'isoler $k$, puis de retrouver la clé privée $d_A$ via la formule :

$$d_A = \frac{s_1 \cdot z_2 - s_2 \cdot z_1}{r \cdot (s_2 - s_1)} \mod n$$

Ce projet exécute cette attaque automatiquement pour prouver la vulnérabilité.

## 🚀 Installation et Utilisation

### Prérequis
* Python 3.x installé sur votre machine.

### Installation
Clonez ce dépôt :
```bash
git clone [https://github.com/modesto77/Nom-De-Votre-Repo.git](https://github.com/modesto77/Nom-De-Votre-Repo.git)
cd Nom-De-Votre-Repo


