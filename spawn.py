import pygame
from random import randint

from config import *

COLLIDER_OFFSET_X = 25
COLLIDER_WIDTH = 110
COLLIDER_HEIGHT = 130

class HitInfo:
    def __init__(self, hit: bool, score: int):
        self.hit = hit
        self.score = score

class Spawner:
    def __init__(self, pos: tuple[int, int], min_collider_bound: tuple[int, int], max_collider_bound : tuple[int, int]):
        self.__pos = pos
        self.__min_collider_bound = min_collider_bound
        self.__max_collider_bound = max_collider_bound
        self.__whackable = False

    @property
    def pos(self):
        return self.__pos

    @property
    def whackable(self):
        return self.__whackable

    def shift_hittable_state(self):
        self.__whackable = True

    def shift_unhittable_state(self):
        self.__whackable = False

    def hit(self, hit_pos) -> HitInfo:
        is_colliding = self.__is_in_bound(hit_pos, 0) and self.__is_in_bound(hit_pos, 1)
        return HitInfo(is_colliding, 10 if self.__whackable else 0)

    def __is_in_bound(self, input_pos: (int, int), idx: int) -> bool:
        return input_pos[idx] >= self.__min_collider_bound[idx] and input_pos[idx] <= self.__max_collider_bound[idx]

class SpawnManager:
    def __init__(self, window, spawners: list[Spawner]):
        self.__window = window
        self.__spawn_sprite = pygame.transform.scale(pygame.image.load("res/Zombie_Spawn.png"), (SPAWN_SIDE_LEN, SPAWN_SIDE_LEN))
        self.__zombie_sprite = pygame.transform.scale(pygame.image.load("res/Regular_Zombie.png"), (160, 160))
        self.__spawners = spawners

    def render_spawners(self):
        for spawner in self.__spawners:
            self.__window.blit(self.__spawn_sprite, (spawner.pos[0], spawner.pos[1]))
            if spawner.whackable:
                self.__window.blit(self.__zombie_sprite, (spawner.pos[0], spawner.pos[1] - 34))

    def hit(self, hit_pos: tuple[int, int]) -> HitInfo:
        return self.__hit(hit_pos, self.__spawners)

    def __hit(self, hit_pos: tuple[int, int], spawns: list[Spawner]) -> HitInfo:
        if not spawns:
            return HitInfo(False, 0)

        hit_info = spawns[0].hit(hit_pos)
        if hit_info.hit:
            return hit_info

        return self.__hit(hit_pos, spawns[1:])

    def random_spawn(self):
        [spawn.shift_unhittable_state() for spawn in self.__spawners]
        rand_idx = randint(0, len(self.__spawners) - 1)
        self.__spawners[rand_idx].shift_hittable_state()
