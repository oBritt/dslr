import pygame
from getdata import *
from utils import *
import math

class Histogramm:
    def __init__(self, width: int, height: int, data:dict[str, dict[str, list[float]]]) -> None:
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption('Histogramm')
        self.running = True
        self.information = data
        self.all_values = []
        self.mean = 0
        self.std = 0
        self.distance = 66
        self.font_words = pygame.font.SysFont('Arial', 30)
        self.font_numbers = pygame.font.SysFont('Arial', 12)

    def handle_event(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
    
    def handle_keys(self) -> None:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            self.running = False

    def get_by_range(self, data:dict[str, list[float]], splited:list[list[float]])->dict[str, list[int]]:
        out = {}
        for key in data.keys():
            out[key] = [0 for _ in range(len(splited))]

        for key in data.keys():
            range_n = 0
            for e in data[key]:
                while len(splited) > range_n and e > splited[range_n][1]:
                    range_n += 1
                if (len(splited) > range_n):
                    out[key][range_n] += 1
                else:
                    out[key][range_n - 1] += 1
        return out
    
    def display_colors_and_courses(self, colors_dict:dict[str: tuple[int]])->None:
        distance = 100
        y = 50
        for key in colors_dict.keys():
            # pygame.draw.rect(self.screen, colors_dict[key], (distance, 30, 40, 40))
            pygame.draw.circle(self.screen, colors_dict[key], (distance + 20, y), 20)
            width = self.get_width_text(key, self.font_words)
            self.draw_text(key, (distance + width,y), 0, self.font_words)
            distance += width 
            distance += width 

    
    def get_width_text(self, text:str, font)->int:
        text_surface = font.render(text, True, (0, 0, 0))
        text_width, text_height = text_surface.get_size()
        return text_width
    
    def draw_text(self, text: str, position: tuple[int, int], angle: int, font) -> None:
        text_surface = font.render(text, True, (0, 0, 0))
        rotated_surface = pygame.transform.rotate(text_surface, angle)
        rotated_rect = rotated_surface.get_rect(center=position)
        self.screen.blit(rotated_surface, rotated_rect.topleft)

    def draw_y_axis(self, x:int, y:int, height:int, max_value:int)-> None:
        step = max_value / 10
        for i in range(10):
            self.draw_text(str("%.0f" % max_value), (x - len(str("%.0f" % max_value)) * 3 - 5, y + height * i / 10), 0, self.font_numbers)
            pygame.draw.line(self.screen, (0, 0, 0), (x - 3 ,y + height * i / 10), (x + 3 ,y + height * i / 10), 1)
            max_value -= step
    
    def draw_x_axis(self, x:int, y:int, width:int, ranges:list[list[float]])->None:
        for i in range(4):
            ind = 4 + i * 4
            self.draw_text(str("%.0f" % ranges[ind][0]), (x + width * ind / 20, y + 10), 0, self.font_numbers)
            pygame.draw.line(self.screen, (0, 0, 0), (x + width * ind / 20, y - 3), (x + width * ind / 20, y + 3), 1)

    def get_width_height(self, amount:int):
        amount //= 2
        width = (self.width - 100 + self.distance) / amount - self.distance
        width = width // 20 * 20
        if width > 200:
            width = 200
        return width, width * 2
    
    def draw_colomn(self, x:int, y:int, width:int, height:int, color:tuple[int])->None:
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        surface.fill((*color, 128))
        self.screen.blit(surface, (x, y - height + 1))
        # pygame.draw.line(self.screen, color, (x, y), (x + 10, y), 2)

    def draw_information(self, x:int, y:int, width:int, height:int, max_num:int, data:dict[str, list[int]], colors_dict:dict[str, tuple[int]])->None:
        for key in data.keys():
            for i in range(len(data[key])):
                self.draw_colomn(x + width * i / len(data[key]) , y + height, width / len(data[key]), height / max_num * data[key][i], colors_dict[key])

    def display_histogram(self, x:int, y:int, width:int, height:int, data:dict[str, list[float]], name:str, colors_dict:dict[str, tuple[int]])->None:
        pygame.draw.polygon(self.screen, (0, 0, 0), [[x, y], [x + width, y], [x + width, y + height], [x, y + height]], 1)
        self.draw_text(name, (x  + width / 2, y - 20), 0, self.font_words)
        all_numbers = []
        for key in data.keys():
            all_numbers += data[key]
        all_numbers = sorted(all_numbers)
        # can use max and min potentially for improve perfomance
        ranges = split_range(all_numbers[0], all_numbers[len(all_numbers) -1], 20)
        get_by_range = self.get_by_range(data, ranges)
        all_ranges = []
        for key in get_by_range.keys():
            all_ranges += get_by_range[key]
        max_numb = max(all_ranges)
        self.draw_y_axis(x, y, height, (max_numb // 10 + 2) * 10)
        self.draw_x_axis(x, y + height, width, ranges)
        self.draw_information(x, y, width, height, (max_numb // 10 + 2) * 10, get_by_range, colors_dict)

    def display(self) -> None:
        self.screen.fill("white")
        amount:int = len(list(self.information.keys()))
        width_h, height_h = self.get_width_height(amount)
        counter = 0
        second = 0
        colors = generate_colors()
        all_houses = set()
        for key in self.information.keys():
            all_houses |= set(self.information[key].keys())
        colors_dict:dict[str: tuple[int]] = {key: next(colors) for key in all_houses}
        self.display_colors_and_courses(colors_dict)

        for key in self.information.keys():
            if not second:
                self.display_histogram(self.distance + (self.distance + width_h) * counter, 150, width_h, height_h, self.information[key], key, colors_dict)
                counter += 1
                if counter >= amount / 2:
                    counter = 0
                    second = 1 
            else:
                self.display_histogram(self.distance + (self.distance + width_h) * counter, 150 + height_h + 100, width_h, height_h, self.information[key], key, colors_dict)
                counter += 1

    def run(self) -> None:
        clock = pygame.time.Clock()
        while self.running:
            self.handle_event()
            self.handle_keys()
            self.display()
            pygame.display.flip() 
            clock.tick(60) 

        pygame.quit() 

# # pygame setup
# pygame.init()
# screen = pygame.display.set_mode((1280, 720))
# clock = pygame.time.Clock()
# running = True
# dt = 0

# player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

# while running:
#     # poll for events
#     # pygame.QUIT event means the user clicked X to close your window
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False

#     # fill the screen with a color to wipe away anything from last frame
#     screen.fill("purple")

#     pygame.draw.circle(screen, "red", player_pos, 40)

#     keys = pygame.key.get_pressed()
#     if keys[pygame.K_w]:
#         player_pos.y -= 300 * dt
#     if keys[pygame.K_s]:
#         player_pos.y += 300 * dt
#     if keys[pygame.K_a]:
#         player_pos.x -= 300 * dt
#     if keys[pygame.K_d]:
#         player_pos.x += 300 * dt

#     # flip() the display to put your work on screen
#     pygame.display.flip()

#     # limits FPS to 60
#     # dt is delta time in seconds since last frame, used for framerate-
#     # independent physics.
#     dt = clock.tick(60) / 1000

# pygame.quit()