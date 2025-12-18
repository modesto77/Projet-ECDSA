import hashlib
import secrets

# -------------------------
# 1. Paramètres de la courbe Elliptique (secp256k1)
# -------------------------
# Equation: y^2 = x^3 + ax + b
P = 2**256 - 2**32 - 977
N = 115792089237316195423570985008687907852837564279074904382605163141518161494337
A = 0
B = 7
G_X = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
G_Y = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
G = (G_X, G_Y)

# -------------------------
# 2. Fonctions Mathématiques
# -------------------------

# Addition de deux points (P1 + P2)
def point_add(p1, p2):
    if p1 is None: return p2
    if p2 is None: return p1
    
    x1, y1 = p1
    x2, y2 = p2

    if x1 == x2 and y1 != y2:
        return None # Point à l'infini

    if x1 == x2:
        # P1 == P2, on utilise le doublement
        m = (3 * x1**2 + A) * pow(2 * y1, -1, P)
    else:
        # P1 != P2, addition classique
        m = (y1 - y2) * pow(x1 - x2, -1, P)
    
    m = m % P
    x3 = (m**2 - x1 - x2) % P
    y3 = (m * (x1 - x3) - y1) % P
    return (x3, y3)

# Multiplication scalaire (k * Point) - Algorithme Double-and-Add
def point_multiply(k, point):
    current = point
    result = None # Point à l'infini (élément neutre)

    # On parcourt les bits de k (converti en binaire)
    for bit in bin(k)[2:][::-1]: # Du bit de poids faible au fort
        if bit == '1':
            result = point_add(result, current)
        current = point_add(current, current) # Doublement
    
    return result

# -------------------------
# 3. Cryptographie (Signer & Vérifier)
# -------------------------

def sign_message(private_key, message):
    # 1. Hacher le message (simule la fonction à signer)
    message_bytes = message.encode('utf-8')
    z = int(hashlib.sha256(message_bytes).hexdigest(), 16)
    
    # 2. Générer un nonce k aléatoire (IMPORTANT: Doit être unique !)
    # Note: Dans ton projet PS3, c'est ici que Sony a échoué en réutilisant k
    while True:
        k = secrets.randbelow(N)
        if k > 0: break
    
    # 3. Calculer le point R = k * G
    point_r = point_multiply(k, G)
    r = point_r[0] % N
    
    if r == 0: return sign_message(private_key, message) # Cas rarissime, on recommence
    
    # 4. Calculer s = k^-1 * (z + r * private_key) mod n
    k_inv = pow(k, -1, N)
    s = (k_inv * (z + r * private_key)) % N
    
    if s == 0: return sign_message(private_key, message)
    
    return {"r": r, "s": s}

def verify_signature(public_key, message, signature):
    r = signature["r"]
    s = signature["s"]
    
    # Vérifications de base
    if not (1 <= r < N) or not (1 <= s < N):
        return False
        
    # 1. Hacher le message
    message_bytes = message.encode('utf-8')
    z = int(hashlib.sha256(message_bytes).hexdigest(), 16)
    
    # 2. Calculer w = s^-1 mod n
    w = pow(s, -1, N)
    
    # 3. Calculer u1 = z * w mod n  et  u2 = r * w mod n
    u1 = (z * w) % N
    u2 = (r * w) % N
    
    # 4. Point final = u1*G + u2*PublicKey
    p1 = point_multiply(u1, G)
    p2 = point_multiply(u2, public_key)
    point_final = point_add(p1, p2)
    
    # 5. La signature est valide si x du point final == r
    if point_final is None: return False
    return point_final[0] == r

# -------------------------
# 4. Exemple d'exécution
# -------------------------

# A. Génération de clés (simulée)
# On prend une clé privée au hasard
private_key_int = secrets.randbelow(N) 
public_key_point = point_multiply(private_key_int, G)

print(f"🔑 Clé Privée : {hex(private_key_int)}")
print(f"🌍 Clé Publique (x,y) : {hex(public_key_point[0])}, {hex(public_key_point[1])}")
print("-" * 60)

# B. Définition de la 'fonction' ou 'commande' à signer
ma_fonction = "virement(montant=500, destinataire='Bob')"
print(f"📜 Commande à signer : '{ma_fonction}'")

# C. Signature
signature = sign_message(private_key_int, ma_fonction)
print(f"✍️  Signature générée :")
print(f"   r: {hex(signature['r'])}")
print(f"   s: {hex(signature['s'])}")

print("-" * 60)

# D. Vérification
# Imaginons que quelqu'un reçoive le message et la signature
est_valide = verify_signature(public_key_point, ma_fonction, signature)
print(f"✅ Signature valide pour '{ma_fonction}' ? -> {est_valide}")

# E. Tentative de fraude (changer le message sans re-signer)
message_falsifie = "virement(montant=90000, destinataire='Hacker')"
est_valide_faux = verify_signature(public_key_point, message_falsifie, signature)
print(f"❌ Signature valide pour '{message_falsifie}' ? -> {est_valide_faux}")