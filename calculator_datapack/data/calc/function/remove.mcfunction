# 計算機撤去
kill @e[tag=calc_origin]
scoreboard objectives remove calc
tellraw @s [{"text":"[計算機] ","color":"gold"},{"text":"撤去しました","color":"yellow"}]