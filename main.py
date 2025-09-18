# main.py
import random
from typing import Optional, Dict
from abc import ABC, abstractmethod

# ====== Оружие ======
class Weapon:
    def __init__(self, wid: str, name_ru: str, damage: int, dmg_type: str, dmg_type_ru: str):
        self.id = wid
        self.name_ru = name_ru
        self.damage = damage
        self.dmg_type = dmg_type        # "Slashing" | "Bludgeoning" | "Piercing"
        self.dmg_type_ru = dmg_type_ru

WEAPONS: Dict[str, Weapon] = {
    "Sword":  Weapon("Sword",  "Меч", 3, "Slashing", "Рубящий"),
    "Club":   Weapon("Club",   "Дубина", 3, "Bludgeoning", "Дробящий"),
    "Dagger": Weapon("Dagger", "Кинжал", 2, "Piercing", "Колющий"),
    "Axe":    Weapon("Axe",    "Топор", 4, "Slashing", "Рубящий"),
    "Spear":  Weapon("Spear",  "Копьё", 3, "Piercing", "Колющий"),
    "LegendarySword": Weapon("LegendarySword", "Легендарный Меч", 10, "Slashing", "Рубящий"),
}

# ====== Классы персонажа (ООП) ======
class BaseClass(ABC):
    def __init__(self, name_ru: str, hp_per_level: int, start_weapon_id: str):
        self.name_ru = name_ru
        self.hp_per_level = hp_per_level
        self.start_weapon_id = start_weapon_id

    @abstractmethod
    def apply_level_bonus(self, level: int, player: "Player") -> None:
        """Перки на 1–3 уровнях."""
        pass

class Rogue(BaseClass):
    def __init__(self):
        super().__init__("Разбойник", 4, "Dagger")
    def apply_level_bonus(self, level: int, player: "Player") -> None:
        if level == 1:
            print("Бонус: Скрытая атака — +1 урона, если ваша Ловкость выше Ловкости цели.")
        elif level == 2:
            player.DEX += 1; print("Бонус: Ловкость +1.")
        elif level == 3:
            print("Бонус: Яд — на 2-м ходу +1 урона, на 3-м +2, и т.д.")

class Warrior(BaseClass):
    def __init__(self):
        super().__init__("Воин", 5, "Sword")
    def apply_level_bonus(self, level: int, player: "Player") -> None:
        if level == 1:
            print("Бонус: Порыв к действию — в первый свой ход доп. урон = урону оружия.")
        elif level == 2:
            print("Бонус: Щит — если ваша Сила > Силы врага, входящий урон −3.")
        elif level == 3:
            player.STR += 1; print("Бонус: Сила +1.")

class Barbarian(BaseClass):
    def __init__(self):
        super().__init__("Варвар", 6, "Club")
    def apply_level_bonus(self, level: int, player: "Player") -> None:
        if level == 1:
            print("Бонус: Ярость — +2 урона в первые 3 хода, затем −1.")
        elif level == 2:
            print("Бонус: Каменная кожа — входящий урон уменьшается на вашу Выносливость.")
        elif level == 3:
            player.STA += 1; print("Бонус: Выносливость +1.")

CLASSES: Dict[str, BaseClass] = {
    "Warrior": Warrior(),
    "Barbarian": Barbarian(),
    "Rogue": Rogue(),
}
CLASS_KEYS = list(CLASSES.keys())

# ====== Противники ======
class Enemy:
    def __init__(self, eid: str, name_ru: str, hp: int, weapon_dmg: int, STR: int, DEX: int, STA: int, reward_weapon_id: Optional[str]):
        self.id = eid
        self.name_ru = name_ru
        self.hp = hp
        self.weapon_dmg = weapon_dmg
        self.STR = STR
        self.DEX = DEX
        self.STA = STA
        self.reward_weapon_id = reward_weapon_id

ENEMIES: Dict[str, Enemy] = {
    "Goblin":   Enemy("Goblin", "Гоблин", 5, 2, 1, 1, 1, "Dagger"),
    "Skeleton": Enemy("Skeleton", "Скелет", 10, 2, 2, 2, 1, "Club"),
    "Slime":    Enemy("Slime", "Слайм", 8, 1, 3, 1, 2, "Spear"),
    "Ghost":    Enemy("Ghost", "Призрак", 6, 3, 1, 3, 1, "Sword"),
    "Golem":    Enemy("Golem", "Голем", 10, 1, 3, 1, 3, "Axe"),
    "Dragon":   Enemy("Dragon", "Дракон", 20, 4, 3, 3, 3, "LegendarySword"),
}

# ====== Игрок ======
class Player:
    def __init__(self, name: str, STR: int, DEX: int, STA: int, weapon_id: str, hp: int, max_hp: int):
        self.name = name
        self.STR = STR
        self.DEX = DEX
        self.STA = STA
        self.weapon_id = weapon_id
        self.hp = hp
        self.max_hp = max_hp
        self.levels: Dict[str, int] = {"Rogue": 0, "Warrior": 0, "Barbarian": 0}
    @property
    def total_level(self) -> int:
        return sum(self.levels.values())

# ====== UI ======
def choose_class() -> str:
    print("Выберите начальный класс:")
    for i, key in enumerate(CLASS_KEYS, start=1):
        print(f"{i}. {CLASSES[key].name_ru}")
    while True:
        s = input("Введите номер класса: ").strip()
        if s.isdigit() and 1 <= int(s) <= len(CLASS_KEYS):
            return CLASS_KEYS[int(s) - 1]
        print("Неверный выбор. Введите 1–3.")

def ask_name() -> str:
    while True:
        name = input("Введите имя героя: ").strip()
        if name: return name
        print("Имя не может быть пустым.")

def show_player_sheet(p: Player) -> None:
    w = WEAPONS[p.weapon_id]
    print("\n=== Характеристики героя ===")
    print(f"Имя: {p.name}")
    print(f"Уровни: Разбойник={p.levels['Rogue']}, Воин={p.levels['Warrior']}, Варвар={p.levels['Barbarian']} (∑={p.total_level})")
    print(f"HP: {p.hp}/{p.max_hp}")
    print(f"STR: {p.STR} | DEX: {p.DEX} | STA: {p.STA}")
    print(f"Оружие: {w.name_ru} (урон {w.damage}, тип {w.dmg_type_ru})")

# ====== Попадание ======
def hit_success(att_dex: int, def_dex: int) -> bool:
    r = random.randint(1, att_dex + def_dex)
    return r > def_dex

# ====== Оффенс игрока ======
def player_offense_parts(player: Player, enemy: Enemy, turn_count: int):
    w = WEAPONS[player.weapon_id]
    weapon_part = w.damage
    other_part = player.STR
    bonus = 0
    if player.levels["Rogue"] >= 1 and player.DEX > enemy.DEX:
        bonus += 1
    if player.levels["Rogue"] >= 3 and turn_count >= 2:
        bonus += (turn_count - 1)
    if player.levels["Warrior"] >= 1 and turn_count == 1:
        other_part += w.damage   # важно: работает против Слайма
    if player.levels["Barbarian"] >= 1:
        bonus += 2 if turn_count <= 3 else -1
    other_part += bonus
    return weapon_part, other_part

# ====== Защита игрока ======
def reduce_incoming_to_player(player: Player, enemy: Enemy, raw_dmg: int) -> int:
    dmg = raw_dmg
    if player.levels["Warrior"] >= 2 and player.STR > enemy.STR:
        dmg -= 3
    if player.levels["Barbarian"] >= 2:
        dmg -= player.STA
    return max(dmg, 0)

# ====== Особенности целей ======
def apply_enemy_weakness(enemy: Enemy, player_weapon_id: str, weapon_part: int, other_part: int) -> int:
    wtype = WEAPONS[player_weapon_id].dmg_type
    total = weapon_part + other_part
    if enemy.id == "Skeleton" and wtype == "Bludgeoning":
        return total * 2
    if enemy.id == "Slime" and wtype == "Slashing":
        return max(other_part, 0)
    if enemy.id == "Golem":
        return max(total - enemy.STA, 0)
    return max(total, 0)

# ====== Ходы ======
def player_attack(player: Player, enemy: Enemy, enemy_hp: int, turn_count: int) -> int:
    print("\n--- Ход игрока ---")
    while True:
        act = input("Нажмите 'a' чтобы атаковать: ").strip().lower()
        if act == "a": break
    if not hit_success(player.DEX, enemy.DEX):
        print("Вы промахнулись!")
        print(f"У {enemy.name_ru} осталось HP: {enemy_hp}\n")
        return enemy_hp
    weapon_part, other_part = player_offense_parts(player, enemy, turn_count)
    dmg = apply_enemy_weakness(enemy, player.weapon_id, weapon_part, other_part)
    print(f"{player.name} попадает и наносит {dmg} урона.")
    enemy_hp = max(enemy_hp - dmg, 0)
    print(f"У {enemy.name_ru} осталось HP: {enemy_hp}\n")
    return enemy_hp

def enemy_attack(enemy: Enemy, player: Player, turn_count: int) -> None:
    print("\n--- Ход противника ---")
    if not hit_success(enemy.DEX, player.DEX):
        print(f"{enemy.name_ru} промахнулся!")
        print(f"У вас осталось HP: {player.hp}\n")
        return
    raw = enemy.weapon_dmg + enemy.STR
    if enemy.id == "Ghost" and enemy.DEX > player.DEX:
        raw += 1
    if enemy.id == "Dragon" and turn_count % 3 == 0:
        raw += 3
    dmg = reduce_incoming_to_player(player, enemy, raw)
    print(f"{enemy.name_ru} попадает и наносит {dmg} урона.")
    player.hp = max(player.hp - dmg, 0)
    print(f"У вас осталось HP: {player.hp}\n")

# ====== Бой ======
def start_fight(player: Player, enemy: Enemy) -> bool:
    print(f"\nНа вас нападает: {enemy.name_ru}!")
    enemy_hp = enemy.hp
    p_turns = e_turns = 0
    if player.DEX >= enemy.DEX:
        turn = "player"; print("Вы ходите первыми." if player.DEX == enemy.DEX else "Вы быстрее и ходите первыми.")
    else:
        turn = "enemy"; print(f"{enemy.name_ru} ходит первым.")

    while player.hp > 0 and enemy_hp > 0:
        if turn == "player":
            p_turns += 1
            enemy_hp = player_attack(player, enemy, enemy_hp, p_turns)
            turn = "enemy"
        else:
            e_turns += 1
            enemy_attack(enemy, player, e_turns)
            turn = "player"

    if player.hp <= 0:
        print("\nВы пали в бою... Игра окончена.")
        return False
    print(f"\n{enemy.name_ru} повержен!")
    return True

# ====== Лут и лечение ======
def offer_loot_and_heal(player: Player, enemy: Enemy) -> None:
    player.hp = player.max_hp
    print(f"Ваше здоровье восстановлено: {player.hp}/{player.max_hp}\n")
    if not enemy.reward_weapon_id: return
    new_w, old_w = WEAPONS[enemy.reward_weapon_id], WEAPONS[player.weapon_id]
    print("Вы нашли оружие:")
    print(f"- Новое:   {new_w.name_ru} | Урон {new_w.damage}, {new_w.dmg_type_ru}")
    print(f"- Текущее: {old_w.name_ru} | Урон {old_w.damage}, {old_w.dmg_type_ru}")
    while True:
        ans = input("Заменить текущее оружие на новое? (y/n): ").strip().lower()
        if ans in ("y", "yes", "д", "да"):
            player.weapon_id = new_w.id
            print(f"Вы экипировали: {new_w.name_ru}\n"); break
        if ans in ("n", "no", "н", "нет"):
            print("Вы оставили текущее оружие.\n"); break

# ====== Превью бонуса для меню апа ======
def bonus_preview_text(class_key: str, next_level: int) -> str:
    if class_key == "Rogue":
        return {
            1: "Скрытая атака (+1 урона, если DEX > DEX цели)",
            2: "DEX +1",
            3: "Яд (+1 на 2-м ходу, +2 на 3-м ...)",
        }.get(next_level, "—")
    if class_key == "Warrior":
        return {
            1: "Порыв (в 1-й ход доп. урон = урону оружия)",
            2: "Щит (если STR > врага, входящий урон −3)",
            3: "STR +1",
        }.get(next_level, "—")
    if class_key == "Barbarian":
        return {
            1: "Ярость (+2 урона 3 хода, затем −1)",
            2: "Каменная кожа (−STA к входящему урону)",
            3: "STA +1",
        }.get(next_level, "—")
    return "—"

# ====== Повышение уровня (лимит суммарных уровней = 3) ======
def level_up(player: Player) -> None:
    if player.total_level >= 3:
        # строго по ТЗ: после капа — только лечение (уже сделано), без апов
        print("Лимит суммарных уровней достигнут (3). Продолжаем путешествие.")
        return

    print("Повышение уровня! Выберите класс для повышения:")
    for i, key in enumerate(CLASS_KEYS, 1):
        cur = player.levels[key]
        nxt = cur + 1
        preview = bonus_preview_text(key, nxt)
        print(f"{i}. {CLASSES[key].name_ru} (текущий ур.: {cur} → {nxt}) — получишь: {preview}")

    chosen_key: Optional[str] = None
    while chosen_key is None:
        s = input("Номер класса: ").strip()
        if s.isdigit() and 1 <= int(s) <= len(CLASS_KEYS):
            chosen_key = CLASS_KEYS[int(s) - 1]
        else:
            print("Введите 1–3.")

    # Прирост уровня
    player.levels[chosen_key] += 1
    lvl = player.levels[chosen_key]

    cls = CLASSES[chosen_key]
    # Прирост max HP по формуле ТЗ
    player.max_hp += cls.hp_per_level + player.STA
    player.hp = player.max_hp

    print(f"\n=== +1 уровень в классе {cls.name_ru} (теперь {lvl}) ===")
    print(f"Макс. здоровье теперь: {player.max_hp}")
    cls.apply_level_bonus(lvl, player)

# ====== Кампания ======
def campaign(player: Player, wins_to_finish: int = 5) -> bool:
    wins = 0
    pool = list(ENEMIES.values()); random.shuffle(pool); idx = 0
    while wins < wins_to_finish:
        if idx >= len(pool): random.shuffle(pool); idx = 0
        enemy = pool[idx]; idx += 1
        if start_fight(player, enemy):
            wins += 1
            offer_loot_and_heal(player, enemy)
            level_up(player)   # после капа просто сообщение
            print(f"Побед: {wins}/{wins_to_finish}\n")
        else:
            if player.hp <= 0:
                return False
            print("Вы продолжили путь...\n")
    print("\n✨ Поздравляем! Вы прошли игру! ✨")
    return True

# ====== Одна сессия ======
def run_session() -> bool:
    start_key = choose_class()
    name = ask_name()
    STR, DEX, STA = (random.randint(1, 3) for _ in range(3))
    start_class = CLASSES[start_key]
    max_hp = start_class.hp_per_level + STA
    player = Player(name=name, STR=STR, DEX=DEX, STA=STA,
                    weapon_id=start_class.start_weapon_id, hp=max_hp, max_hp=max_hp)
    player.levels[start_key] = 1
    print(f"\nСтартовые атрибуты: STR={STR}, DEX={DEX}, STA={STA}")
    show_player_sheet(player)
    return campaign(player, wins_to_finish=5)
def main():
    try:
        start = input("Начать игру? (y/n): ").strip().lower()
        if start not in ("y", "yes", "д", "да"):
            print("До встречи!"); return
        while True:
            _ = run_session()
            again = input("\nНачать игру заново? (y/n): ").strip().lower()
            if again not in ("y", "yes", "д", "да"):
                print("Спасибо за игру!"); break
    except KeyboardInterrupt:
        print("\n\nВы прервали игру. До встречи!")

if __name__ == "__main__":
    main()
