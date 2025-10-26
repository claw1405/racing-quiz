import pygame, sys, random, json
from main_menu import Menu
from quiz import Quiz
from score import ScoreScreen

class MotorSportQuiz:
    def __init__(self):
        pygame.init()
        self.width, self.height = 800, 600
        self.screen = pygame.display.set_mode((self.width, self.height))
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

        # States
        self.STATE_MENU = "box box"
        self.STATE_PLAYING = "lights out"
        self.STATE_SCORE = "points"
        self.state = self.STATE_MENU

        #Read questions from JSON and store in variable questions
        with open("questions/f1.json", "r", encoding="utf-8") as f1:
            self.questions = json.load(f1)

        random.shuffle(self.questions)

        # Screens
        self.menu_screen_obj = Menu(self.screen, self.width, self.height, self.fonts, self.colors, self.start_quiz)
        self.quiz_screen_obj = Quiz(self.screen, self.width, self.height, self.fonts, self.colors, self.questions, self.finish_quiz)
        self.score_screen_obj = None

        self.clock = pygame.time.Clock()

    def start_quiz(self):
        random.shuffle(self.questions)
        self.quiz_screen_obj = Quiz(
            self.screen,
            self.width,
            self.height,
            self.fonts,
            self.colors,
            self.questions,
            self.finish_quiz
        )
        self.state = self.STATE_PLAYING

    def finish_quiz(self, score):
        self.score_screen_obj = ScoreScreen(self.screen, self.width, self.height, self.fonts, self.colors, score, len(self.questions), self.start_quiz)
        self.state = self.STATE_SCORE

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            if self.state == self.STATE_MENU:
                self.menu_screen_obj.render()
            elif self.state == self.STATE_PLAYING:
                self.quiz_screen_obj.render()
            elif self.state == self.STATE_SCORE and self.score_screen_obj is not None:
                self.score_screen_obj.render()

            pygame.display.flip()
            self.clock.tick(30)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    MotorSportQuiz().run()