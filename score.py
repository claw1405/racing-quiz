import pygame, sys

class ScoreScreen:
    """Score display screen"""
    def __init__(self, screen, width, height, fonts, colors, score, total_questions, restart_action):
        self.screen = screen
        self.width = width
        self.height = height
        self.fonts = fonts
        self.colors = colors
        self.score = score
        self.total_questions = total_questions
        self.restart_action = restart_action
        self.mouse_clicked = False

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

        self.draw_text(text, self.fonts["option"], self.colors["WHITE"], x + w / 2, y + h / 2)

    def render(self):
        self.screen.fill(self.colors["BLACK"])
        self.draw_text("Quiz Complete!", self.fonts["title"], self.colors["WHITE"], self.width / 2, self.height / 3)
        self.draw_text(f"Score: {self.score}/{self.total_questions}", self.fonts["question"], self.colors["GREEN"], self.width / 2, self.height / 2)
        self.draw_button("Play Again", self.width / 2 - 100, self.height / 2 + 100, 200, 60, self.colors["BLUE"], self.colors["GREEN"], self.restart_action)
        self.draw_button("Quit", self.width / 2 - 100, self.height / 2 + 180, 200, 60, self.colors["RED"], self.colors["GREY"], sys.exit)