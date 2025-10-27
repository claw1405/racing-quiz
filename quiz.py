import pygame, time

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

        # Timer
        self.time_limit = 20
        self.start_time = time.time()

    def reset_timer(self):
        self.start_time = time.time()

    def get_time_left(self):
        elapsed = time.time() - self.start_time
        return max(0, self.time_limit - int(elapsed))

    def draw_text(self, text, font, color, x, y, max_width=None, line_spacing=5):
        """Draw text on screen at position (x, y). wraps text if max width is set"""
        if max_width is None:
            text_obj = font.render(text, True, color)
            text_rect = text_obj.get_rect(center=(x, y))
            self.screen.blit(text_obj, text_rect)
            return
        
        # Wrap text
        words = text.split(' ')
        lines = []
        current_line = ''
        for word in words:
            test_line = current_line + (' ' if current_line else '') + word
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word
        lines.append(current_line)

        # Draw each line centered at x
        total_height = len(lines) * font.get_height() + (len(lines) - 1) * line_spacing
        start_y = y - total_height / 2
        for i, line in enumerate(lines):
            text_obj = font.render(line, True, color)
            text_rect = text_obj.get_rect(center=(x, start_y + i * (font.get_height() + line_spacing)))
            self.screen.blit(text_obj, text_rect)

    def draw_button(self, text, x, y, w, h, color, hover_color, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()[0]

        hovered = x + w > mouse[0] > x and y + h > mouse[1] > y
        current_colour = hover_color if hovered else color
        pygame.draw.rect(self.screen, current_colour, (x, y, w, h))

        if hovered and click and self.click_released:
            action()
            self.click_released = False

        if not click:
            self.click_released = True

        font = self.fonts["option"]
        text_width = font.size(text)[0]
        while text_width > w - 10 and font.get_height() > 10:
            font = pygame.font.Font(None, font.get_height() - 1)
            text_width = font.size(text)[0]

        self.draw_text(text, font, self.colors["WHITE"], x + w / 2, y + h / 2)


    def handle_answer(self, selected):
        correct = self.questions[self.current_question]["answer"]
        if selected == correct:
            self.score += 1
        self.current_question += 1

        if self.current_question >= len(self.questions):
            self.finish_callback(self.score)
        else :
            self.reset_timer()

    def render(self):
        if self.current_question >= len(self.questions):
            return  # Nothing to render
    
       # --- Timer logic ---
        time_left = self.get_time_left()
        if time_left <= 0:
            # Time's up — move to next question
            self.current_question += 1
            if self.current_question >= len(self.questions):
                self.finish_callback(self.score)
                return
            else:
                self.reset_timer()  # reset timer only for the next question
                time_left = self.time_limit

        # --- Draw UI ---
        self.screen.fill(self.colors["BLACK"])
        q = self.questions[self.current_question]

        # Question text
        self.draw_text(
            q["question"],
            self.fonts["question"],
            self.colors["WHITE"],
            self.width / 2,
            100,
            max_width=600
        )

        # Timer display — big, centered at the top
        timer_color = self.colors["GREEN"]
        if time_left <= 10:
            timer_color = (255, 215, 0)  # Yellow when under 10s
        if time_left <= 5:
            timer_color = self.colors["RED"]  # Red when under 5s

        timer_text = f"Time Left: {time_left}s"
        padding = 20  # distance from screen edges
        self.draw_text(timer_text, self.fonts["title"], timer_color, padding + self.fonts["title"].size(timer_text)[0]/2, padding + self.fonts["title"].get_height()/2)


        # Score display (top left)
        score_text = f"Points: {self.score}/{len(self.questions)}"
        self.draw_text(score_text, self.fonts["option"], self.colors["GREEN"], self.width - 120, 30)

        # Answer buttons
        for i, option in enumerate(q["options"]):
            self.draw_button(
                option,
                self.width / 2 - 150,
                200 + i * 80,
                300,
                60,
                self.colors["BLUE"],
                self.colors["GREEN"],
                lambda i=i: self.handle_answer(i)
            )