from lib import pygame,np,time


class Game(object):
    def __init__(self,game_map:np.ndarray,init_player_pos: tuple,block_size:int,screen_size: tuple) -> None:
        self.game_map = game_map
        self.player_position = init_player_pos
        self.block_colors = {-1: (0, 0, 0), # None Block: black
                1: (255, 255, 0), # Yellow Block: yellow
                2: (210, 180, 140), # Tan Block: tan
                -2: (255, 255, 255), # White Block: white
                -3: (255, 192, 203)} # Pink Block: pink
        self.block_size = block_size
        self.screen_size = screen_size
        self.screen_bg_color = (128, 128, 128) # gray
        self.player_color = (0, 0, 255) # blue
    def update_game_map(self):
        block_value = self.game_map[self.player_position[0], self.player_position[1]]
        if block_value == 1:
            self.game_map[self.player_position[0], self.player_position[1]] = -1
        elif block_value == 2:
            self.game_map[self.player_position[0], self.player_position[1]] = 1
    def is_game_over(self):
        if (self.player_position[0] > 0 and self.game_map[self.player_position[0] - 1][self.player_position[1]] != -1) or \
       (self.player_position[0] < self.game_map.shape[0] - 1 and self.game_map[self.player_position[0] + 1][self.player_position[1]] != -1) or \
       (self.player_position[1] > 0 and self.game_map[self.player_position[0]][self.player_position[1] - 1] != -1) or \
       (self.player_position[1] < self.game_map.shape[1] - 1 and self.game_map[self.player_position[0]][self.player_position[1] + 1] != -1):
            return False
        return True
    def draw_game_map(self,screen):
        map_size = (self.game_map.shape[1] * self.block_size,
                self.game_map.shape[0] * self.block_size)
        map_position = ((self.screen_size[0] - map_size[0]) // 2,
                    (self.screen_size[1] - map_size[1]) // 2)
        for row in range(self.game_map.shape[0]):
            for col in range(self.game_map.shape[1]):
                block_value = self.game_map[row, col]
                block_color = self.block_colors[block_value]
                block_rect = (map_position[0] + col * self.block_size,
                          map_position[1] + row * self.block_size,
                          self.block_size,
                          self.block_size)
                pygame.draw.rect(screen, block_color, block_rect)
    def draw_player(self,screen):
        map_size = (self.game_map.shape[1] * self.block_size,
                self.game_map.shape[0] * self.block_size)
        map_position = ((self.screen_size[0] - map_size[0]) // 2,
                    (self.screen_size[1] - map_size[1]) // 2)
        player_rect = (map_position[0] + self.player_position[1] * self.block_size + self.block_size // 4,
                   map_position[1] + self.player_position[0] * self.block_size + self.block_size // 4,
                   self.block_size // 2,
                   self.block_size // 2)
        pygame.draw.ellipse(screen, self.player_color, player_rect)
    def game_loop(self):
        screen = pygame.display.set_mode(self.screen_size)
        self.running=True
        self.game_over = False
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if not self.game_over:
                        if event.key == pygame.K_UP:
                            if self.player_position[0] > 0 and self.game_map[self.player_position[0] - 1, self.player_position[1]]!=-1:
                                self.update_game_map()
                                self.player_position = (self.player_position[0] - 1, self.player_position[1])
                        elif event.key == pygame.K_DOWN:
                            if self.player_position[0] < self.game_map.shape[0] - 1 and self.game_map[self.player_position[0] + 1, self.player_position[1]]!=-1:
                                self.update_game_map()
                                self.player_position = (self.player_position[0] + 1, self.player_position[1])
                        elif event.key == pygame.K_LEFT:
                            if self.player_position[1] > 0 and self.game_map[self.player_position[0], self.player_position[1] - 1]!=-1:
                                self.update_game_map()
                                self.player_position = (self.player_position[0], self.player_position[1] - 1)
                        elif event.key == pygame.K_RIGHT:
                            if self.player_position[1] < self.game_map.shape[1] - 1 and self.game_map[self.player_position[0], self.player_position[1] + 1]!=-1:
                                self.update_game_map()
                                self.player_position = (self.player_position[0], self.player_position[1] + 1)
            self.game_over = self.is_game_over()
            screen.fill(self.screen_bg_color)
            self.draw_game_map(screen)
            self.draw_player(screen)
            pygame.display.flip()
    def geneticAlgorithmPlay(self,solution:list):
        screen = pygame.display.set_mode(self.screen_size)
        self.game_over = False
        for move in solution:
            if move == 'w':
              if self.player_position[0] > 0 and self.game_map[self.player_position[0] - 1, self.player_position[1]]!=-1:
                self.update_game_map()
                self.player_position = (self.player_position[0] - 1, self.player_position[1])
              else:
                  print('Nước đi này không thực hiện được')
                  break
            elif move == 'd':
              if self.player_position[1] < self.game_map.shape[1] - 1 and self.game_map[self.player_position[0], self.player_position[1] + 1]!=-1:
                self.update_game_map()
                self.player_position = (self.player_position[0], self.player_position[1] + 1)
              else:
                  print('Nước đi này không thực hiện được')
                  break
            elif move == 's':
              if self.player_position[0] < self.game_map.shape[0] - 1 and self.game_map[self.player_position[0] + 1, self.player_position[1]]!=-1:
                self.update_game_map()
                self.player_position = (self.player_position[0] + 1, self.player_position[1])
              else:
                  print('Nước đi này không thực hiện được')
                  break
            elif move == 'a':
              if self.player_position[1] > 0 and self.game_map[self.player_position[0], self.player_position[1] - 1]!=-1:
                self.update_game_map()
                self.player_position = (self.player_position[0], self.player_position[1] - 1)
              else:
                  print('Nước đi này không thực hiện được')
                  break
            self.game_over = self.is_game_over()
            screen.fill(self.screen_bg_color)
            self.draw_game_map(screen)
            self.draw_player(screen)
            pygame.display.flip()
            time.sleep(0.15)
        time.sleep(0.5)
        
