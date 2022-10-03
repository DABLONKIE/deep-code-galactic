tiles.set_current_tilemap(tilemap("""levelTemplate"""))

#------------------{Variables}
#------------------[PlayerData]
playerSprite = sprites.create(assets.image("""testPlayer"""), SpriteKind.player)
playerHealth = 100
playerIsGrounded = False
playerGravity: number = 0
#------------------{Starting Code}
playerSprite.set_position(50, 120)
scene.camera_follow_sprite(playerSprite)

#------------------{Functions}
def PlayerJump():
    global playerIsGrounded, playerGravity
    if playerIsGrounded:
        playerGravity = -3
        playerSprite.y += -3

def GenerateSlice(sX, sW1, sW2):
    for sY in range(16):
        if sY > sW1 and sY < sW2:
            continue
        if sY == sW1:
            tiles.set_tile_at(tiles.get_tile_location(sX, sY), assets.tile("""rockRoof"""))
        elif sY == sW2:
            tiles.set_tile_at(tiles.get_tile_location(sX, sY), assets.tile("""rockFloor"""))
        else:
            tiles.set_tile_at(tiles.get_tile_location(sX, sY), assets.tile("""rock"""))
        tiles.set_wall_at(tiles.get_tile_location(sX, sY), True)
def GenerateLevel():
    for row in range(91):
        GenerateSlice(row + 5,6,10)
GenerateLevel()
#------------------{Main Game Loop}
def PlayerLoop():
    global playerHealth, playerIsGrounded, playerGravity
    if playerSprite.tile_kind_at(TileDirection.BOTTOM, assets.tile("""rockFloor""")):
        if not playerIsGrounded:
            if playerGravity > 4:
                music.thump.play()
            scene.camera_shake(playerGravity / 4.5, 100)
        playerIsGrounded = True
        playerGravity = 0

    else:
        playerIsGrounded = False
    
    if playerSprite.tile_kind_at(TileDirection.BOTTOM, assets.tile("""rockFloor""")):
        if not playerIsGrounded:
            if playerGravity > 3:
                music.thump.play()
            scene.camera_shake(playerGravity / 3, 100)
        playerIsGrounded = True
        playerGravity = 0
    else:
        playerIsGrounded = False

    if not playerIsGrounded:
        if playerGravity < 5:
            playerGravity += 0.3 * Delta.DELTA()
        playerSprite.vy += (playerGravity * Delta.DELTA()) * 15
        playerSprite.vy *= 0.8
    
    playerSprite.vx += controller.dx() * 10
    playerSprite.vx *= 0.8

    if playerSprite.vx > 0.1:
        playerSprite.set_image(assets.image("""testPlayer"""))
    elif playerSprite.vx < -0.1:
        playerSprite.set_image(assets.image("""testPlayerFlip"""))

    if controller.up.is_pressed():
        PlayerJump()

controller.player1.on_button_event(ControllerButton.UP, ControllerButtonEvent.PRESSED, PlayerJump)
forever(PlayerLoop)

#------------------