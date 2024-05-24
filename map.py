# main.py

import pygame
import sys
import pygame
import sys

def npc_dialog(screen, background, npcs, player_order, npc_name, font, draw_dialog_box, clock):
    npc = next((npc for npc in npcs if npc.name == npc_name), None)
    if npc is None:
        return player_order

    dialog = npc.interact()
    can = npc.interact2()
    current_line = 0
    progress = 0
    dialog_speed = 1  # 控制文字显示速度，每隔多少帧显示一个字
    right_order = npc.order == player_order

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if right_order:
                    if dialog:
                        # 如果有对话在显示，点击屏幕直接显示完整对话或切换到下一句
                        if progress < len(dialog[current_line]):
                            progress = len(dialog[current_line])
                        elif current_line < len(dialog) - 1:
                            current_line += 1
                            progress = 0
                        else:
                            running = False
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

        # 绘制游戏场景
        screen.blit(background, (0, 0))
        npc.draw(screen)

        # 显示对话框
        if right_order:
            if dialog:
                if progress < len(dialog[current_line]):
                    progress += dialog_speed  # 增加显示的字符数
                draw_dialog_box(screen, dialog[current_line], font, progress=progress)
        else:
            if can:
                if progress < len(can[current_line]):
                    progress += dialog_speed  # 增加显示的字符数
                draw_dialog_box(screen, can[current_line], font, progress=progress)

        pygame.display.flip()
        clock.tick(60)


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
    def __init__(self, name, image_path, x, y, width, height, order, can, dialog):
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

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def interact(self):
        return self.dialog
    
    def interact2(self):
        return self.can
    
# 创建多个NPC
npcs = [
    NPC("魔鏡", "魔鏡.png", 150, 150, 500, 300, 1, '你有什麼問題想要問我？', "都幾歲了，還不懂得怎麼跟父母相處？\n好吧，既然你們都低聲下氣的問我了，告訴你們也無妨。\n要成為有勇氣能夠和父母表達真正的想法並理性溝通的人，\n你們要通過許多挑戰、學習技能，最後擊敗大魔王！\n首先呢，你們要向一個<em>五歲的男童</em>請教反抗父母的辦法，去吧！"),
    NPC("小新", "小新.jpg", 300, 200, 200, 220, 2, '嘿嘿～大姐姐，妳是來看我的嗎？', "反抗父母？！\n我忍受我爸爸的腳臭味很久了！\n我本來都不敢和他正面對決\n但是！自從我學會了【必殺技】之後，\n我終於成功反抗父母了！\n所以，要反抗父母必須要學會自己一個必殺技\n<em></em>我有一個圓圓胖胖的熊貓好朋友，身懷絕技，\n<em></em>可以向他請教要怎麼培養出最厲害的必殺技！"),
    NPC("鴨嘴獸泰瑞", "鴨嘴獸泰瑞.png", 150, 150, 500, 300, 8, '什麼！？杜芬舒斯又有新的邪惡計畫了！', "你們想要我一起和月野兔去月球？\n可是我聽說杜芬舒斯的邪惡計畫了\n如果不阻止他的邪惡計畫\n月球都要不復存在了！\n但你們需要一個打敗他的武器\n武器就在黃毛長腿男的手上。\n他可能不會直接給你，\n記得要使用這個暫停敵人動作的咒語\n「嘎嘎呱嘎嘎，shagalaga，boom~」\n拿到後就直接去打敗邪惡博士吧！"),
    NPC("功夫熊貓", "功夫熊貓.png", 280, 200, 250, 375, 3,"我是神龍大俠！ㄏㄧ ㄏㄚˋ", "你們這些小毛頭也想來找我學必殺技嗎？\n你們連最基本的功伕都沒有\n我但看在你們誠懇的份上\n<em></em>你們就先去找我的國際美人朋友\n<em></em>讓他教導你們基本功吧！"),
    NPC("鍾明軒", "鍾明軒.png", 100, 100, 600, 375, 4, "哈囉我是國際美人鍾明軒！", "哎呀～沒想到那熊貓把你們引薦給我\n看來是有點資質呢\n我就來教你們基本功吧！\n這招叫「氣」！\n顧名思義就是要學著控制你們的氣息\n才能好好集氣\n我們開始練功吧！\
        \n(一陣練功後)....\n哇很好，你們現在已經學會基本功「氣」了\n但功伕哪有這麼簡單！\n<em></em>哼！現在去找那個最愛唸小孩的大媽學其他基本功吧"),
    NPC("多拉A夢", "多拉A夢.png", 150, 150, 500, 300, 7, '大雄～你又怎麼了', "你們是來找美少女戰士要的交通工具嗎？\n我的百寶袋裡面有許多交通工具可以給你們選擇耶\n(選擇任意門)\n好勒，那我就把任意門交給你們吧！\n因為怕月球上危機四伏，你還是讓美少女帶上一位助手吧！\n去找那位鴨嘴獸特務吧，他感覺很樂意幫忙"),
    NPC("香吉士", "香吉士.png", 300, 100, 300, 375, 9, "美麗的女孩，想看看我的惡魔風腳嗎？", "「嘎嘎呱嘎嘎，shagalaga，boom~」\n(香吉士被動住）\n(偷走武器)"),
    NPC("杜芬舒斯", "杜芬舒斯.png", 100, 100, 600, 375, 10, "我恨你！鴨嘴獸泰瑞！", "小鬼頭，等你們很久了\n你們以為這麼簡單可以阻止我嗎？\n（拿出手槍指著你）\n哈哈哈！這是我新研發的洗腦終結者，\n你就這樣精神錯亂下去吧哇哈哈！\n(透過矯健的身手躲開了子彈)\n你們…怎麼做到的，我知道了\
        \n一定是鴨嘴獸泰瑞教你們的身法\n我恨你！鴨嘴獸泰瑞！\n(用武器擊敗杜芬舒斯)\n(和杜芬舒斯大戰之後覺得非常躁熱)\n(想要冷靜下來繼續學習必殺技)"),
    NPC("鄧不利多", "鄧不利多.png", 100, 100, 600, 375, 16, "吼吼吼，welcome to the magic world", "讓我來看看，恩...這是用古老的細菌語寫的呢\n讓我來問問我的水晶球吧\n(一陣魔法施展過後)\n歐！！！！\n水晶球上慢慢浮出了字\n：終於打敗我了呢，引靈者\n：在這趟旅程中你充分展示了勇氣的特質\n：看來你具備能反抗父母的能力了...選擇自己的命運吧\n看來勇氣的問題已經被解決了\n就讓我施展魔法讓你去到其他平行時空\n幫助菲利爾解決其他問題吧！"),
    NPC("艾莎", "艾莎.png", 100, 100, 600, 375, 11, "全部都給我 let it go！", "看來你就是那位剛拯救完月球的勇者吧？\n我聽說了你想幫主一位男孩解決勇氣的問題\n我就來教你們我在冰天雪地中生活習得的耐力吧！\n我的訓練是很辛苦的喔\n我冰雪女王的稱號可不是浪得虛名的\n：有輸過沒怕過拉哈\n好吧，既然你們那麼堅持\
        \n(艾莎一頓瘋狂冰雪輸出)\不錯嘛你們，你們已經得到耐力的真傳了\n是時候展現你們的訓練成果了\n去挑戰那個製造髒亂的大魔王吧！"),
    NPC("細菌人", "細菌人.png", 100, 100, 600, 375, 12, "可愛又迷人的反派角色-細菌人！", "聽說你們想挑戰我啊？！\n啊～～拜託你們饒了我吧~~\n這些糖果給你們吃，拜託你們放過我吧！！\n哈哈哈！中計了你們！！\n你們收下了我的蛀牙小惡魔，被我感染了！\n才能好好集氣\n不趕快找那個被蜘蛛小過的男孩解毒的話你們的小命就不保了"),
    NPC("蜘蛛人", "蜘蛛人.png", 100, 100, 600, 375, 13, "The greater the ability, the greater the responsibility", "WHAT？？你們居然中了細菌人的毒！\n他可是出了名的愛耍賤\n怎麼會上那種小人的當呢？\n哀...現在說再多也於事無補\n你們要解毒那真的是來對地方了\n來，這裡是我的備用血清\n你們快喝下去！\n(咕嚕咕嚕...)\n很好，為了讓解毒過程更加快速\n去做些激烈運動加速血液循環吧！\n我聽說我們這有很會衝浪\n快點去找他吧！"),
    NPC("海斗", "海斗.png", 100, 100, 600, 375, 14, "不能撫去女人眼淚的男人，根本不配做男人", "你們想來學衝浪？？\n你們算個老六阿！憑甚麼要我教你？\n：我有路亞的泳裝照！\n大哥你想從哪開始學...\n(練習完衝浪後，毒終於解掉了)\n你是說，你是被細菌人下毒的嗎？\n這已經是哄騙+詐欺了\n這是可以告的哦\n刑法第987條\n若惡意將他人下毒或欺騙\n依法可以告訴老師，最高判罰站 30秒\n快去找那位警察幫忙解決細菌人吧！"),
    NPC("兩津勘吉", "兩津勘吉.png", 100, 100, 600, 375, 15, "閃啦！閃啦！撞到不負責喔！", "你居然經歷了這般遭遇\n走，我們一起去告死細菌人吧\n(細菌人鋃鐺入獄，最後留下了一封信)\n這是蝦咪東西啊看都看不懂\n但他感覺很有料，要不擬去找那位留著長鬍子的智者幫忙翻譯\n說不定就能讀懂信上的內容了！"),
    NPC("花媽", "花媽.png", 100, 100, 600, 375, 5, "Do Re Mi So！", "小朋友們，真可愛啊，是來請教基本功的嗎？\n讓我來教教你們吧！\n今天，我們要學的是「念！\n現在開始繞口令來練習這項基本功吧！\n(南港展覽館的館長掌管的官方觀光網站綻放萬丈光芒)\n(單槓盪單槓，鋼彈盪鋼彈，單槓盪鋼彈，鋼彈盪單槓，\n鋼彈不給單槓盪，鋼彈硬要盪單槓，鋼彈盪斷單槓。)\
        \n(八百標兵奔北坡，炮兵並排北邊跑，砲兵怕把標兵碰，標兵怕碰標兵炮。)\n看來你們有能力學好念呢，看好囉，我只示範一次。\n(展示念)\n你們已經學會基本功了，回去學會必殺技吧\n<em></em>去把你們學會的功夫展現給那位穿著水手服的美少女吧！"),
    NPC("美少女戰士", "美少女戰士.png", 100, 100, 600, 375, 6, "我要代替月亮來懲罰你們！", "我聽說這地球上有人想學會必殺技？\n看來就是你了\n我當然願意傳授我的獨門必殺技給你\n但我最近沒空ㄟ\n最近月球上出了大事\n我需要可以去月球的交通工具，\n幫忙解決問題才能回來教你們！\n<em></em>說不定藍色狸貓的百寶袋裡會有我要的東西？\n"),
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
