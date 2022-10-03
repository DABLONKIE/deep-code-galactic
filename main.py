tiles.set_current_tilemap(tilemap("""testingGround"""))

#------------------Variables
#------------PlayerData
playerSprite = sprites.create(assets.image("""testPlayer"""), SpriteKind.player)
playerHealth = 100
playerIsGrounded = False
playerJumping = False
playerGravity: number = 0
#------------------Starting Code
playerSprite.set_position(50, 50)
scene.camera_follow_sprite(playerSprite)

#------------------Functions
def PlayerJump():
    global playerIsGrounded, playerGravity, playerJumping
    print("jumpie")
    if playerIsGrounded:
        print("true!")
        #playerJumping = True
        playerGravity = -3.5
        playerSprite.y += -3

#------------------Main Game Loop
def PlayerLoop():
    global playerHealth, playerIsGrounded, playerGravity

    if playerSprite.tile_kind_at(TileDirection.BOTTOM, assets.tile("""rockFloor""")):
        if not playerIsGrounded:
            if playerGravity > 3:
                music.thump.play()
            scene.camera_shake(playerGravity / 3, 100)
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
            playerGravity += 0.2 * Delta.DELTA()
        playerSprite.vy += (playerGravity * Delta.DELTA()) * 15
        playerSprite.vy *= 0.8
    
    playerSprite.vx += controller.dx() * 10
    playerSprite.vx *= 0.8

    if playerSprite.vx > 0.1:
        playerSprite.set_image(assets.image("""testPlayer"""))
    elif playerSprite.vx < -0.1:
        playerSprite.set_image(assets.image("""testPlayerFlip"""))

controller.player1.on_button_event(ControllerButton.UP, ControllerButtonEvent.PRESSED, PlayerJump)
forever(PlayerLoop)

#------------------