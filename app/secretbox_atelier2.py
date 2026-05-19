import sys
import os
import nacl.secret
import nacl.utils

# SecretBox nécessite impérativement une clé symétrique de 32 octets (256 bits)
KEY_FILE = "pynacl_secret.key"

def load_or_generate_nacl_key():
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "rb") as kf:
            return kf.read()
    else:
        # Génération sécurisée d'une clé brute de 32 octets
        key = nacl.utils.random(nacl.secret.SecretBox.KEY_SIZE)
        with open(KEY_FILE, "wb") as kf:
            kf.write(key)
        return key

def main():
    if len(sys.argv) < 4:
        print("Usage: python app/secretbox_atelier2.py [encrypt|decrypt] [source] [destination]")
        sys.exit(1)

    action = sys.argv[1]
    source_path = sys.argv[2]
    dest_path = sys.argv[3]

    raw_key = load_or_generate_nacl_key()
    box = nacl.secret.SecretBox(raw_key)

    try:
        if action == "encrypt":
            with open(source_path, "rb") as f:
                plaintext = f.read()
            # Chiffre le contenu et génère/inclut automatiquement un Nonce unique de 24 octets
            encrypted_data = box.encrypt(plaintext)
            with open(dest_path, "wb") as f:
                f.write(encrypted_data)
            print(f"[PyNaCl XSalsa20/Poly1305] Fichier chiffré généré : {dest_path}")

        elif action == "decrypt":
            with open(source_path, "rb") as f:
                ciphertext = f.read()
            # Déchiffre et vérifie l'intégrité Poly1305 (lève une exception si altéré)
            decrypted_data = box.decrypt(ciphertext)
            with open(dest_path, "wb") as f:
                f.write(decrypted_data)
            print(f"[PyNaCl XSalsa20/Poly1305] Fichier déchiffré généré : {dest_path}")

    except Exception as e:
        print(f"Erreur d'authentification ou clé invalide PyNaCl : {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
