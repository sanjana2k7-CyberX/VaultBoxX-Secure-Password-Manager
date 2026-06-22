import customtkinter as ctk

from screens.base import BasePage


class AddCredentialPage(BasePage):
    """Form for adding encrypted credentials."""

    def __init__(self, parent, app):
        super().__init__(parent, app)
        self.password_visible = False
        self.page_title("Add Credential", "Store a new encrypted login")

        form = self.make_card(self, row=1, column=0, sticky="nsew")
        form.grid_columnconfigure(0, weight=1)

        self.website_entry = self._entry(form, 0, "Website")
        self.username_entry = self._entry(form, 1, "Username")

        password_row = ctk.CTkFrame(form, fg_color="transparent")
        password_row.grid(row=2, column=0, padx=24, pady=10, sticky="ew")
        password_row.grid_columnconfigure(0, weight=1)

        self.password_entry = ctk.CTkEntry(
            password_row,
            height=46,
            corner_radius=12,
            placeholder_text="Password",
            show="*",
            fg_color="#081829",
            border_color=self.colors["panel_alt"],
        )
        self.password_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10))

        self.toggle_button = ctk.CTkButton(
            password_row,
            text="Show",
            width=92,
            height=46,
            corner_radius=12,
            fg_color=self.colors["panel_alt"],
            hover_color="#1b3958",
            command=self._toggle_password,
        )
        self.toggle_button.grid(row=0, column=1)

        self.status_label = ctk.CTkLabel(form, text="", text_color=self.colors["muted"])
        self.status_label.grid(row=3, column=0, padx=24, pady=(4, 0), sticky="w")

        ctk.CTkButton(
            form,
            text="Save Credential",
            height=48,
            corner_radius=12,
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color=self.colors["accent_dark"],
            hover_color="#0bbbe8",
            command=self._save,
        ).grid(row=4, column=0, padx=24, pady=24, sticky="ew")

    def _entry(self, parent, row, placeholder):
        entry = ctk.CTkEntry(
            parent,
            height=46,
            corner_radius=12,
            placeholder_text=placeholder,
            fg_color="#081829",
            border_color=self.colors["panel_alt"],
        )
        entry.grid(row=row, column=0, padx=24, pady=10, sticky="ew")
        return entry

    def _toggle_password(self):
        self.password_visible = not self.password_visible
        self.password_entry.configure(show="" if self.password_visible else "*")
        self.toggle_button.configure(text="Hide" if self.password_visible else "Show")

    def _save(self):
        website = self.website_entry.get().strip()
        username = self.username_entry.get().strip()
        password = self.password_entry.get()

        if not website or not username or not password:
            self.status_label.configure(text="All fields are required.", text_color=self.colors["danger"])
            return

        try:
            self.app.save_credential(website, username, password)
        except Exception as exc:
            self.status_label.configure(text=f"Could not save credential: {exc}", text_color=self.colors["danger"])
            return

        self.website_entry.delete(0, "end")
        self.username_entry.delete(0, "end")
        self.password_entry.delete(0, "end")
        self.status_label.configure(text="Credential saved successfully.", text_color=self.colors["success"])
        self.app.refresh_dashboard()
