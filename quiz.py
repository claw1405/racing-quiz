import pygame, time, random

class Quiz:
    """Handles question displays, answer selection, timer, and feedback."""
    def __init__(self, screen, width, height, fonts, colors, questions, finish_callback, sounds):
        """Initialize quiz attributes"""
        self.screen = screen
        self.width = width
        self.height = height
        self.fonts = fonts
        self.colors = colors
        self.finish_callback = finish_callback
        self.current_question = 0
        self.score = 0
        self.click_released = True
        self.sounds = sounds

        # Limit to 20 random questions
        if len(questions) > 20:
            self.questions = random.sample(questions, 20)
        else:
            self.questions = questions

        # Setup Timer
        self.time_limit = 20
        self.start_time = time.time()
        self.last_time_displayed = self.time_limit

        # Feedback screen setup to give user real time feedback on the 
        # correctness of their answer.
        self.feedback = None  # tuple (text, color)
        self.feedback_time = 0

    def reset_timer(self):
        """Reset the question timer"""
        self.start_time = time.time()
        self.last_time_displayed = self.time_limit


    def get_time_left(self):
        """Calculate how much time the user has to answer the question"""
        elapsed = time.time() - self.start_time
        return max(0, self.time_limit - int(elapsed))

    def draw_text(self, text, font, color, x, y, max_width=None, line_spacing=5):
        """Draw text at (x, y). Wraps if max_width set."""
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

        # Draw each line centered
        total_height = len(lines) * font.get_height() + (len(lines) - 1) * line_spacing
        start_y = y - total_height / 2
        for i, line in enumerate(lines):
            text_obj = font.render(line, True, color)
            text_rect = text_obj.get_rect(center=(x, start_y + i * (font.get_height() + line_spacing)))
            self.screen.blit(text_obj, text_rect)

    def draw_button(self, text, x, y, w, h, color, hover_color, action=None):
        """Draw each option button and listen for any click events"""
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()[0]

        hovered = x + w > mouse[0] > x and y + h > mouse[1] > y
        current_colour = hover_color if hovered else color
        pygame.draw.rect(self.screen, current_colour, (x, y, w, h))

        # Listen for click events
        if hovered and click and self.click_released:
            pygame.mixer.Sound.play(self.sounds["click"])
            action()
            self.click_released = False

        if not click:
            self.click_released = True

        # Setup option buttons
        font = self.fonts["option"]
        text_width = font.size(text)[0]
        while text_width > w - 10 and font.get_height() > 10:
            font = pygame.font.Font(None, font.get_height() - 1)
            text_width = font.size(text)[0]

        self.draw_text(text, font, self.colors["WHITE"], x + w / 2, y + h / 2)

    def handle_answer(self, selected):
        """A method to check the correctness of an answer"""
        correct_index = self.questions[self.current_question]["answer"]
        correct_text = self.questions[self.current_question]["options"][correct_index]

        # If answer is correct output correct text else output incorrect and the
        #correct answer.
        if selected == correct_index:
            self.score += 1
            self.feedback = ("Correct!", self.colors["GREEN"])
            pygame.mixer.Sound.play(self.sounds["correct"])

        else:
            self.feedback = (f"Incorrect! Correct: {correct_text}", self.colors["RED"])
            pygame.mixer.Sound.play(self.sounds["wrong"])
        
        self.feedback_time = time.time() 

    def render(self):
        """Render feedback screen for 0.7 seconds and draw all other elements to 
        the screen"""
        # --- Feedback display ---
        if self.feedback:
            if time.time() - self.feedback_time < 0.5:
                self.screen.fill(self.colors["BLACK"])
                text, color = self.feedback
                self.draw_text(text, self.fonts["question"], color, 
                               self.width / 2, self.height / 2)
                pygame.display.flip()
                return
            else:
                self.feedback = None
                self.current_question += 1
                if self.current_question >= len(self.questions):
                    self.finish_callback(self.score)
                    return
                else:
                    self.reset_timer()

        if self.current_question >= len(self.questions):
            return  # Nothing to render

        # --- Timer logic ---
        time_left = self.get_time_left()

        # Only play tick sound if the second changed
        if time_left != self.last_time_displayed:
            self.last_time_displayed = time_left
            if "timer_tick" in self.sounds:
                self.sounds["timer_tick"].play()

        # Time's up — move to next question only once
        if time_left <= 0:
            self.feedback = (f"Time's up! Correct: {q['options'][q['answer']]}", self.colors["RED"])
            self.feedback_time = time.time()
            return  # Show feedback for this question before advancing


        # --- Draw UI ---
        self.screen.fill(self.colors["BLACK"])
        q = self.questions[self.current_question]

        # Question
        self.draw_text(q["question"], self.fonts["question"], 
                       self.colors["WHITE"], self.width / 2, 100, max_width=600)

        # Timer display (top left)
        timer_color = self.colors["GREEN"] # Green timer
        if time_left <= 10:
            timer_color = (255, 215, 0)  # Yellow once half the time is gone
        if time_left <= 5:
            timer_color = self.colors["RED"]  # Red when user only has 5 secs left
        padding = 20
        timer_text = f"Time Left: {time_left}s"
        self.draw_text(timer_text, self.fonts["option"], timer_color,
                       padding + self.fonts["option"].size(timer_text)[0]/2,
                       padding + self.fonts["option"].get_height()/2)

        # Score display (top right)
        score_text = f"Points: {self.score}/{len(self.questions)}"
        self.draw_text(score_text, self.fonts["option"], self.colors["GREEN"],
                        self.width - 120, 30)

        # Answer buttons
        for i, option in enumerate(q["options"]):
            self.draw_button(option, self.width / 2 - 150, 200 + i * 80, 300, 60,
                             self.colors["BLUE"], self.colors["GREEN"], 
                             lambda i=i: self.handle_answer(i))
