import pygame

from resources import ResourceName

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
        
        # Grid configuration
        self.grid_rows = 2
        self.grid_cols = 2
        self.chart_padding = 10

    def draw_chart(self, price_history, grid_x=0, grid_y=0, num_cycles=100, title=None):
        """
        Draw a chart at the specified grid position.
        
        Args:
            price_history: List of price values to plot
            grid_x: X position in the grid (0-based)
            grid_y: Y position in the grid (0-based)
            num_cycles: Number of cycles to display
            title: Optional title for the chart
        """
        # Calculate chart dimensions based on grid position
        chart_width = (self.width - (self.chart_padding * (self.grid_cols + 1))) // self.grid_cols
        chart_height = (self.height - (self.chart_padding * (self.grid_rows + 1))) // self.grid_rows
        
        # Calculate chart position
        chart_x = self.chart_padding + grid_x * (chart_width + self.chart_padding)
        chart_y = self.chart_padding + grid_y * (chart_height + self.chart_padding)
        
        # Draw chart background
        pygame.draw.rect(self.screen, (240, 240, 240), 
                         (chart_x, chart_y, chart_width, chart_height))
        
        # Draw chart border
        pygame.draw.rect(self.screen, (0, 0, 0), 
                         (chart_x, chart_y, chart_width, chart_height), 1)
        
        # Draw title if provided
        if title:
            title_text = self.font.render(title, True, (0, 0, 0))
            self.screen.blit(title_text, (chart_x + 10, chart_y + 5))
            title_offset = 25  # Space for the title
        else:
            title_offset = 5
            
        # Limit the price history to the last `num_cycles` entries
        if len(price_history) > num_cycles:
            price_history = price_history[-num_cycles:]

        # Define chart area within the grid cell
        margin = 30
        chart_area_x = chart_x + margin
        chart_area_y = chart_y + title_offset
        chart_area_width = chart_width - (margin * 2)
        chart_area_height = chart_height - (margin + title_offset)
        
        # Draw axes
        pygame.draw.line(self.screen, (0, 0, 0), 
                         (chart_area_x, chart_area_y), 
                         (chart_area_x, chart_area_y + chart_area_height), 2)  # Y-axis
        pygame.draw.line(self.screen, (0, 0, 0), 
                         (chart_area_x, chart_area_y + chart_area_height), 
                         (chart_area_x + chart_area_width, chart_area_y + chart_area_height), 2)  # X-axis

        if len(price_history) > 1:
            max_price = max(price_history)
            min_price = min(price_history)
            price_range = max_price - min_price if max_price != min_price else 1

            # Draw Y-axis scale (3 values: min, middle, max)
            for i in range(3):
                y_value = min_price + (price_range / 2) * i
                y_pos = chart_area_y + chart_area_height - ((y_value - min_price) / price_range * chart_area_height)
                text = self.font.render(f'{int(y_value)}', True, (0, 0, 0))
                self.screen.blit(text, (chart_area_x - 25, y_pos - 10))

            # Draw the price history
            for i in range(1, len(price_history)):
                x1 = chart_area_x + (i - 1) * (chart_area_width / len(price_history))
                y1 = chart_area_y + chart_area_height - ((price_history[i - 1] - min_price) / price_range * chart_area_height)
                x2 = chart_area_x + i * (chart_area_width / len(price_history))
                y2 = chart_area_y + chart_area_height - ((price_history[i] - min_price) / price_range * chart_area_height)
                pygame.draw.line(self.screen, (0, 0, 255), (x1, y1), (x2, y2), 2)

    def draw(self, global_market):
        """Draw multiple charts in a grid layout."""
        self.screen.fill((255, 255, 255))  # Clear screen with white background
        
        # Draw Iron price history in top-left (0,0)
        self.draw_chart(
            global_market.price_history[ResourceName.Iron], 
            grid_x=0, 
            grid_y=0, 
            title=f"Iron Price (Current: {int(global_market.current_price[ResourceName.Iron])})"
        )
        
        # Draw Iron consumption in top-right (1,0)
        if hasattr(global_market, 'consumption_history') and ResourceName.Iron in global_market.consumption_history:
            self.draw_chart(
                global_market.consumption_history[ResourceName.Iron], 
                grid_x=1, 
                grid_y=0, 
                title=f"Iron Consumption (Current: {global_market.total_consumed[ResourceName.Iron]})"
            )
        
        # Draw Iron production in bottom-left (0,1)
        if hasattr(global_market, 'production_history') and ResourceName.Iron in global_market.production_history:
            self.draw_chart(
                global_market.production_history[ResourceName.Iron], 
                grid_x=0, 
                grid_y=1, 
                title=f"Iron Production (Current: {global_market.total_produced[ResourceName.Iron]})"
            )
        
        # Draw net change in bottom-right (1,1)
        if hasattr(global_market, 'net_change_history') and ResourceName.Iron in global_market.net_change_history:
            net_change = global_market.total_produced.get(ResourceName.Iron, 0) - global_market.total_consumed.get(ResourceName.Iron, 0)
            self.draw_chart(
                global_market.net_change_history[ResourceName.Iron], 
                grid_x=1, 
                grid_y=1, 
                title=f"Net Change (Current: {net_change})"
            )

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit() 
        pygame.display.flip()
        self.clock.tick(self.fps)  # Limit to 60 frames per second

