tiles.set_current_tilemap(tilemap("""levelTemplate"""))

#------------------{Variables}
#------------------[PlayerData]
playerSprite = sprites.create(assets.image("""testPlayer"""), SpriteKind.player)
playerHealth = 100
playerIsGrounded = False
playerGravity: number = 0
playerStatus = "idle"
tempSprites: List[Sprite] = []
playerDirection = 1
tempSpriteNum = 0
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
    global playerStatus, playerDirection
    flip = IsFlipNecessary()
    if playerDirection == 1:
        animation.run_image_animation(playerSprite, assets.animation("""testPlayerMine"""), 75, False)
    elif playerDirection == -1:
        animation.run_image_animation(playerSprite, FlipAnimation(assets.animation("""testPlayerMine""")), 75, False)
    playerStatus = "mining"
    def on_after():
        global playerStatus
        playerStatus = "idle"
        sprite = assets.image("""testPlayer""")
        if playerDirection == 1:
            playerSprite.set_image(sprite)
        elif playerDirection == -1:
            sprite.flip_x()
            playerSprite.set_image(sprite)
        location = tiles.location_of_sprite(playerSprite)
        if tiles.tile_at_location_equals(location, assets.tile("testDeposit")):
            tiles.set_tile_at(location, assets.tile("testDepositMine"))
    timer.after(600, on_after)
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
    if randint(0,10) == 0:
        tiles.set_tile_at(tiles.get_tile_location(sX, sW2 - 1), assets.tile("""testDeposit"""))
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
#------------------[QOL Functions]
def FlipAnimation(animation):
    newAnimation: List[Image] = []
    for i in animation:
        curSprite: Image = i
        curSprite.flip_x()
        newAnimation.append(curSprite)
    return newAnimation
def IsFlipNecessary():
    result = 0
    if playerSprite.vx > 0.1:
        result = 1
    elif playerSprite.vx < -0.1:
        result = -1
    return result
def CreateTempSprite(spriteAnimation: List[Image], x, y, speed, z = 100, tileset = False): #Creates a temporary sprite to play an animation
    global tempSprites, tempSpriteNum
    tempSprites.append(sprites.create(assets.image("""emptySpace""")))
    tempSprites[len(tempSprites) - 1].x = x
    tempSprites[len(tempSprites) - 1].y = y
    tempSprites[len(tempSprites) - 1].z = z
    tempSpriteNum += 1
    animation.run_image_animation(tempSprites[len(tempSprites) - 1], spriteAnimation, speed, False)
    delay = speed * len(spriteAnimation)
    def on_debounce():
        tempSprites.shift().destroy()
    timer.debounce(str(tempSpriteNum), delay, on_debounce)

#------------------{Main Game Loop}
GenerateLevel()
def PlayerLoop():
    global playerHealth, playerIsGrounded, playerGravity, playerDirection
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
        flip = IsFlipNecessary()
        if flip == 1:
            playerSprite.set_image(sprite)
        elif flip == -1:
            sprite.flip_x()
            playerSprite.set_image(sprite)
        if flip != 0:
            playerDirection = flip
        playerSprite.vx += controller.dx() * 20
    playerSprite.vx *= 0.8

    

    if controller.up.is_pressed() and playerStatus == "idle":
        PlayerJump()
    if controller.B.is_pressed() and playerStatus == "idle":
        PlayerMine()

forever(PlayerLoop)

#------------------