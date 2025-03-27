class Boundary:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.middle_x = screen_width // 2

    def enforce(self, player):
        # Keep player within top and bottom bounds
        if player.rect.top < 0:
            player.rect.top = 0
        if player.rect.bottom > self.screen_height:
            player.rect.bottom = self.screen_height
        
        # Keep PlayerRed on the left side
        if "PlayerRed" in player.image_path:
            if player.rect.left < 0:
                player.rect.left = 0
            if player.rect.right > self.middle_x:
                player.rect.right = self.middle_x
        
        # Keep PlayerBlue on the right side
        elif "PlayerBlue" in player.image_path:
            if player.rect.right > self.screen_width:
                player.rect.right = self.screen_width
            if player.rect.left < self.middle_x:
                player.rect.left = self.middle_x
