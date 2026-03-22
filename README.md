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

[![GitHub Logo Block Art Demo](https://img.youtube.com/vi/SzhAYqYjIYI/0.jpg)](https://youtu.be/SzhAYqYjIYI)

▶️ [動画を見る](https://youtu.be/SzhAYqYjIYI)

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

[![Tokyo Tower Demo](https://img.youtube.com/vi/YLA5kPAJyoU/0.jpg)](https://youtu.be/YLA5kPAJyoU)

▶️ [動画を見る](https://youtu.be/YLA5kPAJyoU)

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

[![Calculator Demo](https://img.youtube.com/vi/OojzFMah6OU/0.jpg)](https://youtu.be/OojzFMah6OU)

▶️ [動画を見る](https://youtu.be/OojzFMah6OU)

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

#### 4. 🎞️ Octocat GIF アニメーション

GitHub の Octocat（[Octodex](https://octodex.github.com/) の Hula Hoop Octocat）の GIF アニメーションを、Minecraft 内でリアルタイムに再生するデータパック。19枚のフレームが自動でループ再生されます。

| 元の GIF | Minecraft で再生（イメージ） |
|:--------:|:---------------------------:|
| <!-- TODO: GIF画像を追加 --> *画像は後から追加* | <!-- TODO: Minecraft内のスクリーンショットを追加 --> *画像は後から追加* |

<!-- TODO: 動画リンクを追加 -->
<!-- [![Octocat Animation Demo](https://img.youtube.com/vi/XXXXX/0.jpg)](https://youtu.be/XXXXX) -->

- **スクリプト**: [`create_gif_animation.py`](create_gif_animation.py)
- **データパック**: [`octcatmove_datapack/`](octcatmove_datapack/)
- **仕組み**: GIF の各フレームを CIE Lab 色空間 + Floyd-Steinberg ディザリングで 78色のブロックに変換し、`tick.json` + marker entity で自動アニメーション再生
- **使い方**:
  ```
  /reload
  /function octcatmove:place    # セットアップ＆自動再生開始
  /function octcatmove:stop     # 一時停止
  /function octcatmove:start    # 再開
  /function octcatmove:remove   # 撤去
  ```

> ⚠️ **ロゴの使用について**: Octocat / GitHub ロゴは [GitHub Logos and Usage](https://github.com/logos) のガイドラインに従っています。本リポジトリは**非商用・教育目的**での使用であり、GitHub の商標を侵害する意図はありません。Octodex のイラストは [GitHub Octodex](https://octodex.github.com/) からのもので、GitHub, Inc. に帰属します。

---

### 🔧 アニメーション仕組み — 実際のアニメとの比較

#### Minecraft アニメーションの仕組み

```
┌─────────────┐    ┌──────────────┐    ┌──────────────┐
│  GIF 分解    │ →  │ ブロック変換   │ →  │  データパック  │
│  19フレーム   │    │ CIE Lab色空間 │    │  tick.json   │
│  896×896px   │    │ ディザリング   │    │  marker方式  │
└─────────────┘    └──────────────┘    └──────────────┘

[ 再生時の流れ ]
┌──────────┐   tick.json    ┌──────────┐   clone     ┌──────────┐
│ scoreboardl │ ─────────→ │  tick()  │ ────────→  │ 表示壁    │
│ #frame=0  │  毎ティック   │ 3tick待機 │  高速コピー │ 128×128  │
│ #tick=0   │              │ advance() │            │ ブロック  │
└──────────┘              └──────────┘            └──────────┘
```

| 要素 | 実際のアニメーション（映像） | Minecraft アニメーション |
|------|--------------------------|------------------------|
| **フレーム** | セル画 / デジタル画像（24fps が標準） | `.mcfunction` ファイル（1ファイル = 1フレーム） |
| **再生速度** | 1秒24コマ（映画）/ 30fps（TV） | 1秒あたり約6.7コマ（3 tick × 50ms = 150ms/フレーム） |
| **色数** | 1677万色（24bit カラー） | 78色（Minecraft ブロック限定パレット） |
| **色再現** | sRGB / DCI-P3 色空間 | CIE Lab 色空間で最近接ブロック選択 |
| **なめらかさの工夫** | 中割り / トゥイーニング | Floyd-Steinberg ディザリング |
| **フレーム切替** | フィルム送り / デジタルバッファ切替 | `clone` コマンドで格納エリアから一括コピー |
| **ループ制御** | タイムライン / ループ再生 | スコアボード変数でフレーム番号を循環 |
| **透明背景** | アルファチャンネル / クロマキー合成 | フラッドフィル方式で背景色を `air` に変換 |

#### 類似する概念

- **パラパラ漫画と同じ原理**: 人間の目の残像効果（persistence of vision）を利用し、連続する静止画を高速で切り替えることで動きを知覚させます。Minecraft でも同じ原理をブロックの置き換えで実現。
- **スプライトアニメーション**: ゲーム開発で使われるスプライトシート（1枚の画像に全フレームを並べたもの）と同様に、Minecraft では格納エリア（Z=300〜318）に全フレームを事前配置し、`clone` で表示壁にコピーします。
- **ダブルバッファリング**: 映像のちらつき防止技術と同様に、格納エリアから表示壁への `clone` は1ティック内で完了するため、ちらつきなく滑らかに切り替わります。

---

### 🚧 試行錯誤の記録 — 何がうまくいき、何が失敗したか

#### ❌ 失敗した方法: コマンドブロック方式

最初のアプローチでは、`repeating_command_block` を mcfunction ファイル内で `setblock` コマンドにより設置し、アニメーションのティックループを駆動しようとしました。

```mcfunction
# ❌ この構文がMinecraft 1.21+でパースエラーとなり、関数全体がロード失敗
setblock ~-3 ~-1 ~-1 minecraft:repeating_command_block{Command:"function octcatmove:build_step",auto:1b}
```

**失敗の原因**: Minecraft 1.20.5 以降でブロックエンティティのNBT構文が変更され、`setblock` コマンド内のブロックエンティティデータ（`{Command:"...",auto:1b}`）がパースエラーとなりました。結果として `place.mcfunction` のみがロード不可となり、他の関数は正常に表示されるが `place` だけが見つからないという現象が発生しました。

#### ❌ 失敗した方法: RGB ユークリッド距離による色選択

```python
# ❌ RGB空間での距離は人間の色知覚と大きくずれる
d = (r - cr) ** 2 + (g - cg) ** 2 + (b - cb) ** 2
```

| 原画の色 | RGB距離の結果 | 問題 |
|---------|-------------|------|
| 肌色 `RGB(255,220,176)` | → `white_concrete` | 肌色が真っ白に |
| 暗紫灰 `RGB(42,37,47)` | → `gray_concrete` | キャラの体色が灰色に |
| ベージュ `RGB(217,188,156)` | → `white_concrete` | 暖色が全て白に |

#### ✅ 成功した方法: tick.json + marker entity + CIE Lab

| 改善点 | 詳細 |
|--------|------|
| **tick.json 方式** | `data/minecraft/tags/function/tick.json` でティック関数を登録。コマンドブロックを一切使用せず、バージョン互換性が高い |
| **marker entity** | `summon marker` で設置位置を記憶。`execute as @e[tag=...] at @s` で正確な相対座標を実現 |
| **CIE Lab 色空間** | 人間の色知覚に基づく色差計算。肌色 → `end_stone_bricks`、暗紫灰 → `polished_blackstone` と自然な色選択 |
| **Floyd-Steinberg ディザリング** | 量子化誤差を隣接ピクセルに拡散。78色でもグラデーションが滑らかに |
| **パレット拡張** | 56色 → 78色。`blackstone`、`deepslate`、木材系を追加し暗色・肌色域を補強 |

#### 色品質の比較

| 原画の色 | 旧方式（RGB距離） | 新方式（CIE Lab） |
|---------|-------------------|-------------------|
| 肌色 `(255,220,176)` | `white_concrete` ❌ | `end_stone_bricks` ✅ |
| 暗紫灰 `(42,37,47)` | `gray_concrete` ❌ | `polished_blackstone` ✅ |
| ベージュ `(217,188,156)` | `white_concrete` ❌ | `smooth_sandstone` ✅ |
| 暗い茶灰 `(85,75,63)` | `green_concrete` ❌ | `deepslate` ✅ |
| 中間灰 `(150,150,150)` | `light_gray_concrete` | `smooth_stone` ✅ |

---

### 🏫 教育版 Minecraft（Minecraft Education）での可能性

#### 実現可能な部分
- **ブロックアート（静止画）**: 教育版でも `setblock` コマンドは利用可能なため、1フレーム分のブロックアートは再現できます。
- **スコアボードによる変数管理**: 教育版でも `scoreboard` コマンドは利用可能です。
- **基本的な `function` コマンド**: データパックの仕組みは教育版でもサポートされています（ただし Bedrock 版ベースの「ビヘイビアパック」形式）。

#### 課題・制限
- **`clone` コマンドの制限**: 教育版（Bedrock ベース）では `clone` の対象ブロック数に制限がある場合があり、128×128（16,384ブロック）のフレーム一括コピーは失敗する可能性があります。
- **`tick.json` の非対応**: 教育版では Java 版のデータパックの `tick.json` は使えません。代わりに `/tickingarea` や `system` イベントで代替する必要があります。
- **`marker` エンティティの不在**: Bedrock 版には `marker` エンティティが存在しないため、代わりに透明なアーマースタンド等を使う必要があります。
- **パフォーマンス**: 教育版はスペックの低い端末で動作することが多いため、19フレーム × 約4,600ブロック = 約87,000ブロックのデータは重くなる可能性があります。サイズを64×64以下に縮小する等の工夫が必要です。

#### 教育的な活用のアイデア
- **小さなアニメーション（32×32, 4〜8フレーム）** から始めれば教育版でも実現可能
- **プログラミング教育**: 「画像を分解してドット絵にする」「ループで動かす」といった概念を視覚的に学べる
- **数学**: 色空間の変換（RGB → Lab）は座標変換の実例として活用できる
- **アート**: ピクセルアートの制約下での表現は、限られた色数での創造性を育てる

---

### やってみてわかったこと

- Copilot CLI に「GitHubのロゴをMinecraftのブロックにして」と言うだけで、画像処理から `.mcfunction` 生成まで全自動で行えた
- WSL2 上の Copilot CLI から `/mnt/c/` 経由で Minecraft の `datapacks/` に直接コピーでき、ワークフローがシームレスだった
- 建築（東京タワー）、ロジック（計算機）、アート（ロゴ）と幅広いジャンルのデータパックを自然言語だけで生成できた
- **GIF アニメーションの再生**という高度な課題にも、Copilot CLI との対話で試行錯誤しながら到達できた
- **失敗から学ぶプロセス**（コマンドブロック NBT 構文 → tick.json 方式への切り替え）も Copilot CLI が支援してくれた
- CIE Lab 色空間やディザリングといった**画像処理の専門知識**も、Copilot CLI が適切に適用してくれた

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

[![GitHub Logo Block Art Demo](https://img.youtube.com/vi/SzhAYqYjIYI/0.jpg)](https://youtu.be/SzhAYqYjIYI)

▶️ [Watch video](https://youtu.be/SzhAYqYjIYI)

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

[![Tokyo Tower Demo](https://img.youtube.com/vi/YLA5kPAJyoU/0.jpg)](https://youtu.be/YLA5kPAJyoU)

▶️ [Watch video](https://youtu.be/YLA5kPAJyoU)

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

[![Calculator Demo](https://img.youtube.com/vi/OojzFMah6OU/0.jpg)](https://youtu.be/OojzFMah6OU)

▶️ [Watch video](https://youtu.be/OojzFMah6OU)

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

#### 4. 🎞️ Octocat GIF Animation

A datapack that plays the GitHub Octocat ([Octodex](https://octodex.github.com/) Hula Hoop Octocat) GIF animation in real-time inside Minecraft. 19 frames loop automatically.

| Original GIF | Minecraft Playback (Image) |
|:------------:|:--------------------------:|
| <!-- TODO: Add GIF image --> *Image to be added* | <!-- TODO: Add Minecraft screenshot --> *Image to be added* |

<!-- TODO: Add video link -->
<!-- [![Octocat Animation Demo](https://img.youtube.com/vi/XXXXX/0.jpg)](https://youtu.be/XXXXX) -->

- **Script**: [`create_gif_animation.py`](create_gif_animation.py)
- **Datapack**: [`octcatmove_datapack/`](octcatmove_datapack/)
- **How it works**: Converts each GIF frame to blocks using CIE Lab color space + Floyd-Steinberg dithering (78-color palette), then auto-plays animation via `tick.json` + marker entity
- **Usage**:
  ```
  /reload
  /function octcatmove:place    # Setup & auto-play
  /function octcatmove:stop     # Pause
  /function octcatmove:start    # Resume
  /function octcatmove:remove   # Remove
  ```

> ⚠️ **Logo Usage Disclaimer**: Octocat / GitHub logos are used in accordance with the [GitHub Logos and Usage](https://github.com/logos) guidelines. This repository is for **non-commercial, educational purposes only** and does not intend to infringe on GitHub's trademarks. The Octodex illustrations are from [GitHub Octodex](https://octodex.github.com/) and belong to GitHub, Inc.

---

### 🔧 How the Animation Works — Comparison with Real Animation

#### Minecraft Animation Architecture

```
┌──────────────┐    ┌───────────────┐    ┌──────────────┐
│ GIF Decompose │ →  │ Block Convert  │ →  │   Datapack   │
│  19 frames    │    │ CIE Lab color  │    │   tick.json  │
│  896×896px    │    │  Dithering     │    │ marker-based │
└──────────────┘    └───────────────┘    └──────────────┘

[ Playback Flow ]
┌────────────┐   tick.json    ┌──────────┐   clone      ┌──────────┐
│ scoreboard │ ────────────→ │  tick()  │ ──────────→  │ Display  │
│ #frame=0   │  every tick   │ wait 3t  │  fast copy   │  Wall    │
│ #tick=0    │               │ advance()│              │ 128×128  │
└────────────┘               └──────────┘              └──────────┘
```

| Element | Traditional Animation | Minecraft Animation |
|---------|----------------------|---------------------|
| **Frames** | Cel drawings / digital images (24fps standard) | `.mcfunction` files (1 file = 1 frame) |
| **Playback Speed** | 24fps (film) / 30fps (TV) | ~6.7fps (3 ticks × 50ms = 150ms/frame) |
| **Colors** | 16.7M colors (24-bit) | 78 colors (Minecraft block palette) |
| **Color Reproduction** | sRGB / DCI-P3 color space | CIE Lab nearest-block selection |
| **Smoothness Technique** | In-betweening / tweening | Floyd-Steinberg dithering |
| **Frame Switching** | Film advance / digital buffer swap | `clone` command: bulk copy from storage |
| **Loop Control** | Timeline / loop playback | Scoreboard variables cycling frame numbers |
| **Transparent Background** | Alpha channel / chroma key | Flood-fill background detection → `air` blocks |

#### Shared Concepts

- **Flipbook Principle**: Both use *persistence of vision* — rapidly switching static images to create the illusion of motion. Minecraft achieves this by replacing blocks at high speed.
- **Sprite Animation**: Similar to sprite sheets in game development (all frames laid out in one image), Minecraft pre-places all frames in a storage area (Z=300–318) and uses `clone` to copy them to the display wall.
- **Double Buffering**: Just as video systems prevent flicker by writing to an off-screen buffer, the `clone` command completes in a single tick, ensuring smooth, flicker-free frame transitions.

---

### 🚧 Trial and Error — What Worked and What Didn't

#### ❌ Failed Approach: Command Block Method

The initial approach tried to place `repeating_command_block` via `setblock` inside an mcfunction file to drive the animation tick loop.

```mcfunction
# ❌ This syntax causes a parse error in Minecraft 1.21+, making the entire function fail to load
setblock ~-3 ~-1 ~-1 minecraft:repeating_command_block{Command:"function octcatmove:build_step",auto:1b}
```

**Root Cause**: Since Minecraft 1.20.5, block entity NBT syntax in `setblock` commands changed. The `{Command:"...",auto:1b}` data caused a parse error, preventing `place.mcfunction` from loading entirely. Other functions appeared normally — only `place` was missing from autocomplete.

#### ❌ Failed Approach: RGB Euclidean Distance for Color Selection

```python
# ❌ RGB-space distance doesn't match human color perception
d = (r - cr) ** 2 + (g - cg) ** 2 + (b - cb) ** 2
```

| Original Color | RGB Distance Result | Problem |
|---------------|--------------------|---------| 
| Skin tone `RGB(255,220,176)` | → `white_concrete` | Skin turned white |
| Dark purple-gray `RGB(42,37,47)` | → `gray_concrete` | Character body became gray |
| Beige `RGB(217,188,156)` | → `white_concrete` | All warm tones mapped to white |

#### ✅ Successful Approach: tick.json + marker entity + CIE Lab

| Improvement | Details |
|-------------|---------|
| **tick.json method** | Registered tick function via `data/minecraft/tags/function/tick.json`. Zero command blocks — high version compatibility |
| **marker entity** | `summon marker` remembers placement position. `execute as @e[tag=...] at @s` provides accurate relative coordinates |
| **CIE Lab color space** | Perceptually-based color distance. Skin → `end_stone_bricks`, dark purple-gray → `polished_blackstone` |
| **Floyd-Steinberg dithering** | Spreads quantization error to neighboring pixels. Smooth gradients even with 78 colors |
| **Expanded palette** | 56 → 78 colors. Added `blackstone`, `deepslate`, wood planks for better dark and skin tones |

#### Color Quality Comparison

| Original Color | Old Method (RGB) | New Method (CIE Lab) |
|----------------|------------------|---------------------|
| Skin `(255,220,176)` | `white_concrete` ❌ | `end_stone_bricks` ✅ |
| Dark purple-gray `(42,37,47)` | `gray_concrete` ❌ | `polished_blackstone` ✅ |
| Beige `(217,188,156)` | `white_concrete` ❌ | `smooth_sandstone` ✅ |
| Dark brown-gray `(85,75,63)` | `green_concrete` ❌ | `deepslate` ✅ |
| Mid gray `(150,150,150)` | `light_gray_concrete` | `smooth_stone` ✅ |

---

### 🏫 Minecraft Education Edition — Feasibility Assessment

#### What's Possible
- **Block art (still images)**: `setblock` commands work in Education Edition, so single-frame block art is reproducible.
- **Scoreboard variable management**: `scoreboard` commands are available.
- **Basic `function` command**: Datapack functionality is supported (though in Bedrock-based "behavior pack" format).

#### Challenges / Limitations
- **`clone` command limits**: Education Edition (Bedrock-based) may limit the number of blocks that can be cloned at once. A 128×128 frame (16,384 blocks) may fail. Reducing size to 64×64 or smaller is recommended.
- **No `tick.json`**: Education Edition doesn't support Java Edition's `tick.json`. Alternatives include `/tickingarea` or system events.
- **No `marker` entity**: Bedrock Edition lacks the `marker` entity. Invisible armor stands can be used instead.
- **Performance**: Education Edition often runs on lower-spec devices. 19 frames × ~4,600 blocks = ~87,000 blocks may be heavy. Scaling down to 32×32 or fewer frames is advisable.

#### Educational Use Ideas
- **Small animations (32×32, 4–8 frames)** are feasible in Education Edition
- **Programming education**: Concepts like "decomposing images into pixels" and "loop-based animation" become visually tangible
- **Mathematics**: Color space conversion (RGB → Lab) serves as a real-world example of coordinate transformation
- **Art**: Creating under the constraint of limited colors fosters creativity within boundaries

---

### Key Takeaways

- Simply telling Copilot CLI "turn the GitHub logo into Minecraft blocks" produced a complete pipeline from image processing to `.mcfunction` generation
- WSL2's Copilot CLI could directly copy datapacks to Minecraft's `datapacks/` folder via `/mnt/c/`, creating a seamless workflow
- We successfully generated datapacks across diverse categories — architecture (Tokyo Tower), logic (calculator), and art (logo) — all through natural language alone
- **GIF animation playback** — an advanced challenge — was achieved through iterative conversation with Copilot CLI
- The **learning-from-failure process** (command block NBT syntax → tick.json migration) was also guided by Copilot CLI
- Specialized **image processing knowledge** like CIE Lab color spaces and dithering was correctly applied by Copilot CLI

---

## 📝 License

MIT License

> ⚠️ GitHub logo (`GitHub-Mark-ea2971cee799.png`) and Octodex illustrations are trademarks of GitHub, Inc. Used here for **non-commercial, educational purposes only** under [GitHub's logo usage guidelines](https://github.com/logos). The Hula Hoop Octocat is from [GitHub Octodex](https://octodex.github.com/).

## 🔗 参考リンク / References

- [GitHub Copilot CLI Documentation](https://docs.github.com/en/copilot/copilot-cli/using-github-copilot-cli)
- [GitHub CLI](https://cli.github.com/)
- [Minecraft Java Edition Datapacks](https://minecraft.wiki/w/Data_pack)
- [GitHub Logos and Usage Guidelines](https://github.com/logos)
- [Minecraft Wiki - Commands](https://minecraft.wiki/w/Commands)
- [Autodesk Minecraft Workshop Board](https://boards.autodesk.com/ccsjp/%E6%B0%97%E5%88%86%E8%BB%A2%E6%8F%9B/autodeskminecraft)
