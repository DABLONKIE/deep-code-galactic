tiles.setCurrentTilemap(tilemap`testingGround`)
// ------------------Variables
// ------------PlayerData
let playerSprite = sprites.create(assets.image`testPlayer`, SpriteKind.Player)
let playerHealth = 100
let playerIsGrounded = false
let playerJumping = false
let playerGravity = 0
// ------------------Starting Code
playerSprite.setPosition(50, 50)
scene.cameraFollowSprite(playerSprite)
// ------------------Functions
// ------------------Main Game Loop
controller.player1.onButtonEvent(ControllerButton.Up, ControllerButtonEvent.Pressed, function PlayerJump() {
    
    console.log("jumpie")
    if (playerIsGrounded) {
        console.log("true!")
        // playerJumping = True
        playerGravity = -3.5
        playerSprite.y += -3
    }
    
})
forever(function PlayerLoop() {
    
    if (playerSprite.tileKindAt(TileDirection.Bottom, assets.tile`rockFloor`)) {
        if (!playerIsGrounded) {
            if (playerGravity > 3) {
                music.thump.play()
            }
            
            scene.cameraShake(playerGravity / 3, 100)
        }
        
        playerIsGrounded = true
        playerGravity = 0
    } else {
        playerIsGrounded = false
    }
    
    if (playerSprite.tileKindAt(TileDirection.Bottom, assets.tile`rockFloor`)) {
        if (!playerIsGrounded) {
            if (playerGravity > 3) {
                music.thump.play()
            }
            
            scene.cameraShake(playerGravity / 3, 100)
        }
        
        playerIsGrounded = true
        playerGravity = 0
    } else {
        playerIsGrounded = false
    }
    
    if (!playerIsGrounded) {
        if (playerGravity < 5) {
            playerGravity += 0.2 * Delta.DELTA()
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
    
})
