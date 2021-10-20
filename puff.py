import melee

console = melee.Console(path="/SlippiOnline/", is_dolphin=True, dolphin_home_path=None, tmp_home_directory=True, slippi_address='127.0.0.1', slippi_port=51441, online_delay=2, blocking_input=False, polling_mode=False, allow_old_version=False, logger=None)

controller = melee.Controller(console=console, port=2)
controller_human = melee.Controller(console=console,
                                    port=1,
                                    type=melee.ControllerType.GCN_ADAPTER)

console.run()
console.connect()

controller.connect()
controller_human.connect()

while True:
    gamestate = console.step()
    # Press buttons on your controller based on the GameState here!
    if gamestate.menu_state in [melee.enums.Menu.IN_GAME, melee.enums.Menu.SUDDEN_DEATH]:
        #If player is in rest range, press down b, otherwise move towards the player
        if gamestate.distance < 4:
            controller.press_button(melee.enums.Button.BUTTON_B)
            controller.tilt_analog(melee.enums.Button.BUTTON_MAIN, 0.5, 0)
        else:
            #If the player is to the left of the bot, move the bot to the left. Otherwise move the bot to the right
            onleft = gamestate.players[2].x < gamestate.players[1].x
            controller.tilt_analog(melee.enums.Button.BUTTON_MAIN, int(onleft), 0.5)
            controller.release_button(melee.enums.Button.BUTTON_B)
            #If the player is above the bot make the bot jump
            if gamestate.players[2].y < gamestate.players[1].y
                controller.release_button(melee.enums.Button.BUTTON_X)
            else:
                controller.release_button(melee.enums.Button.BUTTON_X)
    else:
        costume = random.randint(0, 4)
        melee.MenuHelper.menu_helper_simple(gamestate,
                                            controller,
                                            melee.Character.JIGGLYPUFF,
                                            melee.Stage.YOSHIS_STORY,
                                            "",
                                            costume=costume,
                                            autostart=False,
                                            swag=False)
