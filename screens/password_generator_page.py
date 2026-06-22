import customtkinter as ctk

from screens.base import BasePage


class PasswordGeneratorPage(BasePage):
    """Password generation screen backed by password_generator.py."""

    def __init__(self, parent, app):
        super().__init__(parent, app)
        self.page_title("Password Generator", "Create strong random passwords")

        card = self.make_card(self, row=1, column=0, sticky="nsew")
        card.grid_columnconfigure(0, weight=1)

        self.length_label = ctk.CTkLabel(
            card,
            text="Length: 16",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self.colors["text"],
        )
        self.length_label.grid(row=0, column=0, padx=24, pady=(26, 8), sticky="w")

        self.length_slider = ctk.CTkSlider(card, from_=8, to=64, number_of_steps=56, command=self._length_changed)
        self.length_slider.set(16)
        self.length_slider.grid(row=1, column=0, padx=24, pady=(0, 26), sticky="ew")

        self.output_entry = ctk.CTkEntry(
            card,
            height=48,
            corner_radius=12,
            placeholder_text="Generated password",
            fg_color="#081829",
            border_color=self.colors["panel_alt"],
        )
        self.output_entry.grid(row=2, column=0, padx=24, pady=(0, 16), sticky="ew")

        buttons = ctk.CTkFrame(card, fg_color="transparent")
        buttons.grid(row=3, column=0, padx=24, pady=(0, 24), sticky="ew")
        buttons.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkButton(
            buttons,
            text="Generate",
            height=46,
            corner_radius=12,
            fg_color=self.colors["accent_dark"],
            hover_color="#0bbbe8",
            command=self._generate,
        ).grid(row=0, column=0, padx=(0, 8), sticky="ew")

        ctk.CTkButton(
            buttons,
            text="Copy",
            height=46,
            corner_radius=12,
            fg_color=self.colors["panel_alt"],
            hover_color="#1b3958",
            command=self._copy,
        ).grid(row=0, column=1, padx=(8, 0), sticky="ew")

        self.status_label = ctk.CTkLabel(card, text="", text_color=self.colors["muted"])
        self.status_label.grid(row=4, column=0, padx=24, pady=(0, 24), sticky="w")

    def _length_changed(self, value):
        self.length_label.configure(text=f"Length: {int(value)}")

    def _generate(self):
        try:
            password = self.app.make_password(int(self.length_slider.get()))
        except Exception as exc:
            self.status_label.configure(text=f"Could not generate password: {exc}", text_color=self.colors["danger"])
            return

        self.output_entry.delete(0, "end")
        self.output_entry.insert(0, password)
        self.status_label.configure(text="Password generated.", text_color=self.colors["success"])

    def _copy(self):
        value = self.output_entry.get()
        if not value:
            self.status_label.configure(text="Generate a password first.", text_color=self.colors["danger"])
            return
        self.app.copy_to_clipboard(value)
        self.status_label.configure(text="Copied to clipboard.", text_color=self.colors["success"])
