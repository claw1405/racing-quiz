import pygame

class Quiz:
    """This class will handle question displays, options and answer selection"""
    def __init__(self, screen, width, height, fonts, colors, questions, finish_callback):
        self.screen = screen
        self.width = width
        self.height = height
        self.fonts = fonts
        self.colors = colors
        self.questions = questions
        self.finish_callback = finish_callback
        self.current_question = 0
        self.score = 0
        self.click_released = True


    def draw_text(self, text, font, color, x, y):
        text_obj = font.render(text, True, color)
        text_rect = text_obj.get_rect(center=(x, y))
        self.screen.blit(text_obj, text_rect)

    def draw_button(self, text, x, y, w, h, color, hover_color, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()[0]

        hovered =  x + w > mouse[0] > x and y + h > mouse[1] > y
        current_colour = hover_color if hovered else color
        pygame.draw.rect(self.screen, current_colour, (x, y, w, h))

        if hovered and click and self.click_released:
            action()
            self.click_released = False

        # Reset the flag when the mouse button is released
        if not click:
            self.click_released = True

        self.draw_text(text, self.fonts["option"], self.colors["WHITE"], x + w / 2, y + h / 2)

    def handle_answer(self, selected):
        correct = self.questions[self.current_question]["answer"]
        if selected == correct:
            self.score += 1
        self.current_question += 1
        if self.current_question >= len(self.questions):
            self.finish_callback(self.score)

    def render(self):
        if self.current_question >= len(self.questions):
            return  # Nothing to render

        self.screen.fill(self.colors["BLACK"])
        q = self.questions[self.current_question]
        self.draw_text(q["question"], self.fonts["question"], self.colors["WHITE"], self.width / 2, 100)

        # Display current score at top-right corner
        score_text = f"Points: {self.score}/{len(self.questions)}"
        self.draw_text(score_text, self.fonts["option"], self.colors["GREEN"], self.width - 120, 30)

        for i, option in enumerate(q["options"]):
            self.draw_button(option, self.width / 2 - 150, 200 + i * 80, 300, 60, self.colors["BLUE"], self.colors["GREEN"], lambda i=i: self.handle_answer(i))