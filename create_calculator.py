#!/usr/bin/env python3
"""
Minecraft Java版 4ビット加算計算機データパック生成
レバー操作でリアルタイムに A(0-15) + B(0-15) を計算・表示
"""
import os
import json

PACK_DIR = "/home/ktanino/project/calculator_datapack"

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        if isinstance(content, (dict, list)):
            json.dump(content, f, indent=2, ensure_ascii=False)
        else:
            f.write(content)

def sign_nbt(text, color="white"):
    msg = '\'{"text":"' + text + '","color":"' + color + '","bold":true}\''
    e = "'\"\"'"
    return '{front_text:{messages:[' + msg + ',' + e + ',' + e + ',' + e + ']}}'

def main():
    write_file(f"{PACK_DIR}/pack.mcmeta", {
        "pack": {"pack_format": 15, "description": "4-bit Redstone Calculator"}
    })

    write_file(f"{PACK_DIR}/data/minecraft/tags/function/tick.json", {
        "values": ["calc:tick"]
    })

    # ===== place.mcfunction =====
    p = []
    p.append("# === 4ビット加算計算機 ===")
    p.append("# レバーでA(0-15)+B(0-15)をリアルタイム計算")
    p.append("")
    p.append("kill @e[tag=calc_origin]")
    p.append("scoreboard objectives add calc dummy")
    p.append("scoreboard players set #2 calc 2")
    p.append("scoreboard players set #4 calc 4")
    p.append("scoreboard players set #8 calc 8")
    p.append("scoreboard players set #16 calc 16")
    p.append('summon marker ~ ~ ~ {Tags:["calc_origin"]}')
    p.append("")

    # Platform & clear
    p.append("# プラットフォーム")
    p.append("fill ~0 ~0 ~0 ~18 ~0 ~11 smooth_stone")
    p.append("fill ~0 ~1 ~0 ~18 ~3 ~11 air")
    p.append("")

    # Input A border (red)
    p.append("# 入力Aエリア (赤)")
    p.append("fill ~0 ~0 ~2 ~8 ~0 ~2 red_concrete")
    p.append("fill ~0 ~0 ~4 ~8 ~0 ~4 red_concrete")
    p.append("fill ~0 ~0 ~2 ~0 ~0 ~4 red_concrete")
    p.append("fill ~8 ~0 ~2 ~8 ~0 ~4 red_concrete")

    # Input B border (blue)
    p.append("# 入力Bエリア (青)")
    p.append("fill ~10 ~0 ~2 ~18 ~0 ~2 blue_concrete")
    p.append("fill ~10 ~0 ~4 ~18 ~0 ~4 blue_concrete")
    p.append("fill ~10 ~0 ~2 ~10 ~0 ~4 blue_concrete")
    p.append("fill ~18 ~0 ~2 ~18 ~0 ~4 blue_concrete")

    # Center
    p.append("setblock ~9 ~0 ~3 gold_block")

    # Output border (yellow)
    p.append("# 結果エリア (黄)")
    p.append("fill ~4 ~0 ~8 ~14 ~0 ~8 yellow_concrete")
    p.append("fill ~4 ~0 ~10 ~14 ~0 ~10 yellow_concrete")
    p.append("fill ~4 ~0 ~8 ~4 ~0 ~10 yellow_concrete")
    p.append("fill ~14 ~0 ~8 ~14 ~0 ~10 yellow_concrete")

    p.append("setblock ~9 ~0 ~6 gold_block")
    p.append("")

    # Levers
    p.append("# 入力レバー A (8,4,2,1)")
    for x in [1, 3, 5, 7]:
        p.append(f"setblock ~{x} ~1 ~3 lever[face=floor]")
    p.append("# 入力レバー B (8,4,2,1)")
    for x in [11, 13, 15, 17]:
        p.append(f"setblock ~{x} ~1 ~3 lever[face=floor]")

    # +, = signs
    p.append(f"setblock ~9 ~1 ~3 oak_sign[rotation=0]{sign_nbt('+', 'gold')}")
    p.append(f"setblock ~9 ~1 ~6 oak_sign[rotation=0]{sign_nbt('=', 'gold')}")
    p.append("")

    # Output lamps
    p.append("# 出力ランプ (16,8,4,2,1)")
    for x in [5, 7, 9, 11, 13]:
        p.append(f"setblock ~{x} ~1 ~9 redstone_lamp")
    p.append("")

    # Labels
    p.append("# ラベル")
    p.append(f"setblock ~4 ~1 ~1 oak_sign[rotation=0]{sign_nbt('A', 'red')}")
    p.append(f"setblock ~14 ~1 ~1 oak_sign[rotation=0]{sign_nbt('B', 'aqua')}")

    for x, val in [(1, "8"), (3, "4"), (5, "2"), (7, "1")]:
        p.append(f"setblock ~{x} ~1 ~4 oak_sign[rotation=0]{sign_nbt(val, 'red')}")
    for x, val in [(11, "8"), (13, "4"), (15, "2"), (17, "1")]:
        p.append(f"setblock ~{x} ~1 ~4 oak_sign[rotation=0]{sign_nbt(val, 'aqua')}")

    for x, val in [(5, "16"), (7, "8"), (9, "4"), (11, "2"), (13, "1")]:
        p.append(f"setblock ~{x} ~2 ~9 oak_sign[rotation=0]{sign_nbt(val, 'yellow')}")

    p.append("")
    p.append('tellraw @s [{"text":"[計算機] ","color":"gold","bold":true},{"text":"設置完了！レバーでA,Bを入力するとリアルタイムで計算します","color":"green"}]')

    write_file(f"{PACK_DIR}/data/calc/function/place.mcfunction", "\n".join(p))

    # ===== tick.mcfunction =====
    write_file(f"{PACK_DIR}/data/calc/function/tick.mcfunction",
        "execute as @e[tag=calc_origin,limit=1] at @s run function calc:tick_logic\n")

    # ===== tick_logic.mcfunction =====
    t = []
    t.append("# 毎tick: レバー読み取り → 加算 → ランプ&アクションバー表示")
    t.append("")
    t.append("# 入力A読み取り")
    t.append("scoreboard players set #A calc 0")
    t.append("execute if block ~1 ~1 ~3 lever[powered=true] run scoreboard players add #A calc 8")
    t.append("execute if block ~3 ~1 ~3 lever[powered=true] run scoreboard players add #A calc 4")
    t.append("execute if block ~5 ~1 ~3 lever[powered=true] run scoreboard players add #A calc 2")
    t.append("execute if block ~7 ~1 ~3 lever[powered=true] run scoreboard players add #A calc 1")
    t.append("")
    t.append("# 入力B読み取り")
    t.append("scoreboard players set #B calc 0")
    t.append("execute if block ~11 ~1 ~3 lever[powered=true] run scoreboard players add #B calc 8")
    t.append("execute if block ~13 ~1 ~3 lever[powered=true] run scoreboard players add #B calc 4")
    t.append("execute if block ~15 ~1 ~3 lever[powered=true] run scoreboard players add #B calc 2")
    t.append("execute if block ~17 ~1 ~3 lever[powered=true] run scoreboard players add #B calc 1")
    t.append("")
    t.append("# 加算")
    t.append("scoreboard players operation #R calc = #A calc")
    t.append("scoreboard players operation #R calc += #B calc")
    t.append("")

    # Bit extraction → lamp control
    t.append("# ビット抽出 → ランプ制御")
    lamps = [(13, 1), (11, 2), (9, 4), (7, 8), (5, 16)]
    for lamp_x, bit_val in lamps:
        t.append("scoreboard players operation #bit calc = #R calc")
        if bit_val > 1:
            t.append(f"scoreboard players operation #bit calc /= #{bit_val} calc")
        t.append("scoreboard players operation #bit calc %= #2 calc")
        t.append(f"execute if score #bit calc matches 1 run setblock ~{lamp_x} ~0 ~9 redstone_block")
        t.append(f"execute if score #bit calc matches 0 run setblock ~{lamp_x} ~0 ~9 smooth_stone")
    t.append("")

    # Actionbar display
    actionbar = json.dumps([
        "",
        {"text": " A=", "color": "red"},
        {"score": {"name": "#A", "objective": "calc"}, "color": "red", "bold": True},
        {"text": " + ", "color": "gold", "bold": True},
        {"text": "B=", "color": "aqua"},
        {"score": {"name": "#B", "objective": "calc"}, "color": "aqua", "bold": True},
        {"text": " = ", "color": "white"},
        {"score": {"name": "#R", "objective": "calc"}, "color": "green", "bold": True}
    ], ensure_ascii=False)
    t.append(f"title @a[distance=..30] actionbar {actionbar}")

    write_file(f"{PACK_DIR}/data/calc/function/tick_logic.mcfunction", "\n".join(t))

    # ===== remove.mcfunction =====
    write_file(f"{PACK_DIR}/data/calc/function/remove.mcfunction", "\n".join([
        "# 計算機撤去",
        "kill @e[tag=calc_origin]",
        "scoreboard objectives remove calc",
        'tellraw @s [{"text":"[計算機] ","color":"gold"},{"text":"撤去しました","color":"yellow"}]'
    ]))

    print("✅ 計算機データパック生成完了！")
    print()
    print("レイアウト (上から見た図):")
    print("  z=1: [A]                        [B]")
    print("  z=2: ┌──── 赤 ────┐    ┌──── 青 ────┐")
    print("  z=3: │ L  L  L  L │ [+] │ L  L  L  L │  ← レバー")
    print("  z=4: └ 8  4  2  1 ┘    └ 8  4  2  1 ┘")
    print("  z=6:              [=]")
    print("  z=8: ┌────── 黄 ──────┐")
    print("  z=9: │ ◎  ◎  ◎  ◎  ◎ │  ← ランプ (16,8,4,2,1)")
    print("  z=10:└────────────────┘")
    print()
    print("画面上部のアクションバーに 'A=X + B=Y = Z' と10進数で表示されます")


if __name__ == "__main__":
    main()
