import sys, pygame
from time import sleep

class MotorSportQuiz :
    """This will be the main class for my motorsport quiz app"""
    def __init__(self):
        """Initiate the games assets and resources"""
        pygame.init() # Instantiate pygame
        pygame.mixer.init() #Initiate the mixer controls for game sounds

        self.clock = pygame.time.Clock()

        # Set the boolean flags with starting states
        self.lights_out = False
        self.box_box = True
        self.game_muted = False
    

