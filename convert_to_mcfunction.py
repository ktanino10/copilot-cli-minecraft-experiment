#!/usr/bin/env python3
"""
GitHubロゴ画像をMinecraft Java版のブロックアートに変換するスクリプト。
.mcfunction ファイルを生成し、データパックとして使用可能。
"""

from PIL import Image
import os

INPUT_IMAGE = "/home/ktanino/spray_guard/GitHub-Mark-ea2971cee799.png"
OUTPUT_DIR = "/home/ktanino/project/github_logo_datapack/data/github_logo/function"
BLOCK_SIZE = 64  # 64x64 ブロックで再現

# Minecraft ブロックカラーパレット (RGB -> block ID)
BLOCK_PALETTE = [
    ((255, 255, 255), "minecraft:white_concrete"),
    ((209, 209, 209), "minecraft:light_gray_concrete"),
    ((125, 125, 125), "minecraft:gray_concrete"),
    ((55,  55,  55),  "minecraft:gray_concrete"),
    ((30,  30,  30),  "minecraft:black_concrete"),
    ((0,   0,   0),   "minecraft:black_concrete"),
]

def color_distance(c1, c2):
    return sum((a - b) ** 2 for a, b in zip(c1, c2))

def nearest_block(r, g, b, a=255):
    if a < 128:
        return "minecraft:air"
    # 白黒画像なので輝度ベースで判定
    brightness = 0.299 * r + 0.587 * g + 0.114 * b
    if brightness > 200:
        return "minecraft:white_concrete"
    elif brightness > 150:
        return "minecraft:light_gray_concrete"
    elif brightness > 100:
        return "minecraft:gray_concrete"
    else:
        return "minecraft:black_concrete"

def main():
    img = Image.open(INPUT_IMAGE).convert("RGBA")
    img = img.resize((BLOCK_SIZE, BLOCK_SIZE), Image.LANCZOS)

    commands = []
    commands.append(f"# GitHub Logo Block Art ({BLOCK_SIZE}x{BLOCK_SIZE})")
    commands.append(f"# コマンド実行位置が左下の角になります")
    commands.append(f"# 壁面（南向き）に生成されます")
    commands.append("")

    block_count = 0
    air_count = 0

    for py in range(BLOCK_SIZE):
        for px in range(BLOCK_SIZE):
            r, g, b, a = img.getpixel((px, py))
            block = nearest_block(r, g, b, a)

            if block == "minecraft:air":
                air_count += 1
                continue

            # 画像の上が y+ 方向、左が x+ 方向（南向きの壁面）
            x = px
            y = BLOCK_SIZE - 1 - py  # 画像Y軸を反転（上が高い）
            z = 0

            commands.append(f"setblock ~{x} ~{y} ~{z} {block}")
            block_count += 1

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path = os.path.join(OUTPUT_DIR, "place.mcfunction")
    with open(output_path, "w") as f:
        f.write("\n".join(commands) + "\n")

    print(f"変換完了!")
    print(f"  画像サイズ: {BLOCK_SIZE}x{BLOCK_SIZE} ブロック")
    print(f"  配置ブロック数: {block_count}")
    print(f"  スキップ(透明): {air_count}")
    print(f"  出力: {output_path}")

    # ブロック使用統計
    block_stats = {}
    for py in range(BLOCK_SIZE):
        for px in range(BLOCK_SIZE):
            r, g, b, a = img.getpixel((px, py))
            block = nearest_block(r, g, b, a)
            block_stats[block] = block_stats.get(block, 0) + 1
    print("\nブロック使用数:")
    for block, count in sorted(block_stats.items(), key=lambda x: -x[1]):
        print(f"  {block}: {count}")

    # プレビュー用のASCIIアート出力
    print(f"\nプレビュー (縮小表示):")
    preview_size = 32
    preview_img = img.resize((preview_size, preview_size // 2), Image.LANCZOS)
    for py in range(preview_size // 2):
        line = ""
        for px in range(preview_size):
            r, g, b, a = preview_img.getpixel((px, py))
            if a < 128:
                line += " "
            else:
                brightness = 0.299 * r + 0.587 * g + 0.114 * b
                if brightness > 200:
                    line += "░"
                elif brightness > 150:
                    line += "▒"
                elif brightness > 100:
                    line += "▓"
                else:
                    line += "█"
        print(f"  {line}")


if __name__ == "__main__":
    main()
