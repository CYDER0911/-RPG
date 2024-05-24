# main.py

import pygame
import sys
from npc_dialog import npc_dialog

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
    def __init__(self, name, image_path, x, y, order, can, dialog):
        self.name = name
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (200, 220))
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
    NPC("魔鏡", "魔鏡.png", 200, 150, 1, '你有什麼問題想要問我？', "都幾歲了，還不懂得怎麼跟父母相處？\n好吧，既然你們都低聲下氣的問我了，告訴你們也無妨。\n要成為有勇氣能夠和父母表達真正的想法並理性溝通的人，\n你們要通過許多挑戰、學習技能，最後擊敗大魔王！\n首先呢，你們要向一個<em>五歲的男童</em>請教反抗父母的辦法，去吧！"),
    NPC("小新", "小新.jpg", 200, 150, 2, '嘿嘿～大姐姐，妳是來看我的嗎？', "反抗父母？！\n我忍受我爸爸的腳臭味很久了！\n我本來都不敢和他正面對決\n但是！自從我學會了【必殺技】之後，\n我終於成功反抗父母了！\n所以，要反抗父母必須要學會自己一個必殺技\n<em></em>我有一個圓圓胖胖的熊貓好朋友，身懷絕技，\n<em></em>可以向他請教要怎麼培養出最厲害的必殺技！"),
    NPC("功夫熊貓", "功夫熊貓.png", 280, 200, 3,"我是神龍大俠！ㄏㄧ ㄏㄚˋ", "你們這些小毛頭也想來找我學必殺技嗎？\n你們連最基本的功伕都沒有\n我但看在你們誠懇的份上\n<em></em>你們就先去找我的國際美人朋友\n<em></em>讓他教導你們基本功吧！"),
    NPC("鍾明軒", "鍾明軒.png", 100, 100, 4, "哈囉我是國際美人鍾明軒！", "哎呀～沒想到那熊貓把你們引薦給我\n看來是有點資質呢\n我就來教你們基本功吧！\n這招叫「氣」！\n顧名思義就是要學著控制你們的氣息\n才能好好集氣\n我們開始練功吧！"),
    NPC("魔鏡", "魔鏡.png", 200, 150, 5, '你有什麼問題想要問我？', "都幾歲了，還不懂得怎麼跟父母相處？\n好吧，既然你們都低聲下氣的問我了，告訴你們也無妨。\n要成為有勇氣能夠和父母表達真正的想法並理性溝通的人，\n你們要通過許多挑戰、學習技能，最後擊敗大魔王！\n首先呢，你們要向一個<em>五歲的男童</em>請教反抗父母的辦法，去吧！"),
    NPC("魔鏡", "魔鏡.png", 200, 150, 6, '你有什麼問題想要問我？', "都幾歲了，還不懂得怎麼跟父母相處？\n好吧，既然你們都低聲下氣的問我了，告訴你們也無妨。\n要成為有勇氣能夠和父母表達真正的想法並理性溝通的人，\n你們要通過許多挑戰、學習技能，最後擊敗大魔王！\n首先呢，你們要向一個<em>五歲的男童</em>請教反抗父母的辦法，去吧！"),
    NPC("魔鏡", "魔鏡.png", 200, 150, 7, '你有什麼問題想要問我？', "都幾歲了，還不懂得怎麼跟父母相處？\n好吧，既然你們都低聲下氣的問我了，告訴你們也無妨。\n要成為有勇氣能夠和父母表達真正的想法並理性溝通的人，\n你們要通過許多挑戰、學習技能，最後擊敗大魔王！\n首先呢，你們要向一個<em>五歲的男童</em>請教反抗父母的辦法，去吧！"),
    NPC("魔鏡", "魔鏡.png", 200, 150, 8, '你有什麼問題想要問我？', "都幾歲了，還不懂得怎麼跟父母相處？\n好吧，既然你們都低聲下氣的問我了，告訴你們也無妨。\n要成為有勇氣能夠和父母表達真正的想法並理性溝通的人，\n你們要通過許多挑戰、學習技能，最後擊敗大魔王！\n首先呢，你們要向一個<em>五歲的男童</em>請教反抗父母的辦法，去吧！"),
    NPC("魔鏡", "魔鏡.png", 200, 150, 9, '你有什麼問題想要問我？', "都幾歲了，還不懂得怎麼跟父母相處？\n好吧，既然你們都低聲下氣的問我了，告訴你們也無妨。\n要成為有勇氣能夠和父母表達真正的想法並理性溝通的人，\n你們要通過許多挑戰、學習技能，最後擊敗大魔王！\n首先呢，你們要向一個<em>五歲的男童</em>請教反抗父母的辦法，去吧！"),
    NPC("魔鏡", "魔鏡.png", 200, 150, 10, '你有什麼問題想要問我？', "都幾歲了，還不懂得怎麼跟父母相處？\n好吧，既然你們都低聲下氣的問我了，告訴你們也無妨。\n要成為有勇氣能夠和父母表達真正的想法並理性溝通的人，\n你們要通過許多挑戰、學習技能，最後擊敗大魔王！\n首先呢，你們要向一個<em>五歲的男童</em>請教反抗父母的辦法，去吧！"),
    NPC("魔鏡", "魔鏡.png", 200, 150, 11, '你有什麼問題想要問我？', "都幾歲了，還不懂得怎麼跟父母相處？\n好吧，既然你們都低聲下氣的問我了，告訴你們也無妨。\n要成為有勇氣能夠和父母表達真正的想法並理性溝通的人，\n你們要通過許多挑戰、學習技能，最後擊敗大魔王！\n首先呢，你們要向一個<em>五歲的男童</em>請教反抗父母的辦法，去吧！"),
    NPC("魔鏡", "魔鏡.png", 200, 150, 12, '你有什麼問題想要問我？', "都幾歲了，還不懂得怎麼跟父母相處？\n好吧，既然你們都低聲下氣的問我了，告訴你們也無妨。\n要成為有勇氣能夠和父母表達真正的想法並理性溝通的人，\n你們要通過許多挑戰、學習技能，最後擊敗大魔王！\n首先呢，你們要向一個<em>五歲的男童</em>請教反抗父母的辦法，去吧！"),
    NPC("魔鏡", "魔鏡.png", 200, 150, 13, '你有什麼問題想要問我？', "都幾歲了，還不懂得怎麼跟父母相處？\n好吧，既然你們都低聲下氣的問我了，告訴你們也無妨。\n要成為有勇氣能夠和父母表達真正的想法並理性溝通的人，\n你們要通過許多挑戰、學習技能，最後擊敗大魔王！\n首先呢，你們要向一個<em>五歲的男童</em>請教反抗父母的辦法，去吧！"),
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
