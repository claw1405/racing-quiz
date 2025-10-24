import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,
    QLabel, QRadioButton, QPushButton,
    QMessageBox, QButtonGroup
)
from PySide6.QtGui import QPainter, QColor, QFont
from PySide6.QtCore import Qt, QRect, QTimer
class MotorSportQuiz(QWidget) :
    """This will be the main class for my motorsport quiz app"""
    def __init__(self):
        """Initiate the games assets and resources"""
        super().__init__()
        self.setWindowTitle("Motorsport Quiz")
        self.resize(800, 600)
        self.setStyleSheet("background-color: black;")

        # Quiz Data
        self.questions = [
            {
                "question" : "Which F1 driver won the drivers championship in 2024?",
                "options" : ["Lewis Hamilton", "Max Verstappen", "Piere Gasly", "Sebastian Vettel"],
                "answer" : "Max Verstappen"
            },
            {
                "question" : "Who was the last driver that won a WDC for Mclaren?",
                "options" : ["Lewis Hamilton", "Lando Norris", "Ayrton Senna", "Checo Perez"],
                "answer" : "Lewis Hamilton"
            }
        ]
        
        self.score = 0
        self.current_index = 0

        # Buttons for answers
        self.buttons = []
        for i in range(4):
            btn = QPushButton(self)
            btn.setGeometry(QRect(250, 300 + i * 60, 300, 50))
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #2e8b57;
                    color: white;
                    font-size: 18px;
                    border-radius: 10px;
                }
                QPushButton:hover {
                    background-color: #3cb371;
                }
            """)
            btn.clicked.connect(self.check_answer)
            self.buttons.append(btn)

        # Set the boolean flags with starting states
        self.lights_out = False
        self.box_box = True
        self.game_muted = False

        self.load_question()

    def load_question(self):
        """Load the current question and update button"""
        if self.current_index >= len(self.questions):
            self.end_quiz()
            return
        
        q = self.questions[self.current_index]
        self.current_question = q["question"]
        self.correct_answer = q["answer"]

        for i, option in enumerate(q["options"]):
            self.buttons[i].setText(option)

        self.update() # Refresh Display

    def check_answer(self):
        """Check if the selected answer is correct"""
        sender = self.sender()
        answer = sender.text()

        if answer == self.correct_answer:
            sender.setStyleSheet("background-color: #228b22; color: white;font-size: 18px; border-radius: 10px;")
            self.score += 1
        else:
            sender.setStyleSheet("background-color: #b22222; color: white; font-size: 18px; border-radius: 10px;")
        
        # Move to the next question after a short delay
        QApplication.instance().processEvents()
        self.repaint()
        self.current_index += 1
        QTimer.singleShot(1000, self.load_question)

    def show_result(self):
        QMessageBox.information (
            self,
            "Quiz Finished",
            f"Your final score: {self.score}/{len(self.questions)}"
        )
        self.close()

    def draw_event(self, event):
        """Draw background and text"""
        painter = QPainter(self)

        #set bg colour
        painter.fillRect(self.rect(), QColor("#1e1e1e"))

        # Draw text
        painter.setPen(Qt.white)
        painter.setFont(QFont("Ariel", 24, QFont.bold))
        painter.drawText(200, 200, "Hello placeholder")

        #Current question
        painter.setFont(QFont("Arial", 20))
        if hasattr(self, "current_question"):
            painter.drawText(50, 200, self.current_question)

        painter.setFont(QFont("Consolas", 20))
        painter.drawText(QFont(650, 50, f"Score: {self.score}"))

    def end_quiz(self):
        """End the quiz and display score"""
        for btn in self.buttons:
            btn.hide()
        self.current_question = f"Quiz complete! Final Score: {self.score}/{len(self.questions)}"
        self.update()
        QTimer.singleShot(2000, self.show_result)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MotorSportQuiz()
    window.show()
    sys.exit(app.exec())

    

