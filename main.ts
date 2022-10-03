tiles.setCurrentTilemap(tilemap`levelTemplate`)
// ------------------{Variables}
// ------------------[PlayerData]
let playerSprite = sprites.create(assets.image`testPlayer`, SpriteKind.Player)
let playerHealth = 100
let playerIsGrounded = false
let playerGravity = 0
// ------------------{Starting Code}
playerSprite.setPosition(50, 120)
scene.cameraFollowSprite(playerSprite)
// ------------------{Functions}
function PlayerJump() {
    
    if (playerIsGrounded) {
        playerGravity = -3
        playerSprite.y += -3
    }
    
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
}

function GenerateLevel() {
    for (let row = 0; row < 91; row++) {
        GenerateSlice(row + 5, 6, 10)
    }
}

GenerateLevel()
// ------------------{Main Game Loop}
forever(function PlayerLoop() {
    
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
    
    playerSprite.vx += controller.dx() * 10
    playerSprite.vx *= 0.8
    if (playerSprite.vx > 0.1) {
        playerSprite.setImage(assets.image`testPlayer`)
    } else if (playerSprite.vx < -0.1) {
        playerSprite.setImage(assets.image`testPlayerFlip`)
    }
    
    if (controller.up.isPressed()) {
        PlayerJump()
    }
    
})
