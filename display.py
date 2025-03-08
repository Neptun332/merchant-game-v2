import pygame

class Display:
    def __init__(self, width=800, height=600, title="Pygame Chart"):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 24)
        self.running = True
        self.fps = 60

    def draw_chart(self, price_history, num_cycles=100):
        self.screen.fill((255, 255, 255))  # Clear screen with white background

        # Limit the price history to the last `num_cycles` entries
        if len(price_history) > num_cycles:
            price_history = price_history[-num_cycles:]

        # Draw axes
        pygame.draw.line(self.screen, (0, 0, 0), (50, 50), (50, self.height - 50), 2)  # Y-axis
        pygame.draw.line(self.screen, (0, 0, 0), (50, self.height - 50), (self.width - 50, self.height - 50), 2)  # X-axis

        if len(price_history) > 1:
            max_price = max(price_history)
            min_price = min(price_history)
            price_range = max_price - min_price if max_price != min_price else 1

            # Draw Y-axis scale
            for i in range(5):
                y_value = min_price + (price_range / 4) * i
                y_pos = self.height - 50 - ((y_value - min_price) / price_range * (self.height - 100))
                text = self.font.render(f'{int(y_value)}', True, (0, 0, 0))
                self.screen.blit(text, (10, y_pos - 10))

            # Draw X-axis scale
            for i in range(len(price_history)):
                if i % (len(price_history) // 10 + 1) == 0:  # Adjust the scale frequency
                    x_pos = 50 + i * ((self.width - 100) / len(price_history))
                    text = self.font.render(f'{i + 1}', True, (0, 0, 0))
                    self.screen.blit(text, (x_pos - 10, self.height - 40))

            # Draw the price history
            for i in range(1, len(price_history)):
                x1 = 50 + (i - 1) * ((self.width - 100) / len(price_history))
                y1 = self.height - 50 - ((price_history[i - 1] - min_price) / price_range * (self.height - 100))
                x2 = 50 + i * ((self.width - 100) / len(price_history))
                y2 = self.height - 50 - ((price_history[i] - min_price) / price_range * (self.height - 100))
                pygame.draw.line(self.screen, (0, 0, 255), (x1, y1), (x2, y2), 2)

    def draw(self, price_history):
        self.draw_chart(price_history)

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit() 
        pygame.display.flip()
        self.clock.tick(self.fps)  # Limit to 60 frames per second

