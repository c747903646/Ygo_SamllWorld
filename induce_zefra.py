import xlrd
from pdb import set_trace as st

monsters_xls   = xlrd.open_workbook(r'monsters_zefra.xlsx')
monsters_sheet = monsters_xls.sheet_by_index(0)


### 汇总怪兽信息
monsters_list = []
tag_list      = []


# 此处序号对应xlsx中，怪兽信息所在行数-2
# 手动填写序号，跳过必定不作为中转的怪兽
transit_skip_list = [9, 10] 
# 手动填写序号，跳过必定不作为终端的怪兽
termial_skip_list = [11, 16, 19, 21] 

for i in range(1, monsters_sheet.nrows):
    monster = []

    for j in range(monsters_sheet.ncols):        
        monster.append(monsters_sheet.cell(i, j).value)

        if isinstance(monster[-1], float):
            monster[-1] = int(monster[-1])

    monsters_list.append(monster)


### 比较是否有且仅有一个属性重叠
def comp_ints(monster1, monster2):
    pivor = 0
    for i in range(1, len(monster1)):
        if (monster1[i] == monster2[i]):
            if pivor > 0:
                return 0
            else:
                pivor = i
    return pivor


### 搜索下一级结点
def select_transit(anchors):
    transit_list = []

    for i in range(len(monsters_list)):
        if i not in anchors:
            pivor = comp_ints((monsters_list)[anchors[0]], 
                              monsters_list[i])
            if pivor > 0:
                transit_list.append([i, pivor])

    return transit_list


### 搜索并记录连接路线
link_list = []

for i in range(len(monsters_list)):
    link     = [i]
    transits = select_transit([i] + transit_skip_list)
    termial_skip_list.append(i)

    for j in range(len(transits)):
        transit = transits[j]
        transit.append(select_transit([transit[0]] + termial_skip_list))
        link.append(transit)

    link_list.append(link)


### 打印连接路线
for i in range(len(link_list)):
    link          = link_list[i]
    start_monster = monsters_list[link[0]]

    print("起点：{0}\n".format(start_monster[0]))

    for j in range(1, len(link)):
        transit         = link[j]
        transit_monster = monsters_list[transit[0]]
        transit_pivor   = transit[1]
        terminal_list   = transit[2]

        for k in range(len(terminal_list)):
            termial         = terminal_list[k]
            termial_monster = monsters_list[termial[0]]
            termial_pivor   = termial[1]

            print("{0}({1}{2}) -> {3}({4}{5}, {6}{7}) -> {8}({9}{10})\n".format(start_monster[0], 
                                                                                monsters_sheet.cell(0, transit_pivor).value,
                                                                                start_monster[transit_pivor],
                                                                                transit_monster[0],
                                                                                monsters_sheet.cell(0, transit_pivor).value,
                                                                                transit_monster[transit_pivor],
                                                                                monsters_sheet.cell(0, termial_pivor).value,
                                                                                transit_monster[termial_pivor],
                                                                                termial_monster[0], 
                                                                                monsters_sheet.cell(0, termial_pivor).value,
                                                                                termial_monster[termial_pivor]))

    print('\n')
