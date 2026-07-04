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
PIXELS_PER_METER = 50
reset_button = pygame.Rect(650, 20, 120, 40)

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
            if reset_button.collidepoint(mouse_x, mouse_y):
                ball_x = 400
                ball_y = 300
                velocity_x = 0
                velocity_y = 0
                mass = 1.0    

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
                old_mass = mass
                mass += 0.5
                velocity_x *= old_mass / mass
                velocity_y *= old_mass / mass
            if event.key == pygame.K_DOWN:
                old_mass = mass
                mass = max(0.5, mass - 0.5)
                velocity_x *= old_mass / mass
                velocity_y *= old_mass / mass
            if event.key == pygame.K_r:
                ball_x = 400
                ball_y = 300
                velocity_x = 0
                velocity_y = 0
                mass = 1.0    

        display_radius = int(ball_radius * (mass ** 0.5))

    if not dragging:
        velocity_y += gravity
        ball_x += velocity_x
        ball_y += velocity_y

        # Floor
        if ball_y + display_radius > 600:
            ball_y = 600 - display_radius
            velocity_y = -velocity_y * 0.7
            velocity_x *= 0.98

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

        pull_x = current_mouse[0] - drag_start_x
        pull_y = current_mouse[1] - drag_start_y
        preview_vx = (pull_x * 0.15) / mass
        preview_vy = (pull_y * 0.15) / mass
        power = (preview_vx ** 2 + preview_vy ** 2) ** 0.5

        launch_speed_preview = power / PIXELS_PER_METER
        power_text = f"Launch speed: {launch_speed_preview:.2f} m/s"
        power_surface = font.render(power_text, True, (255, 255, 0))
        screen.blit(power_surface, (int(ball_x) + display_radius + 10, int(ball_y) - 10))
    display_radius = int(ball_radius * (mass ** 0.5))
    def draw_sphere(surface, x, y, radius, base_color):
        light_x = x - radius * 0.4
        light_y = y - radius * 0.4

        for i in range(radius, 0, -1):
            t = i / radius

            r = int(base_color[0] * t + 255 * (1 - t))
            g = int(base_color[1] * t + 255 * (1 - t))
            b = int(base_color[2] * t + 255 * (1 - t))

            r = min(255, r)
            g = min(255, g)
            b = min(255, b)

            offset_x = int(light_x + (x - light_x) * (1 - t))
            offset_y = int(light_y + (y - light_y) * (1 - t))

            pygame.draw.circle(surface, (r, g, b), (offset_x, offset_y), i)

    draw_sphere(screen, int(ball_x), int(ball_y), display_radius, (200, 40, 40))
    speed = (velocity_x ** 2 + velocity_y ** 2) ** 0.5
    speed_mps = speed / PIXELS_PER_METER
    info_text = f"Mass: {mass:.1f} kg   Speed: {speed_mps:.2f} m/s"
    text_surface = font.render(info_text, True, (255, 255, 255))
    screen.blit(text_surface, (10, 10))

    pygame.draw.rect(screen, (80, 80, 200), reset_button)
    reset_text = font.render("Reset", True, (255, 255, 255))
    screen.blit(reset_text, (reset_button.x + 30, reset_button.y + 10))

    pygame.display.flip()

    clock.tick(60)

pygame.quit()