import pygame
import numpy as np
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

        self.cached_surface = None
        self.last_cell_size = None
        self.needs_redraw = True
        self.buffer = pygame.Surface((width, height))
        self.color_map = {
            'DEEP_WATER': (0, 102, 204),
            'SHALLOW_WATER': (0, 128, 255),
            'SAND': (238, 214, 175),
            'PLAINS': (0, 153, 0),
            'HIGHLAND': (0, 102, 0),
            'MOUNTAIN': (128, 128, 128),
            'MOUNTAIN_PEAK': (255, 255, 255),
            'RIVER': (0, 114, 228),
            'DEFAULT': (255, 255, 255)
        }

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
        self.draw_terrain_map(map)
        print(self.clock.get_fps())

    def handle_input(self, map):
        self.redraw_needed = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    self.dragging = True
                    self.last_mouse_pos = event.pos
                elif event.button in  (4, 5):
                    mouse_x, mouse_y = event.pos
                    world_x = (mouse_x - self.map_offset_x) / self.cell_size
                    world_y = (mouse_y - self.map_offset_y) / self.cell_size
                    old_cell_size = self.cell_size
                    if event.button == 4:  # Mouse wheel up (zoom in)
                        self.cell_size = min(self.cell_size + 1, self.max_cell_size)
                    elif event.button == 5:  # Mouse wheel down (zoom out)
                        self.cell_size = max(self.cell_size - 1, self.min_cell_size)
                    if old_cell_size != self.cell_size:
                        self.redraw_needed = True
                        new_offset_x = mouse_x - (world_x * self.cell_size)
                        new_offset_y = mouse_y - (world_y * self.cell_size)
                        self.map_offset_x = self.adjust_offset_x(new_offset_x, map)
                        self.map_offset_y = self.adjust_offset_y(new_offset_y, map)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Left mouse button
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
        map_pixel_width = map.terrain_type_map.shape[1] * self.cell_size
        min_offset = min(0, (self.width - map_pixel_width)/2)
        return max(min(0, offset_x), min_offset)

    def adjust_offset_y(self, offset_y, map):
        map_pixel_height = map.terrain_type_map.shape[0] * self.cell_size
        min_offset = min(0, (self.height - map_pixel_height)/2)
        return max(min(0, offset_y), min_offset)

    def draw_terrain_map(self, map):
        terrain = map.terrain_type_map
        if terrain is None:
            return
        if (self.cached_surface is None or
            self.last_cell_size != self.cell_size or
            self.needs_redraw):
            map_width = terrain.shape[1] * self.cell_size
            map_height = terrain.shape[0] * self.cell_size
            self.cached_surface = pygame.Surface((map_width, map_height))
            colors = [
                self.color_map['DEEP_WATER'],
                self.color_map['SHALLOW_WATER'],
                self.color_map['SAND'],
                self.color_map['PLAINS'],
                self.color_map['HIGHLAND'],
                self.color_map['MOUNTAIN'],
                self.color_map['MOUNTAIN_PEAK'],
                self.color_map['RIVER'],
            ]
            CHUNK_SIZE = 1024
            for y_chunk in range(0, terrain.shape[0], CHUNK_SIZE):
                for x_chunk in range(0, terrain.shape[1], CHUNK_SIZE):
                    chunk_end_y = min(y_chunk + CHUNK_SIZE, terrain.shape[0])
                    chunk_end_x = min(x_chunk + CHUNK_SIZE, terrain.shape[1])
                    chunk_surface = pygame.Surface((
                        (chunk_end_x - x_chunk) * self.cell_size,
                        (chunk_end_y - y_chunk) * self.cell_size
                    ))
                    for i in range(y_chunk, chunk_end_y):
                        for j in range(x_chunk, chunk_end_x):
                            color = colors[terrain[i][j]]
                            if self.cell_size > 1:
                                pygame.draw.rect(
                                    chunk_surface,
                                    color,
                                    (
                                        (j - x_chunk) * self.cell_size,
                                        (i - y_chunk) * self.cell_size,
                                        self.cell_size,
                                        self.cell_size
                                    )
                                )
                            else:
                                chunk_surface.set_at(
                                    (j - x_chunk, i - y_chunk),
                                    color
                                )
                    self.cached_surface.blit(
                        chunk_surface,
                        (x_chunk * self.cell_size, y_chunk * self.cell_size)
                    )
            self.last_cell_size = self.cell_size
            self.needs_redraw = False
        map_width = map.terrain_type_map.shape[1] * self.cell_size
        map_height = map.terrain_type_map.shape[0] * self.cell_size
        visible_rect = pygame.Rect(
            -self.map_offset_x,
            -self.map_offset_y,
            map_width,
            map_height
        )
        self.buffer.fill(self.color_map['DEFAULT'])
        self.buffer.blit(self.cached_surface, (self.map_offset_x, self.map_offset_y), visible_rect)
        self.screen.blit(self.buffer, (0, 0))

    def update(self):
        pygame.display.flip()
        self.clock.tick(self.fps)