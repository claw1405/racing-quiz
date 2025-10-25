import pygame, sys, random
from main_menu import Menu

class MotorSportQuiz:
    """This is the main overarching class for my motorsport quiz"""
    def __init__(self):
        """Initiate all attributes used throughout the motorsport quiz"""
        pygame.init()

        # Set up the surface
        self.width, self.height = 800, 600
        self.screen = pygame.display.set_mode((self.width, self.height))

        #This is the window title
        pygame.display.set_caption("Grand Prix Trivia") 

        # Fonts & Colors
        self.fonts = {
            "title": pygame.font.Font(None, 60),
            "question": pygame.font.Font(None, 40),
            "option": pygame.font.Font(None, 36)
        }
        self.colors = {
            "WHITE": (255, 255, 255),
            "BLACK": (0, 0, 0),
            "RED": (200, 50, 50),
            "GREEN": (50, 200, 50),
            "BLUE": (70, 130, 180),
            "GREY": (180, 180, 180)
        }

        # Game states
        self.STATE_MENU = "box box"
        self.STATE_PLAYING = "lights out"
        self.STATE_SCORE = "points"
        self.state = self.STATE_MENU

        # Questions
        self.questions = [
            {"question": "Who won the 2023 Formula 1 World Championship?", "options": ["Lewis Hamilton", "Max Verstappen", "Charles Leclerc", "Lando Norris"], "answer": 1},
            {"question": "Which circuit features the Eau Rouge corner?", "options": ["Monza", "Spa-Francorchamps", "Silverstone", "Suzuka"], "answer": 1},
            {"question": "What color flag signals the end of a race?", "options": ["Yellow", "Red", "Checkered", "Green"], "answer": 2}
        ]
        random.shuffle(self.questions) # Output questions in a random order

        self.current_question = 0
        self.score = 0
        self.mouse_clicked = False  # Track mouse clicks
        self.clock = pygame.time.Clock()

        # Menu instance
        self.menu_screen_obj = Menu(self.screen, self.width, self.height, self.fonts, self.colors, self.start_quiz)

    # --- Quiz & Score Screens ---
    def draw_text(self, text, font, color, x, y):
        text_obj = font.render(text, True, color)
        text_rect = text_obj.get_rect(center=(x, y))
        self.screen.blit(text_obj, text_rect)

    def draw_button(self, text, x, y, w, h, color, hover_color, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()[0]
        if x + w > mouse[0] > x and y + h > mouse[1] > y:
            pygame.draw.rect(self.screen, hover_color, (x, y, w, h))
            if click and not self.mouse_clicked and action is not None:
                action()
            self.mouse_clicked = click
        else:
            pygame.draw.rect(self.screen, color, (x, y, w, h))

        # Update click state when mouse is not over button
        if not click:
            self.mouse_clicked = False

        self.draw_text(text, self.fonts["option"], self.colors["WHITE"], x + w / 2, y + h / 2)

    def start_quiz(self):
        self.state = self.STATE_PLAYING
        self.current_question = 0
        self.score = 0

    def handle_answer(self, selected):
        correct = self.questions[self.current_question]["answer"]
        if selected == correct:
            self.score += 1
        self.current_question += 1
        if self.current_question >= len(self.questions):
            self.state = self.STATE_SCORE

    def quiz_screen(self):
        self.screen.fill(self.colors["BLACK"])
        q = self.questions[self.current_question]
        self.draw_text(q["question"], self.fonts["question"], self.colors["WHITE"], self.width / 2, 100)
        for i, option in enumerate(q["options"]):
            self.draw_button(option, self.width / 2 - 150, 200 + i * 80, 300, 60, self.colors["BLUE"], self.colors["GREEN"], lambda i=i: self.handle_answer(i))

    def score_screen(self):
        self.screen.fill(self.colors["BLACK"])
        self.draw_text("Quiz Complete!", self.fonts["title"], self.colors["WHITE"], self.width / 2, self.height / 3)
        self.draw_text(f"Score: {self.score}/{len(self.questions)}", self.fonts["question"], self.colors["GREEN"], self.width / 2, self.height / 2)
        self.draw_button("Play Again", self.width / 2 - 100, self.height / 2 + 100, 200, 60, self.colors["BLUE"], self.colors["GREEN"], self.start_quiz)
        self.draw_button("Quit", self.width / 2 - 100, self.height / 2 + 180, 200, 60, self.colors["RED"], self.colors["GREY"], sys.exit)

    # --- Main Loop ---
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            if self.state == self.STATE_MENU:
                self.menu_screen_obj.render()
            elif self.state == self.STATE_PLAYING:
                self.quiz_screen()
            elif self.state == self.STATE_SCORE:
                self.score_screen()

            pygame.display.flip()
            self.clock.tick(30)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    MotorSportQuiz().run()