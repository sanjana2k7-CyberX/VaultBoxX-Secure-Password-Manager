import customtkinter as ctk


class LoginScreen(ctk.CTkFrame):
    """Master-password login screen."""

    def __init__(self, parent, app):
        super().__init__(parent, fg_color=app.colors["bg"])
        self.app = app
        self.colors = app.colors

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        panel = ctk.CTkFrame(self, corner_radius=24, fg_color=self.colors["panel"])
        panel.grid(row=0, column=0, padx=28, pady=28)
        panel.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            panel,
            text="VaultBoxX",
            font=ctk.CTkFont(size=38, weight="bold"),
            text_color=self.colors["accent"],
        ).grid(row=0, column=0, padx=34, pady=(46, 6), sticky="w")

        ctk.CTkLabel(
            panel,
            text="Encrypted credential command center",
            font=ctk.CTkFont(size=14),
            text_color=self.colors["muted"],
        ).grid(row=1, column=0, padx=34, pady=(0, 34), sticky="w")

        self.password_entry = ctk.CTkEntry(
            panel,
            height=48,
            corner_radius=12,
            placeholder_text="Master password",
            show="*",
            border_color=self.colors["accent_dark"],
            fg_color="#081829",
        )
        self.password_entry.grid(row=2, column=0, padx=34, pady=(0, 14), sticky="ew")
        self.password_entry.bind("<Return>", lambda _event: self._attempt_login())

        self.error_label = ctk.CTkLabel(
            panel,
            text="",
            font=ctk.CTkFont(size=13),
            text_color=self.colors["danger"],
        )
        self.error_label.grid(row=3, column=0, padx=34, pady=(0, 8), sticky="w")

        ctk.CTkButton(
            panel,
            text="Unlock Vault",
            height=48,
            corner_radius=12,
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color=self.colors["accent_dark"],
            hover_color="#0bbbe8",
            command=self._attempt_login,
        ).grid(row=4, column=0, padx=34, pady=(4, 34), sticky="ew")

        ctk.CTkLabel(
            panel,
            text="MongoDB + cryptography protected storage",
            font=ctk.CTkFont(size=12),
            text_color=self.colors["muted"],
        ).grid(row=5, column=0, padx=34, pady=(0, 32), sticky="w")

        # Keep the login card polished on small and large windows.
        panel.configure(width=430)

        self.password_entry.focus_set()

    def _attempt_login(self):
        password = self.password_entry.get().strip()
        if not password:
            self.error_label.configure(text="Enter your master password.")
            return

        if not self.app.login(password):
            self.error_label.configure(text="Incorrect master password.")
