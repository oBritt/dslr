import pygame
from getdata import *
from utils import *
import time
from scipy.stats import pearsonr

class Scatter_plot:
    def __init__(self, width:int, height:int, inf:dict[str, dict[str, list[float]]], scat_inf:list[list]) -> None:
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
        self.scat_inf = scat_inf
        self.zoomed = 0
        self.zoomed_cords = [0, 1]
        self.solution = []

    def handle_event(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
    
    def handle_keys(self) -> None:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            self.running = False
        if time.time_ns() // 1_000_000 - self.last > 300:
            if (keys[pygame.K_RIGHT] and not self.zoomed):
                self.current += 1
                if (self.current == len(self.courses)):
                    self.current = 0
                self.last = time.time_ns() // 1_000_000
            elif (keys[pygame.K_LEFT] and not self.zoomed):
                self.current -= 1
                if (self.current == -1):
                    self.current = len(self.courses) - 1
                self.last = time.time_ns() // 1_000_000
            elif keys[pygame.K_KP_PLUS]:
                self.zoomed = 1
                self.last = time.time_ns() // 1_000_000
            elif keys[pygame.K_KP_MINUS]:
                self.zoomed = 0
                self.last = time.time_ns() // 1_000_000
            elif self.zoomed and keys[pygame.K_r]:
                self.zoomed_cords.reverse()
                self.last = time.time_ns() // 1_000_000
            elif (keys[pygame.K_s]):
                self.zoomed_cords[0] = self.solution[0]
                self.zoomed_cords[1] = self.solution[1]
                self.zoomed = 1
                self.last = time.time_ns() // 1_000_000
            elif (keys[pygame.K_RIGHT] and self.zoomed):
                self.increment_zoomed()
                self.last = time.time_ns() // 1_000_000
            elif (keys[pygame.K_LEFT] and self.zoomed):
                self.decrement_zoomed()
                self.last = time.time_ns() // 1_000_000

    def increment_zoomed(self)->None:
        self.zoomed_cords[1] += 1
        if (self.zoomed_cords[0] == self.zoomed_cords[1]):
            self.zoomed_cords[1] += 1
        if (self.zoomed_cords[1] == len(self.courses)):
            self.zoomed_cords[0] += 1
            if (self.zoomed_cords[0] == len(self.courses)):
                self.zoomed_cords[0] = 0
                self.zoomed_cords[1] = 1
            else:
                self.zoomed_cords[1] = 0
    
    def decrement_zoomed(self)->None:
        self.zoomed_cords[1] -= 1
        if (self.zoomed_cords[1] == self.zoomed_cords[0]):
            self.zoomed_cords[1] -= 1
        if (self.zoomed_cords[1] == -1):
            self.zoomed_cords[0] -= 1
            if (self.zoomed_cords[0] == -1):
                self.zoomed_cords[0] = len(self.courses) - 1
                self.zoomed_cords[1] = len(self.courses) - 2
            else:
                self.zoomed_cords[1] = len(self.courses) - 1

    def get_width_text(self, text:str, angle:int, font)->int:
        text_surface = font.render(text, True, (0, 0, 0))
        rotated_surface = pygame.transform.rotate(text_surface, angle)
        rotated_rect = rotated_surface.get_rect(center=(self.width // 2, self.height // 2))
        return rotated_rect.width
    
    def get_height_text(self, text:str, angle:int, font)->int:
        text_surface = font.render(text, True, (0, 0, 0))
        rotated_surface = pygame.transform.rotate(text_surface, angle)
        rotated_rect = rotated_surface.get_rect(center=(self.width // 2, self.height // 2))
        return rotated_rect.height

    def draw_text(self, text: str, position: tuple[int, int], angle: int, font) -> None:
        text_surface = font.render(text, True, (0, 0, 0))
        rotated_surface = pygame.transform.rotate(text_surface, angle)
        rotated_rect = rotated_surface.get_rect(center=position)
        self.screen.blit(rotated_surface, rotated_rect.topleft)

    def display_colors_houses(self, colors_dict:dict[str:tuple[int]])->None:
        distance = 40
        for key in colors_dict.keys():
            additon_distance = self.get_width_text(key, 0, self.font_cwords)
            pygame.draw.circle(self.screen, colors_dict[key], (distance, 35), 20)
            self.draw_text(key, (distance + additon_distance / 2 + 25, 35), 0, self.font_cwords)
            distance += additon_distance + 80

    def get_max_min(self, d:dict[str, list[float]]):
        mini = None
        maxi = None
        for key in d.keys():
            t_maxi = max(d[key])
            t_mini = min(d[key])
            if maxi == None or t_maxi > maxi:
                maxi = t_maxi
            if mini == None or t_mini < mini:
                mini = t_mini
        return maxi, mini
    
    def draw_x_axis(self, x:int, y:int, width:int, ranges:list[list[float]])->None:
        for i in range(4):
            self.draw_text(str("%.0f" % ranges[i * 4 + 4][0]), (x + width * (i * 4 + 4) / 20, y + 10), 0, self.font_numbers)
            pygame.draw.line(self.screen, (0, 0, 0), (x + width * (i * 4 + 4) / 20, y - 3), (x + width * (i * 4 + 4) / 20, y + 3))

    def draw_y_axis(self, x:int, y:int, height:int, ranges:list[list[float]])->None:
        for i in range(4):
            length = self.get_width_text(str("%.0f" % ranges[i * 4 + 4][0]), 0, self.font_numbers)
            self.draw_text(str("%.0f" % ranges[i * 4 + 4][0]), (x - length / 2 - 5, y - height * (4 + i * 4) / 20), 0, self.font_numbers)
            pygame.draw.line(self.screen, (0, 0, 0), (x - 3, y - height * (4 + i * 4) / 20), (x + 3, y - height * (4 + i * 4) / 20))

    def draw_dot(self, x:int, y:int, width:int, height:int, min_val_x:float, max_val_x:float, value_x:float, min_val_y:float,
                 max_val_y:float, value_y:float, color:tuple[int], radius:float)->None:
        x_pos = x + map_number(value_x, min_val_x, max_val_x, 0, width)
        y_pos = y - map_number(value_y, min_val_y, max_val_y, 0, height)
        pygame.draw.circle(self.screen, color, (x_pos, y_pos), radius)

    def display_scatter(self, x:int, y:int, width:int, height:int, compare_with:str, ind:int, colors_dict:dict[str:tuple[int]])->None:
        pygame.draw.rect(self.screen, (0, 0, 0), (x, y, width, height), 1)
        self.draw_text(compare_with, (x + width / 2, y + height + 50), 0, self.font_words)
        max_x, min_x = self.get_max_min(self.information[compare_with])
        ranges_x = split_range_scatter(min_x, max_x, 20)
        self.draw_x_axis(x, y + height, width, ranges_x)
        max_y, min_y = self.get_max_min(self.information[self.courses[self.current]])
        ranges_y = split_range_scatter(min_y, max_y, 20)
        self.draw_y_axis(x, y + height, height, ranges_y)
        min_val_x = ranges_x[0][0]
        max_val_x = ranges_x[19][1]
        max_val_y = ranges_y[19][1]
        min_val_y = ranges_y[0][0]
        for student in self.scat_inf:
            if student[ind + 1] != "" and student[self.current + 1] != "":
                self.draw_dot(x, y + height, width, height, min_val_x, max_val_x, float(student[ind + 1]), min_val_y, max_val_y, float(student[self.current + 1]), colors_dict[student[0]], 2)      

    def draw_y_axis_zoomed(self, x:int, y:int, height:int, ranges:list[list[float]])->None:
        pygame.draw.line(self.screen, (0, 0, 0), (x, y), (x, y - height - 40), 3)
        pygame.draw.polygon(self.screen, (0, 0, 0), [[x, y - height - 70], [x - 11, y - height - 15], [x, y - height - 40], [x + 11, y - height - 15]])
        for i in range(10):
            lenght = self.get_width_text(str("%.1f" % (ranges[len(ranges) // 10 * (i + 1) - 1][1])), 0, self.font_words)
            self.draw_text(str("%.1f" % (ranges[len(ranges) // 10 * (i + 1) - 1][1])), (x - 15 - lenght / 2, y - height * (i + 1) / 10), 0, self.font_words)     
            pygame.draw.line(self.screen, (0, 0, 0), (x - 10, y - height * (i + 1) / 10), (x + 10, y - height * (i + 1) / 10), 3)

    def draw_x_axis_zoomed(self, x:int, y:int, width:int, ranges:list[list[float]])->None:
        pygame.draw.line(self.screen, (0, 0, 0), (x, y), (x + width + 40, y), 3)
        pygame.draw.polygon(self.screen, (0, 0, 0), [[x + width + 70, y], [x + width + 15, y - 11], [x + width + 40, y], [x + width + 15, y + 11]])
        for i in range(10):
            self.draw_text(str("%.1f" % (ranges[len(ranges) // 10 * (i + 1) - 1][1])), (x + width * (i + 1) / 10, y + 35), 0, self.font_words)
            pygame.draw.line(self.screen, (0, 0, 0), (x + width * (i + 1) / 10, y - 10), (x + width * (i + 1) / 10, y + 10), 3)

    def display_scatter_zoomed(self, colors_dict:dict[str:tuple[int]])->None:
        width = 1500
        height = 750
        x = 220
        y = self.height - 130
        x_ind = self.zoomed_cords[1]
        y_ind = self.zoomed_cords[0]

        self.draw_text(self.courses[x_ind], (x + width / 2, y + 80), 0, self.font_cwords)
        self.draw_text(self.courses[y_ind], (50, y - height / 2), 90, self.font_cwords)
        max_x, min_x = self.get_max_min(self.information[self.courses[x_ind]])
        ranges_x = split_range_scatter(min_x, max_x, 20)
        self.draw_x_axis(x, y + height, width, ranges_x)
        max_y, min_y = self.get_max_min(self.information[self.courses[y_ind]])
        ranges_y = split_range_scatter(min_y, max_y, 20)

        min_val_x = ranges_x[0][0]
        max_val_x = ranges_x[19][1]
        max_val_y = ranges_y[19][1]
        min_val_y = ranges_y[0][0]

        self.draw_x_axis_zoomed(x, y, width, ranges_x)
        self.draw_y_axis_zoomed(x, y, height, ranges_y)

        for student in self.scat_inf:
            if student[x_ind + 1] != "" and student[y_ind + 1] != "":
                self.draw_dot(x, y, width, height, min_val_x, max_val_x, float(student[x_ind + 1]), min_val_y, max_val_y, float(student[y_ind + 1]), colors_dict[student[0]], 4)

    def display(self, colors_dict:dict[str:tuple[int]])->None:
        self.screen.fill("white")
        self.display_colors_houses(colors_dict)
        if (not self.zoomed):
            self.draw_text(self.courses[self.current], (self.width - self.get_width_text(self.courses[self.current], 0, self.font_cwords) / 2 - 30, 35), 0, self.font_cwords)
            counter = 0
            first = 1
            height_s = 250
            width_s  = 250
            distance = 55
            self.draw_text(self.courses[self.current], (30, height_s / 2 + 150), 90, self.font_words)
            self.draw_text(self.courses[self.current], (30, height_s * 3 / 2 + 300), 90, self.font_words)
            for ind, key in enumerate(self.information.keys()):
                if ind != self.current:
                    if (first):
                        self.display_scatter(distance * 2 + (width_s + distance) * counter, 150, width_s, height_s, key, ind, colors_dict)
                        counter += 1
                        if (len(self.courses) - 1) / 2 <= counter:
                            counter = 0
                            first = 0
                    else:
                        self.display_scatter(distance * 2 + (width_s + distance) * counter, 150 + height_s + 150, width_s, height_s, key, ind, colors_dict)
                        counter += 1
        else:
            self.display_scatter_zoomed(colors_dict)

    def print_most_similar(self)->None:
        ind1 = None
        ind2 = None
        coef = None
        for i in range(1, len(self.scat_inf[0]) - 1):
            for e in range(i + 1, len(self.scat_inf[0])):
                X = []
                Y = []
                for l in range(0, len(self.scat_inf)):
                    if self.scat_inf[l][i] != "" and self.scat_inf[l][e] != "":
                        X.append(float(self.scat_inf[l][i]))
                        Y.append(float(self.scat_inf[l][e]))
                corr_coefficient, p_value = pearsonr(X, Y)
                if coef == None or p_value < coef:
                    coef = p_value
                    ind1 = i - 1
                    ind2 = e - 1
        self.solution = [ind1, ind2]

    def run(self)->None:
        if (len(self.information) < 2):
            print("sorry there must be at least two features")
            return
        self.print_most_similar()
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
