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
        pygame.init()
        self.settings = Settings()

        # Load mixer for sound effects
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
            "GREY": (180, 180, 180),
            "YELLOW": (255, 210, 0)
        }

        # Set up game screen
        self.windowed_mode()
        pygame.display.set_caption("Grand Prix Trivia")

        # States
        self.STATE_MENU = "menu"
        self.STATE_PLAYING = "playing"
        self.STATE_SCORE = "score"
        self.state = self.STATE_MENU

        # Initialise Screens
        self.menu_screen_obj = Menu(
        self.screen, self.settings.screen_width, self.settings.screen_height,
        self.fonts, self.colors, self.start_quiz
        )
        self.quiz_screen_obj = None
        self.score_screen_obj = None

        # Create questions list
        self.questions = []
        self.clock = pygame.time.Clock()
        self.max_questions = 20

        # Sound Effects
        self.sounds = {
            "correct": pygame.mixer.Sound("assets/sounds/correct.wav"),
            "wrong": pygame.mixer.Sound("assets/sounds/wrong.wav"),
            "click": pygame.mixer.Sound("assets/sounds/click.wav"),
            "timer_tick": pygame.mixer.Sound("assets/sounds/tick.wav"),
            "game_over": pygame.mixer.Sound("assets/sounds/gameover.wav"),
        }

        # Adjust base volumes
        self.sounds["timer_tick"].set_volume(0.02)
        self.base_volumes = {k: s.get_volume() for k, s in self.sounds.items()}

        # Add muted flag
        self.settings.muted = False

    # --- Display Modes ---
    def make_fullscreen(self):
        """Switch to fullscreen mode."""
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height

        # Rebuild menu as per new resolution
        self.menu_screen_obj = Menu(
        self.screen, self.settings.screen_width,
        self.settings.screen_height, self.fonts,
        self.colors, self.start_quiz
        )

    def windowed_mode(self):
        """Switch to windowed mode."""
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )
        self.menu_screen_obj = Menu(
        self.screen, self.settings.screen_width,
        self.settings.screen_height, self.fonts,
        self.colors, self.start_quiz
        )

    # --- Core Game Flow ---
    def _quit(self):
        """Exit the program"""
        pygame.quit()
        sys.exit()

    def start_quiz(self, json_path):
        """Load questions from JSON, shuffle them, and start the quiz."""
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                self.questions = json.load(f)
        except Exception as e:
            print(f"Error loading {json_path}: {e}")
            return

        # Randomize the question order and add a slice of 20 questions.
        random.shuffle(self.questions)
        self.questions = self.questions[:self.max_questions]

        self.quiz_screen_obj = Quiz(
        self.screen, self.settings.screen_width, self.settings.screen_height,
        self.fonts, self.colors, self.questions, self.finish_quiz, self.sounds,
        self.menu_back_to_menu
        )
        self.state = self.STATE_PLAYING

    def finish_quiz(self, score):
        """Once quiz is completed, show score screen."""
        self.score_screen_obj = ScoreScreen(
        self.screen, self.settings.screen_width,
        self.settings.screen_height, self.fonts,
        self.colors, score, len(self.questions),
        self.menu_back_to_menu, self.questions
        )
        self.state = self.STATE_SCORE

    def menu_back_to_menu(self):
        """Return to the main menu"""
        # Stop any sounds that are still playing
        if self.quiz_screen_obj and hasattr(self.quiz_screen_obj, 'sounds'):
            if 'timer_tick' in self.quiz_screen_obj.sounds:
                self.quiz_screen_obj.sounds['timer_tick'].stop()

        self.quiz_screen_obj = None
        self.score_screen_obj = None
        self.state = self.STATE_MENU

    # --- Key Shortcuts ---
    def _check_keydown_events(self, event):
        """Handle keyboard shortcuts."""
        if event.key == pygame.K_q:
            self._quit()
        elif event.key == pygame.K_f:
            if self.screen.get_flags() & pygame.FULLSCREEN:
                self.windowed_mode()
            else:
                self.make_fullscreen()
        elif event.key == pygame.K_m:
            self.settings.muted = not self.settings.muted
            for name, sound in self.sounds.items():
                sound.set_volume(0 if self.settings.muted 
                        else self.base_volumes[name])
        elif event.key == pygame.K_ESCAPE:
            self.menu_back_to_menu()

    def run(self):
        """Main game loop"""
        running = True
        while running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    self._check_keydown_events(event)

            # Render based on current state
            if self.state == self.STATE_MENU:
                self.menu_screen_obj.render(events)
            elif self.state == self.STATE_PLAYING and self.quiz_screen_obj:
                self.quiz_screen_obj.render(events)
            elif self.state == self.STATE_SCORE and self.score_screen_obj:
                self.score_screen_obj.render(events)

            # Optional shortcut hints
            hint_font = self.fonts["option"]
            hint_text = "F: Fullscreen | M: Mute | ESC: Menu | Q: Quit"
            hint_surface = hint_font.render(hint_text, True, self.colors["GREY"])
            self.screen.blit(hint_surface, (10, self.settings.screen_height - 30))

            pygame.display.flip()
            self.clock.tick(30)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = MotorSportQuiz()
    game.run()
