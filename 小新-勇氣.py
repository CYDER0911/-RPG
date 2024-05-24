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
        self.image = pygame.transform.scale(self.image, (200, 220))
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
    NPC("小新", "小新.jpg", 300, 200, "反抗父母？！\n我忍受我爸爸的腳臭味很久了！\n我本來都不敢和他正面對決\n但是！自從我學會了【必殺技】之後，\n我終於成功反抗父母了！\n所以，要反抗父母必須要學會自己一個必殺技\n<em></em>我有一個圓圓胖胖的熊貓好朋友，身懷絕技，\n<em></em>可以向他請教要怎麼培養出最厲害的必殺技！"),
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

# 绘制选项框函数
def draw_options_box(surface, options, font, selected_index):
    box_width = surface.get_width() - 100
    box_height = 150
    box_x = 50
    box_y = surface.get_height() - box_height - 30
    pygame.draw.rect(surface, (255, 255, 255), (box_x, box_y, box_width, box_height))
    
    y = box_y + 10
    for i, option in enumerate(options):
        color = (0, 0, 0) if i != selected_index else (255, 0, 0)
        text_surface = font.render(option, True, color)
        surface.blit(text_surface, (box_x + 10, y))
        y += text_surface.get_height() + 5

# 设置游戏循环
clock = pygame.time.Clock()
dialog = []
current_line = 0
progress = 0
dialog_speed = 1  # 控制文字显示速度，每隔多少帧显示一个字

options = ["請教屁股走路的辦法", "請教捉弄正男的辦法", "請教反抗父母的辦法"]
selected_index = 0
show_options = False
current_npc = None

def main():
    global dialog, current_line, progress, show_options, selected_index, current_npc

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
                elif show_options:
                    if options[selected_index] == "請教反抗父母的辦法":
                        dialog = current_npc.interact()
                    else:
                        dialog = ["嘿嘿～大姐姐，妳是來看我的嗎"]
                    current_line = 0
                    progress = 0
                    show_options = False
                else:
                    # 如果没有对话，检查是否点击了NPC
                    for npc in npcs:
                        if npc.rect.collidepoint(mouse_pos):
                            show_options = True
                            selected_index = 0
                            current_npc = npc

            elif event.type == pygame.KEYDOWN and show_options:
                if event.key == pygame.K_UP:
                    selected_index = (selected_index - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected_index = (selected_index + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    if options[selected_index] == "請教反抗父母的辦法":
                        dialog = current_npc.interact()
                    else:
                        dialog = ["嘿嘿～大姐姐，妳是來看我的嗎"]
                    current_line = 0
                    progress = 0
                    show_options = False

        # 绘制游戏场景
        screen.blit(background, (0, 0))
        for npc in npcs:
            npc.draw(screen)

        # 显示对话框
        if dialog:
            if progress < len(dialog[current_line]):
                progress += dialog_speed  # 增加显示的字符数
            draw_dialog_box(screen, dialog[current_line], font, progress=progress)

        # 显示选项框
        if show_options:
            draw_options_box(screen, options, font, selected_index)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
