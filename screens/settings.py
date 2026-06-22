import customtkinter as ctk

from screens.base import BasePage


class SettingsPage(BasePage):
    """Application preferences and about screen."""

    def __init__(self, parent, app):
        super().__init__(parent, app)
        self.page_title("Settings", "Appearance and product information")

        card = self.make_card(self, row=1, column=0, sticky="nsew")
        card.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            card,
            text="Theme",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=self.colors["text"],
        ).grid(row=0, column=0, padx=24, pady=(24, 8), sticky="w")

        self.theme_switch = ctk.CTkSwitch(
            card,
            text="Light mode",
            progress_color=self.colors["accent_dark"],
            command=self._toggle_theme,
        )
        self.theme_switch.grid(row=1, column=0, padx=24, pady=(0, 28), sticky="w")

        ctk.CTkLabel(
            card,
            text="About VaultBoxX",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=self.colors["text"],
        ).grid(row=2, column=0, padx=24, pady=(6, 8), sticky="w")

        about = (
            "VaultBoxX is a desktop password manager built with Python, CustomTkinter, "
            "MongoDB, and cryptography. It stores encrypted credentials locally through "
            "the existing VaultBoxX backend modules."
        )

        ctk.CTkLabel(
            card,
            text=about,
            font=ctk.CTkFont(size=14),
            text_color=self.colors["muted"],
            wraplength=760,
            justify="left",
        ).grid(row=3, column=0, padx=24, pady=(0, 24), sticky="w")

    def _toggle_theme(self):
        ctk.set_appearance_mode("light" if self.theme_switch.get() else "dark")
