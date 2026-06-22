import customtkinter as ctk

from screens.base import BasePage


class DashboardPage(BasePage):
    """Overview page with vault statistics."""

    def __init__(self, parent, app):
        super().__init__(parent, app)
        self.page_title("Dashboard", "Vault health and credential activity")

        content = ctk.CTkFrame(self, fg_color="transparent")
        content.grid(row=1, column=0, sticky="nsew")
        content.grid_columnconfigure((0, 1), weight=1, uniform="cards")

        self.total_value = self._stat_card(content, 0, "Total Credentials", "0")
        self.last_value = self._stat_card(content, 1, "Last Added Credential", "None")

        activity = self.make_card(content, row=1, column=0, columnspan=2, padx=0, pady=(22, 0), sticky="nsew")
        activity.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            activity,
            text="Security Snapshot",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=self.colors["text"],
        ).grid(row=0, column=0, padx=24, pady=(24, 8), sticky="w")

        ctk.CTkLabel(
            activity,
            text="Credentials are encrypted before storage and decrypted only after master-password login.",
            font=ctk.CTkFont(size=14),
            text_color=self.colors["muted"],
            wraplength=720,
            justify="left",
        ).grid(row=1, column=0, padx=24, pady=(0, 24), sticky="w")

        self.refresh()

    def _stat_card(self, parent, column, label, value):
        card = self.make_card(parent, row=0, column=column, padx=(0, 12) if column == 0 else (12, 0), pady=0, sticky="nsew")
        card.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            card,
            text=label,
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=self.colors["muted"],
        ).grid(row=0, column=0, padx=24, pady=(24, 8), sticky="w")

        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=ctk.CTkFont(size=34, weight="bold"),
            text_color=self.colors["accent"],
        )
        value_label.grid(row=1, column=0, padx=24, pady=(0, 26), sticky="w")
        return value_label

    def refresh(self):
        try:
            credentials = self.app.fetch_credentials()
            self.total_value.configure(text=str(len(credentials)))
            self.last_value.configure(text=credentials[-1].get("website", "Unknown") if credentials else "None")
        except Exception as exc:
            self.total_value.configure(text="--")
            self.last_value.configure(text=f"Database error: {exc}")
