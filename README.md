# 🎮 Copilot CLI × Minecraft 実験記録 / Experiment Log

> **GitHub Copilot CLI を使って Minecraft Java Edition のデータパックを自動生成する実験です。**
>
> **This is an experiment using GitHub Copilot CLI to auto-generate Minecraft Java Edition datapacks.**

---

## 📖 目次 / Table of Contents

- [日本語](#-概要)
- [English](#-overview)

---

## 🇯🇵 概要

GitHub Copilot CLI（ターミナル版）に自然言語で指示するだけで、Minecraft Java版で遊べるデータパックを自動生成できることを実証しました。Python スクリプトの作成からデータパックの構築まで、すべて Copilot CLI との対話で完結しています。

### セットアップ

#### 必要なもの

| ツール | バージョン / 備考 |
|--------|------------------|
| [Minecraft Java Edition](https://www.minecraft.net/ja-jp/store/minecraft-java-bedrock-edition-pc) | 1.20.x 以降推奨 |
| [GitHub Copilot CLI](https://docs.github.com/en/copilot/copilot-cli/using-github-copilot-cli) | `gh copilot` コマンド |
| [GitHub CLI (`gh`)](https://cli.github.com/) | 認証済みであること |
| Python 3 + Pillow | 画像変換に使用 |
| WSL2 (Windows の場合) | Linux 環境として使用 |

#### インストール手順

1. **GitHub CLI のインストール**
   - https://cli.github.com/ からダウンロード・インストール
   - `gh auth login` で認証

2. **GitHub Copilot CLI のセットアップ**
   - https://docs.github.com/en/copilot/copilot-cli/using-github-copilot-cli
   - `gh extension install github/gh-copilot` でインストール

3. **Python / Pillow のインストール**（画像変換用）
   ```bash
   pip install Pillow
   ```

4. **Minecraft Java Edition**
   - https://www.minecraft.net/ja-jp/store/minecraft-java-bedrock-edition-pc
   - ワールドの `datapacks/` フォルダにデータパックを配置

#### WSL2 から Minecraft のフォルダにアクセスする方法

WSL2 環境からは `/mnt/c/` 経由で Windows のファイルシステムにアクセスできます：

```bash
# データパックを Minecraft の saves フォルダにコピー
cp -r github_logo_datapack "/mnt/c/Users/<ユーザー名>/AppData/Roaming/.minecraft/saves/<ワールド名>/datapacks/"
```

Windows エクスプローラーからは `\\wsl$\Ubuntu\home\<ユーザー名>\` でWSL内のファイルにもアクセスできます。

---

### 作ったもの

#### 1. 🐙 GitHub ロゴ ブロックアート

GitHub のロゴ画像（PNG）を64×64ブロックのブロックアートに変換するデータパック。

| 入力画像 | Minecraft で生成した結果 |
|:--------:|:-----------------------:|
| <img src="images/GitHub-Mark-ea2971cee799.png" width="200"> | <img src="images/octcat.png" width="400"> |

- **スクリプト**: [`convert_to_mcfunction.py`](convert_to_mcfunction.py)
- **データパック**: [`github_logo_datapack/`](github_logo_datapack/)
- **仕組み**: PNG 画像をピクセル単位で読み取り、明度に応じて白/灰/黒コンクリートの `setblock` コマンドに変換
- **使い方**:
  ```
  /reload
  /function github_logo:place
  ```

> ⚠️ **ロゴの使用について**: GitHub ロゴは [GitHub Logos and Usage](https://github.com/logos) のガイドラインに従っています。本リポジトリは**非商用・教育目的**での使用であり、GitHub の商標を侵害する意図はありません。

#### 2. 🗼 東京タワー

高さ150ブロックの東京タワーを一瞬で建設するデータパック。

<img src="images/tokyotower.png" width="500">

- **スクリプト**: [`create_tokyo_tower.py`](create_tokyo_tower.py)
- **データパック**: [`tokyo_tower_datapack/`](tokyo_tower_datapack/)
- **特徴**:
  - 高さ150ブロック（本体130 + アンテナ20）
  - 赤白の航空障害灯バンド（`orange_concrete` / `white_concrete`）
  - 大展望台（y=55）と特別展望台（y=95）- ガラス張り
  - X字クロスブレース（斜め補強材）
  - ライトアップ（`glowstone`）
  - 避雷針（`lightning_rod`）
- **使い方**:
  ```
  /reload
  /function tokyo_tower:place    # 建設
  /function tokyo_tower:remove   # 撤去
  ```

#### 3. 🔢 4ビット加算計算機

レバー操作でリアルタイムに A(0-15) + B(0-15) を計算する、レッドストーン風データパック計算機。

- **スクリプト**: [`create_calculator.py`](create_calculator.py)
- **データパック**: [`calculator_datapack/`](calculator_datapack/)
- **特徴**:
  - 入力: 8本のレバー（A: 4本, B: 4本）で2進数入力
  - 出力: 5つのレッドストーンランプで2進数表示
  - アクションバーに `A=5 + B=3 = 8` のように10進数で表示
  - 毎tick（1/20秒）で自動計算
- **レイアウト**:
  ```
  [A: 8 4 2 1]  [+]  [B: 8 4 2 1]   ← レバー
                 [=]
         [16  8  4  2  1]             ← ランプ
  ```
- **使い方**:
  ```
  /reload
  /function calc:place    # 設置
  /function calc:remove   # 撤去
  ```

---

### やってみてわかったこと

- Copilot CLI に「GitHubのロゴをMinecraftのブロックにして」と言うだけで、画像処理から `.mcfunction` 生成まで全自動で行えた
- WSL2 上の Copilot CLI から `/mnt/c/` 経由で Minecraft の `datapacks/` に直接コピーでき、ワークフローがシームレスだった
- 建築（東京タワー）、ロジック（計算機）、アート（ロゴ）と幅広いジャンルのデータパックを自然言語だけで生成できた

---

## 🇬🇧 Overview

This project demonstrates that **GitHub Copilot CLI** (terminal version) can auto-generate fully functional **Minecraft Java Edition datapacks** from natural language instructions alone. From Python script creation to datapack construction, everything was done through conversation with Copilot CLI.

### Setup

#### Prerequisites

| Tool | Version / Notes |
|------|----------------|
| [Minecraft Java Edition](https://www.minecraft.net/en-us/store/minecraft-java-bedrock-edition-pc) | 1.20.x or later recommended |
| [GitHub Copilot CLI](https://docs.github.com/en/copilot/copilot-cli/using-github-copilot-cli) | `gh copilot` command |
| [GitHub CLI (`gh`)](https://cli.github.com/) | Must be authenticated |
| Python 3 + Pillow | Used for image conversion |
| WSL2 (on Windows) | Used as Linux environment |

#### Installation

1. **Install GitHub CLI**
   - Download from https://cli.github.com/
   - Authenticate with `gh auth login`

2. **Set up GitHub Copilot CLI**
   - Reference: https://docs.github.com/en/copilot/copilot-cli/using-github-copilot-cli
   - Install with `gh extension install github/gh-copilot`

3. **Install Python / Pillow** (for image conversion)
   ```bash
   pip install Pillow
   ```

4. **Minecraft Java Edition**
   - https://www.minecraft.net/en-us/store/minecraft-java-bedrock-edition-pc
   - Place datapacks in your world's `datapacks/` folder

#### Accessing Minecraft Folders from WSL2

From WSL2, you can access the Windows filesystem via `/mnt/c/`:

```bash
# Copy datapack to Minecraft saves folder
cp -r github_logo_datapack "/mnt/c/Users/<username>/AppData/Roaming/.minecraft/saves/<world_name>/datapacks/"
```

From Windows Explorer, you can also access WSL files at `\\wsl$\Ubuntu\home\<username>\`.

---

### What We Built

#### 1. 🐙 GitHub Logo Block Art

A datapack that converts the GitHub logo (PNG) into a 64×64 block art in Minecraft.

| Input Image | Result in Minecraft |
|:-----------:|:-------------------:|
| <img src="images/GitHub-Mark-ea2971cee799.png" width="200"> | <img src="images/octcat.png" width="400"> |

- **Script**: [`convert_to_mcfunction.py`](convert_to_mcfunction.py)
- **Datapack**: [`github_logo_datapack/`](github_logo_datapack/)
- **How it works**: Reads the PNG image pixel by pixel and converts brightness levels to `setblock` commands using white/gray/black concrete blocks
- **Usage**:
  ```
  /reload
  /function github_logo:place
  ```

> ⚠️ **Logo Usage Disclaimer**: The GitHub logo is used in accordance with the [GitHub Logos and Usage](https://github.com/logos) guidelines. This repository is for **non-commercial, educational purposes only** and does not intend to infringe on GitHub's trademarks.

#### 2. 🗼 Tokyo Tower

A datapack that instantly builds a 150-block tall Tokyo Tower.

<img src="images/tokyotower.png" width="500">

- **Script**: [`create_tokyo_tower.py`](create_tokyo_tower.py)
- **Datapack**: [`tokyo_tower_datapack/`](tokyo_tower_datapack/)
- **Features**:
  - 150 blocks tall (130 body + 20 antenna)
  - Red-white aviation warning bands (`orange_concrete` / `white_concrete`)
  - Main observation deck (y=55) and special observatory (y=95) with glass walls
  - X-shaped cross-bracing (diagonal support beams)
  - Illumination with `glowstone`
  - Lightning rod at the top
- **Usage**:
  ```
  /reload
  /function tokyo_tower:place    # Build
  /function tokyo_tower:remove   # Remove
  ```

#### 3. 🔢 4-bit Addition Calculator

A redstone-style datapack calculator that computes A(0-15) + B(0-15) in real-time using levers.

- **Script**: [`create_calculator.py`](create_calculator.py)
- **Datapack**: [`calculator_datapack/`](calculator_datapack/)
- **Features**:
  - Input: 8 levers (A: 4 bits, B: 4 bits) for binary input
  - Output: 5 redstone lamps showing binary result
  - Action bar displays decimal: `A=5 + B=3 = 8`
  - Auto-calculates every tick (1/20 second)
- **Layout**:
  ```
  [A: 8 4 2 1]  [+]  [B: 8 4 2 1]   ← Levers
                 [=]
         [16  8  4  2  1]             ← Lamps
  ```
- **Usage**:
  ```
  /reload
  /function calc:place    # Place
  /function calc:remove   # Remove
  ```

---

### Key Takeaways

- Simply telling Copilot CLI "turn the GitHub logo into Minecraft blocks" produced a complete pipeline from image processing to `.mcfunction` generation
- WSL2's Copilot CLI could directly copy datapacks to Minecraft's `datapacks/` folder via `/mnt/c/`, creating a seamless workflow
- We successfully generated datapacks across diverse categories — architecture (Tokyo Tower), logic (calculator), and art (logo) — all through natural language alone

---

## 📝 License

MIT License

> ⚠️ GitHub logo (`GitHub-Mark-ea2971cee799.png`) is a trademark of GitHub, Inc. Used here for **non-commercial, educational purposes only** under [GitHub's logo usage guidelines](https://github.com/logos).

## 🔗 参考リンク / References

- [GitHub Copilot CLI Documentation](https://docs.github.com/en/copilot/copilot-cli/using-github-copilot-cli)
- [GitHub CLI](https://cli.github.com/)
- [Minecraft Java Edition Datapacks](https://minecraft.wiki/w/Data_pack)
- [GitHub Logos and Usage Guidelines](https://github.com/logos)
- [Minecraft Wiki - Commands](https://minecraft.wiki/w/Commands)
- [Autodesk Minecraft Workshop Board](https://boards.autodesk.com/ccsjp/%E6%B0%97%E5%88%86%E8%BB%A2%E6%8F%9B/autodeskminecraft)
