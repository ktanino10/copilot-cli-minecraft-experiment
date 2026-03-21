# === 4ビット加算計算機 ===
# レバーでA(0-15)+B(0-15)をリアルタイム計算

kill @e[tag=calc_origin]
scoreboard objectives add calc dummy
scoreboard players set #2 calc 2
scoreboard players set #4 calc 4
scoreboard players set #8 calc 8
scoreboard players set #16 calc 16
summon marker ~ ~ ~ {Tags:["calc_origin"]}

# プラットフォーム
fill ~0 ~0 ~0 ~18 ~0 ~11 smooth_stone
fill ~0 ~1 ~0 ~18 ~3 ~11 air

# 入力Aエリア (赤)
fill ~0 ~0 ~2 ~8 ~0 ~2 red_concrete
fill ~0 ~0 ~4 ~8 ~0 ~4 red_concrete
fill ~0 ~0 ~2 ~0 ~0 ~4 red_concrete
fill ~8 ~0 ~2 ~8 ~0 ~4 red_concrete
# 入力Bエリア (青)
fill ~10 ~0 ~2 ~18 ~0 ~2 blue_concrete
fill ~10 ~0 ~4 ~18 ~0 ~4 blue_concrete
fill ~10 ~0 ~2 ~10 ~0 ~4 blue_concrete
fill ~18 ~0 ~2 ~18 ~0 ~4 blue_concrete
setblock ~9 ~0 ~3 gold_block
# 結果エリア (黄)
fill ~4 ~0 ~8 ~14 ~0 ~8 yellow_concrete
fill ~4 ~0 ~10 ~14 ~0 ~10 yellow_concrete
fill ~4 ~0 ~8 ~4 ~0 ~10 yellow_concrete
fill ~14 ~0 ~8 ~14 ~0 ~10 yellow_concrete
setblock ~9 ~0 ~6 gold_block

# 入力レバー A (8,4,2,1)
setblock ~1 ~1 ~3 lever[face=floor]
setblock ~3 ~1 ~3 lever[face=floor]
setblock ~5 ~1 ~3 lever[face=floor]
setblock ~7 ~1 ~3 lever[face=floor]
# 入力レバー B (8,4,2,1)
setblock ~11 ~1 ~3 lever[face=floor]
setblock ~13 ~1 ~3 lever[face=floor]
setblock ~15 ~1 ~3 lever[face=floor]
setblock ~17 ~1 ~3 lever[face=floor]
setblock ~9 ~1 ~3 oak_sign[rotation=0]{front_text:{messages:['{"text":"+","color":"gold","bold":true}','""','""','""']}}
setblock ~9 ~1 ~6 oak_sign[rotation=0]{front_text:{messages:['{"text":"=","color":"gold","bold":true}','""','""','""']}}

# 出力ランプ (16,8,4,2,1)
setblock ~5 ~1 ~9 redstone_lamp
setblock ~7 ~1 ~9 redstone_lamp
setblock ~9 ~1 ~9 redstone_lamp
setblock ~11 ~1 ~9 redstone_lamp
setblock ~13 ~1 ~9 redstone_lamp

# ラベル
setblock ~4 ~1 ~1 oak_sign[rotation=0]{front_text:{messages:['{"text":"A","color":"red","bold":true}','""','""','""']}}
setblock ~14 ~1 ~1 oak_sign[rotation=0]{front_text:{messages:['{"text":"B","color":"aqua","bold":true}','""','""','""']}}
setblock ~1 ~1 ~4 oak_sign[rotation=0]{front_text:{messages:['{"text":"8","color":"red","bold":true}','""','""','""']}}
setblock ~3 ~1 ~4 oak_sign[rotation=0]{front_text:{messages:['{"text":"4","color":"red","bold":true}','""','""','""']}}
setblock ~5 ~1 ~4 oak_sign[rotation=0]{front_text:{messages:['{"text":"2","color":"red","bold":true}','""','""','""']}}
setblock ~7 ~1 ~4 oak_sign[rotation=0]{front_text:{messages:['{"text":"1","color":"red","bold":true}','""','""','""']}}
setblock ~11 ~1 ~4 oak_sign[rotation=0]{front_text:{messages:['{"text":"8","color":"aqua","bold":true}','""','""','""']}}
setblock ~13 ~1 ~4 oak_sign[rotation=0]{front_text:{messages:['{"text":"4","color":"aqua","bold":true}','""','""','""']}}
setblock ~15 ~1 ~4 oak_sign[rotation=0]{front_text:{messages:['{"text":"2","color":"aqua","bold":true}','""','""','""']}}
setblock ~17 ~1 ~4 oak_sign[rotation=0]{front_text:{messages:['{"text":"1","color":"aqua","bold":true}','""','""','""']}}
setblock ~5 ~2 ~9 oak_sign[rotation=0]{front_text:{messages:['{"text":"16","color":"yellow","bold":true}','""','""','""']}}
setblock ~7 ~2 ~9 oak_sign[rotation=0]{front_text:{messages:['{"text":"8","color":"yellow","bold":true}','""','""','""']}}
setblock ~9 ~2 ~9 oak_sign[rotation=0]{front_text:{messages:['{"text":"4","color":"yellow","bold":true}','""','""','""']}}
setblock ~11 ~2 ~9 oak_sign[rotation=0]{front_text:{messages:['{"text":"2","color":"yellow","bold":true}','""','""','""']}}
setblock ~13 ~2 ~9 oak_sign[rotation=0]{front_text:{messages:['{"text":"1","color":"yellow","bold":true}','""','""','""']}}

tellraw @s [{"text":"[計算機] ","color":"gold","bold":true},{"text":"設置完了！レバーでA,Bを入力するとリアルタイムで計算します","color":"green"}]