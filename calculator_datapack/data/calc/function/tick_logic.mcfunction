# 毎tick: レバー読み取り → 加算 → ランプ&アクションバー表示

# 入力A読み取り
scoreboard players set #A calc 0
execute if block ~1 ~1 ~3 lever[powered=true] run scoreboard players add #A calc 8
execute if block ~3 ~1 ~3 lever[powered=true] run scoreboard players add #A calc 4
execute if block ~5 ~1 ~3 lever[powered=true] run scoreboard players add #A calc 2
execute if block ~7 ~1 ~3 lever[powered=true] run scoreboard players add #A calc 1

# 入力B読み取り
scoreboard players set #B calc 0
execute if block ~11 ~1 ~3 lever[powered=true] run scoreboard players add #B calc 8
execute if block ~13 ~1 ~3 lever[powered=true] run scoreboard players add #B calc 4
execute if block ~15 ~1 ~3 lever[powered=true] run scoreboard players add #B calc 2
execute if block ~17 ~1 ~3 lever[powered=true] run scoreboard players add #B calc 1

# 加算
scoreboard players operation #R calc = #A calc
scoreboard players operation #R calc += #B calc

# ビット抽出 → ランプ制御
scoreboard players operation #bit calc = #R calc
scoreboard players operation #bit calc %= #2 calc
execute if score #bit calc matches 1 run setblock ~13 ~0 ~9 redstone_block
execute if score #bit calc matches 0 run setblock ~13 ~0 ~9 smooth_stone
scoreboard players operation #bit calc = #R calc
scoreboard players operation #bit calc /= #2 calc
scoreboard players operation #bit calc %= #2 calc
execute if score #bit calc matches 1 run setblock ~11 ~0 ~9 redstone_block
execute if score #bit calc matches 0 run setblock ~11 ~0 ~9 smooth_stone
scoreboard players operation #bit calc = #R calc
scoreboard players operation #bit calc /= #4 calc
scoreboard players operation #bit calc %= #2 calc
execute if score #bit calc matches 1 run setblock ~9 ~0 ~9 redstone_block
execute if score #bit calc matches 0 run setblock ~9 ~0 ~9 smooth_stone
scoreboard players operation #bit calc = #R calc
scoreboard players operation #bit calc /= #8 calc
scoreboard players operation #bit calc %= #2 calc
execute if score #bit calc matches 1 run setblock ~7 ~0 ~9 redstone_block
execute if score #bit calc matches 0 run setblock ~7 ~0 ~9 smooth_stone
scoreboard players operation #bit calc = #R calc
scoreboard players operation #bit calc /= #16 calc
scoreboard players operation #bit calc %= #2 calc
execute if score #bit calc matches 1 run setblock ~5 ~0 ~9 redstone_block
execute if score #bit calc matches 0 run setblock ~5 ~0 ~9 smooth_stone

title @a[distance=..30] actionbar ["", {"text": " A=", "color": "red"}, {"score": {"name": "#A", "objective": "calc"}, "color": "red", "bold": true}, {"text": " + ", "color": "gold", "bold": true}, {"text": "B=", "color": "aqua"}, {"score": {"name": "#B", "objective": "calc"}, "color": "aqua", "bold": true}, {"text": " = ", "color": "white"}, {"score": {"name": "#R", "objective": "calc"}, "color": "green", "bold": true}]