import pygame
from getdata import *
from utils import *
import time

class Scatter_plot:
    def __init__(self, width:int, height:int, inf:dict[str, dict[str, list[float]]]) -> None:
        pygame.init()
        self.width = width
        self.height = height
        self.information = inf
        self.running = True
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption('scatter_plot')
        self.font_words = pygame.font.SysFont('Arial', 30)
        self.font_cwords = pygame.font.SysFont('Arial', 50)
        self.font_numbers = pygame.font.SysFont('Arial', 12)
        self.courses = [key for key in self.information.keys()]
        self.current = 0
        self.last = 0

    def handle_event(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
    
    def handle_keys(self) -> None:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            self.running = False
        if time.time_ns() // 1_000_000 - self.last > 300:
            if (keys[pygame.K_RIGHT] and self.current < len(self.courses) - 1):
                self.current += 1
                self.last = time.time_ns() // 1_000_000
            elif (keys[pygame.K_LEFT] and self.current >= 1):
                self.current -= 1
                self.last = time.time_ns() // 1_000_000

    def get_width_text(self, text:str, angle:int, font)->int:
        text_surface = font.render(text, True, (0, 0, 0))
        rotated_surface = pygame.transform.rotate(text_surface, angle)
        rotated_rect = rotated_surface.get_rect(center=(self.width // 2, self.height // 2))
        return rotated_rect.width

    def draw_text(self, text: str, position: tuple[int, int], angle: int, font) -> None:
        text_surface = font.render(text, True, (0, 0, 0))
        rotated_surface = pygame.transform.rotate(text_surface, angle)
        rotated_rect = rotated_surface.get_rect(center=position)
        self.screen.blit(rotated_surface, rotated_rect.topleft)

    def display_colors_houses(self, colors_dict:dict[str:tuple[int]])->None:
        distance = 40
        for key in colors_dict.keys():
            additon_distance = self.get_width_text(key, 0, self.font_words)
            pygame.draw.circle(self.screen, colors_dict[key], (distance, 35), 20)
            self.draw_text(key, (distance + additon_distance / 2 + 25, 35), 0, self.font_words)
            distance += additon_distance + 70

    def display_scatter(self, x:int, y:int, width:int, height:int, compare_with:str, colors_dict:dict[str:tuple[int]])->None:
        pygame.draw.rect(self.screen, (0, 0, 0), (x, y, width, height), 1)
        # len_text = self.get_width_text(compare_with, 0, self.font_words)
        self.draw_text(compare_with, (x + width / 2, y + height + 50), 0, self.font_words)

    def display(self, colors_dict:dict[str:tuple[int]])->None:
        self.screen.fill("white")
        self.draw_text(self.courses[self.current], (self.width - self.get_width_text(self.courses[self.current], 0, self.font_cwords) / 2 - 30, 35), 0, self.font_cwords)
        self.display_colors_houses(colors_dict)
        counter = 0
        first = 1
        height_s = 250
        width_s  = 250
        distance = 55
        for ind, key in enumerate(self.information.keys()):
            if ind != self.current:
                if (first):
                    self.display_scatter(distance * 2 + (width_s + distance) * counter, 150, width_s, height_s, key, colors_dict)
                    counter += 1
                    if (len(self.courses) - 1) / 2 <= counter:
                        counter = 0
                        first = 0
                else:
                    self.display_scatter(distance * 2 + (width_s + distance) * counter, 150 + height_s + 150, width_s, height_s, key, colors_dict)
                    counter += 1

    def run(self)->None:
        if (len(self.information) < 2):
            print("sorry there must be at least two features")
            return
        clock = pygame.time.Clock()
        colors = generate_colors()
        all_houses = set()
        for key in self.information.keys():
            all_houses |= set(self.information[key].keys())
        colors_dict:dict[str: tuple[int]] = {key: next(colors) for key in all_houses}
        while (self.running):
            self.handle_event()
            self.handle_keys()
            self.display(colors_dict)
            pygame.display.flip() 
            clock.tick(60) 
        pygame.quit() 
