import pygame
import sys

def npc_dialog(screen, background, npcs, player_order, npc_name, font, draw_dialog_box, clock):
    npc = next((npc for npc in npcs if npc.name == npc_name), None)
    if npc is None:
        return player_order

    dialog = npc.interact()
    can = npc.interact2()
    options = npc.options
    current_line = 0
    progress = 0
    dialog_speed = 1  # 控制文字显示速度，每隔多少帧显示一个字
    right_order = npc.order == player_order

    running = True
    option_selected = None

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if right_order:
                    if options and option_selected is None:
                        # Check if an option was clicked
                        mouse_pos = pygame.mouse.get_pos()
                        for i, option in enumerate(options):
                            if option['rect'].collidepoint(mouse_pos):
                                option_selected = i
                                break
                    elif option_selected is not None:
                        # Display dialog based on the selected option
                        selected_option = options[option_selected]
                        if selected_option['correct']:
                            if progress < len(dialog[current_line]):
                                progress = len(dialog[current_line])
                            elif current_line < len(dialog) - 1:
                                current_line += 1
                                progress = 0
                            else:
                                running = False
                                return player_order + 1
                        else:
                            if progress < len(can[current_line]):
                                progress = len(can[current_line])
                            elif current_line < len(can) - 1:
                                current_line += 1
                                progress = 0
                            else:
                                running = False
                                return player_order
                else:
                    if can:
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

        # 显示对话框或选项
        if right_order:
            if options and option_selected is None:
                for i, option in enumerate(options):
                    pygame.draw.rect(screen, option['color'], option['rect'])
                    draw_text(screen, option['text'], option['rect'].topleft, font)
            elif option_selected is not None:
                selected_option = options[option_selected]
                if selected_option['correct']:
                    if progress < len(dialog[current_line]):
                        progress += dialog_speed  # 增加显示的字符数
                    draw_dialog_box(screen, dialog[current_line], font, progress=progress)
                else:
                    if progress < len(can[current_line]):
                        progress += dialog_speed  # 增加显示的字符数
                    draw_dialog_box(screen, can[current_line], font, progress=progress)
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
    def __init__(self, name, image_path, x, y, width, height, order, can, dialog, options):
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
        self.options = [{'text': opt['text'], 'correct': opt['correct'], 'rect': pygame.Rect(opt['rect']), 'color': opt['color']} for opt in options]

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def interact(self):
        return self.dialog
    
    def interact2(self):
        return self.can

# 创建多个NPC
npcs = [
    NPC("魔鏡", "魔鏡.png", 150, 150, 500, 300, 1, '你有什麼問題想要問我？', "都幾歲了，還不懂得怎麼跟父母相處？\n好吧，既然你們都低聲下氣的問我了，告訴你們也無妨。\n要成為有勇氣能夠和父母表達真正的想法並理性溝通的人，\n你們要通過許多挑戰、學習技能，最後擊敗大魔王！\n首先呢，你們要向一個<em>五歲的男童</em>請教反抗父母的辦法，去吧！", [
        {'text': '問小新', 'correct': True, 'rect': (300, 400, 200, 50), 'color': (0, 255, 0)},
        {'text': '問功夫熊貓', 'correct': False, 'rect': (300, 460, 200, 50), 'color': (255, 0, 0)},
        {'text': '問鄧不利多', 'correct': False, 'rect': (300, 520, 200, 50), 'color': (255, 0, 0)}
    ]),
    NPC("小新", "小新.jpg", 300, 200, 200, 220, 2, '嘿嘿～大姐姐，妳是來看我的嗎？', "反抗父母？！\n我忍受我爸爸的腳臭味很久了！\n我本來都不敢和他正面對決\n但是！自從我學會了【必殺技】之後，\n我終於成功反抗父母了！\n所以，要反抗父母必須要學會自己一個必殺技\n<em></em>我有一個圓圓胖胖的熊貓好朋友，身懷絕技，\n<em></em>可以向他請教要怎麼培養出最厲害的必殺技！", [
        {'text': '問功夫熊貓', 'correct': True, 'rect': (300, 400, 200, 50), 'color': (0, 255, 0)},
        {'text': '問艾莎', 'correct': False, 'rect': (300, 460, 200, 50), 'color': (255, 0, 0)},
        {'text': '問花媽', 'correct': False, 'rect': (300, 520, 200, 50), 'color': (255, 0, 0)}
    ]),
    # Define other NPCs similarly...
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
    Location("海斗", (431, 23, 25, 40), "有機械方面的問題想問我嗎？"),
    Location("皮卡丘", (505, 90, 25, 40), "皮卡～皮卡～"),
]

# 设置字体
font = pygame.font.Font(None, 36)

def draw_text(screen, text, position, font, color=(0, 0, 0)):
    lines = text.splitlines()
    x, y = position
    for line in lines:
        text_surface = font.render(line, True, color)
        screen.blit(text_surface, (x, y))
        y += text_surface.get_height()

def draw_dialog_box(screen, text, font, progress=0):
    dialog_box = pygame.Rect(50, 450, 700, 100)
    pygame.draw.rect(screen, (255, 255, 255), dialog_box)
    pygame.draw.rect(screen, (0, 0, 0), dialog_box, 2)

    if progress > 0:
        text = text[:progress]
    draw_text(screen, text, (60, 460), font)

def main():
    player_order = 1  # 初始的玩家順序
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for location in locations:
                    if location.rect.collidepoint(mouse_pos):
                        player_order = npc_dialog(screen, map, npcs, player_order, location.name, font, draw_dialog_box, clock)
                        break

        # 绘制游戏场景
        screen.blit(map, (0, 0))

        for location in locations:
            pygame.draw.rect(screen, (0, 0, 255), location.rect)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
