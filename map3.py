import pygame
import sys
import subprocess

player_order = 1  # 全局变量

completed_paths = sys.argv[1:]

# Ensure the current path is marked as completed
if '友情' not in completed_paths:
    completed_paths.append('友情')

def npc_dialog(screen, background, npcs, player_order, npc_name, font, draw_dialog_box, clock):
    npc = next((npc for npc in npcs if npc.name == npc_name), None)
    if npc is None:
        return player_order

    dialog = npc.interact()
    can = npc.interact2()
    options = npc.options
    key = npc.key
    current_line = 0
    progress = 0
    dialog_speed = 1  # 控制文字显示速度，每隔多少帧显示一个字
    right_order = npc.order == player_order
    can_finished = False
    dialog_finished = False  # 用于标记结果后的对话是否结束
    player_choice = None
    running = True
    result = None
    selected_index = 0
    WHITE = (255, 255, 255)

    while running:
        if not right_order:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if can and not can_finished:
                        # 如果有对话在显示，点击屏幕直接显示完整对话或切换到下一句
                        if progress < len(can[current_line]):
                            progress = len(can[current_line])
                        elif current_line < len(can) - 1:
                            current_line += 1
                            progress = 0
                        else:
                            can_finished = True  # 对话结束后设置标志
                            return player_order
                
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if can and not can_finished:
                    # 如果有对话在显示，点击屏幕直接显示完整对话或切换到下一句
                    if progress < len(can[current_line]):
                        progress = len(can[current_line])
                    elif current_line < len(can) - 1:
                        current_line += 1
                        progress = 0
                    else:
                        can_finished = True  # 对话结束后设置标志
                elif result is not None and not dialog_finished:
                    if progress < len(dialog[current_line]):
                        progress = len(dialog[current_line])
                    elif current_line < len(dialog) - 1:
                        current_line += 1
                        progress = 0
                    else:
                        dialog_finished = True
                elif dialog_finished:
                    if player_order == 11:  # 检查是否与第16个NPC交互
                                pygame.quit()
                                subprocess.Popen(['python', 'GUI2.py'] + completed_paths)  # 运行新脚本
                                sys.exit()
                    else:
                        return player_order + 1
                else:
                    if can:
                        # 如果有对话在显示，点击屏幕直接显示完整对话或切换到下一句
                        if progress < len(can[current_line]):
                            progress = len(can[current_line])
                        elif current_line < len(can) - 1:
                            current_line += 1
                            progress = 0
                        else:
                            running = False
                            return player_order
                        
            elif can_finished and result is None:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selected_index = (selected_index - 1) % len(options)
                    elif event.key == pygame.K_DOWN:
                        selected_index = (selected_index + 1) % len(options)
                    elif event.key == pygame.K_RETURN:
                        player_choice = options[selected_index]
                        result = get_result2(player_choice, key)
                        if result:
                            dialog = npc.interact()
                        else:
                            dialog = ['我不知道你在說什麼']
                            player_order -= 1
                        dialog_finished = False
                        current_line = 0
                        progress = 0

        screen.blit(background, (0, 0))
        npc.draw(screen)

        if can and not can_finished:
            if progress < len(can[current_line]):
                progress += dialog_speed  # 增加显示的字符数
            draw_dialog_box(screen, can[current_line], font, progress=progress)
        elif can_finished and result is None:
            # 显示选项
            for i, option in enumerate(options):
                color = WHITE
                if i == selected_index:
                    color = (255, 0, 0)  # 高亮显示选中的选项
                draw_text(screen, option, (270, 150 + i * 40), font, color)

        if result is not None and not dialog_finished:
            if progress < len(dialog[current_line]):
                progress += dialog_speed  # 增加显示的字符数
            draw_dialog_box(screen, dialog[current_line], font, progress=progress)

        pygame.display.flip()
        clock.tick(60)

    return player_order

def get_result2(player_choice, key):
    return player_choice == key



# 初始化 pygame
pygame.init()

# 设置游戏窗口
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("RPG Game")

# 加载图像资源
map = pygame.image.load("map.jpg")
map = pygame.transform.scale(map, (800, 600))  # 缩放背景图像以适应窗口尺寸
background = pygame.image.load("人物背景.png")
background = pygame.transform.scale(background, (800, 600))  # 缩放背景图像以适应窗口尺寸

# 创建NPC类
class NPC:
    def __init__(self, name, image_path, x, y, width, height, order, options, key, can, dialog):
        self.name = name
        self.width = width
        self.height = height
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.x = x
        self.y = y
        self.rect = self.image.get_rect(topleft=(x, y))
        self.can = can.split('\n')
        self.dialog = dialog.split('\n')  # 将对话内容按行分割
        self.order = order
        self.options = options
        self.key = key

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def interact(self):
        return self.dialog
    
    def interact2(self):
        return self.can
    
# 创建多个NPC
npcs = [
    NPC("鍾明軒", "鍾明軒.png", 100, 100, 600, 375, 1,  ['菲利爾的學校發生過甚麼嗎?', '我不擅長跟爸媽相處...', '可以推薦我好用的面膜嗎?'],'菲利爾的學校發生過甚麼嗎?', "我是國際美人鐘明軒~", "yeah！ I know！\n你們肯定想從我這裡得到一些八卦right?\n這間學校阿，確實發生過一些差點上社會新聞的事喔\n真是太horrible 了\n至於更多的detail\n<em></em>去找那個粗魯的police officer問吧!"),
    NPC("兩津勘吉", "兩津勘吉.png", 250, 100, 250, 375, 2, ['我們想了解菲利爾家裡的案件', '我們想了解菲利爾女朋友的案件', '我們想了解菲利爾學校的案件'],'我們想了解菲利爾學校的案件', "閃啦！閃啦！撞到不負責喔！", "那間學校的案件?\n阿呦，你是說那個自殺事件喔?\n那個死者是一個叫做蓋瑞的男高中生\n他真的是很可憐餒\n在學校只有一個叫做菲力爾的朋友\n不過現在說甚麼也都沒有用了\n如果你們真的想找到拯救蓋瑞的方法\n<em></em>可能只有那面有魔力的鏡子才能回答你們了"),
    NPC("魔鏡", "魔鏡.png", 150, 150, 500, 300, 3,  ['你知道要怎麼拯救菲利爾嗎?', '你知道要怎麼拯救蓋瑞嗎?', '你知道要怎麼拯救我嗎?'],'你知道要怎麼拯救蓋瑞嗎?','你有什麼問題想要問我？', "拯救蓋瑞...你們想改變過去？\n我很遺憾，這件事沒有你們想的這麼簡單\n你們必須先去調查出完整的前因後果才行\n並且我的魔力並不足以幫上你們\n在你們了解一切後\n<em></em>去找那位比我更擅長施法的偉大魔法師吧！\n至於如何開始調查事件的來龍去脈\n<em></em>我想紫色小壞蛋那邊會有線索的"),
    NPC("細菌人", "細菌人.png", 250, 100, 300, 375, 4, ['蓋瑞究竟為甚麼會自殺?', '蓋瑞究竟為甚麼會考不好?', '蓋瑞究竟為甚麼會交不到女朋友?'],'蓋瑞究竟為甚麼會自殺?', "可愛又迷人的反派角色-細菌人！", "嘿嘿，你們想知道蓋瑞自殺的原因嗎？\n但我不想直接告訴你們欸！\n這樣就太無聊了，嘿嘿!\n不然這樣，你知道John走進7-11會變成甚麼嗎?\n:我、我不知道欸\n哈哈哈哈，好笨喔!\n是open John啦!\n嘿嘿，看在你們這麼需要我的份上\n我就告訴你們好了\n蓋瑞是因為鬱悶才自我了結的\n這一切都被他記錄在自己的日記了\n<em></em>同樣身為高中生的那位少年應該會知道日記在哪邊吧\n嘿嘿"),
    NPC("海斗", "海斗.png", 300, 100, 200, 375, 5, ['你知道蓋瑞的的日記在哪裡嗎?', '你知道蓋瑞的的寶物在哪裡嗎?', '你知道蓋瑞的的朋友在哪裡嗎?'],'你知道蓋瑞的的日記在哪裡嗎?', "不能撫去女人眼淚的男人，根本不配做男人", "日記會在哪裡?\n我自己的日記都會隨身帶著啦\n畢竟上面記滿了女生的電話呢\n不過我有聽說最近有不少人在路上撿到了日記的零散頁面\n<em></em>其中一位甚至是女王的樣子\n我想那應該就是你們要的東西\n想感謝我的話記得晚上打給我喔~\n下次見~"),
    NPC("艾莎", "艾莎.png", 300, 100, 250, 375, 6,  ['你有撿到過剪刀之類的東西嗎...', '你有撿到過日記之類的東西嗎...', '你有撿到過巧克力之類的東西嗎...'],'你有撿到過日記之類的東西嗎...',"全部都給我 let it go！", "我的確是有撿到一張奇怪的紙啦\n原來是別人的日記嗎?\n那上面充滿了兩位少年的合照還有一面旗幟\n記日記的人想必很珍惜彼此之間的感情吧!\n不過後來我不小心將那面日記冰凍了\n<em></em>或許你們可以去找會氣功的動物朋友試著將紙張回復原樣\n給你們吧(遞出日記)"),
    NPC("功夫熊貓", "功夫熊貓.png", 280, 200, 250, 375, 7, ['我們想請你用功夫把這張日記解涷!', '我們想請你用功夫把這張日記打敗!', '我們想請你用功夫把這張日記燒掉!'],'我們想請你用功夫把這張日記解涷!',"我是神龍大俠！ㄏㄧ ㄏㄚˋ", "喔?想要利用功夫把日記解凍?\n這對我來說當然是小菜一碟\n(ㄏㄜㄏㄜㄏㄚˋㄏㄧˋ)\n(日記上的冰霜馬上消融了)\n看!我就說這難不倒我吧\n等等\n(從身後掏出一張紙)\n我前幾天也在竹林裡撿到了類似的紙張欸\n看來這也是你們在找的日記吧!\n那就讓你們拿走好了\n(這張日記上面有張少年的背影)\n(旁邊只有一個英文單詞)\n(“LOVE”)\n(原來這就是蓋瑞的祕密嗎?)\n<em></em>(或許可以去找一位母親聊聊)"),
    NPC("花媽", "花媽.png", 250, 130, 300, 300, 8, ['我們想找你聊聊有關蓋瑞...', '我們想找你吃晚餐', '我們想找你織毛衣'],'我們想找你聊聊有關蓋瑞...', "Do Re Mi So！", "聊聊?\n(將日記交給花媽看看)\n喔買尬，好純情好可愛的少年!\n這種純粹的感情可是青春最珍貴的一部分齁\n蛤?!你說甚麼?!\n這位年輕人自殺了?!?!\n太令人難以置信了!!\n一定還發生了別的事情啦!!\n<em></em>我認識一位雙馬尾的少女也讀同一所學校\n她是富有同情心以及觀察力的少女\n一定知道更多細節啦!"),
    NPC("美少女戰士", "美少女戰士.png", 150, 30, 500, 600, 9, ['或許，你知道小小兵是誰嗎?', '或許，你知道多拉A夢是誰嗎?', '或許，你知道蓋瑞是誰嗎?'],'或許，你知道蓋瑞是誰嗎?', "我要代替月亮來懲罰你們！", "蓋瑞?我知道他\n當我每次回月球出任務時\n他都會默默幫助我完成地球的作業\n但他的靦腆和沉默\n讓他與同學們漸漸有了隔閡\n有一次他將日記遺忘在座位上後\n就被同學翻看了\n他對菲力爾的感情就這樣突然的被曝光\n明明是乾淨而美好的愛\n卻成為了大家茶餘飯後的談資\n我想這就是為甚麼他會獨自消化那些鬱悶吧...\n這些日記竟然被這樣亂丟!!\n太令人生氣了!!\n<em></em>你們去找正義的特務幫忙代替月亮懲罰那些加害者們吧!!\n<em></em>別忘了最終要去找魔法師改變過去喔!!"),
    NPC("鴨嘴獸泰瑞", "鴨嘴獸泰瑞.png", 270, 120, 300, 300, 10, ['(告訴他二二八事件)', '(告訴他蓋瑞事件)', '(告訴他神龍事件)'],'(告訴他蓋瑞事件)', '什麼！？杜芬舒斯又有新的邪惡計畫了！', "嘎嘎，這些人真的是太可惡了!!\n校園霸凌是鴨嘴獸最無法忍受的惡行!!嘎嘎!!\n嘎，這裡有我從邪惡博士那邊沒收的霸凌終結者\n走!我們去收拾那些傢伙!\n(與鴨嘴獸泰瑞一同找到了嘲笑蓋瑞的同學們)\n(並且利用終結者痛扁他們一頓)\n嘎嘎!相信他們都受到應有的懲罰了\n快去你們應該去的地方\n然後將所有事情拉回正軌吧!嘎!"),
    NPC("鄧不利多", "鄧不利多.png", 150, 100, 500, 375, 11,  ['請幫助我們回到過去拯救蓋瑞!', '請幫助我們成為百萬富翁!', '請幫助我們學會魔法!'],'請幫助我們回到過去拯救蓋瑞!',"吼吼吼，welcome to the magic world", "你們想回到過去?\n我可以幫助你們完成這件事\n但在那之前\n菲力爾的自我反省也很重要\n在蓋瑞最需要他的時刻\n菲力爾不僅不在\n也不知道那些在蓋瑞身上發生的殘酷笑罵\n鬱悶與心結必須由當事人解開才行\n(恍然大悟後沉默了下來)\n:...\n:你說的沒錯!\n:我們重來一次的話\n:最重要的並非阻止一切發生\n:而是陪伴蓋瑞度過這一切!!\n:來吧!!\n:我們準備好了!!!\n(一陣眩暈後，大家回到了過去)\n(這次，蓋瑞與菲力爾共同撐過了痛苦的時光)\n(儘管蓋瑞的愛情沒有開花結果)\n(他的臉龐仍然綻放了閃耀的笑容)\n(似乎又有新的時光通道開啟了)"),   
    NPC("香吉士", "香吉士.png", 280, 100, 300, 375, 12, ['啊!是鏡子!', '我不擅長跟爸媽相處...', '誰是世界上最好看的人?'],'我不擅長跟爸媽相處...', "美麗的女孩，想看看我的惡魔風腳嗎？", "「嘎嘎呱嘎嘎，shagalaga，boom~」\n(香吉士被凍住）\n(偷走武器)"),
    NPC("杜芬舒斯", "杜芬舒斯.png", 250, 150, 250, 300, 13, ['啊!是鏡子!', '我不擅長跟爸媽相處...', '誰是世界上最好看的人?'],'我不擅長跟爸媽相處...', "我恨你！鴨嘴獸泰瑞！", "小鬼頭，等你們很久了\n你們以為這麼簡單可以阻止我嗎？\n（拿出手槍指著你）\n哈哈哈！這是我新研發的洗腦終結者，\n你就這樣精神錯亂下去吧哇哈哈！\n(透過矯健的身手躲開了子彈)\n你們…怎麼做到的，我知道了\
        \n一定是鴨嘴獸泰瑞教你們的身法\n我恨你！鴨嘴獸泰瑞！\n(用武器擊敗杜芬舒斯)\n(和杜芬舒斯大戰之後覺得非常躁熱)\n<em></em>(想要冷靜下來繼續學習必殺技)"),
    NPC("蜘蛛人", "蜘蛛人.png", 100, 100, 600, 375, 14, ['啊!是鏡子!', '我不擅長跟爸媽相處...', '誰是世界上最好看的人?'],'我不擅長跟爸媽相處...', "The greater the ability, the greater the responsibility", "WHAT？？你們居然中了細菌人的毒！\n他可是出了名的愛耍賤\n怎麼會上那種小人的當呢？\n哀...現在說再多也於事無補\n你們要解毒那真的是來對地方了\n來，這裡是我的備用血清\n你們快喝下去！\n(咕嚕咕嚕...)\n很好，為了讓解毒過程更加快速\n<em></em>去做些激烈運動加速血液循環吧！\n<em></em>我聽說我們這有很會衝浪的男孩\n快點去找他吧！"),
    NPC("小新", "小新.jpg", 300, 200, 200, 220, 15, ['啊!是鏡子!', '我不擅長跟爸媽相處...', '誰是世界上最好看的人?'],'我不擅長跟爸媽相處...', '嘿嘿～大姐姐，妳是來看我的嗎？', "反抗父母？！\n我忍受我爸爸的腳臭味很久了！\n我本來都不敢和他正面對決\n但是！自從我學會了【必殺技】之後，\n我終於成功反抗父母了！\n所以，要反抗父母必須要學會自己一個必殺技\n<em></em>我有一個圓圓胖胖的熊貓好朋友，身懷絕技，\n<em></em>可以向他請教要怎麼培養出最厲害的必殺技！"),
    NPC("多拉A夢", "多拉A夢.png", 200, 0, 450, 600, 16, ['(告訴他二二八事件)', '(告訴他蓋瑞事件)', '(告訴他神龍事件)'],'(告訴他蓋瑞事件)', '大雄～你又怎麼了', "你們是來找美少女戰士要的交通工具嗎？\n我的百寶袋裡面有許多交通工具可以給你們選擇耶\n(選擇任意門)\n好勒，那我就把任意門交給你們吧！\n因為怕月球上危機四伏，你還是讓美少女帶上一位助手吧！\n<em></em>去找那位鴨嘴獸特務吧，他感覺很樂意幫忙"),
]
# 创建地点类
class Location:
    def __init__(self, name, rect, dialog):
        self.name = name
        self.rect = pygame.Rect(rect) 
        self.dialog = dialog

    def interact(self):
        return self.dialog

# 创建多个地点
locations = [
    Location("小新", (60, 55, 25, 40), "嘿嘿～大姐姐，妳是來看我的嗎？"),
    Location("杜芬舒斯", (283, 17, 25, 40), "我恨你！鴨嘴獸泰瑞！"),
    Location("香吉士", (343, 70, 25, 40), "美麗的女孩，想看看我的惡魔風腳嗎？"),
    Location("多拉A夢", (375, 120, 25, 40), "大雄～你又怎麼了？"),
    Location("海斗", (515, 130, 25, 40), "不能撫去女人眼淚的男人，根本不配做男人"),
    Location("鴨嘴獸泰瑞", (475, 170, 25, 40), "什麼！？杜芬舒斯又有新的邪惡計畫了？"),
    Location("細菌人", (715, 160, 25, 40), "可愛又迷人的反派角色-細菌人！"),
    Location("功夫熊貓", (590, 225, 25, 40), "我是神龍大俠！ㄏㄧ ㄏㄚ！"),
    Location("美少女戰士", (570, 275, 25, 40), "我要代替月亮來懲罰你們！"),
    Location("艾莎", (195, 250, 25, 40), "全部都給我 let it go！"),
    Location("鄧不利多", (195, 350, 25, 40), "吼吼吼，welcome to the magic world！"),
    Location("蜘蛛人", (285, 380, 25, 40), "The greater the ability, the greater the responsibility."),
    Location("花媽", (400, 285, 25, 40), "Do Re Mi So！"),
    Location("兩津勘吉", (720, 305, 25, 40), "閃啦！閃啦！撞到不負責喔！"),
    Location("魔鏡", (485, 455, 25, 40), "你想知道誰是世界上最漂亮的女人嗎？"),
    Location("鍾明軒", (620, 510, 25, 40), "哈囉！我是國際美人鍾明軒~"),
]

# 设置字体
font_path = "SourceHanSansSC-Regular.otf"  # 字体文件的路径
font = pygame.font.Font(font_path, 20)  # 调整字体大小

# 绘制文本函数
def draw_text(surface, text, position, font, color=(255, 255, 255), highlight_color=(255, 0, 0), max_width=None):
    words = text.split(' ')
    space_width, _ = font.size(' ')
    max_width = max_width or surface.get_width()
    x, y = position
    for word in words:
        if '<em>' in word and '</em>' in word:
            word = word.replace('<em>', '').replace('</em>', '')
            word_surface = font.render(word, True, highlight_color)
        else:
            word_surface = font.render(word, True, color)
        word_width, word_height = word_surface.get_size()
        if x + word_width >= max_width:
            x = position[0]  # reset the x
            y += word_height  # start on new row
        surface.blit(word_surface, (x, y))
        x += word_width + space_width
    return y + word_height

# 绘制对话框函数
def draw_dialog_box(surface, text, font, progress=1, box_color=(0, 0, 0), text_color=(255, 255, 255)):
    box_width = surface.get_width() - 100
    box_height = 150  # 增加对话框高度
    box_x = 50
    box_y = surface.get_height() - box_height - 50
    pygame.draw.rect(surface, box_color, (box_x, box_y, box_width, box_height))
    
    max_width = box_x + box_width - 20
    draw_text(surface, text[:progress], (box_x + 10, box_y + 10), font, text_color, max_width=max_width)

# 设置游戏循环
clock = pygame.time.Clock()
dialog = ""
current_scene = None  # 当前场景对象

def main():
    global dialog, current_scene
    player_order = 1
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for location in locations:
                    if location.rect.collidepoint(mouse_pos):
                        player_order = npc_dialog(screen, background, npcs, player_order, location.name, font, draw_dialog_box, clock)

        # 绘制游戏场景
        screen.blit(map, (0, 0))
        for location in locations:
            pygame.draw.rect(screen, (255, 0, 0), location.rect, 2)  # 绘制地点边框

        # 显示对话框
        if dialog:
            draw_dialog_box(screen, dialog, font)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
