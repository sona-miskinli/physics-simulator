import pygame

pygame.init()
font = pygame.font.SysFont(None, 30)

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Physics Simulator")
clock = pygame.time.Clock()

ball_x = 400
ball_y = 300
ball_radius = 20
velocity_x = 0
velocity_y = 0
gravity = 0.5
drag_start_x = 0
drag_start_y = 0
drag_start_time = 0
mass = 1.0

dragging = False

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            distance = ((mouse_x - ball_x) ** 2 + (mouse_y - ball_y) ** 2) ** 0.5
            if distance < ball_radius:
                dragging = True
                velocity_x = 0
                velocity_y = 0
                drag_start_x = mouse_x
                drag_start_y = mouse_y
                drag_start_time = pygame.time.get_ticks()

        if event.type == pygame.MOUSEBUTTONUP:
            if dragging:
                dragging = False
                mouse_x, mouse_y = event.pos
                pull_x = mouse_x - drag_start_x
                pull_y = mouse_y - drag_start_y

                velocity_x = (pull_x * 0.15) / mass
                velocity_y = (pull_y * 0.15) / mass

        if event.type == pygame.MOUSEMOTION:
            if dragging:
                ball_x, ball_y = event.pos

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                mass += 0.5
            if event.key == pygame.K_DOWN:
                mass = max(0.5, mass - 0.5)

        display_radius = int(ball_radius * (mass ** 0.5))

    if not dragging:
        velocity_y += gravity
        ball_x += velocity_x
        ball_y += velocity_y

        # Floor
        if ball_y + display_radius > 600:
            ball_y = 600 - display_radius
            velocity_y = -velocity_y * 0.7

        # Ceiling
        if ball_y - display_radius < 0:
            ball_y = display_radius
            velocity_y = -velocity_y * 0.7

        # Right wall
        if ball_x + display_radius > 800:
            ball_x = 800 - display_radius
            velocity_x = -velocity_x * 0.7

        # Left wall
        if ball_x - display_radius < 0:
            ball_x = display_radius
            velocity_x = -velocity_x * 0.7

    screen.fill((30, 30, 30))

    if dragging:
        current_mouse = pygame.mouse.get_pos()
        pygame.draw.line(screen, (255, 255, 0), (drag_start_x, drag_start_y), current_mouse, 3)
    display_radius = int(ball_radius * (mass ** 0.5))
    pygame.draw.circle(screen, (255, 100, 100), (int(ball_x), int(ball_y)), display_radius)
    speed = (velocity_x ** 2 + velocity_y ** 2) ** 0.5
    info_text = f"Mass: {mass:.1f}   Speed: {speed:.1f}"
    text_surface = font.render(info_text, True, (255, 255, 255))
    screen.blit(text_surface, (10, 10))
    pygame.display.flip()

    clock.tick(60)

pygame.quit()