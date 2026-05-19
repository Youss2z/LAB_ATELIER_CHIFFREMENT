import os
import sys
from cryptography.fernet import Fernet

def get_secret_key():
    # Récupération de la clé depuis les variables d'environnement système
    key = os.environ.get("FERNET_KEY")
    if not key:
        print("Erreur : La variable d'environnement 'FERNET_KEY' est introuvable.")
        print("Veuillez configurer le Secret GitHub ou exécuter: export FERNET_KEY='...'")
        sys.exit(1)
    return Fernet(key.encode())

def main():
    if len(sys.argv) < 4:
        print("Usage: python app/fernet_atelier1.py [encrypt|decrypt] [source] [destination]")
        sys.exit(1)

    action = sys.argv[1]
    source_path = sys.argv[2]
    dest_path = sys.argv[3]

    try:
        cipher = get_secret_key()

        if action == "encrypt":
            with open(source_path, "rb") as f:
                data = f.read()
            encrypted_data = cipher.encrypt(data)
            with open(dest_path, "wb") as f:
                f.write(encrypted_data)
            print(f"Chiffrement réussi (Clé masquée via Secret). Fichier : {dest_path}")

        elif action == "decrypt":
            with open(source_path, "rb") as f:
                data = f.read()
            decrypted_data = cipher.decrypt(data)
            with open(dest_path, "wb") as f:
                f.write(decrypted_data)
            print(f"Déchiffrement réussi (Clé masquée via Secret). Fichier : {dest_path}")

    except Exception as e:
        print(f"Erreur lors de l'opération cryptographique : {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
