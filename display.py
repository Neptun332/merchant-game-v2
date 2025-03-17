import pygame

from perlin_noise import generate_fractal_noise_2d
from resources import ResourceName

class Display:
    def __init__(self, width=1400, height=1000, title="Pygame Chart"):
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
        self.grid_rows = 3
        self.grid_cols = 3
        self.chart_padding = 10

    def draw_chart(self, price_history, grid_x=0, grid_y=0, num_cycles=1000, title=None):
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
            # Always start from 0 for the y-axis
            min_price = 0
            max_price = max(max(price_history), 1)  # Ensure max is at least 1 to avoid division by zero
            price_range = max_price - min_price

            # Draw grid lines
            grid_color = (200, 200, 200)  # Light gray
            
            # Horizontal grid lines
            for i in range(4):
                y_value = min_price + (price_range / 3) * i
                y_pos = chart_area_y + chart_area_height - ((y_value - min_price) / price_range * chart_area_height)
                # Draw horizontal grid line
                pygame.draw.line(self.screen, grid_color, 
                                (chart_area_x, y_pos), 
                                (chart_area_x + chart_area_width, y_pos), 1)
                # Draw y-axis label
                text = self.font.render(f'{int(y_value)}', True, (0, 0, 0))
                self.screen.blit(text, (chart_area_x - 25, y_pos - 10))
            
            # Vertical grid lines (every 10 data points)
            if len(price_history) > 10:
                step = max(1, len(price_history) // 5)
                for i in range(0, len(price_history), step):
                    x_pos = chart_area_x + i * (chart_area_width / len(price_history))
                    # Draw vertical grid line
                    pygame.draw.line(self.screen, grid_color, 
                                    (x_pos, chart_area_y), 
                                    (x_pos, chart_area_y + chart_area_height), 1)
                    # Draw x-axis label for every other grid line to avoid crowding
                    if i % (step * 2) == 0:
                        text = self.font.render(f'{i}', True, (0, 0, 0))
                        self.screen.blit(text, (x_pos - 10, chart_area_y + chart_area_height + 5))

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
            title=f"Global Iron Price (Current: {int(global_market.current_price[ResourceName.Iron])})"
        )
        # Draw net change in bottom-right (1,1)
        if hasattr(global_market, 'amount_history') and ResourceName.Iron in global_market.amount_history:
            self.draw_chart(
                global_market.amount_history[ResourceName.Iron], 
                grid_x=1, 
                grid_y=0, 
                title=f"Iron in the market (Current: {global_market.total_amount[ResourceName.Iron]})"
            )

        if hasattr(global_market, 'base_prices_history') and ResourceName.Iron in global_market.base_prices_history:
            self.draw_chart(
                global_market.base_prices_history[ResourceName.Iron], 
                grid_x=2, 
                grid_y=0, 
                title=f"Iron base prices (Current: {global_market.base_prices[ResourceName.Iron]})"
            )

        # if hasattr(global_market, 'market_share'):
        #     self.draw_chart(
        #         list(global_market.market_share.values()), 
        #         grid_x=0, 
        #         grid_y=1, 
        #         title=f"Market share (Current: {global_market.market_share.values()})"
        #     )

        # if hasattr(global_market, 'total_amount'):
        #     self.draw_chart(
        #         list(global_market.total_amount.values()), 
        #         grid_x=1, 
        #         grid_y=1, 
        #         title=f"Number of resources (Current: {global_market.total_amount.values()})"
        #    )

        # Draw local market prices for each city
        city_index = 0
        for city in global_market.cities.values():
            if city_index < 3:  # Only show first two cities to avoid overcrowding
                self.draw_chart(
                    city.local_market.price_history[ResourceName.Iron],
                    grid_x=city_index,
                    grid_y=1,
                    title=f"{city.name} Local Iron Price (Current: {int(city.local_market.current_price[ResourceName.Iron])})"
                )
                city_index += 1

        city_index = 0
        for city in global_market.cities.values():
            if city_index < 3:  # Only show first two cities to avoid overcrowding
                self.draw_chart(
                    city.local_market.amount_history[ResourceName.Iron],
                    grid_x=city_index,
                    grid_y=2,
                    title=f"{city.name} Amount of Iron (Current: {int(city.local_market.resources[ResourceName.Iron].amount)})"
                )
                city_index += 1

        self.draw_terrain_map(generate_fractal_noise_2d((512, 512), (4, 4), 6))

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit() 
        pygame.display.flip()
        self.clock.tick(self.fps)  # Limit to 60 frames per second

    def draw_terrain_map(self, noise_map, x=0, y=0):
        """
        Draw terrain map based on perlin noise values.
        
        Args:
            noise_map: 2D numpy array of noise values between -1 and 1
            x: Starting x position for drawing
            y: Starting y position for drawing
        """
        if noise_map is None:
            return

        # Define terrain colors
        DEEP_WATER = (0, 0, 139)      # Deep blue
        SHALLOW_WATER = (0, 191, 255)  # Light blue
        SAND = (238, 214, 175)         # Sandy yellow
        PLAINS = (144, 238, 144)       # Light green
        HIGHLAND = (34, 139, 34)       # Green
        MOUNTAIN = (128, 128, 128)     # Grey

        cell_size = 1  # Size of each terrain cell in pixels
        
        height, width = noise_map.shape
        
        for i in range(height):
            for j in range(width):
                value = noise_map[i][j]
                color = DEEP_WATER  # Default color
                
                if value < -0.5:
                    color = DEEP_WATER
                elif value < 0:
                    color = SHALLOW_WATER
                elif value < 0.3:
                    color = SAND
                elif value < 0.5:
                    color = PLAINS
                elif value < 0.7:
                    color = HIGHLAND
                elif value < 0.7:
                    color = MOUNTAIN
                
                pygame.draw.rect(
                    self.screen,
                    color,
                    (x + j * cell_size, y + i * cell_size, cell_size, cell_size)
                )

