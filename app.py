from database import (
    add_credential,
    get_credentials,
    search_credential,
    delete_credential
)

from encryption import (
    encrypt_password,
    decrypt_password
)

from password_generator import generate_password
from auth import verify_master_password


# Master Login
password = input("Enter Master Password: ")

if not verify_master_password(password):
    print("Access Denied")
    exit()

master_password = password


# Main Menu
while True:

    print("\n=== VaultBoxX ===")
    print("1. Add Credential")
    print("2. View Credentials")
    print("3. Generate Password")
    print("4. Search Credential")
    print("5. Delete Credential")
    print("6. Exit")

    choice = input("\nEnter choice: ")

    # Add Credential
    if choice == "1":

        website = input("Website: ")
        username = input("Username: ")
        password = input("Password: ")

        encrypted = encrypt_password(
            password,
            master_password
        )

        add_credential(
            website,
            username,
            encrypted
        )

        print("✅ Credential Saved Successfully!")

    # View Credentials
    elif choice == "2":

        credentials = get_credentials()

        if not credentials:
            print("No credentials found.")
            continue

        for item in credentials:

            decrypted = decrypt_password(
                item["password"],
                master_password
            )

            print("\n------------------------")
            print(f"Website : {item['website']}")
            print(f"Username: {item['username']}")
            print(f"Password: {decrypted}")

    # Generate Password
    elif choice == "3":

        generated = generate_password()

        print("\nGenerated Password:")
        print(generated)

    # Search Credential
    elif choice == "4":

        website = input(
            "Enter website to search: "
        )

        result = search_credential(
            website
        )

        if result:

            decrypted = decrypt_password(
                result["password"],
                master_password
            )

            print("\nCredential Found")
            print("------------------------")
            print(f"Website : {result['website']}")
            print(f"Username: {result['username']}")
            print(f"Password: {decrypted}")

        else:

            print("Credential Not Found")

    # Delete Credential
    elif choice == "5":

        website = input(
            "Enter website to delete: "
        )

        deleted = delete_credential(
            website
        )

        if deleted:

            print(
                "Credential Deleted Successfully"
            )

        else:

            print(
                "Credential Not Found"
            )

    # Exit
    elif choice == "6":

        print(
            "\nThank you for using VaultBoxX!"
        )

        break

    else:

        print(
            "Invalid Choice. Please try again."
        )