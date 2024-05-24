import pygame
import sys

# 初始化 pygame
pygame.init()

# 設置遊戲窗口
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("RPG Game")

# 加載圖像資源
background = pygame.image.load("background.png")
player_img = pygame.image.load("player.png")

# 創建NPC類
class NPC:
    def __init__(self, name, image_path, x, y, dialog):
        self.name = name
        self.image = pygame.image.load(image_path)
        self.x = x
        self.y = y
        self.rect = self.image.get_rect(topleft=(x, y))
        self.dialog = dialog.split('\n')  # 將對話內容按行分割

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def interact(self):
        return self.dialog

# 創建多個NPC
npcs = [
    NPC("Old Man", "npc.png", 200, 150, "都幾歲了，還不懂得怎麼跟父母相處？\n好吧，既然你們都低聲下氣的問我了，告訴你們也無妨。\n要成為有勇氣能夠和父母表達真正的想法並理性溝通的人，\n你們要通過許多挑戰、學習技能，最後擊敗大魔王！\n首先呢，你們要向一個頑皮的五歲男童請教反抗父母的辦法，去吧！"),
]

# 設置字體
font = pygame.font.Font(None, 36)

# 繪製文本函數
def draw_text(surface, text, position, font, color=(255, 255, 255)):
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, position)

# 繪製對話框函數
def draw_dialog_box(surface, text, font, box_color=(0, 0, 0), text_color=(255, 255, 255)):
    box_width = surface.get_width() - 100
    box_height = 100
    box_x = 50
    box_y = surface.get_height() - 150
    pygame.draw.rect(surface, box_color, (box_x, box_y, box_width, box_height))
    draw_text(surface, text, (box_x + 10, box_y + 10), font, text_color)

# 設置遊戲循環
clock = pygame.time.Clock()
dialog = []
current_line = 0

def main():
    global dialog, current_line
    player_x, player_y = 400, 300  # 初始角色位置

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if dialog and current_line < len(dialog) - 1:
                    current_line += 1
                else:
                    dialog = []
                    current_line = 0

        # 更新遊戲狀態
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_x -= 5
        if keys[pygame.K_RIGHT]:
            player_x += 5
        if keys[pygame.K_UP]:
            player_y -= 5
        if keys[pygame.K_DOWN]:
            player_y += 5

        # 碰撞檢測
        player_rect = pygame.Rect(player_x, player_y, player_img.get_width(), player_img.get_height())
        for npc in npcs:
            if player_rect.colliderect(npc.rect):
                if keys[pygame.K_e]:
                    dialog = npc.interact()
                    current_line = 0

        # 繪製遊戲場景
        screen.blit(background, (0, 0))
        screen.blit(player_img, (player_x, player_y))
        for npc in npcs:
            npc.draw(screen)

        # 顯示對話框
        if dialog:
            draw_dialog_box(screen, dialog[current_line], font)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
