import tkinter as tk
from tkinter import filedialog

def open_file_picker(picker_mode="folder"):
    """
    Открывает нативный диалог выбора файла или папки с использованием Tkinter.

    ВНИМАНИЕ: Этот подход имеет серьезные ограничения:
    1. Он работает ТОЛЬКО при локальном запуске приложения на Windows/macOS/Linux.
    2. Он НЕ БУДЕТ работать, если приложение развернуто на сервере (например, в Docker или на Streamlit Cloud).
    3. Он может вызывать проблемы с фокусом окна.

    Используйте с осторожностью, только если целевая аудитория запускает скрипт локально.

    Args:
        picker_mode (str): "folder" для выбора папки, "file" для выбора файла.

    Returns:
        str|None: Возвращает выбранный путь или None, если выбор был отменен.
    """
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    
    selected_path = filedialog.askdirectory(master=root) if picker_mode == "folder" else filedialog.askopenfilename(master=root)
        
    root.destroy()
    return selected_path