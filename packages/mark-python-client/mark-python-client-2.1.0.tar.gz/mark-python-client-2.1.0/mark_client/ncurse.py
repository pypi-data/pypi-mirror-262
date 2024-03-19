'''
Terminal vue of menu

'''
import curses

class Input:
    '''
    Gestion of argument menu
    '''
    def __init__(self, screen, param_info_list) -> None:
        self.screen = screen
        self.ret = []
        self.subscreen = []
        self.position_list = []
        self.param_index = 0
        self.last_decalage = 0
        self.param_info_list = param_info_list
        self.screen.clear()
        # print screen and setup subscreen for inputs
        for i, p in enumerate(param_info_list):
            num_rows, num_cols = self.screen.getmaxyx()
            if 3+i < num_rows:
                self.subscreen.append(self.screen.subwin(1, num_cols-2, 3+i, 2))
                self.subscreen[-1].keypad(True)
                if i == 0:
                    self.subscreen[-1].addstr("*")
                else:
                    self.subscreen[-1].addstr(" ")
                self.subscreen[-1].addstr(f"input {p} : ")
                if i == 0:
                    self.subscreen[-1].addstr(" ", curses.A_REVERSE)
                self.subscreen[-1].refresh()
            self.ret.append("")
            self.position_list.append(0)
        self.screen.addstr(2,2,"Input Parsams")
        self.screen.refresh()

    def print_inputs(self):
        '''
        Print the menu and the input already given
        '''
        decalage = 0
        pos = self.position_list[self.param_index]
        if self.param_index >= len(self.subscreen):
            decalage = self.param_index - len(self.subscreen) +1
        for l, screen in enumerate(self.subscreen):
            user_input = self.ret[l + decalage]
            if self.param_index-1 <= l+decalage <= self.param_index + 1 or\
                  decalage != self.last_decalage:
                screen.clear()
                if l + decalage == self.param_index:
                    screen.addstr("*")
                else:
                    screen.addstr(" ")
                size_input = len(f"input {self.param_info_list[l + decalage]} : ")
                screen.addstr(f"input {self.param_info_list[l + decalage]} : ")
                start = max(0, pos - screen.getmaxyx()[1] + size_input + 4)
                self.screen.addstr(1,1,str(start))
                if start < 0:
                    start = 0
                for i, user_input_char in enumerate(user_input[start:] + " "):
                    if i+size_input+1 >= screen.getmaxyx()[1]:
                        break
                    screen.addstr(
                        0,size_input + i,
                        user_input_char,
                        0 if i != pos or l + decalage != self.param_index else curses.A_REVERSE
                    )

                screen.refresh()
        self.last_decalage = decalage

    def key_action(self, key):
        '''
        What to do when a key is pressed
        '''
        if key==ord('\n'): # go to next input
            self.param_index += 1
        elif key == curses.KEY_BACKSPACE: # remove char
            pos = self.position_list[self.param_index]
            txt = self.ret[self.param_index]
            txt = txt[:pos-1] + txt[pos:]
            self.ret[self.param_index] = txt
            self.position_list[self.param_index]-=1
        elif key == curses.KEY_LEFT: # move cursor left
            self.position_list[self.param_index]-=1
            if self.position_list[self.param_index] < 0:
                self.position_list[self.param_index] = 0
        elif key == curses.KEY_RIGHT: # move cursor right
            self.position_list[self.param_index]+=1
            if self.position_list[self.param_index] > len(self.ret[self.param_index]):
                self.position_list[self.param_index] = len(self.ret[self.param_index])
        elif key == curses.KEY_UP: # go previous input
            if self.param_index > 0:
                self.param_index -= 1
        elif key == curses.KEY_DOWN: # go to next input
            if self.param_index < len(self.param_info_list)-1:
                self.param_index += 1
        else: # add the char to index
            pos = self.position_list[self.param_index]
            txt = self.ret[self.param_index]
            txt = txt[:pos] + chr(key) + txt[pos:]
            self.ret[self.param_index] = txt
            self.position_list[self.param_index] += 1

    def __call__(self) -> str:
        return self.get()

    def get(self):
        '''
        Entry point
        '''
        if len(self.param_info_list)==0:
            return []
        while True:
            c = self.screen.getch()
            if c == ord('\n') and self.param_index == len(self.param_info_list)-1:
                map(lambda x:x.clear(), self.subscreen)
                map(lambda x:x.refresh(), self.subscreen)
                return self.ret
            self.key_action(c)
            self.print_inputs()

class MenuCurses:
    '''
    The Menu
    '''
    def __init__(self):
        self.screen = curses.initscr()
        curses.curs_set(0)
        self.screen.keypad(True)
        self.screen.refresh()
        curses.noecho()

    def get_parameters(self, param_info_list):
        '''
        Get the parameters needed for the function
        '''
        input_param = Input(self.screen, param_info_list)
        return input_param.get()

    def _print_result(self, data):
        '''
        Print result of function and wait for keyboard input
        '''
        nb = 0
        _, num_col = self.screen.getmaxyx()

        while nb * num_col < len(data):
            self.screen.clear()
            self.screen.addstr(2, 2, "result")
            _, num_col = self.screen.getmaxyx()
            self.screen.addstr(4, 3, repr(data[num_col * nb:]))
            self.screen.refresh()
            c = self.screen.getch()
            if c == ord('\n') or c == curses.KEY_DOWN:
                nb+=1
            elif c == curses.KEY_UP and nb > 0:
                nb-=1
        self.screen.clear()
        return

    def print_info(self, menu):
        '''
        print basic info for the menu
        '''
        self.screen.clear()
        self.screen.addstr(2, 8, menu["Title"])
        self.screen.addstr(5, 8, menu["Desc"])
        self.screen.refresh()

    def show_menu(self, menu):
        '''
        show menu and selection of options
        '''
        options = menu["option"].copy()
        options.extend([{"name":"return", "info":"return"}, {"name":"exit", "info":"exit"}])

        pos = 0 # index of the choice
        while True:
            num_rows, _ = self.screen.getmaxyx()
            self.print_info(menu)
            # print choices
            for i in range(num_rows-6):
                if i >= len(options):
                    break
                self.screen.addstr(6+i, 8,
                                options[(i+pos) % len(options)]["name"],
                                0 if i!=0 else curses.A_UNDERLINE)
            # gestion input
            key = self.screen.getch()
            if key == curses.KEY_UP:
                pos-=1
                if pos == -1:
                    pos = len(options)-1
            elif key == curses.KEY_DOWN:
                pos = (pos + 1)%(len(options))
            elif key == 10: # enter
                param_choosed = options[pos]["info"]
                if param_choosed == "return": # come back one sub menu 
                    self.screen.clear()
                    return
                elif param_choosed == "exit": # exit the app
                    exit(0)
                elif param_choosed["type"]=="submenu": # go to a submenu
                    self.show_menu(param_choosed["submenu"])
                elif param_choosed["type"]=="function": # run a function
                    params = param_choosed["params"] if "params" in param_choosed else []
                    self._print_result(param_choosed["function"](*self.get_parameters(params)))
            self.screen.refresh()

    def run(self, menu):
        '''
        Entry point off the program
        '''
        try:
            self.show_menu(menu)
        finally:
            curses.endwin()

class MenuBuilder:
    '''
    Build correctly the menu dict
    '''
    def __init__(self, title:str, description:str) -> None:
        self.menu = {
            "Title":title,
            "Desc":description,
            "option":[]
        }

    def add_function(self, name:str, func, params:list):
        '''
        add a function
        '''
        self.menu["option"].append({
            "name":name,
            "info":{
                    "type":"function",
                    "function":func,
                    "params":params}
                })
        return self

    def add_sub_menu(self, name, menu:dict):
        '''
        add a submenu
        '''
        self.menu["option"].append({
                "name": name,
                "info":{
                    "type":"submenu",
                    "submenu":menu
                }
            }
        )
        return self

    def get(self):
        '''
        get the menu
        '''
        return self.menu


if __name__ == "__main__":
    menu_test = MenuBuilder("test Menu","this is a test menu")\
                    .add_function("print a", lambda a:a[0], [
                        {"1":"str"},
                        {"2":"str"},
                        {"3":"str"},
                        {"4":"str"},
                        {"5":"str"},
                        {"6":"str"},
                        {"7":"str"},
                        {"8":"str"},
                        {"9":"str"},
                        {"10":"str"},
                        {"11":"str"},
                        {"12":"str"}
                    ])\
                    .add_sub_menu("go to menu b",
                                  MenuBuilder("test Menu B","this is a test second menu")\
                    .add_function("print b", lambda : "b", []).get()).get()
    w = MenuCurses()
    w.run(menu=menu_test)
