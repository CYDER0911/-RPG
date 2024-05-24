import pygame
import sys

# 初始化 pygame
pygame.init()

# 设置游戏窗口
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("RPG Game")

# 加载图像资源
map_background = pygame.image.load("background.png")
map_background = pygame.transform.scale(map_background, (800, 600))  # 缩放背景图像以适应窗口尺寸

dumbledore_background = pygame.image.load("人物背景.png")
dumbledore_background = pygame.transform.scale(dumbledore_background, (800, 600))  # 缩放背景图像以适应窗口尺寸

# 设置字体
font_path = "SourceHanSansSC-Regular.otf"  # 字体文件的路径
font = pygame.font.Font(font_path, 28)  # 调整字体大小

# 绘制文本函数
def draw_text(surface, text, position, font, color=(255, 255, 255), max_width=None):
    words = text.split(' ')
    space_width, _ = font.size(' ')
    max_width = max_width or surface.get_width()
    x, y = position
    for word in words:
        word_surface = font.render(word, True, color)
        word_width, word_height = word_surface.get_size()
        if x + word_width >= max_width:
            x = position[0]  # reset the x
            y += word_height  # start on new row
        surface.blit(word_surface, (x, y))
        x += word_width + space_width
    return y + word_height

# 绘制对话框函数
def draw_dialog_box(surface, text, font, box_color=(0, 0, 0), text_color=(255, 255, 255)):
    box_width = surface.get_width() - 100
    box_height = 150  # 增加对话框高度
    box_x = 50
    box_y = surface.get_height() - box_height - 50
    pygame.draw.rect(surface, box_color, (box_x, box_y, box_width, box_height))
    draw_text(surface, text, (box_x + 10, box_y + 10), font, text_color, max_width=box_x + box_width - 20)

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
    Location("蠟筆小新", (60, 55, 25, 40), "嘿嘿～大姐姐，妳是來看我的嗎？"),
    Location("杜芬舒斯", (283, 17, 25, 40), "我恨你！鴨嘴獸泰瑞！"),
    Location("香吉士", (343, 70, 25, 40), "美麗的女孩，想看看我的惡魔風腳嗎？"),
    Location("多拉A夢", (375, 120, 25, 40), "大雄～你又怎麼了？"),
    Location("海斗", (515, 130, 25, 40), "不能撫去女人眼淚的男人，根本不配做男人"),
    Location("鴨嘴獸泰瑞", (475, 170, 25, 40), "什麼！？杜芬舒斯又有新的邪惡計畫了？"),
    Location("細菌人", (715, 160, 25, 40), "可愛又迷人的反派角色-細菌人！"),
    Location("？", (590, 225, 25, 40), "？"),
    Location("？", (570, 275, 25, 40), "？"),
    Location("艾莎", (195, 250, 25, 40), "全部都給我 let it go！"),
    Location("？", (195, 350, 25, 40), "？"),
    Location("蜘蛛人", (285, 380, 25, 40), "The greater the ability, the greater the responsibility."),
    Location("花媽", (400, 285, 25, 40), "Do Re Mi So！"),
    Location("兩津勘吉", (720, 305, 25, 40), "閃啦！閃啦！撞到不負責喔！"),
    Location("魔鏡", (485, 455, 25, 40), "你想知道誰是世界上最漂亮的女人嗎？"),
    Location("鍾明軒", (620, 510, 25, 40), "哈囉！我是國際美人鍾明軒~"),
    Location("鄧不利多", (200, 150, 25, 40), "都幾歲了，還不懂得怎麼跟父母相處？")
]

# 定义场景基类
class Scene:
    def __init__(self):
        self.next_scene = self

    def handle_event(self, event):
        pass

    def update(self):
        pass

    def draw(self, screen):
        pass

# 定义地图场景
class MapScene(Scene):
    def __init__(self):
        super().__init__()
        self.dialog = ""
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for location in locations:
                if location.rect.collidepoint(mouse_pos):
                    self.dialog = location.interact()
                    if location.name == "鄧不利多":  # 切换到新场景
                        self.next_scene = DumbledoreScene()  # 切换到新场景

    def update(self):
        pass

    def draw(self, screen):
        screen.blit(map_background, (0, 0))
        for location in locations:
            pygame.draw.rect(screen, (255, 0, 0), location.rect, 2)  # 绘制地点边框
        if self.dialog:
            draw_dialog_box(screen, self.dialog, font)

# 定义鄧不利多场景
class DumbledoreScene(Scene):
    def __init__(self):
        super().__init__()
        self.dialog = []
        self.current_line = 0
        self.progress = 0
        self.dialog_speed = 1
        self.npcs = [
            NPC("鄧不利多", "鄧不利多.png", 200, 150, "都幾歲了，還不懂得怎麼跟父母相處？\n好吧，既然你們都低聲下氣的問我了，告訴你們也無妨。\n要成為有勇氣能夠和父母表達真正的想法並理性溝通的人，\n你們要通過許多挑戰、學習技能，最後擊敗大魔王！\n首先呢，你們要向一個<em>五歲的男童</em>請教反抗父母的辦法，去吧！")
        ]

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if self.dialog:
                # 如果有对话在显示，点击屏幕直接显示完整对话或切换到下一句
                if self.progress < len(self.dialog[self.current_line]):
                    self.progress = len(self.dialog[self.current_line])
                elif self.current_line < len(self.dialog) - 1:
                    self.current_line += 1
                    self.progress = 0
                else:
                    self.dialog = []
                    self.current_line = 0
                    self.progress = 0
            else:
                # 如果没有对话，检查是否点击了NPC
                for npc in self.npcs:
                    if npc.rect.collidepoint(mouse_pos):
                        self.dialog = npc.interact()
                        self.current_line = 0
                        self.progress = 0

    def update(self):
        if self.dialog and self.progress < len(self.dialog[self.current_line]):
            self.progress += self.dialog_speed

    def draw(self, screen):
        screen.blit(dumbledore_background, (0, 0))
        for npc in self.npcs:
            npc.draw(screen)
        if self.dialog:
            draw_dialog_box(screen, self.dialog[self.current_line], font, progress=self.progress)

# 创建NPC类
class NPC:
    def __init__(self, name, image_path, x, y, dialog):
        self.name = name
        self.image = pygame.image.load(image_path)
        self.x = x
        self.y = y
        self.rect = self.image.get_rect(topleft=(x, y))
        self.dialog = dialog.split('\n')  # 将对话内容按行分割

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def interact(self):
        return self.dialog


