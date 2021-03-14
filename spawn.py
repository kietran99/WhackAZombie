class HitInfo:
    def __init__(self, hit: bool, score: int):
        self.hit = hit
        self.score = score

class Spawn:
    def __init__(self, min: (int, int), max : (int, int)):
        self.__min = min
        self.__max = max
        self.__whackable = False
        
    @property
    def min(self):
        return self.__min

    @property
    def max(self):
        return self.__max

    @property
    def whackable(self):
        return self.__whackable

    def hit(self, hit_pos) -> HitInfo:
        is_colliding = self.__is_in_bound(hit_pos, 0) and self.__is_in_bound(hit_pos, 1)
        return HitInfo(is_colliding, 10 if self.__whackable else 0)

    def __is_in_bound(self, input_pos: (int, int), idx: int):
        return input_pos[idx] >= self.__min[idx] and input_pos[idx] <= self.__max[idx]

class SpawnManager:
    def __init__(self, spawns: list[Spawn]):
        self.__spawns = spawns

    def hit(self, hit_pos: (int, int)):
        return hit(hit_pos, self.__spawns)

    def hit(self, hit_pos: (int, int), spawns: list[Spawn]) -> HitInfo:
        if not spawns:
            return (False, 0)

        hit_info = spawns[0].hit(hit_pos)
        if hit_info.hit:
            return hit_info.score

        return hit(hit_pos, spawns[1:])

