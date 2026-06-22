import customtkinter as ctk

from auth import verify_master_password
from database import add_credential, delete_credential, get_credentials
from encryption import decrypt_password, encrypt_password
from password_generator import generate_password
from screens.add_credential import AddCredentialPage
from screens.dashboard import DashboardPage
from screens.login_screen import LoginScreen
from screens.password_generator_page import PasswordGeneratorPage
from screens.settings import SettingsPage
from screens.view_credentials import ViewCredentialsPage


class VaultBoxXApp(ctk.CTk):
    """Main desktop application and bridge between UI screens and backend modules."""

    def __init__(self):
        super().__init__()
        self.title("VaultBoxX")
        self.geometry("1180x720")
        self.minsize(960, 620)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.master_password = None
        self.active_page = None
        self.nav_buttons = {}

        self.colors = {
            "bg": "#07111f",
            "panel": "#0d1b2e",
            "panel_alt": "#13243a",
            "card": "#10243a",
            "accent": "#12d7ff",
            "accent_dark": "#0a84ff",
            "text": "#f5fbff",
            "muted": "#8ea5bb",
            "danger": "#ff4d6d",
            "success": "#35d07f",
        }

        self.configure(fg_color=self.colors["bg"])
        self.show_login()

    def show_login(self):
        self._clear_root()
        self.master_password = None
        LoginScreen(self, self).pack(fill="both", expand=True)

    def login(self, password):
        if not verify_master_password(password):
            return False

        self.master_password = password
        self._build_shell()
        self.show_page("dashboard")
        return True

    def _build_shell(self):
        self._clear_root()

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = ctk.CTkFrame(self, width=238, corner_radius=0, fg_color=self.colors["panel"])
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(8, weight=1)
        self.sidebar.grid_propagate(False)

        logo = ctk.CTkLabel(
            self.sidebar,
            text="VaultBoxX",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=self.colors["accent"],
        )
        logo.grid(row=0, column=0, padx=24, pady=(30, 4), sticky="w")

        subtitle = ctk.CTkLabel(
            self.sidebar,
            text="Secure Password Vault",
            font=ctk.CTkFont(size=12),
            text_color=self.colors["muted"],
        )
        subtitle.grid(row=1, column=0, padx=24, pady=(0, 24), sticky="w")

        nav_items = [
            ("dashboard", "[D] Dashboard"),
            ("add", "[+] Add Credential"),
            ("view", "[#] View Credentials"),
            ("generator", "[*] Generator"),
            ("settings", "[S] Settings"),
        ]

        for index, (page, label) in enumerate(nav_items, start=2):
            button = ctk.CTkButton(
                self.sidebar,
                text=label,
                height=44,
                corner_radius=10,
                anchor="w",
                font=ctk.CTkFont(size=14, weight="bold"),
                fg_color="transparent",
                hover_color=self.colors["panel_alt"],
                command=lambda name=page: self.show_page(name),
            )
            button.grid(row=index, column=0, padx=16, pady=5, sticky="ew")
            self.nav_buttons[page] = button

        logout = ctk.CTkButton(
            self.sidebar,
            text="[X] Logout",
            height=42,
            corner_radius=10,
            fg_color="#1d2b3d",
            hover_color="#263c55",
            command=self.show_login,
        )
        logout.grid(row=9, column=0, padx=16, pady=22, sticky="ew")

        self.content = ctk.CTkFrame(self, corner_radius=0, fg_color=self.colors["bg"])
        self.content.grid(row=0, column=1, sticky="nsew")
        self.content.grid_columnconfigure(0, weight=1)
        self.content.grid_rowconfigure(0, weight=1)

    def show_page(self, page_name):
        page_map = {
            "dashboard": DashboardPage,
            "add": AddCredentialPage,
            "view": ViewCredentialsPage,
            "generator": PasswordGeneratorPage,
            "settings": SettingsPage,
        }

        if self.active_page is not None:
            self.active_page.destroy()

        for name, button in self.nav_buttons.items():
            button.configure(fg_color=self.colors["accent_dark"] if name == page_name else "transparent")

        self.active_page = page_map[page_name](self.content, self)
        self.active_page.grid(row=0, column=0, sticky="nsew", padx=28, pady=24)

    def save_credential(self, website, username, password):
        encrypted = encrypt_password(password, self.master_password)
        add_credential(website, username, encrypted)

    def fetch_credentials(self):
        return get_credentials()

    def reveal_password(self, encrypted_password):
        return decrypt_password(encrypted_password, self.master_password)

    def remove_credential(self, website):
        return delete_credential(website)

    def make_password(self, length):
        return generate_password(length)

    def copy_to_clipboard(self, value):
        self.clipboard_clear()
        self.clipboard_append(value)
        self.update_idletasks()

    def refresh_dashboard(self):
        if isinstance(self.active_page, DashboardPage):
            self.active_page.refresh()

    def _clear_root(self):
        for child in self.winfo_children():
            child.destroy()
        self.nav_buttons = {}
        self.active_page = None


if __name__ == "__main__":
    app = VaultBoxXApp()
    app.mainloop()
