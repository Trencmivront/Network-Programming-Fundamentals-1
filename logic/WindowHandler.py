import tkinter as tk
import threading
from logger import get_logger
import logic.cache as cache

logger = get_logger("WindowHandler")


def switch_panel(root, panel_class=None, *args, **kwargs):
    """Replaces the current panel displayed in root with an instance of panel_class.

    When panel_class is None (back navigation) the cache is popped and
    get_last_frame() resolves the destination.  For forward navigation the
    supplied panel_class is pushed onto the cache so BackButton can return.

    Args:
        root:        The root Tk window that owns current_panel.
        panel_class: The panel class to instantiate, or None to go back.
    """
    try:
        if panel_class is None:
            # Back navigation: pop current frame and resolve previous destination.
            cache.pop()
            panel_class = cache.get_last_frame()
            if panel_class is None:
                # Lazy import to avoid circular dependency at module load time.
                from gui.panels.MainButtonSetPanel import MainButtonSetPanel
                panel_class = MainButtonSetPanel
        else:
            # Forward navigation: track the destination in the cache.
            cache.push(panel_class)

        old_panel = root.current_panel
        logger.info(f"Switching panel to {panel_class.__name__}")

        # Show loading state
        loading_label = tk.Label(root, text="Loading...", font=("Arial", 14))
        loading_label.pack(expand=True)
        root.update()  # Force GUI refresh

        def create_panel():
            # Destroy old panel in background thread (can be slow)
            if old_panel is not None:
                old_panel.destroy()

            root.current_panel = panel_class(root, *args, **kwargs)

            if root.current_panel is None or not root.current_panel.winfo_exists():
                loading_label.destroy(),
                switch_panel(root)
                return

            root.after(0, lambda: (
                loading_label.destroy(),
                root.current_panel.pack(expand=True),
                logger.info(f"Panel {panel_class.__name__} loaded"),
            ))

        thread = threading.Thread(target=create_panel, daemon=True)
        thread.start()

    except Exception as error:
        logger.error(f"Error switching panel to {getattr(panel_class, '__name__', panel_class)}: {error}", exc_info=True)
