# Imports required by the main MotorSport quiz class
import pygame, sys, random, json, time
from main_menu import Menu
from quiz import Quiz
from score import ScoreScreen

class MotorSportQuiz:
    """Main class to handle the running of a motorsport quiz game"""
    def __init__(self):
        """Initialize all attributes of the quiz using the pygame library"""
        pygame.init()

        # Set up game screen setting dimensions and window title.
        self.width, self.height = 800, 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Grand Prix Trivia")

        #Load the mixer
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

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
        self.STATE_MENU = "menu"
        self.STATE_PLAYING = "playing"
        self.STATE_SCORE = "score"
        self.state = self.STATE_MENU

        # Screens
        self.menu_screen_obj = Menu(self.screen, self.width, self.height, self.fonts, self.colors, self.start_quiz)
        self.quiz_screen_obj = None
        self.score_screen_obj = None

        self.questions = []  # Current category questions
        self.clock = pygame.time.Clock()

        self.max_questions = 20

        self.sounds = {
        "correct": pygame.mixer.Sound("assets/sounds/correct.wav"),
        "wrong": pygame.mixer.Sound("assets/sounds/wrong.wav"),
        "click": pygame.mixer.Sound("assets/sounds/click.wav"),
        "timer_tick": pygame.mixer.Sound("assets/sounds/tick.wav"),
        "game_over": pygame.mixer.Sound("assets/sounds/gameover.wav"),
        }

    def start_quiz(self, json_path):
        """Load questions from JSON, shuffle them, and start the quiz with up to 
        20 questions."""

        # Load questions for selected category
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                self.questions = json.load(f)
        except Exception as e:
            print(f"Error loading {json_path}: {e}")
            return

        # randomly shuffle the questions in the relevant Json file and only pick 
        # 20 questions per round
        random.shuffle(self.questions)
        self.questions = self.questions[:self.max_questions]
 
        # Create new quiz screen
        self.quiz_screen_obj = Quiz(
            self.screen,
            self.width,
            self.height,
            self.fonts,
            self.colors,
            self.questions,
            self.finish_quiz,
            self.sounds
        )

        self.state = self.STATE_PLAYING # set state to playing

    def finish_quiz(self, score):
        """Once quiz is completed output the users score and end the quiz"""
        self.score_screen_obj = ScoreScreen(
            self.screen,
            self.width,
            self.height,
            self.fonts,
            self.colors,
            score,
            len(self.questions),
            self.menu_back_to_menu
        )
        # change state to in score screen rather than playing
        self.state = self.STATE_SCORE 

    def menu_back_to_menu(self):
        """Return to the main menu"""
        self.state = self.STATE_MENU

    def run(self):
        """Main game loop to be running while state = playing"""
        running = True
        while running:
            for event in pygame.event.get():
                # End loop once a user chooses to quit
                if event.type == pygame.QUIT: 
                    running = False

            # Render the current screen based on state
            if self.state == self.STATE_MENU:
                self.menu_screen_obj.render()
            elif self.state == self.STATE_PLAYING and self.quiz_screen_obj:
                self.quiz_screen_obj.render()
            elif self.state == self.STATE_SCORE and self.score_screen_obj:
                self.score_screen_obj.render()

            pygame.display.flip()
            self.clock.tick(30)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    MotorSportQuiz().run()