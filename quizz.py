import tkinter as tk
from tkinter import ttk
import json
import random
import pygame

pygame.mixer.init()


def load_questions(filename="questions.json"):
    with open(filename, "r") as file:
        return json.load(file)

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz App")
        self.root.geometry("500x450")

        self.questions = load_questions()
        random.shuffle(self.questions)

        self.current_question = 0
        self.score = 0

        # Load sound effects
        self.correct_sound = pygame.mixer.Sound("correct.mp3")
        self.wrong_sound = pygame.mixer.Sound("wrong.mp3")

        # Progress Bar
        self.progress = ttk.Progressbar(root, length=300, mode='determinate')
        self.progress.pack(pady=10)

        # Timer Label
        self.timer_label = tk.Label(root, text="", font=("Arial", 12), fg="blue")
        self.timer_label.pack(pady=10)

        # Question Label
        self.label = tk.Label(root, text="", font=("Arial", 14), wraplength=400)
        self.label.pack(pady=20)

        # Answer Buttons
        self.buttons = []
        for i in range(4):
            btn = tk.Button(root, text="", font=("Arial", 14), width=25, height=2, 
                            bg="#f0f0f0", activebackground="#ddd", 
                            command=lambda i=i: self.check_answer(i))
            btn.pack(pady=5)
            self.buttons.append(btn)

        # Play Again Button
        self.play_again_btn = tk.Button(self.root, text="🔄 Play Again", font=("Arial", 14), width=20, bg="#4CAF50", fg="white",
                                        command=self.restart_quiz)
        self.play_again_btn.pack_forget()

        self.next_question()

    def start_timer(self):
        """Start countdown timer (10 seconds)."""
        self.time_left = 10
        self.timer_label.config(text=f"Time Left: {self.time_left}s")
        self.update_timer()

    def update_timer(self):
        """Update timer every second."""
        if self.time_left > 0:
            self.time_left -= 1
            self.timer_label.config(text=f"Time Left: {self.time_left}s")
            self.root.after(1000, self.update_timer)
        else:
            self.label.config(text=f"⏳ Time Up! Correct: {self.correct_answer_text}", fg="red")
            self.current_question += 1
            self.root.after(1000, self.next_question)

    def next_question(self):
        """Load the next question."""
        if self.current_question < len(self.questions):
            q = self.questions[self.current_question]
            self.label.config(text=q["question"])

            self.options = q["options"][:]  
            random.shuffle(self.options)  

            self.correct_answer = q["answer"]
            try:
                self.correct_answer_text = next(opt for opt in self.options if opt.startswith(self.correct_answer + "."))
            except StopIteration:
                self.correct_answer_text = self.options[0]  

            for i, option in enumerate(self.options):
                self.buttons[i].config(text=option, state=tk.NORMAL)
                self.buttons[i].pack()

            self.play_again_btn.pack_forget()

            progress_value = ((self.current_question + 1) / len(self.questions)) * 100
            self.progress["value"] = progress_value

            self.start_timer()
        else:
            self.show_scoreboard()

    def check_answer(self, choice):
        """Check selected answer and play sound."""
        selected_option = self.buttons[choice]["text"]

        if selected_option == self.correct_answer_text:
            self.score += 1
            self.label.config(text="✅ Correct!", fg="green")
            self.correct_sound.play()
        else:
            self.label.config(text=f"❌ Wrong! Correct: {self.correct_answer_text}", fg="red")
            self.wrong_sound.play()

        for btn in self.buttons:
            btn.config(state=tk.DISABLED)

        self.current_question += 1
        self.root.after(1000, self.next_question)

    def show_scoreboard(self):
        """Display quiz results."""
        total_questions = len(self.questions)
        wrong_answers = total_questions - self.score
        percentage = (self.score / total_questions) * 100

        self.label.config(text=f"🏆 Quiz Over!\n\n✅ Correct: {self.score}\n❌ Wrong: {wrong_answers}\n📊 Score: {percentage:.2f}%", font=("Arial", 14))

        self.timer_label.pack_forget()
        self.progress.pack_forget()
        for btn in self.buttons:
            btn.pack_forget()

        self.play_again_btn.pack(pady=20)

    def restart_quiz(self):
        """Restart the quiz."""
        self.current_question = 0
        self.score = 0
        random.shuffle(self.questions)

        self.progress.pack()
        self.timer_label.pack()
        for btn in self.buttons:
            btn.pack()

        self.next_question()

# Run Tkinter App
root = tk.Tk()
app = QuizApp(root)
root.mainloop()
