# ChooseYourAdventure

Hark, Traveler! Welcome to a land of adventure! Our quests use the greatest GPU of all: your imagination. In our welcome hall, you may choose from a quest provided by your fellow Adventurers. Have you a quest in mind already? Create an account and add your own, origional adventure! We only accept adventures written to a certain standard, so please see the explainations and examples below. We can't wait to see what you create! Fare thee well

A Django app for saving and running text-based adventure games written in Python. Uses Brython for running the games. Hosted on Heroku. Uses SQLite locally and Postgres on Heroku.




"""
##### Author Info #####

#### TODO: Replace the underlines below with your email

__author__ = "_____@gmail.com"\
__version__ = 1\
__date__ = "Spring 2019"


##### Record Definitions #####

## Add a new record and modify the existing ones to fit your game.

'''
Records:
    World:
        status (str): Whether or not the game is "playing", "won",
                      or "lost". Initially "playing".
        map (dict[str: Location]): The lookup dictionary matching 
                                   location names to their
                                   information.
        player (Player): The player character's information.
        time (int): The current time of the game, incremented every tick.
        encounter (str): The current thing being encountered, or None if we're
                         not encountering anything.
      
    Player:
        location (str): The name of the player's current location.
        inventory (list[str]): The player's collection of items.
                               Initially empty.
        can bark (bool): Whether or not the player has learned the bark skill.
        animals (list[Animal]): The animals currently in the party.

    Location:
        about (str): A sentence that describes what this location 
                     looks like.
        neighbors (list[str]): A list of the names of other places 
                               that you can reach from this 
                               location.
        stuff (list[str]): A collection of things available at 
                           this location.
                           
    Animal:
        name (str): The full name of the animal.
        energy (int): The energy level of this animal, decreases as you move.
'''

##### Core Game Functions #####

## Implement the following to create your game.

def render_introduction():
    '''
    Create the message to be displayed at the start of your game.
    
    Returns:
        str: The introductory text of your game to be displayed.
    '''
    return ("=================================================\n"
            "..........The Red Dot Quest............\n"
            "By Dr. Bart\n"
            "Starring Ada, Pumpkin, Reese, Klaus, and...\n"
            "         * THE RED DOT *\n"
            "=================================================\n"
            "You are the graceful Lady Ada, a young hero destined to\n"
            "destroy the ultimate evil: The Red Dot.\n"
            "Although you are young, you know that with the power of\n"
            "friendship and barking, you can overcome any challenge.\n"
            "\n"
            "Ada! Your destiny begins now!\n")
            
def create_player():
    return {
        'location': 'home',
        'animals': [create_animal('Lady Ada')],
        'inventory': [],
        'can bark': False
    }
    
def create_animal(name):
    return {
        'name': name,
        'energy': 5
    }

def create_map():
    return {
        'home': {
            'neighbors': ['nearby forest', 'hills', 'town'],
            'about': "This is your warm, pleasant home.",
            'stuff': ['chair']
        },
        'nearby forest': {
            'neighbors': ['home'],
            'about': "A dense forest near your house.\nYou wonder if there is anything around?",
            'stuff': ['catnip']
        },
        'town': {
            'neighbors': ['home', 'chapel', 'castle'],
            'about': "This town is well-populated and bustling.",
            'stuff': []
        },
        'chapel': {
            'neighbors': ['town'],
            'about': "The chapel is somber and quiet.",
            'stuff': ['seer klaus']
        },
        'castle': {
            'neighbors': ['town'],
            'about': "The stately walls are covered in portraits of Duke Pumpkin.",
            'stuff': ['duke pumpkin']
        },
        'hills': {
            'neighbors': ['home', 'the wilds', 'cave'],
            'about': "From this spot, you can see much of the Kingdom.\nBeautiful view!",
            'stuff': []
        },
        'the wilds': {
            'neighbors': ['hills'],
            'about': "The land is treacherous out here.",
            'stuff': ['sir reese']
        },
        'cave': {
            'neighbors': ['hills'],
            'about': "You sense the presence of evil.",
            'stuff': []
        }
    }

def create_world():
    '''
    Creates a new version of the world in its initial state.
    
    Returns:
        World: The initial state of the world
    '''
    return {
        'map': create_map(),
        'status': 'playing',
        'player': create_player(),
        'time': 0,
        'encounter': None,
    }
    
def render_location(world):
    location = world['player']['location']
    return "You are in "+location

def render_about(world):
    location = world['player']['location']
    return world['map'][location]['about']
    
def is_daylight(world):
    return world['time'] % 4 <= 1

def render_location_details(world):
    location = world['player']['location']
    stuff = world['map'][location]['stuff']
    if can_pick_catnip(world):
        return "You see a patch of catnip nearby a tree.\n"
    elif location == "castle" and 'duke pumpkin' in stuff:
        return "Duke Pumpkin sits atop this throne.\n"
    elif location == "the wilds" and 'sir reese' in stuff:
        return "Sir Reese lingers nearby.\n"
    return ""
    
def render_time(world):
    current_time = world['time'] % 4
    if current_time == 0:
        return "Current Time: Morning\n"
    elif current_time == 1:
        return "Current Time: Afternoon\n"
    elif current_time == 2:
        return "Current Time: Evening\n"
    elif current_time == 3:
        return "Current Time: Night\n"
        
def hide_things(stuff, hidden_stuff):
    visible_things = []
    for thing in stuff:
        if thing not in hidden_stuff:
            visible_things.append(thing)
    return visible_things
        
def render_stuff(world):
    location = world['player']['location']
    stuff = world['map'][location]['stuff']
    inventory = world['player']['inventory']
    if 'catnip' in inventory or not is_daylight(world):
        stuff = hide_things(stuff, 'catnip')
    stuff = hide_things(stuff, 'klaus')
    
    if not stuff:
        return "You see nothing of interest."
    else:
        return "You see: "+(", ".join(stuff))

def render(world):
    '''
    Consumes a world and produces a string that will describe the current state
    of the world. Does not print.
    
    Args:
        world (World): The current world to describe.
    
    Returns:
        str: A textual description of the world.
    '''
    if world['encounter']:
        return render_encounter(world)
    else:
        return render_overworld(world)
        
def render_encounter(world):
    encounter = world['encounter']
    message = "-"*40+"\n"
    message += "You are in an encounter with "+encounter+"!\n"
    return message

def render_overworld(world):
    location = world['player']['location']
    here = world['map'][location]
    about = here['about']
    stuff = here['stuff']
    
    return ("-"*40+"\n"+
            render_location(world) + "\n" +
            render_about(world) + "\n" +
            render_location_details(world) + "\n" +
            render_time(world) + "\n" +
            render_stuff(world) + "\n" +
            render_status(world) + "\n" +
            render_inventory(world) + "\n")
            
def any_tired_animals(world):
    animals = world['player']['animals']
    for animal in animals:
        if animal['energy'] <= 0:
            return True
    return False
            
def render_status(world):
    can_bark = world['player']['can bark']
    if any_tired_animals(world):
        return "Your group is tired.\n"
    message = ""
    if can_bark:
        message += "You know how to bark.\n"
    return message + "You are feeling good."
        

def render_inventory(world):
    inventory = world['player']['inventory']
    if not inventory:
        return "You have nothing."
    inventory = ", ".join(inventory)
    return "You have: "+inventory

def can_pick_catnip(world):
    location = world['player']['location']
    inventory = world['player']['inventory']
    return (location.lower() == "nearby forest" and
            is_daylight(world) and
            'catnip' not in inventory)

def get_specific_options(world):
    location = world['player']['location']
    inventory = world['player']['inventory']
    here = world['map'][location]
    neighbors = here['neighbors']
    stuff = here['stuff']
    can_bark = world['player']['can bark']
    
    if can_pick_catnip(world):
        return ["Pick catnip"]
    elif location == "chapel" and not can_bark:
        return ["Wait patiently"]
    elif location == "castle" and 'duke pumpkin' not in inventory:
        return ["Meet pumpkin"]
    elif location == "the wilds" and 'sir reese' not in inventory:
        return ["Meet reese"]
    elif location == "cave":
        return ["Fight Red Dot"]
    return []
    
def get_encounter_options(world):
    commands = ["Quit", "Flee", "Bite"]
    if world['player']['can bark']:
        commands.append("Bark")
    if 'catnip' in world['player']['inventory']:
        commands.append("Befriend")
    return commands

def get_options(world):
    '''
    Consumes a world and produces a list of strings representing the options
    that are available to be chosen given this state.
    
    Args:
        world (World): The current world to get options for.
    
    Returns:
        list[str]: The list of commands that the user can choose from.
    '''
    if world['encounter']:
        return get_encounter_options(world)
    
    location = world['player']['location']
    here = world['map'][location]
    neighbors = here['neighbors']
    
    commands = ["Quit", "Nap"]
    
    if any_tired_animals(world):
        return commands
    
    for neighbor in neighbors:
        commands.append("Go to "+neighbor)
    
    commands.extend(get_specific_options(world))
    
    return commands

def update(world, command):
    '''
    Consumes a world and a command and updates the world according to the
    command, also producing a message about the update that occurred. This
    function should modify the world given, not produce a new one.
    
    Args:
        world (World): The current world to modify.
    
    Returns:
        str: A message describing the change that occurred in the world.
    '''
    if command.lower() == "quit":
        world['status'] = 'quit'
        return "You quit the game."
    if world['encounter']:
        return update_encounter(world, command)
    else:
        return update_overworld(world, command)
        
def take_nap(world):
    for animal in world['player']['animals']:
        animal['energy'] = 5
    return "Everyone took a nap!"
        
def update_overworld(world, command):
    command = command.lower()
    world['time'] += 1
    if command.lower() == "nap":
        return take_nap(world)
    elif command.lower() == "pick catnip":
        world['player']['inventory'].append('catnip')
        return "You picked up some catnip."
    elif command.lower() == "wait patiently":
        world['player']['can bark'] = True
        return (
            "After a few hours of waiting, an old sage suddenly materializes before.\n"
            "He snuffles grumpily and announces:\n"
            " \"Young pupper! To succeed on your quest, you must give forth\n"
            "  mighty barks! Go forth, and bark loudly!\"\n"
            "You learned how to bark!"
        )
    elif command.lower() == "meet pumpkin":
        world['encounter'] = "duke pumpkin"
        return "You went up to Duke Pumpkin!"
    elif command.lower() == "meet reese":
        world['encounter'] = "sir reese"
        return "You went up to Sir Reese!"
    elif command.lower() == "fight red dot":
        world['encounter'] = "the red dot"
        return ("You engaged with the Red Dot!")
    elif command.lower().startswith("go to "):
        return goto(world, command[len("go to "):])
    
def goto(world, where):
    world['player']['location'] = where
    for animal in world['player']['animals']:
        animal['energy'] -= 1
    return "You went to "+where
        
def update_encounter(world, command):
    if command.lower() == "flee":
        world['encounter'] = None
        return "You tucked your tail between your legs and ran away!\n"
    elif command.lower() == "bite":
        return bite(world, world['encounter'])
    elif command.lower() == "bark":
        return bark(world, world['encounter'])
    elif command.lower() == "befriend":
        return befriend(world, world['encounter'])
    
def bite(world, target):
    preamble = "You lunged and snapped your teeth together!\n"
    if target == "sir reese":
        return preamble + "Sir Reese got scared and hissed at you!"
    elif target == "duke pumpkin":
        return preamble + "Duke Pumpkin got mad and swatted your nose."
    elif target == "the red dot":
        if len(world['player']['animals']) == 3:
            world['status'] = 'won'
            return preamble + "The red dot vanished!"
        else:
            world['status'] = 'lost'
            
def bark(world, target):
    preamble = "You barked loudly! Bark, bark!\n"
    if target == "sir reese":
        return preamble + "Sir Reese got scared and hissed at you!"
    elif target == "duke pumpkin":
        world['encounter'] = None
        world['map']['castle']['stuff'].remove('duke pumpkin')
        world['player']['inventory'].append('duke pumpkin')
        world['player']['animals'].append(create_animal('Duke Pumpkin'))
        return preamble + (
            "Duke Pumpkin was impressed!\n"
            "\"Perhaps with your fearsome power, we stand a chance.\"\n"
            "Duke Pumpkin joined your team!\n"
            )
    elif target == "the red dot":
        return "The Red Dot was not impressed!"

def befriend(world, target):
    preamble = "You gave "+target.title()+" the catnip!\n"
    if target == "sir reese":
        world['encounter'] = None
        world['map']['the wilds']['stuff'].remove('sir reese')
        world['player']['inventory'].append('sir reese')
        world['player']['animals'].append(create_animal('Sir Reese'))
        return preamble + (
            "Sir Reese meows happily and pockets the catnip.\n"
            "\"Ah, such generousity! I will aid your fight.\"\n"
            "Sir Reese joined your team!"
        )
    elif target == "Duke Pumpkin":
        world['player']['inventory'].remove('catnip')
        return preamble + (
            "Duke Pumpkin ate your catnip.\n"
            "But he didn't seem very impressed..."
        )
    elif target == "The Red Dot":
        return preamble+"The Red Dot doesn't seem to like catnip..."

def render_ending(world):
    '''
    Create the message to be displayed at the end of your game.
    
    Args:
        world (World): The final world state to use in describing the ending.
    
    Returns:
        str: The ending text of your game to be displayed.
    '''
    status = world['status']
    if status == "quit":
        return ("You gave up on your quest.\n"
                "Will the red dot ever be defeated??")
    elif status == "lost":
        return ("The Red Dot disappears for a moment, but you hear "
                "its laughter echoing in the cave.\n"
                '  "Think you that I would die so easily???"\n'
                "So saying, the Red Dot appears again and launches a "
                "savage attack.\n"
                "As you are overwhelmed, you wish you had just had a "
                "little more help...\n"
                "Game over! Bad end :(")
    elif status == "won":
        return ("The Red Dot disappears for a moment.\n"
                ' "Do not be fooled! It is hiding here!"\n'
                "Sir Reese jumps in the corner and slashes at the light.\n"
                ' "We will not be deceived!" hisses Duke Pumpkin,\n'
                "and all three heroes launched a devestating triple attack!\n"
                "\n"
                "Afterwards, awash in the glory of victory, the three friends\n"
                "reflect on their journey together. Although they part ways\n"
                "for now, they will always be ready to reunite to fight evil\n"
                "no matter how many times it rears its ugly head!")

def choose(options):
    '''
    Consumes a list of commands, prints them for the user, takes in user input
    for the command that the user wants (prompting repeatedly until a valid
    command is chosen), and then returns the command that was chosen.
    
    Note:
        Use your answer to Programming Problem #43.4
    
    Args:
        options (list[str]): The potential commands to select from.
    
    Returns:
        str: The command that was selected by the user.
    '''
    print("You can:")
    for option in options:
        print("\t", option)
    print("What will you do?")
    command = ""
    while command.lower() not in [option.lower() for option in options]:
        command = input(">>> ")
    return command

###### Win/Lose Paths #####
### WIN_PATH (list[str]): A list of commands that win the game when entered
### LOSE_PATH (list[str]): A list of commands that lose the game when entered.

WIN_PATH = ['Go to Town', 'Go to Chapel', 'Wait Patiently', # Get bark
            'Go to Town', 'Go to Castle', 'Meet Pumpkin', 'Bark', # Get pumpkin
            'Nap', 'Go to Town', 'Go to Home', 'Go to nearby Forest', 
                'Nap', 'Nap', 'Pick Catnip', # Get catnip
            'Go to Home', 'Go to Hills', 'Go to The Wilds',
                'Meet Reese', 'Befriend', # Get Reese
            'Nap', 'Go to Hills', 'Go to Cave', 
                'Fight Red Dot', 'Bite', # Win game
            ]
LOSE_PATH = ['Go to Hills', 'Go to Cave', 'Fight Red Dot', 'Bite']
    
###### Unit Tests #####
## Write unit tests here


###### Main Function #####
## Do not modify this area

def main():
    '''
    Run your game using the Text Adventure console engine.
    Consumes and produces nothing, but prints and indirectly takes user input.
    '''
    print(render_introduction())
    world = create_world()
    while world['status'] == 'playing':
        print(render(world))
        options = get_options(world)
        command = choose(options)
        print(update(world, command))
    print(render_ending(world))

if __name__ == '__main__':
    main()
