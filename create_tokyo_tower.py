#!/usr/bin/env python3
"""
東京タワーをMinecraftに生成するデータパック
高さ150ブロック（本体130 + アンテナ20）
赤白バンド、展望台2つ、斜め補強材付き
"""
import os, json, math

PACK_DIR = "/home/ktanino/project/tokyo_tower_datapack"
FUNC_DIR = f"{PACK_DIR}/data/tokyo_tower/function"

HEIGHT = 130
SPIRE_H = 20
BASE_HALF = 14
MAIN_DECK_Y = 55
MAIN_DECK_H = 5
SPECIAL_DECK_Y = 95
SPECIAL_DECK_H = 4
BRACE_INTERVAL = 12


def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        if isinstance(content, (dict, list)):
            json.dump(content, f, indent=2, ensure_ascii=False)
        else:
            f.write(content)


def hw(y):
    """Tower half-width at height y"""
    t = y / HEIGHT
    return max(1.0, BASE_HALF * (1 - t) ** 0.75)


def main():
    write_file(f"{PACK_DIR}/pack.mcmeta", {
        "pack": {"pack_format": 15, "description": "Tokyo Tower - 東京タワー"}
    })

    cmds = []
    cmds.append(f"# === 東京タワー ({HEIGHT + SPIRE_H}ブロック) ===")
    cmds.append("")

    # Clear area
    cmds.append("# エリアクリア")
    for ys in range(0, HEIGHT + SPIRE_H + 5, 20):
        ye = min(ys + 19, HEIGHT + SPIRE_H + 4)
        cmds.append(f"fill ~{-BASE_HALF-5} ~{ys} ~{-BASE_HALF-5} ~{BASE_HALF+5} ~{ye} ~{BASE_HALF+5} air")
    cmds.append("")

    # Ground base
    cmds.append("# 地面ベース")
    cmds.append(f"fill ~{-BASE_HALF-3} ~-1 ~{-BASE_HALF-3} ~{BASE_HALF+3} ~-1 ~{BASE_HALF+3} stone_bricks")
    cmds.append("")

    brace_levels = list(range(0, HEIGHT, BRACE_INTERVAL))

    # Build tower layer by layer
    cmds.append("# タワー本体")
    for y in range(HEIGHT):
        w = hw(y)
        iw = int(round(w))

        band_idx = y // BRACE_INTERVAL
        is_white = band_idx % 2 == 1
        block = "white_concrete" if is_white else "orange_concrete"

        if w >= 3.5:
            # 4 separate legs
            leg_r = max(1, int(w / 7) + 1)
            for sx, sz in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
                cx = int(round(sx * w))
                cz = int(round(sz * w))
                if leg_r > 1:
                    x1, z1 = cx - leg_r + 1, cz - leg_r + 1
                    x2, z2 = cx + leg_r - 1, cz + leg_r - 1
                    if sx < 0:
                        x1, x2 = cx - leg_r + 1, cx + leg_r - 1
                    if sz < 0:
                        z1, z2 = cz - leg_r + 1, cz + leg_r - 1
                    cmds.append(f"fill ~{min(x1,x2)} ~{y} ~{min(z1,z2)} ~{max(x1,x2)} ~{y} ~{max(z1,z2)} {block}")
                else:
                    cmds.append(f"setblock ~{cx} ~{y} ~{cz} {block}")

            # Horizontal bracing
            if y % BRACE_INTERVAL == 0:
                cmds.append(f"fill ~{-iw} ~{y} ~{iw} ~{iw} ~{y} ~{iw} {block}")
                cmds.append(f"fill ~{-iw} ~{y} ~{-iw} ~{iw} ~{y} ~{-iw} {block}")
                cmds.append(f"fill ~{iw} ~{y} ~{-iw} ~{iw} ~{y} ~{iw} {block}")
                cmds.append(f"fill ~{-iw} ~{y} ~{-iw} ~{-iw} ~{y} ~{iw} {block}")
        else:
            # Merged central shaft (hollow)
            if iw >= 2:
                cmds.append(f"fill ~{-iw} ~{y} ~{iw} ~{iw} ~{y} ~{iw} {block}")
                cmds.append(f"fill ~{-iw} ~{y} ~{-iw} ~{iw} ~{y} ~{-iw} {block}")
                cmds.append(f"fill ~{iw} ~{y} ~{-iw} ~{iw} ~{y} ~{iw} {block}")
                cmds.append(f"fill ~{-iw} ~{y} ~{-iw} ~{-iw} ~{y} ~{iw} {block}")
            else:
                cmds.append(f"setblock ~0 ~{y} ~0 {block}")

        # Main observation deck (大展望台)
        if MAIN_DECK_Y <= y <= MAIN_DECK_Y + MAIN_DECK_H:
            dhw = iw + 4
            if y == MAIN_DECK_Y or y == MAIN_DECK_Y + MAIN_DECK_H:
                cmds.append(f"fill ~{-dhw} ~{y} ~{-dhw} ~{dhw} ~{y} ~{dhw} white_concrete")
            else:
                cmds.append(f"fill ~{-dhw} ~{y} ~{dhw} ~{dhw} ~{y} ~{dhw} glass")
                cmds.append(f"fill ~{-dhw} ~{y} ~{-dhw} ~{dhw} ~{y} ~{-dhw} glass")
                cmds.append(f"fill ~{-dhw} ~{y} ~{-dhw} ~{-dhw} ~{y} ~{dhw} glass")
                cmds.append(f"fill ~{dhw} ~{y} ~{-dhw} ~{dhw} ~{y} ~{dhw} glass")
                for lx, lz in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
                    cmds.append(f"setblock ~{lx} ~{y} ~{lz} sea_lantern")

        # Special observatory (特別展望台)
        if SPECIAL_DECK_Y <= y <= SPECIAL_DECK_Y + SPECIAL_DECK_H:
            dhw = iw + 2
            if y == SPECIAL_DECK_Y or y == SPECIAL_DECK_Y + SPECIAL_DECK_H:
                cmds.append(f"fill ~{-dhw} ~{y} ~{-dhw} ~{dhw} ~{y} ~{dhw} white_concrete")
            else:
                cmds.append(f"fill ~{-dhw} ~{y} ~{dhw} ~{dhw} ~{y} ~{dhw} glass")
                cmds.append(f"fill ~{-dhw} ~{y} ~{-dhw} ~{dhw} ~{y} ~{-dhw} glass")
                cmds.append(f"fill ~{-dhw} ~{y} ~{-dhw} ~{-dhw} ~{y} ~{dhw} glass")
                cmds.append(f"fill ~{dhw} ~{y} ~{-dhw} ~{dhw} ~{y} ~{dhw} glass")
                cmds.append(f"setblock ~0 ~{y} ~0 sea_lantern")

    # Diagonal cross-bracing (X pattern on each face)
    cmds.append("")
    cmds.append("# 斜め補強材")
    for i in range(len(brace_levels) - 1):
        y1 = brace_levels[i]
        y2 = brace_levels[i + 1]
        w1 = hw(y1)
        w2 = hw(y2)

        if w1 < 3.5:
            break

        band_idx = y1 // BRACE_INTERVAL
        is_white = band_idx % 2 == 1
        block = "white_concrete" if is_white else "orange_concrete"

        for dy in range(1, y2 - y1):
            y = y1 + dy
            t = dy / (y2 - y1)
            iwy = int(round(hw(y)))

            x_d1 = int(round(-w1 * (1 - t) + w2 * t))
            x_d2 = int(round(w1 * (1 - t) - w2 * t))
            z_d1 = x_d1
            z_d2 = x_d2

            # South & North faces
            cmds.append(f"setblock ~{x_d1} ~{y} ~{iwy} {block}")
            cmds.append(f"setblock ~{x_d2} ~{y} ~{iwy} {block}")
            cmds.append(f"setblock ~{x_d1} ~{y} ~{-iwy} {block}")
            cmds.append(f"setblock ~{x_d2} ~{y} ~{-iwy} {block}")
            # East & West faces
            cmds.append(f"setblock ~{iwy} ~{y} ~{z_d1} {block}")
            cmds.append(f"setblock ~{iwy} ~{y} ~{z_d2} {block}")
            cmds.append(f"setblock ~{-iwy} ~{y} ~{z_d1} {block}")
            cmds.append(f"setblock ~{-iwy} ~{y} ~{z_d2} {block}")

    # Antenna spire
    cmds.append("")
    cmds.append("# アンテナ")
    for y in range(HEIGHT, HEIGHT + SPIRE_H):
        cmds.append(f"setblock ~0 ~{y} ~0 orange_concrete")
    cmds.append(f"setblock ~0 ~{HEIGHT + SPIRE_H - 1} ~0 sea_lantern")
    cmds.append(f"setblock ~0 ~{HEIGHT + SPIRE_H} ~0 lightning_rod")

    # Night illumination (redstone lamps on legs)
    cmds.append("")
    cmds.append("# ライトアップ")
    for y in range(0, HEIGHT, 8):
        w_val = hw(y)
        if w_val >= 3.5:
            iw_val = int(round(w_val))
            for sx, sz in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
                cx = int(round(sx * w_val))
                cz = int(round(sz * w_val))
                cmds.append(f"setblock ~{cx} ~{y} ~{cz} glowstone")

    cmds.append("")
    cmds.append('tellraw @a [{"text":"[東京タワー] ","color":"red","bold":true},{"text":"建設完了！高さ150ブロック","color":"gold"}]')
    cmds.append('playsound minecraft:ui.toast.challenge_complete master @s ~ ~ ~ 1 1')

    write_file(f"{FUNC_DIR}/place.mcfunction", "\n".join(cmds))

    # Remove function
    remove_cmds = [
        "# 東京タワー撤去",
        f"fill ~{-BASE_HALF-5} ~-1 ~{-BASE_HALF-5} ~{BASE_HALF+5} ~{HEIGHT+SPIRE_H+1} ~{BASE_HALF+5} air",
        'tellraw @s [{"text":"[東京タワー] ","color":"red"},{"text":"撤去しました","color":"yellow"}]'
    ]
    write_file(f"{FUNC_DIR}/remove.mcfunction", "\n".join(remove_cmds))

    # Count commands
    cmd_count = len([c for c in cmds if c and not c.startswith("#")])
    print(f"✅ 東京タワーデータパック生成完了！")
    print(f"   高さ: {HEIGHT + SPIRE_H} ブロック")
    print(f"   底面: {BASE_HALF*2} × {BASE_HALF*2} ブロック")
    print(f"   大展望台: y={MAIN_DECK_Y}")
    print(f"   特別展望台: y={SPECIAL_DECK_Y}")
    print(f"   コマンド数: {cmd_count}")
    print()
    print("使い方:")
    print("  /reload")
    print("  /function tokyo_tower:place   → 建設")
    print("  /function tokyo_tower:remove  → 撤去")


if __name__ == "__main__":
    main()
