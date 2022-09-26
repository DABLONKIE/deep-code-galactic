tiles.set_current_tilemap(tilemap("""testingGround"""))

#------------------Variables
#player = Dwarf()
isGrounded = False
#------------------Starting Code



#------------------Classes
class Dwarf:
    def __init__():
        selfSprite = sprites.create(assets.image("""testPlayer"""), SpriteKind.player)
    def update():
        if selfSprite.tile_kind_at(TileDirection.BOTTOM, assets.tile("""rockFloor""")):
            #if isGrounded == False:
                #scene.camera_shake(2, 100)
            isGrounded = True
        if not isGrounded:
            selfSprite.y += 3
        selfSprite.x += controller.dx()  

#------------------Main Game Loop
while True:
    #player.update()
    pause(25)
#------------------