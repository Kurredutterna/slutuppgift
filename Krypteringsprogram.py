import os
import argparse
from cryptography.fernet import Fernet

# Funktion för att generera och spara en nyckel
def skapa_nyckel(nyckel):
    """Generera en nyckel och spara den i en fil"""
    key = Fernet.generate_key()
    with open(nyckel, 'wb') as keyfile:
        keyfile.write(key)
    print(f"Nyckeln har sparats i {nyckel}")

# Funktion för att läsa nyckeln från en fil
def ladda_nyckel(nyckel):
    """Läs nyckeln från en fil"""
    if not os.path.exists(nyckel):
        raise FileNotFoundError(f"Nyckelfilen {nyckel} finns inte.")
    with open(nyckel, 'rb') as keyfile:
        return keyfile.read()

# Funktion för att kryptera en fil
def encrypt_file(input_file, nyckel):
    """Kryptera en fil med hjälp av en given nyckel och spara den som 'hemlis'"""
    key = ladda_nyckel(nyckel)
    cipher = Fernet(key)

    with open(input_file, 'rb') as infile:
        file_data = infile.read()

    encrypted_data = cipher.encrypt(file_data)

    krypterat_meddelande = 'hemlis'  # Filnamnet sätts här till 'hemlis'

    with open(krypterat_meddelande, 'wb') as outfile:
        outfile.write(encrypted_data)

    print(f"Filen {input_file} har krypterats och sparats som 'hemlis'")

# Funktion för att dekryptera en fil
def decrypt_file(input_file, nyckel, output_file):
    """Dekryptera en fil med hjälp av en given nyckel och spara som den angivna filen"""
    key = ladda_nyckel(nyckel)
    cipher = Fernet(key)

    with open(input_file, 'rb') as infile:
        encrypted_data = infile.read()

    try:
        decrypted_data = cipher.decrypt(encrypted_data)
    except Exception as e:
        print(f"Fel vid dekryptering: {e}")
        return

    with open(output_file, 'wb') as outfile:
        outfile.write(decrypted_data)

    print(f"Filen {input_file} har dekrypterats och sparats som {output_file}")

# Huvudfunktion som hanterar argument och kör funktionerna
def main():
    parser = argparse.ArgumentParser(description="Krypteringsverktyg för filer.")
    subparsers = parser.add_subparsers(dest="command")

    # Subkommando för att generera nyckel
    generate_parser = subparsers.add_parser('skapa_nyckel', help="Generera och spara en symmetrisk nyckel")
    generate_parser.add_argument('nyckel', help="Fil där nyckeln ska sparas")

    # Subkommando för att kryptera fil
    encrypt_parser = subparsers.add_parser('kryptera', help="Kryptera en fil med en nyckel. Filen sparas som 'hemlis'")
    encrypt_parser.add_argument('input_file', help="Fil att kryptera")
    encrypt_parser.add_argument('nyckel', help="Nyckelfil")

    # Subkommando för att dekryptera fil
    decrypt_parser = subparsers.add_parser('dekryptera', help="Dekryptera en fil med en nyckel")
    decrypt_parser.add_argument('input_file', help="Krypterad fil att dekryptera")
    decrypt_parser.add_argument('nyckel', help="Nyckelfil")
    decrypt_parser.add_argument('output_file', help="Fil för att spara den dekrypterade versionen")

    args = parser.parse_args()

    if args.command == 'skapa_nyckel': 
        skapa_nyckel(args.nyckel)
    elif args.command == 'kryptera':
        encrypt_file(args.input_file, args.nyckel)
    elif args.command == 'dekryptera':
        decrypt_file(args.input_file, args.nyckel, args.output_file)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
    #hej