import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox, simpledialog
from tkinter import ttk
from PIL import Image, ImageDraw
from PIL import ImageDraw, ImageFont

class DrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Рисовалка с сохранением в PNG")

        self.image = Image.new("RGB", (600, 400), "white")
        self.draw = ImageDraw.Draw(self.image)

        self.canvas = tk.Canvas(root, width=600, height=400, bg='white')
        self.canvas.pack()

        self.color_preview_canvas = tk.Canvas(root, width=50, height=50, bg='black')
        self.color_preview_canvas.pack(side=tk.RIGHT, padx=10, pady=10)

        self.brush_sizes = [1, 2, 5, 10]
        self.setup_ui()

        self.last_x, self.last_y = None, None
        self.pen_color = 'black'
        self.previous_color = self.pen_color

        self.canvas.bind('<B1-Motion>', self.paint)
        self.canvas.bind('<ButtonRelease-1>', self.reset)
        self.canvas.bind('<Button-3>', self.pick_color)

        self.root.bind('<Alt-s>', self.save_image)
        self.root.bind('<Alt-c>', self.choose_color)

        self.canvas.bind('<Double-1>', self.add_text)

    def add_text(self, event):
        save_image = messagebox.askyesno("Сохранить рисунок?",
                                         "Хотите сохранить текущий рисунок перед добавлением текста?")
        if save_image:
            self.save_image()

        text = simpledialog.askstring("Добавить текст", "Введите текст:")
        if text:
            x, y = event.x, event.y
            self.canvas.create_text(x, y, text=text, fill=self.pen_color, font=("Arial", 16))

            font = ImageFont.truetype("arial.ttf", 16)
            self.draw.text((x, y), text, font=font, fill=self.pen_color)


    def change_background_color(self):
        new_color = colorchooser.askcolor(color=self.canvas["bg"])[1]
        if new_color:
             self.canvas.config(background=new_color)

    def change_canvas_size(self):
        new_width = simpledialog.askinteger("Новый размер холста", "Введите новую ширину:")
        new_height = simpledialog.askinteger("Новый размер холста", "Введите новую высоту:")
        if new_width is not None and new_height is not None:
            self.canvas.config(width=new_width, height=new_height)
            self.image = Image.new("RGB", (new_width, new_height), "white")
            self.draw = ImageDraw.Draw(self.image)
            self.clear_canvas()

    def save_image(self, event=None):
        file_path = filedialog.asksaveasfilename(filetypes=[('PNG files', '*.png')])
        if file_path:
            if not file_path.endswith('.png'):
                file_path += '.png'
            self.image.save(file_path)
            messagebox.showinfo("Информация", "Изображение успешно сохранено!")

    def setup_ui(self):
        control_frame = tk.Frame(self.root)
        control_frame.pack(fill=tk.X)

        clear_button = tk.Button(control_frame, text="Очистить", command=self.clear_canvas)
        clear_button.pack(side=tk.LEFT)

        color_button = tk.Button(control_frame, text="Выбрать цвет", command=self.choose_color)
        color_button.pack(side=tk.LEFT)

        save_button = tk.Button(control_frame, text="Сохранить", command=self.save_image)
        save_button.pack(side=tk.LEFT)

        change_size_button = tk.Button(control_frame, text="Изменить размер холста", command=self.change_canvas_size)
        change_size_button.pack(side=tk.LEFT)

        brush_size_label = tk.Label(control_frame, text="Размер кисти:")
        brush_size_label.pack(side=tk.LEFT)

        self.brush_size_option = tk.StringVar(self.root)
        self.brush_size_option.set(str(self.brush_sizes[0]))
        brush_size_menu = tk.OptionMenu(control_frame, self.brush_size_option, *[str(size) for size in self.brush_sizes])
        brush_size_menu.pack(side=tk.LEFT)

        self.graph_style = tk.StringVar(self.root)
        self.graph_style.set("solid")
        graph_style_label = tk.Label(control_frame, text="Стиль графика:")
        graph_style_label.pack(side=tk.LEFT)

        graph_style_menu = ttk.Combobox(control_frame, textvariable=self.graph_style,
                                       values=["solid", "dash", "dot", "dashdot"])
        graph_style_menu.pack(side=tk.LEFT)

        self.eraser_button = tk.Button(control_frame, text="Ластик", command=self.use_eraser)
        self.eraser_button.pack(side=tk.LEFT)

        text_button = tk.Button(control_frame, text="Текст", command=self.add_text)
        text_button.pack(side=tk.LEFT)

        change_background_button = tk.Button(control_frame, text="Изменить фон", command=self.change_background_color)
        change_background_button.pack(side=tk.LEFT)

    def paint(self, event):
        brush_size = int(self.brush_size_option.get())
        if self.last_x and self.last_y:
            if self.graph_style.get() == "solid":
                self.canvas.create_line(self.last_x, self.last_y, event.x, event.y,
                                        width=brush_size, fill=self.pen_color,
                                        capstyle=tk.ROUND, smooth=tk.TRUE)
            else:
                dash_patterns = {
                    "dash": (4, 4),
                    "dot": (2, 2),
                    "dashdot": (4, 2, 2, 2)
                }
                self.canvas.create_line(self.last_x, self.last_y, event.x, event.y,
                                        width=brush_size, fill=self.pen_color,
                                        capstyle=tk.ROUND, smooth=tk.TRUE,
                                        dash=dash_patterns.get(self.graph_style.get(), None))
            self.draw.line([self.last_x, self.last_y, event.x, event.y], fill=self.pen_color,
                           width=brush_size)

        self.last_x = event.x
        self.last_y = event.y

    def reset(self, event):
        self.last_x, self.last_y = None, None

    def clear_canvas(self):
        self.canvas.delete("all")
        self.image = Image.new("RGB", (600, 400), "white")
        self.draw = ImageDraw.Draw(self.image)

    def choose_color(self, event=None):
        color = colorchooser.askcolor(color=self.pen_color)
        if color[1]:
            self.pen_color = color[1]
            self.previous_color = self.pen_color
            self.update_color_preview()

    def pick_color(self, event):
        x, y = event.x, event.y
        color = self.image.getpixel((x, y))
        self.pen_color = '#%02x%02x%02x' % color
        self.previous_color = self.pen_color
        self.update_color_preview()

    def save_image(self, event=None):
        file_path = filedialog.asksaveasfilename(filetypes=[('PNG files', '*.png')])
        if file_path:
            if not file_path.endswith('.png'):
                file_path += '.png'
            self.image.save(file_path)
            messagebox.showinfo("Информация", "Изображение успешно сохранено!")

    def use_eraser(self):
        self.previous_color = self.pen_color
        self.pen_color = "white"
        self.canvas.config(cursor="dot")
        self.update_color_preview()

    def return_to_brush(self):
        self.pen_color = self.previous_color
        self.canvas.config(cursor="")
        self.update_color_preview()

    def update_color_preview(self):
        self.color_preview_canvas.configure(bg=self.pen_color)

def main():
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()



