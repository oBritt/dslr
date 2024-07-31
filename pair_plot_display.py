import pygame
from utils import *

class Pair_plot:
    def __init__(self, inf:dict[str, dict[str, list[float]]], scat_inf:list[list]) -> None:
        pygame.init()
        self.information = inf
        self.running = True
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption('scatter_plot')
        self.font_words = pygame.font.SysFont('Arial', 20)
        self.font_cwords = pygame.font.SysFont('Arial', 50)
        self.font_numbers = pygame.font.SysFont('Arial', 10)
        self.courses = [key for key in self.information.keys()]
        self.current = 0
        self.last = 0
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()
        self.scat_inf = scat_inf

    def handle_event(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
    
    def handle_keys(self) -> None:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            self.running = False

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
        distance = 100
        for key in colors_dict.keys():
            additon_distance = self.get_height_text(key, 90, self.font_cwords)
            pygame.draw.circle(self.screen, colors_dict[key], (self.width - 80, distance), 30)
            self.draw_text(key, (self.width - 80, distance + additon_distance / 2 + 50), 90, self.font_cwords)
            distance += additon_distance + 120

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
    
    def draw_x_axis_s(self, x:int, y:int, width:int, ranges:list[list[float]])->None:
        for i in range(4):
            self.draw_text(str("%.0f" % ranges[i * 4 + 4][0]), (x + width * (i * 4 + 4) / 20, y + 10), 0, self.font_numbers)
            pygame.draw.line(self.screen, (0, 0, 0), (x + width * (i * 4 + 4) / 20, y - 3), (x + width * (i * 4 + 4) / 20, y + 3))

    def draw_y_axis_s(self, x:int, y:int, height:int, ranges:list[list[float]])->None:
        for i in range(4):
            length = self.get_width_text(str("%.0f" % ranges[i * 4 + 4][0]), 0, self.font_numbers)
            self.draw_text(str("%.0f" % ranges[i * 4 + 4][0]), (x - length / 2 - 5, y - height * (4 + i * 4) / 20), 0, self.font_numbers)
            pygame.draw.line(self.screen, (0, 0, 0), (x - 3, y - height * (4 + i * 4) / 20), (x + 3, y - height * (4 + i * 4) / 20))

    def draw_dot(self, x:int, y:int, width:int, height:int, min_val_x:float, max_val_x:float, value_x:float, min_val_y:float,
                 max_val_y:float, value_y:float, color:tuple[int])->None:
        x_pos = x + map_number(value_x, min_val_x, max_val_x, 0, width)
        y_pos = y - map_number(value_y, min_val_y, max_val_y, 0, height)
        pygame.draw.circle(self.screen, color, (x_pos, y_pos), 1)

    def display_scatter(self, x:int, y:int, width:int, height:int, ind_horizontal:int, ind_vertical:int, colors_dict:dict[str:tuple[int]])->None:
        pygame.draw.rect(self.screen, (0, 0, 0), (x, y, width, height), 1)
        max_x, min_x = self.get_max_min(self.information[self.courses[ind_horizontal]])
        ranges_x = split_range_scatter(min_x, max_x, 20)
        self.draw_x_axis_s(x, y + height, width, ranges_x)
        max_y, min_y = self.get_max_min(self.information[self.courses[ind_vertical]])
        ranges_y = split_range_scatter(min_y, max_y, 20)
        self.draw_y_axis_s(x, y + height, height, ranges_y)
        min_val_x = ranges_x[0][0]
        max_val_x = ranges_x[19][1]
        max_val_y = ranges_y[19][1]
        min_val_y = ranges_y[0][0]
        for student in self.scat_inf:
            if student[ind_horizontal + 1] != "" and student[ind_vertical + 1] != "":
                self.draw_dot(x, y + height, width, height, min_val_x, max_val_x, float(student[ind_horizontal + 1]), min_val_y, max_val_y, float(student[ind_vertical + 1]), colors_dict[student[0]])

    def display_names(self, width:int, height:int, distance:int, distance_v:int)->None:
        for y, e in enumerate(self.courses):
            self.draw_text(e, (20 * (y % 3 + 1) , (height + distance) * y + 7 + height / 2), 90, self.font_words)
            self.draw_text(e, ((width + distance_v) * y + width / 2 + distance_v * 2, self.screen.get_height() - 15 * (y % 2) - 12), 0, self.font_words)
   
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

    def draw_y_axis(self, x:int, y:int, height:int, max_value:int)-> None:
        step = max_value / 5
        for i in range(5):
            self.draw_text(str("%.0f" % max_value), (x - len(str("%.0f" % max_value)) * 3 - 5, y + height * i / 5), 0, self.font_numbers)
            pygame.draw.line(self.screen, (0, 0, 0), (x - 3 ,y + height * i / 5), (x + 3 ,y + height * i / 5), 1)
            max_value -= step
    
    def draw_x_axis(self, x:int, y:int, width:int, ranges:list[list[float]])->None:
        for i in range(4):
            ind = 4 + i * 4
            self.draw_text(str("%.0f" % ranges[ind][0]), (x + width * ind / 20, y + 10), 0, self.font_numbers)
            pygame.draw.line(self.screen, (0, 0, 0), (x + width * ind / 20, y - 3), (x + width * ind / 20, y + 3), 1)

    def draw_colomn(self, x:int, y:int, width:int, height:int, color:tuple[int])->None:
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        surface.fill((*color, 200))
        self.screen.blit(surface, (x, y - height + 1))
        # pygame.draw.line(self.screen, color, (x, y), (x + 10, y), 2)

    def draw_information(self, x:int, y:int, width:int, height:int, max_num:int, data:dict[str, list[int]], colors_dict:dict[str, tuple[int]])->None:
        for key in data.keys():
            for i in range(len(data[key])):
                self.draw_colomn(x + width * i / len(data[key]) , y + height, width / len(data[key]), height / max_num * data[key][i], colors_dict[key])

    def display_histogram(self, x:int, y:int, width:int, height:int, data:dict[str, list[float]], name:str, colors_dict:dict[str, tuple[int]])->None:
        pygame.draw.polygon(self.screen, (0, 0, 0), [[x, y], [x + width, y], [x + width, y + height], [x, y + height]], 1)
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

    def display(self, colors_dict:dict[str:tuple[int]])->None:
        self.screen.fill("white")
        self.display_colors_houses(colors_dict)
        width = 120
        height = 90
        distance = 17
        distance_v = 60
        self.display_names(width, height, distance, distance_v)
        for i in range(len(self.courses)):
            for e in range(len(self.courses)):
                if i != e:
                    self.display_scatter((distance_v + width) * i + distance_v * 2, (distance + height) * e + 5, width, height, i, e, colors_dict)
                else:
                    self.display_histogram((distance_v + width) * i + distance_v * 2, (distance + height) * e + 5, width, height, self.information[self.courses[i]], self.courses[i], colors_dict)

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
