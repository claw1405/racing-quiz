import pygame, sys

class Menu:
    """Main menu screen"""
    def __init__(self, screen, width, height, fonts, colors, start_action):
        """Initialize main menu attributes"""
        self.screen = screen
        self.width = width
        self.height = height
        self.font_title = fonts["title"]
        self.font_option = fonts["option"]
        self.colors = colors
        self.start_quiz_callback = start_action
        self.mouse_clicked = False  # Track click state

    def draw_text(self, text, font, color, x, y):
        """Render text to the screen"""
        text_obj = font.render(text, True, color)
        text_rect = text_obj.get_rect(center=(x, y))
        self.screen.blit(text_obj, text_rect)

    def draw_button(self, text, x, y, w, h, color, hover_color, action=None):
        """Draw menu buttons and listen for click events"""
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()[0]
        hovered = x + w > mouse[0] > x and y + h > mouse[1] > y

        pygame.draw.rect(self.screen, hover_color if hovered else color, 
                        (x, y, w, h), border_radius=10)

        if hovered and click and not self.mouse_clicked and action:
            action()
            self.mouse_clicked = True

        if not click:
            self.mouse_clicked = False

        self.draw_text(text, self.font_option, self.colors["WHITE"], 
                       x + w / 2, y + h / 2)

    def render(self, events=None):
        """Draw the menu screen"""
        self.screen.fill(self.colors["BLACK"])

        categories = [
            ("F1", "questions/f1.json"),
            ("Rally", "questions/rally.json"),
            ("MotoGP", "questions/moto.json"),
            ("Endurance", "questions/endurance.json")
        ]

        button_height = 60
        button_width = 200
        spacing = 20
        title_height = self.font_title.get_height()
        total_height = (title_height + spacing + len(categories) * 
                    (button_height + spacing) + button_height)
        start_y = (self.height - total_height) / 2

        # Draw Title text
        self.draw_text("Grand Prix Trivia", self.font_title, 
            self.colors["WHITE"], self.width / 2, start_y + title_height / 2)

        # Category buttons
        current_y = start_y + title_height + spacing
        for name, path in categories:
            self.draw_button(
                name,
                self.width / 2 - button_width / 2,
                current_y,
                button_width,
                button_height,
                self.colors["BLUE"],
                self.colors["GREEN"],
                lambda path=path: self.start_quiz_callback(path)
            )
            current_y += button_height + spacing

        # Quit button
        self.draw_button(
            "Quit",
            self.width / 2 - 100,
            current_y,
            200,
            button_height,
            self.colors["RED"],
            self.colors["GREY"],
            sys.exit
        )
