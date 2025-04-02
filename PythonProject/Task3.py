import pygame


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()

    radius = 5
    mode = (0, 0, 255)  # Blue
    drawing_mode = 'line'
    points = []
    shapes = []


    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 165, 0), (255, 255, 255)]
    selected_color = (0, 0, 255)

    drawing = False
    start_pos = (0, 0)

    while True:
        pressed = pygame.key.get_pressed()
        alt_held = pressed[pygame.K_LALT] or pressed[pygame.K_RALT]
        ctrl_held = pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and ctrl_held:
                    return
                if event.key == pygame.K_F4 and alt_held:
                    return
                if event.key == pygame.K_ESCAPE:
                    return


                if event.key == pygame.K_r:
                    drawing_mode = 'rectangle'
                elif event.key == pygame.K_c:
                    drawing_mode = 'circle'
                elif event.key == pygame.K_l:
                    drawing_mode = 'line'
                elif event.key == pygame.K_e:
                    drawing_mode = 'eraser'

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    start_pos = event.pos
                    drawing = True
                elif event.button == 3:
                    selected_color = colors[(colors.index(selected_color) + 1) % len(colors)]

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and drawing:
                    end_pos = event.pos
                    if drawing_mode == 'rectangle':
                        shapes.append(('rectangle', start_pos, end_pos, selected_color))
                    elif drawing_mode == 'circle':
                        shapes.append(('circle', start_pos, end_pos, selected_color))
                    drawing = False

            if event.type == pygame.MOUSEMOTION and drawing:
                if drawing_mode == 'line':
                    points.append((event.pos, selected_color, radius))
                elif drawing_mode == 'eraser':
                    points.append((event.pos, (0, 0, 0), 20))

        screen.fill((0, 0, 0))


        for shape in shapes:
            if shape[0] == 'rectangle':
                pygame.draw.rect(screen, shape[3],
                                 pygame.Rect(shape[1], (shape[2][0] - shape[1][0], shape[2][1] - shape[1][1])))
            elif shape[0] == 'circle':
                center = ((shape[1][0] + shape[2][0]) // 2, (shape[1][1] + shape[2][1]) // 2)
                radius = max(abs(shape[2][0] - shape[1][0]) // 2, abs(shape[2][1] - shape[1][1]) // 2)
                pygame.draw.circle(screen, shape[3], center, radius)


        for point in points:
            pygame.draw.circle(screen, point[1], point[0], point[2])

        pygame.display.flip()
        clock.tick(60)


main()