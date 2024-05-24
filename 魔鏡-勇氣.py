
import pygame
import sys

# 初始化 pygame
pygame.init()

# 设置游戏窗口
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("RPG Game")

# 加载图像资源
background = pygame.image.load("人物背景.png")
background = pygame.transform.scale(background, (800, 600))  # 缩放背景图像以适应窗口尺寸

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

# 创建多个NPC
npcs = [
    NPC("魔鏡", "魔鏡.png", 150, 150, "都幾歲了，還不懂得怎麼跟父母相處？\n好吧，既然你們都低聲下氣的問我了，告訴你們也無妨。\n要成為有勇氣能夠和父母表達真正的想法並理性溝通的人，\n你們要通過許多挑戰、學習技能，最後擊敗大魔王！\n首先呢，你們要向一個<em>五歲的男童</em>請教反抗父母的辦法，去吧！"),
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
def draw_dialog_box(surface, text, font, box_color=(0, 0, 0), text_color=(255, 255, 255), progress=1):
    box_width = surface.get_width() - 100
    box_height = 150  # 增加对话框高度
    box_x = 50
    box_y = surface.get_height() - box_height - 50
    pygame.draw.rect(surface, box_color, (box_x, box_y, box_width, box_height))
    
    max_width = box_x + box_width - 20
    draw_text(surface, text[:progress], (box_x + 10, box_y + 10), font, text_color, highlight_color=(255, 0, 0), max_width=max_width)

# 设置游戏循环
clock = pygame.time.Clock()
dialog = []
current_line = 0
progress = 0
dialog_speed = 1  # 控制文字显示速度，每隔多少帧显示一个字

def main():
    global dialog, current_line, progress

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if dialog:
                    # 如果有对话在显示，点击屏幕直接显示完整对话或切换到下一句
                    if progress < len(dialog[current_line]):
                        progress = len(dialog[current_line])
                    elif current_line < len(dialog) - 1:
                        current_line += 1
                        progress = 0
                    else:
                        dialog = []
                        current_line = 0
                        progress = 0
                else:
                    # 如果没有对话，检查是否点击了NPC
                    for npc in npcs:
                        if npc.rect.collidepoint(mouse_pos):
                            dialog = npc.interact()
                            current_line = 0
                            progress = 0

        # 绘制游戏场景
        screen.blit(background, (0, 0))
        for npc in npcs:
            npc.draw(screen)

        # 显示对话框
        if dialog:
            if progress < len(dialog[current_line]):
                progress += dialog_speed  # 增加显示的字符数
            draw_dialog_box(screen, dialog[current_line], font, progress=progress)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
