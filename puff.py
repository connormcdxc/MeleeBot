import argparse
import signal
import sys
import melee
# cd Documents/Github/MeleeBot
# python puff.py

def check_port(value):
    ivalue = int(value)
    if ivalue < 1 or ivalue > 4:
        raise argparse.ArgumentTypeError("%s is an invalid controller port. \
                                         Must be 1, 2, 3, or 4." % value)
    return ivalue

def signal_handler(sig, frame):
    console.stop()
    if args.debug:
        log.writelog()
        print("") #because the ^C will be on the terminal
        print("Log file created: " + log.filename)
    print("Shutting down cleanly...")
    sys.exit(0)

console = melee.Console(path="E:/LaunchBox/New Slippi Matchmaking/FM-Slippi", slippi_address='127.0.0.1', logger=None)

controller = melee.Controller(console=console, port=1,type=melee.ControllerType.STANDARD)
controller_human = melee.Controller(console=console,
                                    port=2,
                                    type=melee.ControllerType.GCN_ADAPTER)

console.run(iso_path="E:/LaunchBox/Games/Gamecube/Super Smash Bros. Melee DEFAULT DO NOT MOD.iso")
#console.connect()
print("Connecting to console...")
if not console.connect():
    print("ERROR: Failed to connect to the console.")
    sys.exit(-1)
print("Console connected")
#controller.connect()
print("Connecting controller to console...")
if not controller.connect():
    print("ERROR: Failed to connect the controller.")
    sys.exit(-1)
print("Controller connected")
controller_human.connect()
costume = 0
falser = True
otherer = True
connect_code = ""

while True:
    gamestate = console.step()

    #if gamestate is None:
        #print("None")
        #continue
    #else:
        #print("Non none")
        #print(gamestate.menu_state)

    #if otherer:
        #print("otherer")
        #print(gamestate.menu_state)
        #otherer = False

    if console.processingtime * 1000 > 12:
        print("WARNING: Last frame took " + str(console.processingtime*1000) + "ms to process.")
    # Press buttons on your controller based on the GameState here!
    if gamestate.menu_state in [melee.enums.Menu.IN_GAME, melee.enums.Menu.SUDDEN_DEATH]:
        #if otherer:
            #print("ConsoleThing")
            #otherer = False
        #If player is in rest range, press down b, otherwise move towards the player
        if gamestate.distance < 4:
            controller.press_button(melee.enums.Button.BUTTON_B)
            controller.tilt_analog(melee.enums.Button.BUTTON_MAIN, 0.5, 0)
        else:
            #If the player is to the left of the bot, move the bot to the left. Otherwise move the bot to the right
            onleft = gamestate.players[1].x < gamestate.players[2].x
            controller.tilt_analog(melee.enums.Button.BUTTON_MAIN, int(onleft), 0.5)
            controller.release_button(melee.enums.Button.BUTTON_B)
            #If the player is above the bot make the bot jump
            if gamestate.players[1].y < gamestate.players[2].y:
                controller.press_button(melee.enums.Button.BUTTON_X)
            else:
                controller.release_button(melee.enums.Button.BUTTON_X)
    else:
        #print("Menuthing")
        #if otherer:
            #print("Menuthing")
            #otherer = False
        #if not in a game go to the character select screen and choose a random puff constume.
        melee.MenuHelper.menu_helper_simple(gamestate,
                                            controller,
                                            melee.Character.JIGGLYPUFF,
                                            melee.Stage.YOSHIS_STORY,
                                            connect_code,
                                            costume=costume,
                                            autostart=False,
                                            swag=False)
        #melee.MenuHelper.menu_helper_simple(gamestate,
        #                                    controller,
        #                                    melee.Character.FOX,
        #                                    melee.Stage.YOSHIS_STORY,
        #                                    "",
        #                                    costume=costume,
        #                                    autostart=True,
        #                                    swag=False)
