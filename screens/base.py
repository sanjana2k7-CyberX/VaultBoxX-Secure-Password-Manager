import customtkinter as ctk


class BasePage(ctk.CTkFrame):
    """Shared page styling helpers for the VaultBoxX GUI."""

    def __init__(self, parent, app):
        super().__init__(parent, fg_color=app.colors["bg"], corner_radius=0)
        self.app = app
        self.colors = app.colors
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

    def page_title(self, title, subtitle=None):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", pady=(0, 22))
        header.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            header,
            text=title,
            font=ctk.CTkFont(size=30, weight="bold"),
            text_color=self.colors["text"],
        ).grid(row=0, column=0, sticky="w")

        if subtitle:
            ctk.CTkLabel(
                header,
                text=subtitle,
                font=ctk.CTkFont(size=14),
                text_color=self.colors["muted"],
            ).grid(row=1, column=0, sticky="w", pady=(4, 0))

        return header

    def make_card(self, parent, **grid_options):
        card = ctk.CTkFrame(parent, corner_radius=16, fg_color=self.colors["card"])
        card.grid(**grid_options)
        return card
