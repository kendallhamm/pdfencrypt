import sys
import os
from getpass import getpass
from pypdf import PdfReader, PdfWriter


def encrypt_pdf(input_path: str, password: str) -> str:
    reader = PdfReader(input_path)
    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    # Explicit AES-256 encryption
    writer.encrypt(
        user_password=password,
        owner_password=password,
        algorithm="AES-256"
    )

    base, ext = os.path.splitext(input_path)
    output_path = f"{base}_encrypted{ext}"

    with open(output_path, "wb") as f:
        writer.write(f)

    return output_path


def main():
    if len(sys.argv) != 2:
        print("Usage: python encrypt_pdf.py <path_to_pdf>")
        sys.exit(1)

    input_path = sys.argv[1]

    if not os.path.isfile(input_path):
        print("Error: File not found.")
        sys.exit(1)

    if not input_path.lower().endswith(".pdf"):
        print("Error: File must be a PDF.")
        sys.exit(1)

    password = getpass("Enter encryption password: ")
    confirm = getpass("Confirm password: ")

    if password != confirm:
        print("Error: Passwords do not match.")
        sys.exit(1)

    if len(password) < 8:
        print("Warning: Password is short. Consider using 12+ characters.")

    try:
        output_path = encrypt_pdf(input_path, password)
        print(f"Success: Encrypted file saved as:\n{output_path}")
    except Exception as e:
        print(f"Encryption failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
