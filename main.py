import gd, asyncio, random, time, clipboard
import tkinter as tk
from threading import Thread

client = gd.Client()

try:
    memory = gd.memory.get_state(load=True)
except LookupError:
    input("Geometry Dash is not open.\nPress enter to continue . . .")
    exit()

game_manager = memory.get_game_manager()
editor_layer = game_manager.get_editor_layer()
play_layer = game_manager.get_play_layer()
player = play_layer.get_player()
gamelevel = play_layer.get_level_settings().get_level()
account_manager = memory.get_account_manager()
user_name = account_manager.get_user_name()

gui = True
attempts = 0
dead = True
difficulty = 5
closed = False

def start(usinggui=False):
    if usinggui:
        startbtn.destroy()
        padding.destroy()
        easybtn.destroy()
        mediumbtn.destroy()
        hardbtn.destroy()
        insanebtn.destroy()
        extremebtn.destroy()
    asyncio.set_event_loop(asyncio.new_event_loop())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    
def set_difficulty(diff):
    global difficulty
    difficulty = diff
    
def on_close():
    global closed
    closed = True
    w.destroy()
    
if gui:
    w = tk.Tk()  
    levelvar = tk.StringVar()
    idvar = tk.StringVar()
    lifevar = tk.StringVar()
    completedlevelsvar = tk.StringVar()
    w.geometry("800x600")
    w.configure(bg="#252525")
    w.title("100 Lives Challenge")
    w.resizable(False, False)
    w.protocol("WM_DELETE_WINDOW", on_close)
    
    levelname = tk.Label(w, text="", textvariable=levelvar, font=("TkDefaultFont", 33), fg="#03a9f4")
    levelname.pack()
    levelname['bg'] = levelname.master['bg']
    
    levelid = tk.Label(w, text="", textvariable=idvar, font=("TkDefaultFont", 22), fg="#03a9f4")
    levelid.pack()
    levelid['bg'] = levelid.master['bg']
    
    livesleft = tk.Label(w, text="100 lives left!", textvariable=lifevar, font=("TkDefaultFont", 24), fg="#03a9f4", pady=25)
    livesleft.pack()
    livesleft['bg'] = livesleft.master['bg']
    
    lvlcompleted = tk.Label(w, text="0 levels completed!", textvariable=completedlevelsvar, font=("TkDefaultFont", 24), fg="#03a9f4", pady=25)
    lvlcompleted.pack()
    lvlcompleted['bg'] = lvlcompleted.master['bg']
    
    startbtn = tk.Button(w, text="Start challenge", command=Thread(target=start, args=(True,)).start, font=("TkDefaultFont", 24), fg="#03a9f4")
    startbtn.pack()
    startbtn['bg'] = startbtn.master['bg']
    
    padding = tk.Label(w, text="", pady=50)
    padding.pack()
    padding['bg'] = padding.master['bg']
    
    easybtn = tk.Button(w, text="Easy", command=lambda: set_difficulty(1), font=("TkDefaultFont", 14), fg="#03a9f4", padx=50)
    easybtn.pack(side="left")
    easybtn['bg'] = easybtn.master['bg']
    
    mediumbtn = tk.Button(w, text="Medium", command=lambda: set_difficulty(2), font=("TkDefaultFont", 14), fg="#03a9f4", padx=50)
    mediumbtn.pack(side="left")
    mediumbtn['bg'] = mediumbtn.master['bg']
    
    hardbtn = tk.Button(w, text="Hard", command=lambda: set_difficulty(3), font=("TkDefaultFont", 14), fg="#03a9f4", padx=50)
    hardbtn.pack(side="left")
    hardbtn['bg'] = hardbtn.master['bg']

    insanebtn = tk.Button(w, text="Insane", command=lambda: set_difficulty(4), font=("TkDefaultFont", 14), fg="#03a9f4", padx=50)
    insanebtn.pack(side="left")
    insanebtn['bg'] = insanebtn.master['bg']
    
    extremebtn = tk.Button(w, text="Extreme", command=lambda: set_difficulty(5), font=("TkDefaultFont", 14), fg="#03a9f4", padx=50)
    extremebtn.pack(side="left")
    extremebtn['bg'] = extremebtn.master['bg']

async def main():
    global attempts, dead, play_layer
    if gui:
        completedlevelsvar.set("0 levels completed!")
        lifevar.set("100 lives left!")
    levels = await client.search_levels(filters=gd.Filters(rated=True, difficulty=gd.LevelDifficulty(-2), demon_difficulty=gd.DemonDifficulty(difficulty)))
    random.shuffle(levels)
    for level in levels:
        if not gui:
            print("Next level is " + level.name + " with id " + str(level.id))
        else:
            levelvar.set(level.name + " by " + level.creator.name)
            idvar.set(level.id)
        while not play_layer.percent > 100:
            if closed:
                exit()
            play_layer = memory.get_game_manager().get_play_layer()
            gamelevel = play_layer.get_level_settings().get_level()
            if play_layer.dead:
                if gamelevel.id == level.id:
                    if dead:
                        attempts += 1
                        if not gui:
                            print("You died, you have " + str(100-attempts) + " lives left!")
                        else:
                            lifevar.set(str(100-attempts) + " lives left!")
                    dead = False
            else:
                dead = True
        if gui:
            completedlevelsvar.set(str(int(completedlevelsvar) + 1))
    # random extreme demons (maybe other types soon)

if __name__ == "__main__":
    #asyncio.set_event_loop(asyncio.new_event_loop())
    #loop = asyncio.get_event_loop()
    if gui:
        w.mainloop()
    else:
        Thread(target=start).start()