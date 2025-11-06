# Imports required by the main MotorSport quiz class
import pygame, sys, random, json
from main_menu import Menu
from quiz import Quiz
from score import ScoreScreen
from settings import Settings

class MotorSportQuiz:
    """Main class to handle the running of a motorsport quiz game"""
    def __init__(self):
        """Initialize all attributes of the quiz using the pygame library"""
        pygame.init() # Start pygame
        self.settings = Settings() # New instance of the settings class

        #Load the mixer for game sound effects
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

        # Set up game screen setting dimensions and window title.
        self.windowed_mode()
        pygame.display.set_caption("Grand Prix Trivia")

        # States
        self.STATE_MENU = "menu"
        self.STATE_PLAYING = "playing"
        self.STATE_SCORE = "score"
        self.state = self.STATE_MENU

        # Screens
        self.menu_screen_obj = Menu(self.screen, self.settings.screen_width, 
                            self.settings.screen_height,self.fonts, self.colors, 
                            self.start_quiz)
        self.quiz_screen_obj = None
        self.score_screen_obj = None

        self.questions = []  # Current category questions
        self.clock = pygame.time.Clock()

        self.max_questions = 20 # Only show 20 questions per game

        # Dictionary to store sound effects
        self.sounds = {
        "correct": pygame.mixer.Sound("assets/sounds/correct.wav"),
        "wrong": pygame.mixer.Sound("assets/sounds/wrong.wav"),
        "click": pygame.mixer.Sound("assets/sounds/click.wav"),
        "timer_tick": pygame.mixer.Sound("assets/sounds/tick.wav"),
        "game_over": pygame.mixer.Sound("assets/sounds/gameover.wav"),
        }

        # Set the timer tick volume to 2%
        self.sounds["timer_tick"].set_volume(0.02)

    # --- Display Modes ---
    def make_fullscreen(self):
        """Switch to fullscreen mode."""
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height

        #Rebuild menu as per new resolution
        self.menu_screen_obj = Menu(
            self.screen,
            self.settings.screen_width,
            self.settings.screen_height,
            self.fonts,
            self.colors,
            self.start_quiz
        )

    def windowed_mode(self):
        """Switch to windowed mode."""
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )

        #Rebuild menu as per new resolution
        self.menu_screen_obj = Menu(
            self.screen,
            self.settings.screen_width,
            self.settings.screen_height,
            self.fonts,
            self.colors,
            self.start_quiz
        )
    
    def _quit(self):
        """Exit the program"""
        sys.exit()

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

        # A slice of 20 questions
        self.questions = self.questions[:self.max_questions] 
 
        # Create new quiz screen
        self.quiz_screen_obj = Quiz(
            self.screen,
            self.settings.screen_width,
            self.settings.screen_height,
            self.fonts,
            self.colors,
            self.questions,
            self.finish_quiz,
            self.sounds
        )

        self.state = self.STATE_PLAYING # set state to playing

    def _check_keydown_events(self, event):
        """Handle keyboard shortcuts for convenience."""
        if event.key == pygame.K_q:  # Quit
            self._quit()

        elif event.key == pygame.K_f:  # Fullscreen toggle
            if self.screen.get_flags() & pygame.FULLSCREEN:
                self.windowed_mode()
            else:
                self.make_fullscreen()

        elif event.key == pygame.K_m:  # Mute / Unmute
            self.settings.muted = not getattr(self.settings, "muted", False)
            volume = 0 if self.settings.muted else 1
            for sound in self.sounds.values():
                sound.set_volume(volume)
            print("Muted" if self.settings.muted else "Unmuted")

        elif event.key == pygame.K_ESCAPE:  # Return to menu
            self.menu_back_to_menu()

    def run(self):
        """Main game loop"""
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    self._check_keydown_events(event)

            # Render based on current state
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

    def finish_quiz(self, score):
        """Once quiz is completed output the users score and end the quiz"""
        self.score_screen_obj = ScoreScreen(
            self.screen,
            self.settings.screen_width,
            self.settings.screen_height,
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

if __name__ == "__main__":
    game = MotorSportQuiz()
    game.run()