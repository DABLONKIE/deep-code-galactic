tiles.set_current_tilemap(tilemap("""levelTemplate"""))

#------------------{Variables}
#------------------[PlayerData]
playerSprite = sprites.create(assets.image("""testPlayer"""), SpriteKind.player)
playerHealth = 100
playerIsGrounded = False
playerGravity: number = 0
playerStatus = "idle"
#------------------{Starting Code}
playerSprite.set_position(50, 120)
scene.camera_follow_sprite(playerSprite)
scene.set_background_color(4)
#------------------{Functions}
def PlayerJump():
    global playerIsGrounded, playerGravity
    if playerIsGrounded:
        playerGravity = -3
        playerSprite.y += -3
def PlayerMine():
    global playerStatus
    
    animation.run_image_animation(playerSprite, assets.animation("""playerTestMining"""), 75, False)
    playerStatus = "mining"
    def on_after():
        global playerStatus
        playerStatus = "idle"
    timer.after(300, on_after)
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
    currentW1 = 6
    currentW2 = 10
    timesPrevented = 0
    timesCorrected = 0
    for row in range(91):
        lenienceW1 = 0
        lenienceW2 = 0
        if randint(0, 2 - lenienceW1) == 0: #Mutation chance for roof
            currentW1 += randint(-1,1)
            lenienceW1 = 0

        if randint(0, 2 - lenienceW2) == 0: #Mutation chance for floor
            currentW2 += randint(-1,1)
            lenienceW2 = 0

        while currentW1 - currentW2 < -4:
            timesCorrected += 1
            currentW1 += 1
            currentW2 -= 1
        while currentW1 + 4 >= currentW2: #Ensure that the roof isnt too close to the floor or vice versa.
            timesPrevented += 1
            currentW1 -= 1
            currentW2 += 1

        

        if currentW1 < 2:
            currentW1 = 2
            lenienceW1 += 1
        if currentW2 > 15:
            currentW2 = 15
            lenienceW2 += 1
            
        GenerateSlice(row + 5,currentW1,currentW2)
    print("LEVEL GENERATION COMPLETE")
    print("Times corrected:"+timesCorrected)
    print("Times prevented:"+timesPrevented)
def FlipAnimation(animation):
    for i in animation:
        print(animation[i])
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

    if not playerIsGrounded:
        if playerGravity < 5:
            playerGravity += 0.3 * Delta.DELTA()
        playerSprite.vy += (playerGravity * Delta.DELTA()) * 15
        playerSprite.vy *= 0.8
    if playerStatus == "idle":
        sprite = assets.image("""testPlayer""")
        if playerSprite.vx > 0.1:
            playerSprite.set_image(sprite)
        elif playerSprite.vx < -0.1:
            sprite.flip_x()
            playerSprite.set_image(sprite)
        
        playerSprite.vx += controller.dx() * 20
    playerSprite.vx *= 0.8

    

    if controller.up.is_pressed() and playerStatus == "idle":
        PlayerJump()
    if controller.B.is_pressed() and playerStatus == "idle":
        PlayerMine()

forever(PlayerLoop)

#------------------