import pygame


class Fighter():
    def __init__(self, fighter,  x, y, flip, data, sprite_sheet, animation_steps, sound):
        self.fighter = fighter
        self.size_x = data[0]
        self.size_y = data[1]
        self.image_scale = data[2]
        self.offset = data[3]
        self.animation_list = self.load_animation_images(
            sprite_sheet, animation_steps)
        self.action = 0  # 0:idle 1:run 2:jump 3:attack1 4:attack2 5:hit 6:death
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        # getting timestamp of at that moment
        self.update_time = pygame.time.get_ticks()
        self.rect = pygame.Rect((x, y, 80, 180))
        self.velocity_y = 0
        self.running = False
        self.jump = False
        self.attack_type = 0
        self.attack_reset = 0
        self.attacking = False
        self.attack_sound = sound
        self.health = 100
        self.alive = True
        self.hit = False
        self.flip = flip  # To face opponent being on either side of him

    def show(self, surface):
        img = pygame.transform.flip(
            self.image, self.flip, False)  # flipped img
        surface.blit(img, (self.rect.x -
                     (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))

    # updating action sequence
    def update_action(self, new_action):
        # check if the new action is different to previous one
        if new_action != self.action:
            self.action = new_action
            # update animation
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def load_animation_images(self, sprite_sheet, animation_steps):
        # Extract image from spritesheet
        animation_list = []
        i = 0
        for animation in animation_steps:
            temp_img_list = []
            for j in range(animation):
                # i * self.size => ekta animation row er protita member er starting location 162 unit por por hobe... j * self.size => ek row shesh e arekrow jete hobe, okhaneo 162 unit kore shift hobe. 162 is example of an image size
                temp_img = sprite_sheet.subsurface(
                    j * self.size_x, i * self.size_y, self.size_x, self.size_y)
                temp_img_scaled = pygame.transform.scale(
                    temp_img, (self.size_x * self.image_scale, self.size_y * self.image_scale))
                temp_img_list.append(temp_img_scaled)
            animation_list.append(temp_img_list)
            i += 1

        return animation_list

    def movement(self, screen_width, screen_height, target, round_over, pause):
        # Initially
        DISPLACE = 25
        GRAVITY = 4
        dx = 0
        dy = 0
        self.running = False
        self.attack_type = 0

        # Movement er jonno key press
        key = pygame.key.get_pressed()

        # All functions paused while attacking
        if self.attacking == False and self.alive == True and round_over == False and pause == False:
            # check fighter 1 controls
            if self.fighter == 1:

                # MOVEMENT
                if key[pygame.K_a]:
                    dx = -DISPLACE
                    self.running = True
                if key[pygame.K_d]:
                    dx = DISPLACE
                    self.running = True

                # JUMPING
                if key[pygame.K_w] and self.jump == False:
                    self.velocity_y = -40
                    self.jump = True

                # ATTACKS
                if key[pygame.K_r] or key[pygame.K_t]:
                    self.attack(target)
                    # which keys used for attack
                    if key[pygame.K_r]:
                        self.attack_type = 1
                    if key[pygame.K_t]:
                        self.attack_type = 2

            # check fighter 2 controls
            if self.fighter == 2:

                # MOVEMENT
                if key[pygame.K_LEFT]:
                    dx = -DISPLACE
                    self.running = True
                if key[pygame.K_RIGHT]:
                    dx = DISPLACE
                    self.running = True

                # JUMPING
                if key[pygame.K_UP] and self.jump == False:
                    self.velocity_y = -40
                    self.jump = True

                # ATTACKS
                if key[pygame.K_KP1] or key[pygame.K_KP2]:
                    self.attack(target)
                    # which keys used for attack
                    if key[pygame.K_KP1]:
                        self.attack_type = 1
                    if key[pygame.K_KP2]:
                        self.attack_type = 2

        # Gravity effect
        self.velocity_y += GRAVITY

        dy += self.velocity_y

        # Player stays on screen limit
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > screen_width:
            dx = screen_width - self.rect.right

        # Player stays on the ground
        if self.rect.bottom + dy > screen_height - 120:
            self.velocity_y = 0
            self.jump = False
            dy = screen_height - 120 - self.rect.bottom

        # player jeno always opponent ke face kore
        if target.rect.centerx > self.rect.centerx:
            self.flip = False
        else:
            self.flip = True

        # apply attack reset
        if self.attack_reset > 0:
            self.attack_reset -= 1

        # update player position
        self.rect.x += dx
        self.rect.y += dy

    # animation update

    def animation_update(self):
        # check which animation sequence to run
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.update_action(6)  # death
        elif self.hit == True:
            self.update_action(5)  # hit
        elif self.attacking == True:
            if self.attack_type == 1:
                self.update_action(3)  # attack1
            elif self.attack_type == 2:
                self.update_action(4)  # attack2
        elif self.jump == True:
            self.update_action(2)  # jump
        elif self.running == True:
            self.update_action(1)  # run
        else:
            self.update_action(0)  # idle

        animation_timer = 10
        # update image
        self.image = self.animation_list[self.action][self.frame_index]
        # check if enough time has passed since last update
        if pygame.time.get_ticks() - self.update_time > animation_timer:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()

        # check if the animation has finished
        if self.frame_index >= len(self.animation_list[self.action]):
            # if the player is dead then animation ends
            if self.alive == False:
                # last frame for showing death
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0
                # check if an attack has executed
                if self.action == 3 or self.action == 4:
                    self.attacking = False
                    self.attack_reset = 10
                # check if damage has taken
                if self.action == 5:
                    self.hit = False
                    # if the player was in the middle of an attack when othe player already attacked, new attack will be stopped
                    self.attacking = False
                    self.attack_reset = 15

    def attack(self, target):
        if self.attack_reset == 0:
            # attack executed
            self.attacking = True
            self.attack_sound.play()
            # center theke attack ta initiate hobe, attack range fighter er 4x width cover korbe
            attacking_rect = pygame.Rect(self.rect.centerx - (
                4 * self.rect.width * self.flip), self.rect.y, 4*self.rect.width, self.rect.height)
            # check for attack collision
            if attacking_rect.colliderect(target.rect):
                target.health -= 10
                target.hit = True
