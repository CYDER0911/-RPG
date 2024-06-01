import pygame
import sys
import subprocess

completed_paths = ['勇氣']

completed_paths = sys.argv[1:]

# Ensure the current path is marked as completed
if '勇氣' not in completed_paths:
    completed_paths.append('勇氣')

player_order = 1  # 全局变量

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
                    if player_order == 13:  # 检查是否与第16个NPC交互
                                pygame.quit()
                                subprocess.Popen(['python', 'GUI2.py'] + completed_paths)  # 运行新脚本
                                sys.exit()
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
    NPC("魔鏡", "魔鏡.png", 150, 150, 500, 300, 1, ['啊!是鏡子!', '我不擅長跟爸媽相處...', '誰是世界上最好看的人?'],'我不擅長跟爸媽相處...', '你有什麼問題想要問我？', "都幾歲了，還不懂得怎麼跟父母相處？\n好吧，既然你們都低聲下氣的問我了，告訴你們也無妨。\n要成為有勇氣能夠和父母表達真正的想法並理性溝通的人，\n要先向一個<em>五歲的男童</em>請教反抗父母的辦法，去吧！"),
    NPC("小新", "小新.jpg", 300, 200, 200, 220, 2,['要怎麼反抗父母呢?', '我想追漂亮姐姐！', '小孩，去寫作業。'],'要怎麼反抗父母呢?',  '嘿嘿～大姐姐，妳是來看我的嗎？', "反抗父母？！\n我忍受我爸爸的腳臭味很久了！\n我本來都不敢和他正面對決\n但是！自從我學會了【必殺技】之後，\n我終於成功反抗父母了！\n所以，要反抗父母必須要學會一個必殺技\n<em></em>我有一個圓圓胖胖的熊貓好朋友，身懷絕技，\n<em></em>可以向他請教要怎麼培養出最厲害的必殺技！"),
    NPC("功夫熊貓", "功夫熊貓.png", 280, 200, 250, 375, 3,['你的黑眼圈也太重了吧', '熊貓跟貓熊何者正確?', '可以教我必殺技嗎?'],'可以教我必殺技嗎?', "我是神龍大俠！ㄏㄧ ㄏㄚˋ","你們這些小毛頭也想來找我學必殺技？\n你們連最基本的功伕都沒有\n但看在你們誠懇的份上\n<em></em>你們就先去找我的國際美人朋友\n<em></em>讓他教導你們基本功吧！"),
    NPC("鍾明軒", "鍾明軒.png", 100, 100, 600, 375, 4,['可以唱煎熬給我聽嗎?', '熊貓說你會基本功！', '你好漂亮喔~'],'熊貓說你會基本功！',  "哈囉我是國際美人鍾明軒！", "哎呀～沒想到那熊貓把你們引薦給我\n看來是有點資質呢\n我就來教你們基本功吧！\n這招叫「氣」！\n顧名思義就是要學著控制你們的氣息\n才能好好集氣\n我們開始練功吧！\
        \n(一陣練功後)....\n很好，你們現在已經學會「氣」了!\n去把你們學會的功夫展現給那位穿著水手服的美少女吧！\n相信她能夠帶領你們完成必殺技"),
    NPC("美少女戰士", "美少女戰士.png", 150, 30, 500, 600, 5,['(展示基本功)', '我也來自月球!', '代替月亮懲罰你!'],'(展示基本功)',  "我要代替月亮來懲罰你們！", "看來想學必殺技的人就是你了(❀╹◡╹)\n我當然願意傳授我的獨門必殺技給你(❀╹◡╹)\n但最近月球上出了大事இдஇ\n我必須回去月球解決！\n<em></em>可不可以請你去找藍色狸貓呢?\n他的百寶袋裡會有回到月球的交通工具\n至於必殺技，相信在你們探險的歷程中會自己領悟的!"),
    NPC("多拉A夢", "多拉A夢.png", 200, 0, 450, 600, 6, ['我們需要借用百寶袋...', '你這隻藍色狸貓', '最喜歡竹蜻蜓了!'],'我們需要借用百寶袋...', '大雄～你又怎麼了', "你們是來找美少女戰士要的交通工具嗎？\n可是我有好多種道具可以選擇欸...\n:請給我們能以最快速度抵達月球的工具吧!\n那我就把任意門交給你們吧！\n月球上危機四伏，讓美少女帶上一位助手一起出發比較好喔！\n<em></em>去找那位鴨嘴獸特務吧，他感覺很樂意幫忙"),
    NPC("鴨嘴獸泰瑞", "鴨嘴獸泰瑞.png", 270, 120, 300, 300, 7,['嘎嘎嘎', '能不能請你跟美少女戰士一起回月球呢?', '哈囉綠色鴨子'],'能不能請你跟美少女戰士一起回月球呢?',  '嘎嘎！杜芬舒斯又有新的邪惡計畫了！?', "嘎，你們想要我一起和月野兔去月球？\n可是我聽說杜芬舒斯的邪惡計畫了嘎嘎\n如果不阻止他的邪惡計畫\n月球都要不復存在了嘎嘎！\n這樣好了嘎嘎\n打敗他的武器就在這裡嘎嘎\n<em></em>你們代替我去打敗邪惡博士吧！"),
    NPC("杜芬舒斯", "杜芬舒斯.png", 250, 150, 250, 300, 8,['我們來打敗你了!', '我想應徵邪惡企業', '飛哥小佛又在做甚麼?'],'我們來打敗你了!',  "我恨你！鴨嘴獸泰瑞！", "小鬼頭，等你們很久了\n你們以為這麼簡單可以阻止我嗎？\n（拿出手槍指著你）\n哈哈哈！這是我新研發的洗腦終結者，\n你就這樣精神錯亂下去吧哇哈哈！\n:(透過矯健的身手躲開了子彈)\n你們…怎麼做到的，我知道了\
        \n一定是鴨嘴獸泰瑞教你們的身法\n我恨你！鴨嘴獸泰瑞！\n:(用武器擊敗杜芬舒斯)\n:(和杜芬舒斯大戰之後腦中靈光一閃)\n:將所學實際運用並消化成自己的招式後\n又何妨不是一種獨門必殺技呢?\n<em></em>:(是時候去面對剝奪大家勇氣的髒亂大魔王了)"),
    NPC("細菌人", "細菌人.png", 250, 100, 300, 375, 9,['蛀牙好痛喔嗚嗚嗚', '不用廢話了!挑戰開始!', '你好像需要矯正牙齒'],'不用廢話了!挑戰開始!',  "可愛又迷人的反派角色-細菌人！", "聽說你們想挑戰我啊？！\n嗚嗚嗚我好害怕喔...\n(突然有網子籠罩下來)\n哈哈哈！中計了你們！！\n你們已經被我的蛀牙小惡魔感染了！\n<em></em>不趕快找那個被蜘蛛咬過的男孩解毒的話，你們的小命就不保了"),
    NPC("蜘蛛人", "蜘蛛人.png", 100, 100, 600, 375, 10, ['小辣椒在哪?', '可以跟你借蜘蛛絲嗎?', '中了細菌人的毒怎辦??'],'中了細菌人的毒怎辦??', "The greater the ability, the greater the responsibility",  "WHAT？？你們中了細菌人的毒！\n他可是出了名的愛耍賤\n怎麼會上那種小人的當呢？\n來，這裡是我的備用血清\n你們快喝下去！\n(咕嚕咕嚕...)\n很好，為了讓解毒過程更加快速\n<em></em>去做些激烈運動加速血液循環吧！\n<em></em>我聽說附近有人很會衝浪\n快點去找他吧！"),
    NPC("海斗", "海斗.png", 300, 100, 200, 375, 11,['拜託教我衝浪', '拜託教我追女生', '拜託教我怎麼變帥'],'拜託教我衝浪',  "不能撫去女人眼淚的男人，根本不配做男人", "你們想來學衝浪？？\n你們算甚麼阿！憑甚麼要我教你？\n：我有露亞的泳裝照！\n你想從哪開始學...\n:(練習完衝浪後順利解毒!)\n你說你是被細菌人下毒的？\n這已經是哄騙+詐欺了\n這是可以告的哦\n刑法第987條\n若惡意將他人下毒或欺騙\n依法可以告訴老師，最高判罰站 30秒\n<em></em>快去找那位警察幫忙解決細菌人吧！"),
    NPC("兩津勘吉", "兩津勘吉.png", 250, 100, 250, 375, 12, ['你眼睛上面那是海苔嗎?', '我想告細菌人!', '我的錢包被偷了!'],'我想告細菌人!', "閃啦！閃啦！撞到不負責喔！", "你居然經歷了這款歹誌\n走，我們去告死細菌人\n(細菌人鋃鐺入獄，留下了一封信)\n完蛋了啦!完全看不懂\n但說不定是甚麼重要的線索哩，<em></em>你去找那位留著長鬍子的伯伯幫忙翻譯好了啦\n說不定就能讀懂信上的內容了！"),
    NPC("鄧不利多", "鄧不利多.png", 150, 100, 500, 375, 13,['請問你能翻譯這封信嗎?', '葛來分多加一百分!', '哈哈老頭'],'請問你能翻譯這封信嗎?',  "吼吼吼，welcome to the magic world", "讓我來看看，恩...這是用古老的細菌語寫的呢\n讓我來問問我的水晶球吧\n(一陣魔法施展過後)\n歐！！！！\n水晶球上慢慢浮出了字\n：終於打敗我了呢，引靈者\n：在這趟旅程中你充分展示了勇氣的特質\n：看來你具備能反抗父母的能力了...選擇自己的命運吧\n看來勇氣的問題已經被解決了\n就讓我施展魔法讓你去到其他平行時空\n幫助菲利爾解決其他問題吧！"),   
    NPC("花媽", "花媽.png", 250, 130, 300, 300, 14, ['下次料理小教室可以做烤布蕾嗎', '第三胎會叫李子嗎？', '來吧！這是香吉士做的豬腳'],'來吧！這是香吉士做的豬腳',"Do Re Mi So！", "哎呦威，怎麼會有年輕人來找我啦\n:我們聽說您種了非常多美麗的花!\n蛤，你們想要我種的花喔\n阿可是這是我辛辛苦苦種出來的餒\n阿娘喂，怎麼突然有豬腳的香味\n:這是作為交換帶來的香吉士料理\n哎呀，原來是給我的喔\n好啦好啦，這麼有誠意，我就把花交給你們好了\n(走向陽台)\n這些都是我種的花啦，你們自己選齁\n阿不過，追女孩子不能只有花啦\n沒有包包怎麼可以呢\n<em></em>我平常都是找那個冷冰冰的小女生買包包啦\n記得跟她說你們認識我喔，可以打折餒"),
    NPC("香吉士", "香吉士.png", 280, 100, 300, 375, 15, ['欸欸所以艾斯把寶藏藏哪了', '我想見識你的惡魔風腳', '我想吃你做的午餐！'],'我想吃你做的午餐！',"美麗的女孩，想看看我的惡魔風腳嗎？", "想吃我做的午餐？!?!\n這可沒那麼容易!!!\n來對抗我的惡魔風腳吧!!!\n(咻咻咻!!!嘣嘣嘣!!!)\n啊!!!!好痛!!!!\n你們居然扛得住我的惡魔風腳!!\n好吧!!!只好把新鮮出爐的惡魔豬腳給你們了!!"),
    NPC("艾莎", "艾莎.png", 300, 100, 250, 375, 16, ['你要不要跟妳妹蓋雪人？', '可以跟你買打折包包嗎？', '你的笑話都很冷嗎？'],'可以跟你買打折包包嗎？', "全部都給我 let it go！", ":你好，是花媽介紹我們過來的!\n花媽?\n:她說可以向你買到打折的包包...\n打折包包?\n:不、不行嗎...\n可以(拿出各種包包)\n:…謝謝...但、但是...\n?\n:其實我不太清楚拿到包包後該怎麼做...\n不知道接下來怎麼做?\n…\n<em></em>有位衝浪少年很有經驗\n:謝、謝謝你!\n…再見"),
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
