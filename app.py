import pygame
from config import *
from UI import bind

class Bound:
    def __init__(self, min: (int, int), max):
        self.min = min
        self.max = max

class App:
    def __init__(self):
        self.__window = self.__init_window()
        self.__delta_time = DELTA_TIME

        spawn = pygame.transform.scale(pygame.image.load("res/Zombie_Spawn.png"), (SPAWN_SIDE_LEN, SPAWN_SIDE_LEN))
        spawn_panel = pygame.transform.scale(pygame.image.load("res/Spawn_Panel.png"), (WINDOW_WIDTH, 440))
        self.__window.blit(spawn_panel, (0, 160))

        COLLIDER_OFFSET_X = 25
        COLLIDER_WIDTH = 110
        COLLIDER_HEIGHT = 130
        self.__spawn_bounds = []
        for row in range(N_ROWS):
            for col in range(N_COLS): 
                spawn_x, spawn_y = (SPAWN_PADDING_WIDTH + (SPAWN_PADDING_WIDTH + SPAWN_SIDE_LEN) * col, SPAWN_SIDE_LEN + SPAWN_SIDE_LEN * row)
                bound = Bound((spawn_x + COLLIDER_OFFSET_X, spawn_y), (spawn_x + COLLIDER_WIDTH + COLLIDER_OFFSET_X, spawn_y + COLLIDER_HEIGHT))
                self.__spawn_bounds.append(bound)
                self.__window.blit(spawn, (spawn_x, spawn_y))
                pygame.draw.rect(self.__window, (255, 255, 255), (bound.min[0], bound.min[1], COLLIDER_WIDTH, COLLIDER_HEIGHT), 2)

        self.__init_UI()
        self.__game_loop()

    def __init_window(self):
        pygame.init()
        pygame.display.set_caption("Whack-a-Zombie")
        return pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    def __init_UI(self):
        font = pygame.font.Font(FONT_PATH, FONT_SIZE)
        render_text = bind(self.__window, font)
        large_font = pygame.font.Font(FONT_PATH, LARGE_FONT_SIZE)
        render_large_text = bind(self.__window, large_font)
        score_color = (205, 233, 34)
        misses_color = (223, 53, 34)
        time_color = (255, 255, 255)
        render_text("SCORE", score_color, (540, PADDING_UI_TOP))
        render_text('0', score_color, (550, PADDING_UI_TOP * 2))
        render_text("MISSES", misses_color, (70, PADDING_UI_TOP))
        render_text('0', misses_color, (50, PADDING_UI_TOP * 2))
        render_large_text("TIME LEFT", time_color, (WINDOW_WIDTH // 2, PADDING_LARGE_UI_TOP))
        render_large_text("02:00", time_color, (WINDOW_WIDTH // 2, PADDING_LARGE_UI_TOP * 2.4))

    def __game_loop(self):
        isRunning = True

        while isRunning:
            pygame.time.delay(self.__delta_time)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    isRunning = False

                if (pygame.mouse.get_visible()):
                    mouse_pos = pygame.mouse.get_pos()
                    for bound in self.__spawn_bounds:
                        if mouse_pos[0] >= bound.min[0] and mouse_pos[0] <= bound.max[0] and \
                            mouse_pos[1] >= bound.min[1] and mouse_pos[1] <= bound.max[1]:
                            print("Hit zombie at: " + str(bound.min))
                            break

            pygame.display.update()        

        pygame.quit()	

if __name__ == "__main__":
    App()