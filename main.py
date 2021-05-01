from tkinter import *
from tkinter import ttk
from character import Character
from move import Move

heap_mode = True
insert_mode = False
sicko_mode = False

my_char = []
my_curr_char = ""
opp_curr_char = ""
my_curr_moves = []
opp_curr_moves = []
char_dict = {}


# read in files
def file_reader(character, filename):
    arr = []
    with open(filename) as f:
        lines = f.readlines()

    i = 0
    while i < len(lines):
        notation = lines[i]
        i += 1
        startup = lines[i]
        pos = 0
        for k in range(0, len(startup)):
            if startup[k:k+1] != '1' and startup[k:k+1] != '2' and startup[k:k+1] != '3'\
             and startup[k:k+1] != '4' and startup[k:k+1] != '5' and startup[k:k+1] != '6'\
             and startup[k:k+1] != '7' and startup[k:k+1] != '8' and startup[k:k+1] != '9'\
             and startup[k:k+1] != '0':
                break
            pos = pos + 1
        startup = startup[0:pos]
        i += 1
        active = lines[i]
        i += 1
        recovery = lines[i]
        i += 1
        h = lines[i]
        if h[0:1] != '~' and h[0:1] != '-' and h[0:2] != 'KD':
            h = "+" + h
        i += 1
        b = lines[i]
        if b[0:1] != '~' and b[0:1] != '-' and b[0:2] != 'KD':
            b = "+" + b
        i += 1
        damage = lines[i]
        i += 1
        stun = lines[i]
        i += 1
        knd = lines[i]
        i += 1
        vt_oh = lines[i]
        if vt_oh[0:1] != '~' and vt_oh[0:1] != '-' and vt_oh[0:2] != 'KD':
            vt_oh = "+" + vt_oh
        i += 1
        vt_ob = lines[i]
        if vt_ob[0:1] != '~' and vt_ob[0:1] != '-' and vt_ob[0:2] != 'KD':
            vt_ob = "+" + vt_ob
        i += 1

        if len(startup) > 0:
            move = Move(notation, startup, active, recovery, h, b, damage, stun, knd, vt_oh, vt_ob)
            character.add_move(move)


akuma = Character("Akuma", 900, 900)
my_char.append(akuma.name)
char_dict[akuma.name] = akuma
file_reader(akuma, "akuma.txt")

m_bison = Character("M. Bison", 1000, 1000)
my_char.append(m_bison.name)
char_dict[m_bison.name] = m_bison
file_reader(m_bison, "m_bison.txt")

ken = Character("Ken", 1025, 1050)
my_char.append(ken.name)
char_dict[ken.name] = ken
file_reader(ken, "ken.txt")

ryu = Character("Ryu", 1025, 1050)
my_char.append(ryu.name)
char_dict[ryu.name] = ryu
file_reader(ryu, "ryu.txt")

guile = Character("Guile", 975, 975)
my_char.append(guile.name)
char_dict[guile.name] = guile
file_reader(guile, "guile.txt")


root = Tk()
root.geometry("450x600")
root.title("SFV Frame Data Visualizer")
if heap_mode:
    root.title("SFV Frame Data Visualizer (Heap Sort Mode)")
elif insert_mode:
    root.title("SFV Frame Data Visualizer (Insertion Sort Mode)")
elif sicko_mode:
    root.title("SFV Frame Data Visualizer (SICKO MODE!)")

# frame advantage: default = 0
frame_adv = 0


def reset():
    global frame_adv
    frame_adv = 0
    frame_slider.set(0)
    my_dropdown.set("")
    opp_dropdown.set("")
    infobox.config(text="")
    my_moves.selection_clear(ANCHOR)
    my_moves.delete(0, 'end')
    opp_moves.selection_clear(ANCHOR)
    opp_moves.delete(0, 'end')
    my_movelist.config(text="")
    opp_movelist.config(text="")


def move_select(bro):  # print info
    if my_moves.curselection():
        for move in char_dict[my_curr_char].moveset:
            if move.notation == my_moves.get(ANCHOR):
                infobox.config(text="Move Information:\nNotation: "+move.notation+"Startup Frame: i"+move.startup
                               + "\nActive Frames: "+move.active+"Recovery Frames: "+move.recovery+"On Hit: "
                               + move.h+"On Block: "+move.b+"Damage: "+move.damage+"Stun: "
                               + move.stun+"Knockdown Frames: "+move.knd+"V-Trigger On Hit: "+move.vt_oh
                               + "V-Trigger On Block: "+move.vt_ob)
    elif opp_moves.curselection():
        for move in char_dict[opp_curr_char].moveset:
            if move.notation == opp_moves.get(ANCHOR):
                infobox.config(text="Move Information:\nNotation: "+move.notation+"Startup Frame: i"+move.startup
                               + "\nActive Frames: "+move.active+"Recovery Frames: "+move.recovery+"On Hit: "
                               + move.h+"On Block: "+move.b+"Damage: "+move.damage+"Stun: "
                               + move.stun+"Knockdown Frames: "+move.knd+"V-Trigger On Hit: "+move.vt_oh
                               + "V-Trigger On Block: "+move.vt_ob)

    global frame_adv
    frame_adv = frame_slider.get()


def char_select(event):
    global my_curr_moves
    global my_curr_char
    my_curr_moves = set_moves(my_dropdown.get())
    my_curr_char = my_dropdown.get()
    my_movelist.config(text=my_dropdown.get()+"'s moveset\nHealth: "+str(char_dict[my_dropdown.get()].hp)+
                            " | Stun: "+str(char_dict[my_dropdown.get()].stun))
    my_moves.selection_clear(ANCHOR)
    my_moves.delete(0, 'end')
    for i in my_curr_moves:
        my_moves.insert(END, i)


def opp_select(event):
    global opp_curr_moves
    global opp_curr_char
    opp_curr_moves = set_moves(opp_dropdown.get())
    opp_curr_char = opp_dropdown.get()
    opp_movelist.config(text=opp_dropdown.get()+"'s moveset\nHealth: "+str(char_dict[opp_dropdown.get()].hp)+
                            " | Stun: "+str(char_dict[opp_dropdown.get()].stun))
    opp_moves.selection_clear(ANCHOR)
    opp_moves.delete(0, 'end')
    for i in opp_curr_moves:
        opp_moves.insert(END, i)


def set_moves(name):
    arr = []
    t = []
    if name in char_dict:
        t = char_dict[name].moveset
    for i in t:
        arr.append(i.notation)
    return arr


def loser():
    global frame_adv
    frame_adv = frame_slider.get()
    if my_curr_char in char_dict and opp_curr_char in char_dict and my_moves.curselection():
        if insert_mode:
            insertion_sort("loser")
        if heap_mode:
            heap_sort("loser")
        if sicko_mode:
            print("SICKO MODE")


def trader():
    global frame_adv
    frame_adv = frame_slider.get()
    if my_curr_char in char_dict and opp_curr_char in char_dict and my_moves.curselection():
        if insert_mode:
            insertion_sort("trader")
        if heap_mode:
            heap_sort("trader")
        if sicko_mode:
            print("SICKO MODE")


def winner():
    global frame_adv
    frame_adv = frame_slider.get()
    if my_curr_char in char_dict and opp_curr_char in char_dict and my_moves.curselection():
        if insert_mode:
            insertion_sort("winner")
        if heap_mode:
            heap_sort("winner")
        if sicko_mode:
            print("SICKO MODE")


def heap_sort(tipo):
    threshold = 0
    global opp_curr_moves
    opp_curr_moves.clear()
    opp_moves.selection_clear(ANCHOR)
    opp_moves.delete(0, 'end')
    new_moves = []
    for move in char_dict[my_curr_char].moveset:
        if move.notation == my_moves.get(ANCHOR):
            threshold = int(move.startup) - frame_adv
            break

    for move in char_dict[opp_curr_char].moveset:
        if int(move.startup) < threshold and tipo == "loser":
            new_moves.append(move)
        elif int(move.startup) == threshold and tipo == "trader":
            new_moves.append(move)
        elif int(move.startup) > threshold and tipo == "winner":
            new_moves.append(move)

    # the actual sorting
    min_heap = []
    for move in new_moves:
        min_heap = heap_insert(min_heap, int(len(min_heap)), move)

    new_moves.clear()
    while len(min_heap) > 0:
        new_moves.append(min_heap[0])
        min_heap = heap_remove(min_heap, len(min_heap)-1)

    for move in new_moves:
        opp_curr_moves.append(move.notation)
        opp_moves.insert(END, move.notation)


def heap_insert(heap, size, key):
    heap.append(key)
    while size > 0 and heap[size].startup < heap[int((size-1)/2)].startup:
        heap[size], heap[int((size-1)/2)] = heap[int((size-1)/2)], heap[size]
        size = int((size-1)/2)
    return heap


def heap_remove(heap, size):
    heap[0] = heap[size]
    del(heap[size])
    index = 0
    while index < size:
        left = 2*index+1
        right = 2*index+2
        if left < size < right and int(heap[left].startup) < int(heap[index].startup):
            heap[index], heap[left] = heap[left], heap[index]
            index = left
        elif right < size < left and int(heap[right].startup) < int(heap[index].startup):
            heap[index], heap[right] = heap[right], heap[index]
            index = right
        elif left < size and right < size:
            if int(heap[left].startup) < int(heap[index].startup) and int(heap[left].startup) <= int(heap[right].startup):
                heap[index], heap[left] = heap[left], heap[index]
                index = left
            elif int(heap[right].startup) < int(heap[index].startup) and int(heap[left].startup) > int(heap[right].startup):
                heap[index], heap[right] = heap[right], heap[index]
                index = right
            else:
                break
        else:
            break
    return heap


def insertion_sort(tipo):
    threshold = 0
    global opp_curr_moves
    opp_curr_moves.clear()
    opp_moves.selection_clear(ANCHOR)
    opp_moves.delete(0, 'end')
    new_moves = []
    for move in char_dict[my_curr_char].moveset:
        if move.notation == my_moves.get(ANCHOR):
            threshold = int(move.startup) - frame_adv
            break

    for move in char_dict[opp_curr_char].moveset:
        if int(move.startup) < threshold and tipo == "loser":
            new_moves.append(move)
        elif int(move.startup) == threshold and tipo == "trader":
            new_moves.append(move)
        elif int(move.startup) > threshold and tipo == "winner":
            new_moves.append(move)

    # the actual sorting
    index = 1
    while index < len(new_moves):
        i = index
        while i > 0:
            if int(new_moves[i].startup) < int(new_moves[i - 1].startup):
                new_moves[i], new_moves[i - 1] = new_moves[i - 1], new_moves[i]
            i -= 1
        index += 1

    for move in new_moves:
        opp_curr_moves.append(move.notation)
        opp_moves.insert(END, move.notation)


# buttons
reset = Button(root, text="RESET", command=reset).pack(side=BOTTOM, anchor='se')
lose = Button(root, text="Loses to", command=loser).pack(side=BOTTOM, anchor='s')
trade = Button(root, text="Trades with", command=trader).pack(side=BOTTOM, anchor='s')
win = Button(root, text="Wins against", command=winner).pack(side=BOTTOM, anchor='s')

# move properties/information
infobox = Label(root, text="", anchor='w', justify=LEFT, padx=30)
infobox.pack(side=BOTTOM, fill="both")
frame_label = Label(root, text="Frame Advantage:").pack()

# slider for frame advantage
frame_slider = Scale(root, from_=-20, to_=+20, orient=HORIZONTAL, resolution=1,)
frame_slider.pack()

# labels for character/opponent names
name_frame = Frame(root)
name_frame.pack()
char_label = Label(name_frame, text=" Character\t\t\t            Opponent").pack(padx=15, side=TOP)

# frame and scrollbar for movelists
my_frame = Frame(root)
my_movelist = Label(my_frame, text="")
my_movelist.pack()
my_scrollbar = Scrollbar(my_frame, orient=VERTICAL)

my_moves = Listbox(my_frame, width=25, yscrollcommand=my_scrollbar.set)
my_moves.bind('<<ListboxSelect>>', move_select)  # function that executes when move selected

my_scrollbar.config(command=my_moves.yview)
my_scrollbar.pack(side=RIGHT, fill=Y)
my_frame.pack(side=LEFT, padx=30)

my_moves.pack()

# same but for opponent
opp_frame = Frame(root)
opp_movelist = Label(opp_frame, text="")
opp_movelist.pack()
opp_scrollbar = Scrollbar(opp_frame, orient=VERTICAL)

opp_moves = Listbox(opp_frame, width=25, yscrollcommand=opp_scrollbar.set)
opp_moves.bind('<<ListboxSelect>>', move_select)  # function that executes when move selected

opp_scrollbar.config(command=opp_moves.yview)
opp_scrollbar.pack(side=RIGHT, fill=Y)
opp_frame.pack(side=RIGHT, padx=20)

opp_moves.pack()


my_dropdown = ttk.Combobox(name_frame, value=my_char, width=11)
my_dropdown.bind("<<ComboboxSelected>>", char_select)
my_dropdown.pack(side=LEFT, padx=70)

opp_dropdown = ttk.Combobox(name_frame, value=my_char, width=11)
opp_dropdown.bind("<<ComboboxSelected>>", opp_select)
opp_dropdown.pack(side=BOTTOM, padx=70)

root.mainloop()
