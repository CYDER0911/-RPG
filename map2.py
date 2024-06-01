import pygame
import sys
import subprocess

WHITE =(255,255,255)

player_order = 1  # 全局变量
completed_paths = sys.argv[1:]

# Ensure the current path is marked as completed
if '愛情' not in completed_paths:
    completed_paths.append('愛情')

def get_result3(player_choice):
    if player_choice == '張濬楚' or player_choice == '100':
        return "對！"
    else:
        return "錯！"

lord_background = pygame.image.load("領主背景.png")
lord_background = pygame.transform.scale(lord_background, (800, 600))  # 缩放背景图像以适应窗口尺寸
lord = pygame.image.load("lord.png")
lord = pygame.transform.scale(lord, (500, 400)) 

def lord_b():
    global selected_index
    clock = pygame.time.Clock()
    result = None
    running = True
    options = ['李秉恩', '宋逸恬', '張濬楚', '黃采薇', '林彥廷']
    dialog = "我哈特啦\n玩個遊戲吧".split("\n")
    win_dialog = "\n好啦這次就放過你吧。".split("\n")
    lose_dialog = '\n爛咖！這都能輸！\n就罰你按一百遍滑鼠左鍵好了。開始！\n1\n2\n3\n4\n5\n6\n7\n8\n9\n10\n11\n12\n13\n14\n15\n16\n17\n18\n19\n20\n21\n22\n23\n24\n25\n26\n27\n28\n29\n30\n31\n32\n33\n34\n35\n36\n37\n38\n39\n40\n41\n42\n43\n44\n45\n46\n47\n48\n49\n50\n51\n52\n53\n54\n55\n56\n57\n58\n59\n60\n61\n62\n63\n64\n65\n66\n67\n68\n69\n70\n71\n72\n73\n74\n75\n76\n77\n78\n79\n80\n81\n82\n83\n84\n85\n86\n87\n88\n89\n90\n91\n92\n93\n94\n95\n96\n97\n98\n99\n100\n好啦，走吧！'.split("\n")
    post_result_dialog = win_dialog
    current_line = 0
    progress = 0
    dialog_speed = 1  # 控制文字显示速度，每隔多少帧显示一个字
    dialog_finished = False  # 用于标记对话是否结束
    post_result_dialog_finished = False  # 用于标记结果后的对话是否结束
    player_choice = None
    selected_index = 0
    current_line = 0
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if dialog and not dialog_finished:
                    # 如果有对话在显示，点击屏幕直接显示完整对话或切换到下一句
                    if progress < len(dialog[current_line]):
                        progress = len(dialog[current_line])
                    elif current_line < len(dialog) - 1:
                        current_line += 1
                        progress = 0
                    else:
                        dialog_finished = True  # 对话结束后设置标志
                elif result is not None and not post_result_dialog_finished:
                    if progress < len(post_result_dialog[current_line]):
                        progress = len(post_result_dialog[current_line])
                    elif current_line < len(post_result_dialog) - 1:
                        current_line += 1
                        progress = 0
                    else:
                        return
            elif dialog_finished and result is None:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selected_index = (selected_index - 1) % len(options)
                    elif event.key == pygame.K_DOWN:
                        selected_index = (selected_index + 1) % len(options)
                    elif event.key == pygame.K_RETURN:
                        player_choice = options[selected_index]
                        result = get_result3(player_choice)
                        if result == '錯！':
                            post_result_dialog = lose_dialog

        screen.blit(lord_background, (0, 0))
        screen.blit(lord, (150, 100))

        if dialog and not dialog_finished:
            if progress < len(dialog[current_line]):
                progress += dialog_speed  # 增加显示的字符数
            draw_dialog_box(screen, dialog[current_line], font, progress=progress)
        elif dialog_finished and result is None:
            # 显示选项
            color = WHITE
            draw_dialog_box(screen, "", font, progress=progress)
            draw_text(screen, '下列何者不是本遊戲的作者？', (100, 400), font, color)

            for i, option in enumerate(options):
                color = WHITE
                if i == selected_index:
                    color = (255, 0, 0)  # 高亮显示选中的选项
                draw_text(screen, option, (100, 430 + i * 20), font, color)
        if result is not None and not post_result_dialog_finished:
            if progress < len(post_result_dialog[current_line]):
                progress += dialog_speed  # 增加显示的字符数
            draw_dialog_box(screen, post_result_dialog[current_line], font, progress=progress)



        pygame.display.flip()

    return

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
                    elif player_order != 10:  # 检查是否与第16个NPC交互
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
            draw_dialog_box(screen, '', font, progress=progress)
            for i, option in enumerate(options):
                color = WHITE
                if i == selected_index:
                    color = (255, 0, 0)  # 高亮显示选中的选项
                draw_text(screen, option, (70, 410 + i * 40), font, color)

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
map = pygame.image.load("愛情地圖.jpg")
map = pygame.transform.scale(map, (800, 600))  # 缩放背景图像以适应窗口尺寸
background = pygame.image.load("愛情背景.jpg")
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
    NPC("鄧不利多", "鄧不利多.png", 150, 100, 500, 375, 1, ['你的鬍子也太長了吧點點點', '我想找到愛情！', '哈哈老頭'],'我想找到愛情！', "吼吼吼，welcome to the magic world","讓我來看看...\n恩...聽說，你有一個追不到的女孩...\n好可憐喔...讓我幫你一把吧...\n首先，你應該找一個女生喜歡的東西...\n至於女生喜歡什麼...\n<em></em>去問那個綁著雙馬尾的少女吧..."),   
    NPC("美少女戰士", "美少女戰士.png", 150, 30, 500, 600, 2, ['你知道女生喜歡什麼嗎？', '想看你穿制服的樣子...！', '請跟我交往！'],'你知道女生喜歡什麼嗎？',"我要代替月亮來懲罰你們！", "女生喜歡什麼？(⁰▿⁰)\n我們喜歡的東西可多了(⁰▿⁰)\n最喜歡的當然是芬芳又繽紛的花朵啦(｡◕∀◕｡)!\n不過我這裡沒有花欸(｡ŏ_ŏ)\n這樣好了(⁰▿⁰)\n<em></em>我知道那個家庭主婦很喜歡種花(⁰▿⁰)\n不過她很寶貝自己的植物(⁰▿⁰)\n可能需要帶些東西去跟她交換(⁰▿⁰)<em></em>她特別喜歡吃那個金髮帥哥做的料理(⁰▿⁰)\n如果能幫她帶一份過去，你們一定會成功的(=´ω`=)\n加油喔(⁰▿⁰)"),
    NPC("香吉士", "香吉士.png", 280, 100, 300, 375, 3, ['欸欸所以艾斯把寶藏藏哪了', '我想見識你的惡魔風腳', '我想吃你做的午餐！'],'我想吃你做的午餐！',"美麗的女孩，想看看我的惡魔風腳嗎？", "想吃我做的午餐？!?!\n這可沒那麼容易!!!\n來對抗我的惡魔風腳吧!!!\n(咻咻咻!!!嘣嘣嘣!!!)\n啊!!!!好痛!!!!\n你們居然扛得住我的惡魔風腳!!\n好吧!!!只好把新鮮出爐的惡魔豬腳給你們了!!"),
    NPC("花媽", "花媽.png", 250, 130, 300, 300, 4, ['下次料理小教室可以做烤布蕾嗎', '第三胎會叫李子嗎？', '來吧！這是香吉士做的豬腳'],'來吧！這是香吉士做的豬腳',"Do Re Mi So！", "哎呦威，怎麼會有年輕人來找我啦\n:我們聽說您種了非常多美麗的花!\n蛤，你們想要我種的花喔\n阿可是這是我辛辛苦苦種出來的餒\n阿娘喂，怎麼突然有豬腳的香味\n:這是作為交換帶來的香吉士料理\n哎呀，原來是給我的喔\n好啦好啦，這麼有誠意，我就把花交給你們好了\n(走向陽台)\n這些都是我種的花啦，你們自己選齁\n阿不過，追女孩子不能只有花啦\n沒有包包怎麼可以呢\n<em></em>我平常都是找那個冷冰冰的小女生買包包啦\n記得跟她說你們認識我喔，可以打折餒"),
    NPC("艾莎", "艾莎.png", 300, 100, 250, 375, 5, ['你要不要跟妳妹蓋雪人？', '可以跟你買打折包包嗎？', '你的笑話都很冷嗎？'],'可以跟你買打折包包嗎？', "全部都給我 let it go！", ":你好，是花媽介紹我們過來的!\n花媽?\n:她說可以向你買到打折的包包...\n打折包包?\n:不、不行嗎...\n可以(拿出各種包包)\n:…謝謝...但、但是...\n?\n:其實我不太清楚拿到包包後該怎麼做...\n不知道接下來怎麼做?\n…\n<em></em>有位衝浪少年很有經驗\n:謝、謝謝你!\n…再見"),
    NPC("海斗", "海斗.png", 300, 100, 200, 375, 6, ['拿到包包後要怎麼繼續追女生！', '聽說你和水劍龜有很深的淵源？', '所以你到底喜歡路亞還是采薇？？'],'拿到包包後要怎麼繼續追女生！',"不能撫去女人眼淚的男人，根本不配做男人","喔?你們想知道怎麼得到心上人的愛嗎?\n我還以為你們來找我，是因為你們之中有人被我迷倒了呢\n沒關係，追到女孩子的訣竅可多了\n你們現在做了多少準備呢?\n:我們已經準備好了花和包包!\n天啊!花和包包是甚麼老掉牙的禮物啊\n禮物中沒有從美國進口的高級巧克力的話\n女孩子是不會想理你的\n:真的嗎…可是要去哪裡找到巧克力呢?\n你不知道哪裡可以得到巧克力?\n真是個笨拙青澀的追求者\n<em></em>去找到那位自信的國際美人吧\n可惜你們沒有我這種巧克力色的蜜汁六塊肌\n不然怎麼可能會追不到女孩子呢"),
    NPC("鍾明軒", "鍾明軒.png", 100, 100, 600, 375, 7, ['可以唱煎熬給我聽嗎？', '國際美人的國際巧克力有嗎？', '我才不是酸民。'],'國際美人的國際巧克力有嗎？',"哈囉我是國際美人鍾明軒！", "噢買尬，小帥哥跟我說有人想買巧克力\n原來就是你們喔\n(白眼)\n竟然拖到這種時間才來找我\n如果你們追的是我，我早就跑了\n但看在你們這麼誠懇的拜託我的份上\n我就大發慈悲幫幫你們好了\n來吧，這裡有美國加州德州紐約華盛頓的各種巧克力\n想要甚麼就都拿走吧\n:謝謝!!(將巧克力通通帶走)\n我真是人美心善又大方\n接下來你該去學學你的穿衣打扮了\n請加油改頭換面跟上現在的fashion好嗎\n雖然這件事我也很在行，但現在到我美容覺的時間了\n<em></em>有面鏡子是我比較認可的潮流單品\n它還算有資格作為你穿搭的導師\n去吧"),
    NPC("魔鏡", "魔鏡.png", 150, 150, 500, 300, 8, ['你是一個Fashion Mirror嗎？', '我是不是世界上最帥的人？', '你認識林良鏡嗎？'],'你是一個Fashion Mirror嗎？','你有什麼問題想要問我？', "呀，想學會時尚的穿衣打扮嗎\n你必須先好好地審視一下自己的模樣吧\n::...(盯著鏡子裡的自己)\n你真正的了解自己了嗎?\n看到自己最真實的模樣了嗎?\n:…蛤?\n甚麼?你聽不懂?\n算了，真是朽木不可雕也\n不過，我見到了你眼中正在燃燒的光\n那是充滿了純真與真摯耀眼光芒\n真是打動人心啊\n我就把這些交給你吧\n(獲得亮銀緊身衣)\n(獲得黃金切爾西靴)\n(獲得不鏽鋼安全帽)\n<em></em>接下來就交給那位擁有赤子之心的孩子繼續帶領你吧\n相信你可以成為成熟的大人\n得到一段美好的感情的!"),
    NPC("小新", "小新.jpg", 300, 200, 200, 220, 9, ['你要吃心點嗎？', '擁有赤子之心的人，是你吧！', '橫刀奪愛正男你覺得妥當嗎？'],'擁有赤子之心的人，是你吧！','嘿嘿～大姐姐，妳是來看我的嗎？', "啊哩啊哩，大哥哥你是來找我的嗎?\n:沒錯，我想知道怎麼追到我喜歡的人...\n喔齁齁齁，原來你也在追喜歡的漂亮大姊姊\n可是是誰叫你來的啊?\n:是魔鏡讓我過來的!\n啊!原來是那面會說話的鏡子!\n它是除了春日部防衛隊以外最酷的英雄!\n它一定是想讓我教你怎麼用屁屁走路!\n:...可能是吧?\n(努力向蠟筆小新學習)\n好了!我把我會的都交給你了!\n:小新真的是非常厲害的孩子呢!\n嘿嘿嘿，謝謝誇獎，我也覺得我很厲害喔!\n你也超級厲害的啦!\n你現在可是會用屁屁走路的人!\n<em></em>完成功課後要記得去找那隻厲害的特務交作業喔!"),
    NPC("鴨嘴獸泰瑞", "鴨嘴獸泰瑞.png", 270, 120, 300, 300, 10, ['特~務~P~~~~','帽子給我好嗎？', '我來交作業了！'],'我來交作業了！','什麼！？杜芬舒斯又有新的邪惡計畫了！', "嘎嘎，來讓我看看你們都做了甚麼努力吧\n:這些是我們做好的準備!!\n嘎嘎，有了這麼完善的禮物(看向堆成山的巧克力、盆栽、包包)\n還有這麼齊全的時尚潮流單品(努力躲閃各種金屬的反光)\n看來你們已經做到自己的最好了，嘎嘎\n相信這場告白一定會令人終身難忘的，嘎嘎\n嘎!成功後就會有其他的時空通道開啟\n別忘了繼續你們的拯救行動喔!\n相信你們一定可以的!"),
    NPC("杜芬舒斯", "杜芬舒斯.png", 250, 150, 250, 300, 11, ['啊!是鏡子!', '我不擅長跟爸媽相處...', '誰是世界上最好看的人?'],'我不擅長跟爸媽相處...', "我恨你！鴨嘴獸泰瑞！", "小鬼頭，等你們很久了\n你們以為這麼簡單可以阻止我嗎？\n（拿出手槍指著你）\n哈哈哈！這是我新研發的洗腦終結者，\n你就這樣精神錯亂下去吧哇哈哈！\n(透過矯健的身手躲開了子彈)\n你們…怎麼做到的，我知道了\
        \n一定是鴨嘴獸泰瑞教你們的身法\n我恨你！鴨嘴獸泰瑞！\n(用武器擊敗杜芬舒斯)\n(和杜芬舒斯大戰之後覺得非常躁熱)\n<em></em>(想要冷靜下來繼續學習必殺技)"),
    NPC("多拉A夢", "多拉A夢.png", 200, 0, 450, 600, 12, ['(告訴他二二八事件)', '(告訴他蓋瑞事件)', '(告訴他神龍事件)'],'(告訴他蓋瑞事件)', '大雄～你又怎麼了', "你們是來找美少女戰士要的交通工具嗎？\n我的百寶袋裡面有許多交通工具可以給你們選擇耶\n(選擇任意門)\n好勒，那我就把任意門交給你們吧！\n因為怕月球上危機四伏，你還是讓美少女帶上一位助手吧！\n<em></em>去找那位鴨嘴獸特務吧，他感覺很樂意幫忙"),
    NPC("細菌人", "細菌人.png", 250, 100, 300, 375, 13, ['蓋瑞究竟為甚麼會自殺?', '蓋瑞究竟為甚麼會考不好?', '蓋瑞究竟為甚麼會交不到女朋友?'],'蓋瑞究竟為甚麼會自殺?', "可愛又迷人的反派角色-細菌人！", "嘿嘿，你們想知道蓋瑞自殺的原因嗎？\n但我不想直接告訴你們欸！\n這樣就太無聊了，嘿嘿!\n不然這樣，你知道John走進7-11會變成甚麼嗎?\n:我、我不知道欸\n哈哈哈哈，好笨喔!\n是open John啦!\n嘿嘿，看在你們這麼需要我的份上\n我就告訴你們好了\n蓋瑞是因為鬱悶才自我了結的\n這一切都被他記錄在自己的日記了\n<em></em>同樣身為高中生的那位少年應該會知道日記在哪邊吧\n嘿嘿"),
    NPC("功夫熊貓", "功夫熊貓.png", 280, 90, 250, 375, 14, ['我們想請你用功夫把這張日記解涷!', '我們想請你用功夫把這張日記打敗!', '我們想請你用功夫把這張日記燒掉!'],'我們想請你用功夫把這張日記解涷!',"我是神龍大俠！ㄏㄧ ㄏㄚˋ", "喔?想要利用功夫把日記解凍?\n這對我來說當然是小菜一碟\n(ㄏㄜㄏㄜㄏㄚˋㄏㄧˋ)\n(日記上的冰霜馬上消融了)\n看!我就說這難不倒我吧\n等等\n(從身後掏出一張紙)\n我前幾天也在竹林裡撿到了類似的紙張欸\n看來這也是你們在找的日記吧!\n那就讓你們拿走好了\n(這張日記上面有張少年的背影)\n(旁邊只有一個英文單詞)\n(“LOVE”)\n(原來這就是蓋瑞的祕密嗎?)\n<em></em>(或許可以去找一位母親聊聊)"),
    NPC("蜘蛛人", "蜘蛛人.png", 100, 100, 600, 375, 15, ['啊!是鏡子!', '我不擅長跟爸媽相處...', '誰是世界上最好看的人?'],'我不擅長跟爸媽相處...', "The greater the ability, the greater the responsibility", "WHAT？？你們居然中了細菌人的毒！\n他可是出了名的愛耍賤\n怎麼會上那種小人的當呢？\n哀...現在說再多也於事無補\n你們要解毒那真的是來對地方了\n來，這裡是我的備用血清\n你們快喝下去！\n(咕嚕咕嚕...)\n很好，為了讓解毒過程更加快速\n<em></em>去做些激烈運動加速血液循環吧！\n<em></em>我聽說我們這有很會衝浪的男孩\n快點去找他吧！"),
    NPC("兩津勘吉", "兩津勘吉.png", 250, 100, 250, 375, 16, ['我們想了解菲利爾家裡的案件', '我們想了解菲利爾女朋友的案件', '我們想了解菲利爾學校的案件'],'我們想了解菲利爾學校的案件', "閃啦！閃啦！撞到不負責喔！", "那間學校的案件?\n阿呦，你是說那個自殺事件喔?\n那個死者是一個叫做蓋瑞的男高中生\n他真的是很可憐餒\n在學校只有一個叫做菲力爾的朋友\n不過現在說甚麼也都沒有用了\n如果你們真的想找到拯救蓋瑞的方法\n<em></em>可能只有那面有魔力的鏡子才能回答你們了"),
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
    Location("小新", (360, 330, 60, 70), "嘿嘿～大姐姐，妳是來看我的嗎？"),
    Location("杜芬舒斯", (520, 370, 80, 75), "我恨你！鴨嘴獸泰瑞！"),
    Location("香吉士", (550, 245, 90, 75), "美麗的女孩，想看看我的惡魔風腳嗎？"),
    Location("多拉A夢", (515, 500, 78, 83), "大雄～你又怎麼了？"),
    Location("海斗", (630, 410, 146, 98), "不能撫去女人眼淚的男人，根本不配做男人"),
    Location("鴨嘴獸泰瑞", (165, 390, 72, 75), "什麼！？杜芬舒斯又有新的邪惡計畫了？"),
    Location("細菌人", (455, 40, 55, 75), "可愛又迷人的反派角色-細菌人！"),
    Location("功夫熊貓", (100, 260, 60, 90), "我是神龍大俠！ㄏㄧ ㄏㄚ！"),
    Location("美少女戰士", (95, 80, 140, 85), "我要代替月亮來懲罰你們！"),
    Location("艾莎", (390, 220, 70, 90), "全部都給我 let it go！"),
    Location("鄧不利多", (650, 100, 80, 90), "吼吼吼，welcome to the magic world！"),
    Location("蜘蛛人", (245, 190, 70, 75), "The greater the ability, the greater the responsibility."),
    Location("花媽", (347, 120, 53, 75), "Do Re Mi So！"),
    Location("兩津勘吉", (337, 510, 73, 85), "閃啦！閃啦！撞到不負責喔！"),
    Location("魔鏡", (260, 420, 50, 68), "你想知道誰是世界上最漂亮的女人嗎？"),
    Location("鍾明軒", (30, 480, 140, 90), "哈囉！我是國際美人鍾明軒~"),
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

def draw_transparent_rect(screen, rect, color, alpha):
    # Create a surface with per-pixel alpha
    transparent_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    # Fill the surface with the color and set its alpha
    transparent_surface.fill((*color, alpha))
    # Blit the transparent surface onto the main screen at the rect's position
    screen.blit(transparent_surface, rect.topleft)

def main():
    global dialog, current_scene
    player_order = 1
    lord_b_finish = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for location in locations:
                    if location.rect.collidepoint(mouse_pos):
                        if player_order == 5 and lord_b_finish == False:
                            lord_b()
                            lord_b_finish = True
                        player_order = npc_dialog(screen, background, npcs, player_order, location.name, font, draw_dialog_box, clock)

        # 绘制游戏场景
        screen.blit(map, (0, 0))
        for location in locations:
            draw_transparent_rect(screen, location.rect, (255, 255, 255), 0)  # Draw transparent rectangle

        # 显示对话框
        if dialog:
            draw_dialog_box(screen, dialog, font)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
