import pygame, sys

class Menu:
    """Main menu screen"""
    def __init__(self, screen, width, height, fonts, colors, start_action):
        self.screen = screen
        self.width = width
        self.height = height
        self.font_title = fonts["title"]
        self.font_option = fonts["option"]
        self.colors = colors
        self.start_quiz = start_action
        self.start_quiz_callback = start_action


        self.mouse_clicked = False # Flag to track mouse clicks

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

        if not click:
            self.mouse_clicked = False

        self.draw_text(text, self.font_option, self.colors["WHITE"], x + w / 2, y + h / 2)

    def render(self):
        self.screen.fill(self.colors["BLACK"])

        top_margin = 100  # space from top of screen
        spacing = 80      # vertical spacing between buttons
        button_height = 60

        # Draw title
        self.draw_text("Grand Prix Trivia", self.font_title, self.colors["WHITE"], self.width / 2, top_margin)

        # Category buttons
        categories = [
            ("F1", "questions/f1.json"),
            ("Rally", "questions/rally.json"),
            ("MotoGP", "questions/moto.json"),
            ("Endurance", "questions/endurance.json")
        ]
        for i, (name, path) in enumerate(categories):
            y = top_margin + 80 + i * spacing  # move buttons below title
            self.draw_button(
            name,
            self.width / 2 - 100,
            y,
            200,
            button_height,
            self.colors["BLUE"],
            self.colors["GREEN"],
            lambda path=path: self.start_quiz_callback(path)
        )

        # Quit button below last category
        quit_y = top_margin + 80 + len(categories) * spacing
        self.draw_button(
            "Quit",
            self.width / 2 - 100,
            quit_y,
            200,
            button_height,
            self.colors["RED"],
            self.colors["GREY"],
            sys.exit
        )

