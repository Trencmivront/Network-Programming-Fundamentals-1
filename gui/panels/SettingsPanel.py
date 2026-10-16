from tkinter import Frame, Label, Entry, Button, StringVar, messagebox
from ..components.BackButton import BackButton
import logic.Settings as Settings
from logger import get_logger

logger = get_logger("SettingsPanel")


class SettingsPanel(Frame):
    """Panel for viewing and editing application settings.

    Reads current values from logic.Settings module cache and persists
    changes back through Settings.set(), which also writes to settings.json.
    """

    def __init__(self, root):
        super().__init__(root, padx=30, pady=25)
        logger.info("Initializing SettingsPanel")

        # ── Header ────────────────────────────────────────────────────────────
        self.title_label = Label(
            self,
            text="Settings",
            font=("Arial", 22, "bold"),
            fg="#1a365d",
        )
        self.title_label.pack(pady=(5, 20))

        # ── Card container ────────────────────────────────────────────────────
        self.card_frame = Frame(
            self,
            bg="#f8fafc",
            bd=1,
            relief="solid",
            padx=25,
            pady=20,
        )
        self.card_frame.pack(fill="x", padx=10, pady=10)

        # ── Setting rows (display label, Settings attribute name) ─────────────
        self._fields = []
        self._add_setting_row("Echo Server Host:",        "echoServerHost")
        self._add_setting_row("Echo Server Port:",        "echoServerPort")
        self._add_setting_row("Echo Server Backlog:",     "echoServerBacklog")
        self._add_setting_row("Echo Server Payload (B):", "echoServerDataPayload")
        self._add_setting_row("Echo Test Timeout (s):",   "echoTestTimeout")
        self._add_setting_row("Echo Client Payload Count:", "echoClientPayloadCount")
        self._add_setting_row("NTP Server URL:",          "ntpURL")
        self._add_setting_row("Logging:",                 "loggingEnabled")
        self._add_setting_row("Debugging:",               "debuggingEnabled")

        # ── Action buttons ────────────────────────────────────────────────────
        btn_frame = Frame(self)
        btn_frame.pack(pady=(20, 5))

        self.save_button = Button(
            btn_frame,
            text="Save",
            font=("Arial", 13, "bold"),
            bg="#2b6cb0",
            fg="white",
            activebackground="#2c5282",
            activeforeground="white",
            padx=20,
            pady=6,
            relief="flat",
            cursor="hand2",
            command=self._on_save,
        )
        self.save_button.pack(side="left", padx=(0, 10))

        self.reset_button = Button(
            btn_frame,
            text="Reset to Defaults",
            font=("Arial", 13),
            bg="#e2e8f0",
            fg="#2d3748",
            activebackground="#cbd5e0",
            padx=20,
            pady=6,
            relief="flat",
            cursor="hand2",
            command=self._on_reset,
        )
        self.reset_button.pack(side="left")

        # ── Back button ───────────────────────────────────────────────────────
        self.back_button = BackButton(self)
        self.back_button.pack(pady=(15, 10))

    # ── Helpers ───────────────────────────────────────────────────────────────

    def _add_setting_row(self, label_text, settings_attr):
        """Create one labelled editable row pre-filled with the current value."""
        row_frame = Frame(self.card_frame, bg="#f8fafc")
        row_frame.pack(fill="x", pady=8, anchor="w")

        field_label = Label(
            row_frame,
            text=label_text,
            font=("Arial", 14, "bold"),
            fg="#2d3748",
            bg="#f8fafc",
            width=25,
            anchor="w",
        )
        field_label.pack(side="left")

        var = StringVar(value=str(getattr(Settings, settings_attr, "")))

        entry = Entry(
            row_frame,
            textvariable=var,
            font=("Arial", 14),
            fg="#1a202c",
            bg="#edf2f7",
            relief="groove",
            bd=1,
        )
        entry.pack(side="left", fill="x", expand=True, ipady=5)

        self._fields.append((settings_attr, var))

    def _on_save(self):
        """Read all entry values, validate through Settings.set(), and persist."""
        raw = {attr: var.get().strip() for attr, var in self._fields}
        try:
            Settings.set(
                echo_server_host=raw["echoServerHost"],
                echo_server_port=int(raw["echoServerPort"]),
                echo_server_backlog=int(raw["echoServerBacklog"]),
                echo_server_data_payload=int(raw["echoServerDataPayload"]),
                echo_test_timeout=float(raw["echoTestTimeout"]),
                echo_client_payload_count=int(raw["echoClientPayloadCount"]),
                ntp_url=raw["ntpURL"],
                logging_enabled=raw["loggingEnabled"].lower() in ("true", "1", "yes"),
                debugging_enabled=raw["debuggingEnabled"].lower() in ("true", "1", "yes"),
            )
            logger.info("Settings saved successfully")
            messagebox.showinfo("Settings", "Settings saved successfully.")
        except (ValueError, TypeError) as error:
            logger.error(f"Failed to save settings: {error}")
            messagebox.showerror("Invalid Value", str(error))

    def _on_reset(self):
        """Reset all settings to defaults and refresh the entry fields."""
        if not messagebox.askyesno("Reset Settings", "Reset all settings to defaults?"):
            return
        Settings.init()
        # Refresh displayed values from the updated cache
        for attr, var in self._fields:
            var.set(str(getattr(Settings, attr, "")))
        logger.info("Settings reset to defaults")
        messagebox.showinfo("Settings", "Settings reset to defaults.")
