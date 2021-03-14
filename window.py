import pygame
from config import *
from UI import bind
from spawn import *

class Window:
    def __init__(self):
        self.__window = self.__init_window()
        self.__delta_time = DELTA_TIME
        self.__is_holding_mouse = False  
        self.__reset()
        self.__update()

    def __init_window(self):
        pygame.init()
        pygame.display.set_caption("Whack-a-Zombie")
        return pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    def __reset(self):
        self.__current_score = 0
        self.__current_misses = 0
        self.__time_left = self.__min_to_mil_sec(2) 

    def __min_to_mil_sec(self, min):
        return min * 60000

    def __update(self):
        isRunning = True

        while isRunning:
            pygame.time.delay(self.__delta_time)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    isRunning = False

                self.__handle_input(event)   

            self.__render()
            pygame.display.update()        

        pygame.quit()

    def __handle_input(self, event):
        if not pygame.mouse.get_visible():
            return

        if event.type == pygame.MOUSEBUTTONUP:
            self.__is_holding_mouse = False

        if self.__is_holding_mouse:
            return

        if event.type != pygame.MOUSEBUTTONDOWN:
            return

        self.__is_holding_mouse = True 

        self.__hit(pygame.mouse.get_pos())

    def __hit(self, mouse_pos):      
        hit_info = self.__spawn_manager.hit(mouse_pos)
        if not hit_info.hit:
            return

        if not hit_info.score:
            print("Missed")
            self.__update_misses(1)
            return

        print("Hit")
        self.__update_score(10)

    def __render(self):
        self.__window.fill((0))
        spawn = pygame.transform.scale(pygame.image.load("res/Zombie_Spawn.png"), (SPAWN_SIDE_LEN, SPAWN_SIDE_LEN))
        spawn_panel = pygame.transform.scale(pygame.image.load("res/Spawn_Panel.png"), (WINDOW_WIDTH, 440))
        self.__window.blit(spawn_panel, (0, 160))

        COLLIDER_OFFSET_X = 25
        COLLIDER_WIDTH = 110
        COLLIDER_HEIGHT = 130
        self.__spawns = []
        for row in range(N_ROWS):
            for col in range(N_COLS): 
                spawn_x, spawn_y = (SPAWN_PADDING_WIDTH + (SPAWN_PADDING_WIDTH + SPAWN_SIDE_LEN) * col, SPAWN_SIDE_LEN + SPAWN_SIDE_LEN * row)
                bound = Spawn((spawn_x + COLLIDER_OFFSET_X, spawn_y), (spawn_x + COLLIDER_WIDTH + COLLIDER_OFFSET_X, spawn_y + COLLIDER_HEIGHT))
                self.__spawns.append(bound)
                self.__window.blit(spawn, (spawn_x, spawn_y))
                # pygame.draw.rect(self.__window, (255, 255, 255), (bound.min[0], bound.min[1], COLLIDER_WIDTH, COLLIDER_HEIGHT), 2) # Visualize Colliders
        self.__spawn_manager = SpawnManager(self.__spawns)

        self.__render_UI()  

    def __render_UI(self):
        self.__render_text = bind(self.__window, pygame.font.Font(FONT_PATH, FONT_SIZE))
        self.__render_large_text = bind(self.__window, pygame.font.Font(FONT_PATH, LARGE_FONT_SIZE))
        self.__score_color = (205, 233, 34)
        self.__misses_color = (223, 53, 34)
        self.__time_color = (255, 255, 255)
        self.__render_text("SCORE", self.__score_color, (540, PADDING_UI_TOP))
        self.__render_text(str(self.__current_score), self.__score_color, (550, PADDING_UI_TOP * 2))
        self.__render_text("MISSES", self.__misses_color, (70, PADDING_UI_TOP))
        self.__render_text(str(self.__current_misses), self.__misses_color, (50, PADDING_UI_TOP * 2))
        self.__render_large_text("TIME LEFT", self.__time_color, (WINDOW_WIDTH // 2, PADDING_LARGE_UI_TOP))
        self.__render_large_text("02:00", self.__time_color, (WINDOW_WIDTH // 2, PADDING_LARGE_UI_TOP * 2.4))

    def __update_score(self, score_to_add):
        self.__current_score += score_to_add
        
    def __update_misses(self, misses_to_add):
        self.__current_misses += misses_to_add

if __name__ == "__main__":
    Window()