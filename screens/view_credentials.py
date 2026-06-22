import customtkinter as ctk

from screens.base import BasePage


class ViewCredentialsPage(BasePage):
    """Searchable credential list with reveal, copy, and delete actions."""

    def __init__(self, parent, app):
        super().__init__(parent, app)
        self.credentials = []
        self.visible_passwords = {}
        self.page_title("View Credentials", "Search, reveal, copy, or delete saved logins")

        toolbar = ctk.CTkFrame(self, fg_color="transparent")
        toolbar.grid(row=1, column=0, sticky="ew", pady=(0, 14))
        toolbar.grid_columnconfigure(0, weight=1)

        self.search_entry = ctk.CTkEntry(
            toolbar,
            height=44,
            corner_radius=12,
            placeholder_text="Search by website",
            fg_color="#081829",
            border_color=self.colors["panel_alt"],
        )
        self.search_entry.grid(row=0, column=0, sticky="ew")
        self.search_entry.bind("<KeyRelease>", lambda _event: self._render())

        ctk.CTkButton(
            toolbar,
            text="Refresh",
            width=112,
            height=44,
            corner_radius=12,
            fg_color=self.colors["panel_alt"],
            hover_color="#1b3958",
            command=self.refresh,
        ).grid(row=0, column=1, padx=(12, 0))

        self.table = ctk.CTkScrollableFrame(self, corner_radius=16, fg_color=self.colors["card"])
        self.table.grid(row=2, column=0, sticky="nsew")
        self.table.grid_columnconfigure(0, weight=2)
        self.table.grid_columnconfigure(1, weight=2)
        self.table.grid_columnconfigure(2, weight=2)

        self.grid_rowconfigure(2, weight=1)
        self.refresh()

    def refresh(self):
        try:
            self.credentials = self.app.fetch_credentials()
        except Exception as exc:
            self.credentials = []
            self._message(f"Database error: {exc}", self.colors["danger"])
            return
        self._render()

    def _render(self):
        for child in self.table.winfo_children():
            child.destroy()

        self._header()
        query = self.search_entry.get().strip().lower()
        rows = [item for item in self.credentials if query in item.get("website", "").lower()]

        if not rows:
            self._message("No credentials found.", self.colors["muted"], row=1)
            return

        for row_index, item in enumerate(rows, start=1):
            self._row(row_index, item)

    def _header(self):
        labels = ["Website", "Username", "Password", "Actions"]
        for column, label in enumerate(labels):
            ctk.CTkLabel(
                self.table,
                text=label,
                font=ctk.CTkFont(size=13, weight="bold"),
                text_color=self.colors["accent"],
            ).grid(row=0, column=column, padx=14, pady=(16, 8), sticky="w")

    def _row(self, row_index, item):
        item_id = str(item.get("_id", item.get("website", row_index)))
        website = item.get("website", "Unknown")
        username = item.get("username", "")
        encrypted_password = item.get("password", "")

        ctk.CTkLabel(self.table, text=website, text_color=self.colors["text"], anchor="w").grid(
            row=row_index, column=0, padx=14, pady=9, sticky="ew"
        )
        ctk.CTkLabel(self.table, text=username, text_color=self.colors["text"], anchor="w").grid(
            row=row_index, column=1, padx=14, pady=9, sticky="ew"
        )

        password_text = self.visible_passwords.get(item_id, "**********")
        password_label = ctk.CTkLabel(self.table, text=password_text, text_color=self.colors["muted"], anchor="w")
        password_label.grid(row=row_index, column=2, padx=14, pady=9, sticky="ew")

        actions = ctk.CTkFrame(self.table, fg_color="transparent")
        actions.grid(row=row_index, column=3, padx=10, pady=7, sticky="e")

        ctk.CTkButton(
            actions,
            text="Show",
            width=64,
            height=32,
            corner_radius=9,
            fg_color=self.colors["panel_alt"],
            hover_color="#1b3958",
            command=lambda: self._show_password(item_id, encrypted_password, password_label),
        ).grid(row=0, column=0, padx=3)

        ctk.CTkButton(
            actions,
            text="Copy",
            width=64,
            height=32,
            corner_radius=9,
            fg_color=self.colors["accent_dark"],
            hover_color="#0bbbe8",
            command=lambda: self._copy_password(encrypted_password),
        ).grid(row=0, column=1, padx=3)

        ctk.CTkButton(
            actions,
            text="Delete",
            width=70,
            height=32,
            corner_radius=9,
            fg_color=self.colors["danger"],
            hover_color="#d83d5a",
            command=lambda: self._confirm_delete(website),
        ).grid(row=0, column=2, padx=3)

    def _show_password(self, item_id, encrypted_password, label):
        try:
            password = self.app.reveal_password(encrypted_password)
        except Exception:
            password = "Unable to decrypt"
        self.visible_passwords[item_id] = password
        label.configure(text=password, text_color=self.colors["text"])

    def _copy_password(self, encrypted_password):
        try:
            self.app.copy_to_clipboard(self.app.reveal_password(encrypted_password))
        except Exception:
            self._toast("Unable to copy password.")

    def _confirm_delete(self, website):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Confirm Delete")
        dialog.geometry("380x190")
        dialog.transient(self.winfo_toplevel())
        dialog.grab_set()
        dialog.configure(fg_color=self.colors["panel"])
        dialog.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            dialog,
            text="Delete credential?",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=self.colors["text"],
        ).grid(row=0, column=0, padx=24, pady=(24, 6), sticky="w")
        ctk.CTkLabel(
            dialog,
            text=f"This will remove the saved login for {website}.",
            text_color=self.colors["muted"],
            wraplength=320,
            justify="left",
        ).grid(row=1, column=0, padx=24, pady=(0, 18), sticky="w")

        buttons = ctk.CTkFrame(dialog, fg_color="transparent")
        buttons.grid(row=2, column=0, padx=24, pady=(0, 24), sticky="e")

        ctk.CTkButton(buttons, text="Cancel", width=92, fg_color=self.colors["panel_alt"], command=dialog.destroy).grid(
            row=0, column=0, padx=6
        )
        ctk.CTkButton(
            buttons,
            text="Delete",
            width=92,
            fg_color=self.colors["danger"],
            hover_color="#d83d5a",
            command=lambda: self._delete(website, dialog),
        ).grid(row=0, column=1, padx=6)

    def _delete(self, website, dialog):
        try:
            self.app.remove_credential(website)
            dialog.destroy()
            self.refresh()
            self.app.refresh_dashboard()
        except Exception as exc:
            dialog.destroy()
            self._toast(f"Delete failed: {exc}")

    def _message(self, text, color, row=0):
        ctk.CTkLabel(self.table, text=text, text_color=color).grid(row=row, column=0, columnspan=4, padx=18, pady=18)

    def _toast(self, message):
        popup = ctk.CTkToplevel(self)
        popup.title("VaultBoxX")
        popup.geometry("320x110")
        popup.transient(self.winfo_toplevel())
        popup.configure(fg_color=self.colors["panel"])
        ctk.CTkLabel(popup, text=message, text_color=self.colors["text"], wraplength=270).pack(padx=22, pady=22)
        popup.after(1800, popup.destroy)
