import json

# ===== 读取 JSON 数据 =====
with open("data/enchantments.json", encoding="utf-8") as f:
    ENCHANTMENTS = json.load(f)

with open("data/items.json", encoding="utf-8") as f:
    ITEMS = json.load(f)

# ===== 附魔互斥组 =====
MUTEX_GROUPS = [
    ["sharpness", "smite", "bane_of_arthropods"],  # 武器专属
    ["protection", "fire_protection", "blast_protection", "projectile_protection"],  # 防具专属
    ["loyalty", "riptide", "channeling"],  # 三叉戟
    ["infinity", "mending"]  # 弓专属
]

# ===== 工具函数 =====
def choose_from_list(options, title):
    print("\n" + title)
    keys = list(options)
    for i, key in enumerate(keys, 1):
        zh = options[key]["name_zh"] if isinstance(options[key], dict) else options[key]
        print(f"{i}. {zh} ({key})")
    idx = int(input("请输入编号：")) - 1
    return keys[idx]

def choose_multiple(enchant_keys):
    chosen = {}
    while True:
        print("\n请选择附魔（可多选，用逗号分隔）：")
        for i, e in enumerate(enchant_keys, 1):
            print(f"{i}. {ENCHANTMENTS[e]} ({e})")
        raw = input("输入编号：")
        chosen.clear()
        for part in raw.split(","):
            i = int(part.strip()) - 1
            e = enchant_keys[i]
            lvl = int(input(f"输入 {ENCHANTMENTS[e]} 等级："))
            chosen[e] = lvl

        valid, group = check_mutex(chosen)
        if valid:
            break
        print(f"⚠ 选择的附魔互斥！同一组只能选一个：{[ENCHANTMENTS[e] for e in group]}")
    return chosen

def check_mutex(selected):
    for group in MUTEX_GROUPS:
        count = sum(1 for e in selected if e in group)
        if count > 1:
            return False, group
    return True, None

# ===== 主逻辑 =====
def main():
    # 选择物品
    item_id = choose_from_list(ITEMS, "请选择物品")
    allowed_enchants = ITEMS[item_id]["enchants"]

    # 选择附魔（带互斥检查）
    enchants = choose_multiple(allowed_enchants)

    # 输入名字 & 数量
    name = input("\n请输入物品名字（直接回车跳过）：")
    count_str = input("数量（默认1）：")
    count = int(count_str) if count_str.strip() else 1

    # 拼装 give 指令
    enchant_nbt = [f'{{id:"minecraft:{e}",lvl:{lvl}}}' for e,lvl in enchants.items()]
    nbt_parts = []
    if name:
        nbt_parts.append(f'display:{{Name:\'{{"text":"{name}","color":"gold","bold":true}}\'}}')
    if enchant_nbt:
        nbt_parts.append(f'Enchantments:[{",".join(enchant_nbt)}]')

    nbt_str = ",".join(nbt_parts)
    cmd = f'/give @p minecraft:{item_id}{{{nbt_str}}} {count}'

    print("\n🎉 生成的指令：")
    print(cmd)

if __name__ == "__main__":
    main()
