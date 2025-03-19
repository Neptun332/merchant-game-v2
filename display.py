import pygame
from perlin_noise import generate_fractal_noise_2d
from resources import ResourceName

class Display:
    def __init__(self, width=1024, height=1024, title="Pygame Chart"):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 24)
        self.running = True
        self.fps = 60

        self.grid_rows = 3
        self.grid_cols = 3
        self.chart_padding = 10

        self.cell_size = 2
        self.min_cell_size = 2
        self.max_cell_size = 10
        self.map_offset_x = 0
        self.map_offset_y = 0
        self.dragging = False
        self.last_mouse_pos = None

    def draw_chart(self, price_history, grid_x=0, grid_y=0, num_cycles=1000, title=None):
        chart_width = (self.width - (self.chart_padding * (self.grid_cols + 1))) // self.grid_cols
        chart_height = (self.height - (self.chart_padding * (self.grid_rows + 1))) // self.grid_rows
        chart_x = self.chart_padding + grid_x * (chart_width + self.chart_padding)
        chart_y = self.chart_padding + grid_y * (chart_height + self.chart_padding)
        pygame.draw.rect(self.screen, (240, 240, 240),
                         (chart_x, chart_y, chart_width, chart_height))
        pygame.draw.rect(self.screen, (0, 0, 0),
                         (chart_x, chart_y, chart_width, chart_height), 1)
        if title:
            title_text = self.font.render(title, True, (0, 0, 0))
            self.screen.blit(title_text, (chart_x + 10, chart_y + 5))
            title_offset = 25
        else:
            title_offset = 5
        if len(price_history) > num_cycles:
            price_history = price_history[-num_cycles:]
        margin = 30
        chart_area_x = chart_x + margin
        chart_area_y = chart_y + title_offset
        chart_area_width = chart_width - (margin * 2)
        chart_area_height = chart_height - (margin + title_offset)
        pygame.draw.line(self.screen, (0, 0, 0),
                         (chart_area_x, chart_area_y),
                         (chart_area_x, chart_area_y + chart_area_height), 2)
        pygame.draw.line(self.screen, (0, 0, 0),
                         (chart_area_x, chart_area_y + chart_area_height),
                         (chart_area_x + chart_area_width, chart_area_y + chart_area_height), 2)
        if len(price_history) > 1:
            min_price = 0
            max_price = max(max(price_history), 1)
            price_range = max_price - min_price
            grid_color = (200, 200, 200)
            for i in range(4):
                y_value = min_price + (price_range / 3) * i
                y_pos = chart_area_y + chart_area_height - ((y_value - min_price) / price_range * chart_area_height)
                pygame.draw.line(self.screen, grid_color,
                                (chart_area_x, y_pos),
                                (chart_area_x + chart_area_width, y_pos), 1)
                text = self.font.render(f'{int(y_value)}', True, (0, 0, 0))
                self.screen.blit(text, (chart_area_x - 25, y_pos - 10))
            if len(price_history) > 10:
                step = max(1, len(price_history) // 5)
                for i in range(0, len(price_history), step):
                    x_pos = chart_area_x + i * (chart_area_width / len(price_history))
                    pygame.draw.line(self.screen, grid_color,
                                    (x_pos, chart_area_y),
                                    (x_pos, chart_area_y + chart_area_height), 1)
                    if i % (step * 2) == 0:
                        text = self.font.render(f'{i}', True, (0, 0, 0))
                        self.screen.blit(text, (x_pos - 10, chart_area_y + chart_area_height + 5))
            for i in range(1, len(price_history)):
                x1 = chart_area_x + (i - 1) * (chart_area_width / len(price_history))
                y1 = chart_area_y + chart_area_height - ((price_history[i - 1] - min_price) / price_range * chart_area_height)
                x2 = chart_area_x + i * (chart_area_width / len(price_history))
                y2 = chart_area_y + chart_area_height - ((price_history[i] - min_price) / price_range * chart_area_height)
                pygame.draw.line(self.screen, (0, 0, 255), (x1, y1), (x2, y2), 2)

    def draw(self, global_market, map):
        self.screen.fill((255, 255, 255))
        self.draw_terrain_map(map.terrain_map)

    def handle_input(self, map):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.dragging = True
                    self.last_mouse_pos = event.pos
                elif event.button == 4:
                    old_cell_size = self.cell_size
                    self.cell_size = min(self.cell_size + 1, self.max_cell_size)
                    if old_cell_size != self.cell_size:
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        self.map_offset_x = self.adjust_offset_x(self.map_offset_x - (mouse_x - self.map_offset_x) * 0.1, map)
                        self.map_offset_y = self.adjust_offset_y(self.map_offset_y - (mouse_y - self.map_offset_y) * 0.1, map)
                elif event.button == 5:
                    old_cell_size = self.cell_size
                    self.cell_size = max(self.cell_size - 1, self.min_cell_size)
                    if old_cell_size != self.cell_size:
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        self.map_offset_x = self.adjust_offset_x(self.map_offset_x + (mouse_x - self.map_offset_x) * 0.1, map)
                        self.map_offset_y = self.adjust_offset_y(self.map_offset_y + (mouse_y - self.map_offset_y) * 0.1, map)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.dragging = False
            elif event.type == pygame.MOUSEMOTION:
                if self.dragging:
                    new_pos = event.pos
                    dx = new_pos[0] - self.last_mouse_pos[0]
                    dy = new_pos[1] - self.last_mouse_pos[1]
                    self.map_offset_x = self.adjust_offset_x(self.map_offset_x + dx, map)
                    self.map_offset_y = self.adjust_offset_y(self.map_offset_y + dy, map)
                    self.last_mouse_pos = new_pos
        return True

    def adjust_offset_x(self, offset_x, map):
        map_pixel_width = map.terrain_map.shape[1] * self.cell_size
        min_offset = min(0, self.width - map_pixel_width)
        return max(min(0, offset_x), min_offset)

    def adjust_offset_y(self, offset_y, map):
        map_pixel_height = map.terrain_map.shape[0] * self.cell_size
        min_offset = min(0, self.height - map_pixel_height)
        return max(min(0, offset_y), min_offset)

    def draw_terrain_map(self, noise_map):
        if noise_map is None:
            return
        DEEP_WATER = (0, 0, 139)
        SHALLOW_WATER = (0, 191, 255)
        SAND = (238, 214, 175)
        PLAINS = (50, 238, 50)
        HIGHLAND = (34, 139, 34)
        MOUNTAIN = (128, 128, 128)
        DEFAULT = (255, 255, 255)
        height, width = noise_map.shape
        start_x = max(0, int(-self.map_offset_x / self.cell_size))
        start_y = max(0, int(-self.map_offset_y / self.cell_size))
        end_x = min(width, int((-self.map_offset_x + self.width) / self.cell_size + 1))
        end_y = min(height, int((-self.map_offset_y + self.height) / self.cell_size + 1))
        self.screen.fill(DEFAULT)
        for i in range(start_y, end_y):
            for j in range(start_x, end_x):
                value = noise_map[i][j]
                if -1.1 <= value < -0.5:
                    color = DEEP_WATER
                elif -0.5 <= value < 0:
                    color = SHALLOW_WATER
                elif 0 <= value < 0.1:
                    color = SAND
                elif 0.1 <= value < 0.5:
                    color = PLAINS
                elif 0.5 <= value < 0.7:
                    color = HIGHLAND
                elif 0.7 <= value <= 1.1:
                    color = MOUNTAIN
                else:
                    color = DEFAULT
                pygame.draw.rect(
                    self.screen,
                    color,
                    (self.map_offset_x + j * self.cell_size,
                     self.map_offset_y + i * self.cell_size,
                     self.cell_size,
                     self.cell_size)
                )

    def update(self):
        pygame.display.flip()
        self.clock.tick(self.fps)
