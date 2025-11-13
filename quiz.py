import pygame, time, random

class Quiz:
    """Handles question displays, answer selection, timer, feedback, and facts."""
    def __init__(self, screen, width, height, fonts, colors, questions, finish_callback, sounds, menu_callback):
        self.screen = screen
        self.width = width
        self.height = height
        self.fonts = fonts
        self.colors = colors
        self.finish_callback = finish_callback
        self.menu_callback = menu_callback
        self.current_question = 0
        self.score = 0
        self.click_released = True
        self.sounds = sounds

        # Sound channels
        pygame.mixer.set_num_channels(8)
        self.feedback_channel = pygame.mixer.Channel(0)
        self.timer_channel = pygame.mixer.Channel(1)
        self.click_channel = pygame.mixer.Channel(2)

        # Randomize or trim questions
        self.questions = random.sample(questions, min(20, len(questions)))

        # Timer setup
        self.time_limit = 20
        self.start_time = time.time()
        self.last_time_displayed = self.time_limit

        # Feedback setup
        self.feedback = None
        self.feedback_time = 0
        self.last_feedback_fact = None

        # Option buttons
        self.option_rects = []

        # Menu button
        self.menu_button_rect = pygame.Rect(20, self.height - 80, 100, 50)

        self.ignore_mouse_until_released = True

    def reset_timer(self):
        self.start_time = time.time()
        self.last_time_displayed = self.time_limit

    def get_time_left(self):
        elapsed = time.time() - self.start_time
        return max(0, self.time_limit - int(elapsed))

    def draw_text(self, text, font, color, x, y, max_width=None, line_spacing=5):
        if not text:
            return
        if max_width is None:
            text_obj = font.render(text, True, color)
            text_rect = text_obj.get_rect(center=(x, y))
            self.screen.blit(text_obj, text_rect)
            return

        # Wrap text to fit within width
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

        total_height = len(lines) * font.get_height() + (len(lines)-1)*line_spacing
        start_y = y - total_height / 2
        for i, line in enumerate(lines):
            text_obj = font.render(line, True, color)
            text_rect = text_obj.get_rect(center=(x, start_y + i*(font.get_height()+line_spacing)))
            self.screen.blit(text_obj, text_rect)

    def draw_button(self, text, x, y, w, h, color, hover_color, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()[0]

         # Ignore clicks carried over from previous screen
        if self.ignore_mouse_until_released:
            if not click:
                self.ignore_mouse_until_released = False
            return

        hovered = x < mouse[0] < x + w and y < mouse[1] < y + h
        current_color = hover_color if hovered else color
        pygame.draw.rect(self.screen, current_color, (x, y, w, h))

        if hovered and click and self.click_released and not self.feedback and action:
            self.click_channel.play(self.sounds["click"])
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
        q = self.questions[self.current_question]
        correct_index = q["answer"]
        correct_text = q["options"][correct_index]

        if selected == correct_index:
            self.score += 1
            self.feedback = ("Correct!", self.colors["GREEN"])
            self.feedback_channel.play(self.sounds["correct"])
        else:
            self.feedback = ("Incorrect!", self.colors["RED"])
            self.feedback_channel.play(self.sounds["wrong"])

        # Include fact if available
        self.last_feedback_fact = q.get("fact", f"Correct answer: {correct_text}")
        self.feedback_time = time.time()

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                # Menu button click
                if self.menu_button_rect.collidepoint(mouse_pos):
                    if self.timer_channel.get_busy():
                        self.timer_channel.stop()
                    self.menu_callback()
                    return

                # Option buttons
                for i, rect in enumerate(self.option_rects):
                    if rect.collidepoint(mouse_pos):
                        self.handle_answer(i)

    def render(self, events=None):
        if self.current_question >= len(self.questions):
            return

        # --- Feedback screen ---
        if self.feedback:
            if time.time() - self.feedback_time < 3.0:
                if self.timer_channel.get_busy():
                    self.timer_channel.stop()
                self.screen.fill(self.colors["BLACK"])
                text, color = self.feedback
                self.draw_text(text, self.fonts["question"], color,
                               self.width / 2, self.height / 2 - 50)
                if self.last_feedback_fact:
                    self.draw_text(self.last_feedback_fact, self.fonts["option"], 
                                   self.colors["YELLOW"], self.width / 2, self.height / 2 + 60, max_width=700)
                pygame.display.flip()
                return
            else:
                self.feedback = None
                self.last_feedback_fact = None
                self.current_question += 1
                if self.current_question >= len(self.questions):
                    if self.timer_channel.get_busy():
                        self.timer_channel.stop()
                    self.finish_callback(self.score)
                    return
                else:
                    self.reset_timer()

        q = self.questions[self.current_question]

        # --- Timer ---
        time_left = self.get_time_left()
        if time_left != self.last_time_displayed:
            self.last_time_displayed = time_left
            if "timer_tick" in self.sounds and not self.feedback:
                if not self.timer_channel.get_busy():
                    self.timer_channel.play(self.sounds["timer_tick"])

        if time_left <= 0 and not self.feedback:
            correct_index = q["answer"]
            correct_text = q["options"][correct_index]
            self.feedback = ("Time's up!", self.colors["RED"])
            self.last_feedback_fact = q.get("fact", f"Correct answer: {correct_text}")
            self.feedback_time = time.time()
            return

        # --- Main quiz display ---
        self.screen.fill(self.colors["BLACK"])

        # Question
        self.draw_text(q["question"], self.fonts["question"], self.colors["YELLOW"],
                       self.width / 2, 100, max_width=700)

        # Timer
        timer_color = self.colors["GREEN"]
        if time_left <= 10:
            timer_color = (255, 215, 0)
        if time_left <= 5:
            timer_color = self.colors["RED"]

        timer_text = f"Time Left: {time_left}s"
        self.draw_text(timer_text, self.fonts["option"], timer_color, 100, 30)

        # Score
        score_text = f"Score: {self.score}/{len(self.questions)}"
        self.draw_text(score_text, self.fonts["option"], self.colors["GREEN"],
                       self.width - 130, 30)

        # Options
        self.option_rects = []
        for i, option in enumerate(q["options"]):
            rect = pygame.Rect(self.width / 2 - 150, 220 + i * 80, 300, 60)
            self.option_rects.append(rect)
            self.draw_button(option, rect.x, rect.y, rect.width, rect.height,
                             self.colors["BLUE"], self.colors["GREEN"],
                             lambda i=i: self.handle_answer(i))

        # Menu button
        pygame.draw.rect(self.screen, self.colors["RED"], self.menu_button_rect)
        self.draw_text("Menu", self.fonts["option"], self.colors["WHITE"],
                       self.menu_button_rect.centerx, self.menu_button_rect.centery)

        if not pygame.mouse.get_pressed()[0]:
            self.click_released = True
