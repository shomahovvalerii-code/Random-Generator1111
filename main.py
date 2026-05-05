import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
import os
from datetime import datetime

class RandomQuoteGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Генератор случайных цитат")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # Файлы данных
        self.quotes_file = "quotes.json"
        self.history_file = "history.json"
        
        # Предопределенные цитаты
        self.default_quotes = [
            {"text": "Будьте сами собой, все остальные роли уже заняты.", 
             "author": "Оскар Уайльд", "topic": "Жизнь", "custom": False},
            {"text": "Сложнее всего начать действовать, все остальное зависит только от упорства.", 
             "author": "Амелия Эрхарт", "topic": "Мотивация", "custom": False},
            {"text": "Не ошибается тот, кто ничего не делает.", 
             "author": "Теодор Рузвельт", "topic": "Ошибки", "custom": False},
            {"text": "Успех — это способность идти от поражения к поражению, не теряя энтузиазма.", 
             "author": "Уинстон Черчилль", "topic": "Успех", "custom": False},
            {"text": "Жизнь — это то, что с тобой происходит, пока ты строишь другие планы.", 
             "author": "Джон Леннон", "topic": "Жизнь", "custom": False},
            {"text": "Если вы думаете, что на что-то способны, вы правы; если думаете, что у вас ничего не получится — вы тоже правы.", 
             "author": "Генри Форд", "topic": "Мышление", "custom": False},
            {"text": "Лучшее время посадить дерево было 20 лет назад. Второе лучшее время — сегодня.", 
             "author": "Китайская пословица", "topic": "Действие", "custom": False},
            {"text": "Знание — сила.", 
             "author": "Фрэнсис Бэкон", "topic": "Знание", "custom": False},
            {"text": "Вдохновение существует, но оно должно застать вас за работой.", 
             "author": "Пабло Пикассо", "topic": "Творчество", "custom": False},
            {"text": "Все, что вы можете представить, реально.", 
             "author": "Пабло Пикассо", "topic": "Творчество", "custom": False},
            {"text": "Свобода — это осознанная необходимость.", 
             "author": "Фридрих Энгельс", "topic": "Философия", "custom": False},
            {"text": "Счастье — это не нечто готовое. Оно проистекает из ваших собственных действий.", 
             "author": "Далай-лама", "topic": "Счастье", "custom": False}
        ]
        
        # Текущий список цитат (загружается из файла)
        self.quotes = []
        
        # История генераций
        self.history = []
        
        # Загрузка данных
        self.load_data()
        
        # Переменные для фильтров
        self.filter_author = tk.StringVar(value="Все")
        self.filter_topic = tk.StringVar(value="Все")
        
        # Создание GUI
        self.create_widgets()
        
        # Обновление списков авторов и тем
        self.update_filter_lists()
    
    def load_data(self):
        """Загрузка цитат и истории из JSON-файлов"""
        # Загрузка цитат
        if os.path.exists(self.quotes_file):
            try:
                with open(self.quotes_file, 'r', encoding='utf-8') as f:
                    saved_quotes = json.load(f)
                    # Объединяем с предопределенными, избегая дубликатов по тексту
                    existing_texts = {q['text'] for q in self.default_quotes}
                    custom_quotes = [q for q in saved_quotes if q.get('custom', True) or q['text'] not in existing_texts]
                    self.quotes = self.default_quotes + custom_quotes
            except:
                self.quotes = self.default_quotes.copy()
        else:
            self.quotes = self.default_quotes.copy()
        
        # Загрузка истории
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    self.history = json.load(f)
            except:
                self.history = []
    
    def save_quotes(self):
        """Сохранение только пользовательских цитат в JSON"""
        custom_quotes = [q for q in self.quotes if q.get('custom', False)]
        try:
            with open(self.quotes_file, 'w', encoding='utf-8') as f:
                json.dump(custom_quotes, f, ensure_ascii=False, indent=2)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить цитаты: {str(e)}")
    
    def save_history(self):
        """Сохранение истории генераций в JSON"""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить историю: {str(e)}")
    
    def create_widgets(self):
        """Создание пользовательского интерфейса"""
        # Главный контейнер с прокруткой (на случай маленького экрана)
        main_canvas = tk.Canvas(self.root)
        main_canvas.pack(side="left", fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=main_canvas.yview)
        scrollbar.pack(side="right", fill="y")
        
        main_canvas.configure(yscrollcommand=scrollbar.set)
        main_canvas.bind('<Configure>', lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all")))
        
        main_frame = ttk.Frame(main_canvas, padding=15)
        main_canvas.create_window((0,0), window=main_frame, anchor="nw")
        
        # Заголовок
        title_label = ttk.Label(main_frame, text="📜 Генератор случайных цитат", 
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Фрейм отображения цитаты
        quote_display_frame = ttk.LabelFrame(main_frame, text="Случайная цитата", padding=15)
        quote_display_frame.pack(fill="x", pady=10)
        
        # Текст цитаты
        self.quote_text_var = tk.StringVar(value="Нажмите кнопку для генерации цитаты...")
        quote_label = ttk.Label(quote_display_frame, textvariable=self.quote_text_var,
                               font=("Georgia", 12, "italic"), wraplength=600,
                               justify="center")
        quote_label.pack(pady=10)
        
        # Автор и тема
        info_frame = ttk.Frame(quote_display_frame)
        info_frame.pack(fill="x", pady=5)
        
        ttk.Label(info_frame, text="Автор:", font=("Arial", 10, "bold")).pack(side="left", padx=5)
        self.author_var = tk.StringVar()
        ttk.Label(info_frame, textvariable=self.author_var, font=("Arial", 10)).pack(side="left", padx=5)
        
        ttk.Label(info_frame, text="  Тема:", font=("Arial", 10, "bold")).pack(side="left", padx=5)
        self.topic_var = tk.StringVar()
        ttk.Label(info_frame, textvariable=self.topic_var, font=("Arial", 10)).pack(side="left", padx=5)
        
        # Кнопки управления
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill="x", pady=10)
        
        generate_btn = ttk.Button(button_frame, text="🎲 Сгенерировать цитату", 
                                 command=self.generate_quote, width=25)
        generate_btn.pack(side="left", padx=5)
        
        ttk.Button(button_frame, text="📋 Копировать цитату", 
                  command=self.copy_quote_to_clipboard, width=20).pack(side="left", padx=5)
        
        # Фрейм фильтрации
        filter_frame = ttk.LabelFrame(main_frame, text="Фильтрация", padding=10)
        filter_frame.pack(fill="x", pady=10)
        
        # Автор
        ttk.Label(filter_frame, text="Автор:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.author_combo = ttk.Combobox(filter_frame, textvariable=self.filter_author, 
                                        state="readonly", width=25)
        self.author_combo.grid(row=0, column=1, padx=5, pady=5)
        
        # Тема
        ttk.Label(filter_frame, text="Тема:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.topic_combo = ttk.Combobox(filter_frame, textvariable=self.filter_topic, 
                                       state="readonly", width=25)
        self.topic_combo.grid(row=0, column=3, padx=5, pady=5)
        
        # Кнопки фильтрации
        filter_btn_frame = ttk.Frame(filter_frame)
        filter_btn_frame.grid(row=1, column=0, columnspan=4, pady=10)
        
        ttk.Button(filter_btn_frame, text="Применить фильтр", 
                  command=self.apply_filter).pack(side="left", padx=5)
        ttk.Button(filter_btn_frame, text="Сбросить фильтр", 
                  command=self.reset_filter).pack(side="left", padx=5)
        
        # Фрейм добавления новой цитаты
        add_frame = ttk.LabelFrame(main_frame, text="Добавить свою цитату", padding=10)
        add_frame.pack(fill="x", pady=10)
        
        # Текст цитаты
        ttk.Label(add_frame, text="Текст цитаты:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.new_text = tk.Text(add_frame, height=3, width=50)
        self.new_text.grid(row=0, column=1, columnspan=3, padx=5, pady=5, sticky="we")
        
        # Автор
        ttk.Label(add_frame, text="Автор:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.new_author = ttk.Entry(add_frame, width=25)
        self.new_author.grid(row=1, column=1, padx=5, pady=5)
        
        # Тема
        ttk.Label(add_frame, text="Тема:").grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.new_topic = ttk.Entry(add_frame, width=25)
        self.new_topic.grid(row=1, column=3, padx=5, pady=5)
        
        # Кнопка добавления
        ttk.Button(add_frame, text="Добавить цитату", 
                  command=self.add_custom_quote).grid(row=2, column=1, columnspan=2, pady=10)
        
        # История цитат
        history_frame = ttk.LabelFrame(main_frame, text="История сгенерированных цитат", padding=10)
        history_frame.pack(fill="both", expand=True, pady=10)
        
        # Настройка Treeview
        columns = ("date", "text", "author", "topic")
        self.history_tree = ttk.Treeview(history_frame, columns=columns, 
                                        show="headings", height=10)
        
        self.history_tree.heading("date", text="Дата")
        self.history_tree.heading("text", text="Цитата")
        self.history_tree.heading("author", text="Автор")
        self.history_tree.heading("topic", text="Тема")
        
        self.history_tree.column("date", width=130, anchor="center")
        self.history_tree.column("text", width=350)
        self.history_tree.column("author", width=150)
        self.history_tree.column("topic", width=100, anchor="center")
        
        # Скроллбары для истории
        y_scroll = ttk.Scrollbar(history_frame, orient="vertical", command=self.history_tree.yview)
        x_scroll = ttk.Scrollbar(history_frame, orient="horizontal", command=self.history_tree.xview)
        self.history_tree.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)
        
        self.history_tree.grid(row=0, column=0, sticky="nsew")
        y_scroll.grid(row=0, column=1, sticky="ns")
        x_scroll.grid(row=1, column=0, sticky="ew")
        
        history_frame.grid_rowconfigure(0, weight=1)
        history_frame.grid_columnconfigure(0, weight=1)
        
        # Кнопки для истории
        history_btn_frame = ttk.Frame(main_frame)
        history_btn_frame.pack(fill="x", pady=5)
        
        ttk.Button(history_btn_frame, text="🗑️ Очистить историю", 
                  command=self.clear_history).pack(side="left", padx=5)
        ttk.Button(history_btn_frame, text="📤 Экспорт истории", 
                  command=self.export_history).pack(side="left", padx=5)
        
        # Отображение истории
        self.display_history()
    
    def update_filter_lists(self):
        """Обновление выпадающих списков авторов и тем"""
        authors = sorted(list(set(q['author'] for q in self.quotes)))
        topics = sorted(list(set(q['topic'] for q in self.quotes)))
        
        self.author_combo['values'] = ["Все"] + authors
        self.topic_combo['values'] = ["Все"] + topics
    
    def get_filtered_quotes(self):
        """Получение цитат согласно установленным фильтрам"""
        filtered = self.quotes
        
        author_filter = self.filter_author.get()
        if author_filter and author_filter != "Все":
            filtered = [q for q in filtered if q['author'] == author_filter]
        
        topic_filter = self.filter_topic.get()
        if topic_filter and topic_filter != "Все":
            filtered = [q for q in filtered if q['topic'] == topic_filter]
        
        return filtered
    
    def generate_quote(self):
        """Генерация случайной цитаты из отфильтрованного списка"""
        available = self.get_filtered_quotes()
        if not available:
            messagebox.showwarning("Предупреждение", 
                                  "Нет цитат, соответствующих заданным фильтрам.")
            return
        
        quote = random.choice(available)
        
        # Отображение
        self.quote_text_var.set(f"«{quote['text']}»")
        self.author_var.set(quote['author'])
        self.topic_var.set(quote['topic'])
        
        # Добавление в историю
        history_entry = {
            "date": datetime.now().strftime("%d.%m.%Y %H:%M"),
            "text": quote['text'],
            "author": quote['author'],
            "topic": quote['topic']
        }
        self.history.append(history_entry)
        self.save_history()
        self.display_history()
    
    def apply_filter(self):
        """Применение фильтра"""
        # Обновим только отображение истории; генерация будет учитывать фильтры автоматически
        self.display_history()
        # Покажем сообщение о количестве доступных цитат
        available = self.get_filtered_quotes()
        messagebox.showinfo("Фильтр", f"Доступно цитат: {len(available)}")
    
    def reset_filter(self):
        """Сброс фильтров"""
        self.filter_author.set("Все")
        self.filter_topic.set("Все")
        self.display_history()
    
    def add_custom_quote(self):
        """Добавление пользовательской цитаты"""
        text = self.new_text.get("1.0", "end-1c").strip()
        author = self.new_author.get().strip()
        topic = self.new_topic.get().strip()
        
        # Валидация пустых полей
        if not text:
            messagebox.showerror("Ошибка", "Текст цитаты не может быть пустым!")
            return
        if not author:
            messagebox.showerror("Ошибка", "Имя автора не может быть пустым!")
            return
        if not topic:
            messagebox.showerror("Ошибка", "Тема цитаты не может быть пустой!")
            return
        
        # Проверка на дубликат
        if any(q['text'] == text for q in self.quotes):
            messagebox.showerror("Ошибка", "Такая цитата уже существует!")
            return
        
        new_quote = {
            "text": text,
            "author": author,
            "topic": topic,
            "custom": True
        }
        
        self.quotes.append(new_quote)
        self.save_quotes()
        self.update_filter_lists()
        
        # Очистка полей ввода
        self.new_text.delete("1.0", "end")
        self.new_author.delete(0, "end")
        self.new_topic.delete(0, "end")
        
        messagebox.showinfo("Успех", "Цитата успешно добавлена!")
    
    def display_history(self):
        """Отображение истории в таблице с учетом фильтров"""
        # Очистка
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        
        # Применяем фильтры к истории
        filtered_history = self.history
        author_filter = self.filter_author.get()
        topic_filter = self.filter_topic.get()
        
        if author_filter and author_filter != "Все":
            filtered_history = [h for h in filtered_history if h['author'] == author_filter]
        if topic_filter and topic_filter != "Все":
            filtered_history = [h for h in filtered_history if h['topic'] == topic_filter]
        
        # Отображение (новые сверху)
        for entry in reversed(filtered_history):
            self.history_tree.insert("", "end", values=(
                entry['date'],
                entry['text'],
                entry['author'],
                entry['topic']
            ))
    
    def clear_history(self):
        """Очистка всей истории"""
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить всю историю?"):
            self.history = []
            self.save_history()
            self.display_history()
            messagebox.showinfo("Успех", "История очищена!")
    
    def export_history(self):
        """Экспорт истории в текстовый файл"""
        try:
            filename = f"quotes_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("История сгенерированных цитат\n")
                f.write("=" * 50 + "\n\n")
                for entry in self.history:
                    f.write(f"[{entry['date']}] {entry['author']} ({entry['topic']}):\n")
                    f.write(f"«{entry['text']}»\n")
                    f.write("-" * 40 + "\n")
            messagebox.showinfo("Экспорт", f"История сохранена в файл {filename}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось экспортировать: {str(e)}")
    
    def copy_quote_to_clipboard(self):
        """Копирование текущей цитаты в буфер обмена"""
        text = f"«{self.quote_text_var.get()}» — {self.author_var.get()} ({self.topic_var.get()})"
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        messagebox.showinfo("Копирование", "Цитата скопирована в буфер обмена!")

if __name__ == "__main__":
    root = tk.Tk()
    app = RandomQuoteGenerator(root)
    root.mainloop()