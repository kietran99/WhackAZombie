import pygame
from config import *
from UI import bind

class App:
    def __init__(self):
        self.__window = self.__init_window()
        self.__delta_time = DELTA_TIME
        spawn = pygame.transform.scale(pygame.image.load("res/Zombie_Spawn.png"), (SPAWN_SIDE_LEN, SPAWN_SIDE_LEN))
        spawn_panel = pygame.transform.scale(pygame.image.load("res/Spawn_Panel.png"), (WINDOW_WIDTH, 440))

        self.__window.blit(spawn_panel, (0, 160))

        for row in range(N_ROWS):
            for col in range(N_COLS): 
                self.__window.blit(spawn, (SPAWN_PADDING_WIDTH + (SPAWN_PADDING_WIDTH + SPAWN_SIDE_LEN) * col, SPAWN_SIDE_LEN + SPAWN_SIDE_LEN * row))

        # pygame.draw.rect(self.__window, (255, 0, 0), (30, 160, 160, 160), 2)

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
                    print(pygame.mouse.get_pos())

            pygame.display.update()        

        pygame.quit()	

if __name__ == "__main__":
    App()