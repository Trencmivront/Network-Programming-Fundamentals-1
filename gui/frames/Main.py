import tkinter as tk                                                                                                                                                                          
from ..panels.MainButtonSetPanel import MainButtonSetPanel                                                                                                                                    
from logger import get_logger, attach_gui_error_handler                                                                                                                                       
from logic.GlobalExceptionHandler import GlobalExceptionHandler                                                                                                                               
import logic.WindowHandler as WindowHandler                                                                                                                                                   
import logic.Settings as sett                                                                                                                                                                 
from gui.frames.DebugFrame import DebugFrame                                                                                                                                                  
                                                                                                                                                                                                
logger = get_logger("Main")                                                                                                                                                                   
                                                                                                                                                                                                
class Main(tk.Tk):                                                                                                                                                                            
    _instance = None  # Class-level static reference                                                                                                                                          
                                                                                                                                                                                                
    def __init__(self):                                                                                                                                                                       
        super().__init__()                                                                                                                                                                    
        Main._instance = self  # Register immediately

        # Attach GUI error dialog handler                                                                                                                                                     
        attach_gui_error_handler(self)                                                                                                                                                        
                                                                                                                                                                                                
        # Catch all unhandled exceptions and route them through the logger                                                                                                                    
        GlobalExceptionHandler(self).install()                                                                                                                                                
                                                                                                                                                                                                
        self.option_add("*Font", "Arial 16")                                                                                                                                                  
        self.title("Project - 1")                                                                                                                                                             
        self.geometry("800x600")                                                                                                                                                              
                                                                                                                                                                                                
        # Clean up reference when the window is destroyed                                                                                                                                     
        self.protocol("WM_DELETE_WINDOW", self._on_close)                                                                                                                                     
                                                                                                                                                                                                
        self.current_panel = None                                                                                                                                                             
        WindowHandler.switch_panel(root=self, panel_class=MainButtonSetPanel)              

        self.debug = None # safe instant                                                                                                                                                                                                                                                                                        
        if sett.debuggingEnabled:                                                                                                                                                             
            self.create_debug_win()                                                                                                                                             

    def _on_close(self):
        """Destroy main window and debug window."""                                                                                                                                                 
        Main._instance = None
        self.debug = None                                                                                                                                                                 
        self.destroy()    

    def create_debug_win(self):
        """Creates a debug window if it does not already exist."""
        try:
            if self.debug is None or not self.debug.winfo_exists():
                self.debug = DebugFrame(root=self)
        except (tk.TclError, AttributeError):
            self.debug = DebugFrame(root=self)

    def destroy_debug_win(self):
        """Destroys the debug window if it is alive."""
        if self.debug is not None:
            try:
                if self.debug.winfo_exists():
                    self.debug.destroy()
            except (tk.TclError, AttributeError):
                pass
            self.debug = None 

    # Class methods work even without creating an object.

    @classmethod                                                                                                                                                                              
    def get_instance(cls):                                                                                                                                                                    
        """Returns the active Main instance, or None if not created/closed."""                                                                                                                
        if cls.is_alive():                                                                                                                                                                    
            return cls._instance                                                                                                                                                              
        return None                                                                                                                                                                           
                                                                                                                                                                                                
    @classmethod                                                                                                                                                                              
    def is_alive(cls):                                                                                                                                                                        
        """Checks if the Main window exists and is not destroyed."""                                                                                                                          
        try:                                                                                                                                                                                  
            return cls._instance is not None and cls._instance.winfo_exists() == 1                                                                                                            
        except (tk.TclError, AttributeError):                                                                                                                                                 
            return False