import tkinter as tk
from tkinter import ttk
import keyboard
import dataHandle

class OverlayApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Exile Leveling Overlay")
        self.root.geometry("400x80")
        self.root.attributes("-topmost", True)  # Trzymaj okno na wierzchu
        self.root.attributes("-alpha", 0.9)  # Ustawienie przezroczystości dla całego okna (wartość od 0.0 do 1.0)
        self.root.configure(bg='#262626')  # Ustawienie tła na ciemnoszary
        self.root.overrideredirect(True)
        self.root.geometry("+5+5")
        self.root.lift()
        self.root.wm_attributes("-topmost", True)

        # Przykładowe dane z przewodnika Exile Leveling
        self.leveling_steps = dataHandle.steps
        self.current_step_index = 0

        self.step_label = ttk.Label(self.root, text="", wraplength=380, foreground='white', font=('Arial', 12, 'bold'), background='#262626')  # Biały, pogrubiony tekst na ciemnoszarym tle
        self.step_label.pack(pady=20)

        # Wiązanie klawiszy do funkcji
        keyboard.add_hotkey('c', self.prev_step)
        keyboard.add_hotkey('v', self.next_step)
        keyboard.add_hotkey('ctrl+`', self.close_overlay)

        self.update_step()  # Zaktualizuj wyświetlany krok

    def update_step(self):
        self.step_label.config(text=self.leveling_steps[self.current_step_index])

    def next_step(self):
        if self.current_step_index < len(self.leveling_steps) - 1:
            self.current_step_index += 1
            self.update_step()

    def prev_step(self):
        if self.current_step_index > 0:
            self.current_step_index -= 1
            self.update_step()

    def close_overlay(self):
        self.root.destroy()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = OverlayApp()
    app.run()
