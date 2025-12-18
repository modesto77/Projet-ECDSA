import hashlib
import secrets

# --- 1. Paramètres Bitcoin / Secp256k1 ---
N = 115792089237316195423570985008687907852837564279074904382605163141518161494337
# (On n'a besoin que de N, l'ordre de la courbe, pour l'attaque mathématique)

# --- 2. Outils Mathématiques ---
def inverse_modulaire(a, n):
    return pow(a, -1, n)

def hash_message(msg):
    # Convertit le texte en un nombre entier via SHA256
    return int(hashlib.sha256(msg.encode('utf-8')).hexdigest(), 16)

# --- 3. Simulation de la Victime (Sony) ---
# Clé privée secrète (que l'attaquant ne connait pas au début)
cle_privee_reelle = 0xDEADBEEF12345678DEADBEEF12345678DEADBEEF12345678DEADBEEF12345678

# LE BUG CRITIQUE : Un k FIXE au lieu d'être aléatoire
K_FIXE = 0x1234567890ABCDEF1234567890ABCDEF # Sony a utilisé une constante ici !

def signer_avec_faille(message, private_key, k_fixe):
    z = hash_message(message)
    
    # Calcul de r (simplifié pour la démo, normalement c'est l'abscisse du point k*G)
    # Dans la réalité, r est public et visible dans la signature. 
    # Pour la simu, on triche un peu pour obtenir r car on n'a pas mis tout le code de point_multiply
    # Supposons que ce r est dérivé de k_fixe correctement.
    # Dans une attaque réelle, l'attaquant LIT simplement 'r' dans la signature publique.
    r = 0x5D9981234567 # Valeur arbitraire simulée liée à k (constante car k est constant)
    r = 12345 # Simplification: on dit que r vaut 12345 pour l'exercice
    
    # La formule ECDSA : s = k^-1 * (z + r * priv) mod N
    k_inv = inverse_modulaire(k_fixe, N)
    s = (k_inv * (z + r * private_key)) % N
    
    return {"z": z, "r": r, "s": s}

# --- 4. Exécution de l'Attaque ---

print("--- 1. La victime signe deux messages différents ---")

msg1 = "Jeu: Gran Turismo 5"
sig1 = signer_avec_faille(msg1, cle_privee_reelle, K_FIXE)
print(f"Signature 1 pour '{msg1}':")
print(f"  z1 (hash): {hex(sig1['z'])}")
print(f"  r: {sig1['r']}")
print(f"  s1: {hex(sig1['s'])}")

msg2 = "Jeu: Super Mario (Pirate)"
sig2 = signer_avec_faille(msg2, cle_privee_reelle, K_FIXE) # MÊME K_FIXE !!
print(f"\nSignature 2 pour '{msg2}':")
print(f"  z2 (hash): {hex(sig2['z'])}")
print(f"  r: {sig2['r']}  <-- REMARQUE : r est identique !")
print(f"  s2: {hex(sig2['s'])}")

print("\n--- 2. L'Attaquant analyse les données ---")
print("L'attaquant voit que 'r' est le même pour deux messages différents.")
print("Il sort sa calculatrice...")

# Extraction des valeurs
z1 = sig1['z']
s1 = sig1['s']
z2 = sig2['z']
s2 = sig2['s']
r  = sig1['r'] # r est commun

# ETAPE A : Retrouver k
# Formule magique : k = (z1 - z2) / (s1 - s2)
numerateur = (z1 - z2)
denominateur = inverse_modulaire(s1 - s2, N)
k_trouve = (numerateur * denominateur) % N

print(f"\n[CRACK] k trouvé : {hex(k_trouve)}")
print(f"Est-ce le bon k ? {k_trouve == K_FIXE}")

# ETAPE B : Retrouver la clé privée
# Formule : priv = (s1 * k - z1) / r
priv_numerateur = (s1 * k_trouve - z1)
priv_denominateur = inverse_modulaire(r, N)
cle_calculee = (priv_numerateur * priv_denominateur) % N

print(f"\n[VICTOIRE] Clé privée calculée : {hex(cle_calculee)}")
print(f"Clé privée originale       : {hex(cle_privee_reelle)}")

if cle_calculee == cle_privee_reelle:
    print("\nSUCCESS : La clé privée a été volée ! Vous contrôlez la console.")
else:
    print("\nECHEC.")