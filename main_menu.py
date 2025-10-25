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

    def draw_text(self, text, font, color, x, y):
        text_obj = font.render(text, True, color)
        text_rect = text_obj.get_rect(center=(x, y))
        self.screen.blit(text_obj, text_rect)

    def draw_button(self, text, x, y, w, h, color, hover_color, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x + w > mouse[0] > x and y + h > mouse[1] > y:
            pygame.draw.rect(self.screen, hover_color, (x, y, w, h))
            if click[0] == 1 and action is not None:
                pygame.time.wait(200)
                action()
        else:
            pygame.draw.rect(self.screen, color, (x, y, w, h))
        self.draw_text(text, self.font_option, self.colors["WHITE"], x + w / 2, y + h / 2)

    def render(self):
        self.screen.fill(self.colors["BLACK"])
        self.draw_text("🏁 Grand Prix Trivia 🏁", self.font_title, self.colors["WHITE"], self.width / 2, self.height / 3)
        self.draw_button("Start Quiz", self.width / 2 - 100, self.height / 2, 200, 60, self.colors["BLUE"], self.colors["GREEN"], self.start_quiz)
        self.draw_button("Quit", self.width / 2 - 100, self.height / 2 + 80, 200, 60, self.colors["RED"], self.colors["GREY"], sys.exit)