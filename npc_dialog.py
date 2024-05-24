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
