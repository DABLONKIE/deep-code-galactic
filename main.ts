tiles.setCurrentTilemap(tilemap`levelTemplate`)
// ------------------{Variables}
// ------------------[PlayerData]
let playerSprite = sprites.create(assets.image`testPlayer`, SpriteKind.Player)
let playerHealth = 100
let playerIsGrounded = false
let playerGravity = 0
let playerStatus = "idle"
let playerDirection = 1
// ------------------{Starting Code}
playerSprite.setPosition(50, 120)
scene.cameraFollowSprite(playerSprite)
scene.setBackgroundColor(4)
// ------------------{Functions}
function PlayerJump() {
    
    if (playerIsGrounded) {
        playerGravity = -3
        playerSprite.y += -3
    }
    
}

function PlayerMine() {
    
    let flip = IsFlipNecessary()
    if (playerDirection == 1) {
        animation.runImageAnimation(playerSprite, assets.animation`testPlayerMine`, 75, false)
    } else if (playerDirection == -1) {
        animation.runImageAnimation(playerSprite, FlipAnimation(assets.animation`testPlayerMine`), 75, false)
    }
    
    playerStatus = "mining"
    timer.after(300, function on_after() {
        
        playerStatus = "idle"
        let sprite = assets.image`testPlayer`
        if (playerDirection == 1) {
            playerSprite.setImage(sprite)
        } else if (playerDirection == -1) {
            sprite.flipX()
            playerSprite.setImage(sprite)
        }
        
    })
}

function GenerateSlice(sX: number, sW1: number, sW2: number) {
    for (let sY = 0; sY < 16; sY++) {
        if (sY > sW1 && sY < sW2) {
            continue
        }
        
        if (sY == sW1) {
            tiles.setTileAt(tiles.getTileLocation(sX, sY), assets.tile`rockRoof`)
        } else if (sY == sW2) {
            tiles.setTileAt(tiles.getTileLocation(sX, sY), assets.tile`rockFloor`)
        } else {
            tiles.setTileAt(tiles.getTileLocation(sX, sY), assets.tile`rock`)
        }
        
        tiles.setWallAt(tiles.getTileLocation(sX, sY), true)
    }
    if (randint(0, 10) == 0) {
        tiles.setTileAt(tiles.getTileLocation(sX, sW2 - 1), assets.tile`testDeposit`)
    }
    
}

function GenerateLevel() {
    let lenienceW1: number;
    let lenienceW2: number;
    let currentW1 = 6
    let currentW2 = 10
    let timesPrevented = 0
    let timesCorrected = 0
    for (let row = 0; row < 91; row++) {
        lenienceW1 = 0
        lenienceW2 = 0
        if (randint(0, 2 - lenienceW1) == 0) {
            // Mutation chance for roof
            currentW1 += randint(-1, 1)
            lenienceW1 = 0
        }
        
        if (randint(0, 2 - lenienceW2) == 0) {
            // Mutation chance for floor
            currentW2 += randint(-1, 1)
            lenienceW2 = 0
        }
        
        while (currentW1 - currentW2 < -4) {
            timesCorrected += 1
            currentW1 += 1
            currentW2 -= 1
        }
        while (currentW1 + 4 >= currentW2) {
            // Ensure that the roof isnt too close to the floor or vice versa.
            timesPrevented += 1
            currentW1 -= 1
            currentW2 += 1
        }
        if (currentW1 < 2) {
            currentW1 = 2
            lenienceW1 += 1
        }
        
        if (currentW2 > 15) {
            currentW2 = 15
            lenienceW2 += 1
        }
        
        GenerateSlice(row + 5, currentW1, currentW2)
    }
    console.log("LEVEL GENERATION COMPLETE")
    console.log("Times corrected:" + timesCorrected)
    console.log("Times prevented:" + timesPrevented)
}

// ------------------[QOL Functions]
function FlipAnimation(animation: Image[]): Image[] {
    let curSprite: Image;
    let newAnimation : Image[] = []
    for (let i of animation) {
        curSprite = i
        curSprite.flipX()
        newAnimation.push(curSprite)
    }
    return newAnimation
}

function IsFlipNecessary(): number {
    let result = 0
    if (playerSprite.vx > 0.1) {
        result = 1
    } else if (playerSprite.vx < -0.1) {
        result = -1
    }
    
    return result
}

GenerateLevel()
// ------------------{Main Game Loop}
forever(function PlayerLoop() {
    let sprite: Image;
    let flip: number;
    
    if (playerSprite.tileKindAt(TileDirection.Bottom, assets.tile`rockFloor`)) {
        if (!playerIsGrounded) {
            if (playerGravity > 4) {
                music.thump.play()
            }
            
            scene.cameraShake(playerGravity / 4.5, 100)
        }
        
        playerIsGrounded = true
        playerGravity = 0
    } else {
        playerIsGrounded = false
    }
    
    if (!playerIsGrounded) {
        if (playerGravity < 5) {
            playerGravity += 0.3 * Delta.DELTA()
        }
        
        playerSprite.vy += playerGravity * Delta.DELTA() * 15
        playerSprite.vy *= 0.8
    }
    
    if (playerStatus == "idle") {
        sprite = assets.image`testPlayer`
        flip = IsFlipNecessary()
        if (flip == 1) {
            playerSprite.setImage(sprite)
        } else if (flip == -1) {
            sprite.flipX()
            playerSprite.setImage(sprite)
        }
        
        if (flip != 0) {
            playerDirection = flip
        }
        
        playerSprite.vx += controller.dx() * 20
    }
    
    playerSprite.vx *= 0.8
    if (controller.up.isPressed() && playerStatus == "idle") {
        PlayerJump()
    }
    
    if (controller.B.isPressed() && playerStatus == "idle") {
        PlayerMine()
    }
    
})
