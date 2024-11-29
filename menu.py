import questionary
import re
import os
import json
import sys
from themechanger import change_values

def is_integer(value):
    try:
        int(value)
        return True
    except ValueError:
        return False
    
def is_zero_to_one(value):
    try:
        n = float(value)
        if 0 <= n <= 1:
            return True
        else:
            return False
    except ValueError:
        return False
        
def is_hexcolor(value):
    match = re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', value)
    
    if match:                      
        hex_check = True
    else:
        hex_check = False
        
def apply(name=None): 
    with open("saved_values.json", 'r') as json_file:
        data = json.load(json_file)
    if name:   
        spacing = data[name]['spacing']
        border_width = data[name]['border_width']
        active_opacity = data[name]['active_opacity']
        inactive_opacity = data[name]['inactive_opacity']
        rounding = data[name]['rounding']
        highlight_color = data[name]['highlight_color']
        main_color = data[name]['main_color']
        bg_path = data[name]['bg_path']
        change_values(spacing,border_width,active_opacity,inactive_opacity,rounding,highlight_color,main_color,bg_path)
    else:
        spacing = data['spacing']
        border_width = data['border_width']
        active_opacity = data['active_opacity']
        inactive_opacity = data['inactive_opacity']
        rounding = data['rounding']
        highlight_color = data['highlight_color']
        main_color = data['main_color']
        bg_path = data['bg_path']
        change_values(spacing,border_width,active_opacity,inactive_opacity,rounding,highlight_color,main_color,bg_path)
    main_menu()

def is_colorname(value):
    color_num = 0
    color_names = [ "red", "green", "yellow", "blue", "magenta", "cyan"]
    for n in color_names:
        if Value == n:
            color_num = color_names.index(n)+1
            return True
        
    if color_num == 0:
        return False
    
def load_settings():
    with open("saved_values.json", 'r') as json_file:
        data = json.load(json_file)
    options = []
    options.append("Current")
# Check subtitles in nested dictionaries
    for key, value in data.items():
        if isinstance(value, dict):
            options.append(key)
    save = questionary.select(
        "Choose Save",
        choices = options,
        use_jk_keys = True
        ).ask()
    if save == "Current":
        apply()
    apply(save)
    
def delete_settings():
    with open("saved_values.json", 'r') as json_file:
        data = json.load(json_file)
    options = []
# Check subtitles in nested dictionaries
    for key, value in data.items():
        if isinstance(value, dict) and 'subtitle' in value:
            options.append(key)
    if len(options) == 0:
            print("No previous saves")
            main_menu()
    save = questionary.select(
        "Choose Save",
        choices = options,
        use_jk_keys = True
        ).ask()
    del data[save]

    with open("saved_values.json", 'w') as json_file:
        json.dump(data, json_file, indent=4)
    main_menu()
    
def save_settings():
    with open("saved_values.json", 'r') as json_file:
        data = json.load(json_file)
    name = questionary.text("Enter save name:").ask()
    data[name] = data.get(name, {})
    data[name]['spacing'] = data['spacing']
    data[name]['border_width'] = data['border_width']
    data[name]['active_opacity'] = data['active_opacity']
    data[name]['inactive_opacity'] = data['inactive_opacity']
    data[name]['rounding'] = data['rounding']
    data[name]['highlight_color'] = data['highlight_color']
    data[name]['main_color'] = data['main_color']
    data[name]['bg_path'] = data['bg_path']
    
    with open("saved_values.json", 'w') as json_file:
        json.dump(data, json_file, indent=4)
        
    main_menu()
    
def show_settings():
    with open("saved_values.json", 'r') as json_file:
        data = json.load(json_file)
    options = []
    # Check subtitles in nested dictionaries
    options.append("Current")
    for key, value in data.items():
        if isinstance(value, dict) and 'subtitle' in value:
            options.append(key)
    if len(options) == 0:
            print("No previous saves")
            main_menu()
    save = questionary.select(
        "Choose Save",
        choices = options,
        use_jk_keys = True
        ).ask()
    if save == "Current":
        print("spacing: " + str(data['spacing']))
        print("border_width: " + str(data['border_width']))
        print("active_opacity: " + str(data['active_opacity']))
        print("inactive_opacity: " + str(data['inactive_opacity']))
        print("rounding: " + str(data['rounding']))
        print("highlight_color: " + str(data['highlight_color']))
        print("main_color: " + str(data['main_color']))
        print("bg_path: " + str(data['bg_path']))
    else:
        print("spacing: " + str(data[save]['spacing']))
        print("border_width: " + str(data[save]['border_width']))
        print("active_opacity: " + str(data[save]['active_opacity']))
        print("inactive_opacity: " + str(data[save]['inactive_opacity']))
        print("rounding: " + str(data[save]['rounding']))
        print("highlight_color: " + str(data[save]['highlight_color']))
        print("main_color: " + str(data[save]['main_color']))
        print("bg_path: " + str(data[save]['bg_path']))
        
    with open("saved_values.json", 'w') as json_file:
        json.dump(data, json_file, indent=4)
    main_menu()
    
def enter_settings():
    home_path = os.environ.get('HOME')
    os.system("mkdir -p $HOME/.config/themertui")
    os.chdir(f"{home_path}/.config/themertui")
    with open("saved_values.json", 'r') as json_file:
        data = json.load(json_file)
     
        value = questionary.select(
            "Choose Values",
            choices = ["Spacing", "Border Width", "Opacity", "Rounding", "Highlight Color", "Main Color Name", "Background Path\n", "Back"],
            use_jk_keys = True
            ).ask()
    
    if value == "Spacing":
        spacing  = questionary.text("Enter spacing value in pixels:",validate=is_integer).ask()
        data['spacing'] = spacing
    if value == "Border Width":
        boder_width  = questionary.text("Enter border width in pixels:",validate=is_integer).ask()
        data['border_width'] = boder_width
    if value == "Opacity":
        sub_value = questionary.select(
            "Choose Values",
            choices = ["Active Opacity", "Inactive Opacity"],
            use_jk_keys = True
            ).ask()
        if sub_value == "Active Opacity":
            active_opacity  = questionary.text("Enter active opacity 0 to 1:",validate=is_zero_to_one).ask()
            data['active_opacity'] = active_opacity
        if sub_value == "Inactive Opacity":
            inactive_opacity  = questionary.text("Enter inactive opacity 0 to 1:",validate=is_zero_to_one).ask()
            data['inactive_opacity'] = inactive_opaticy
    if value == "Rounding":
        rounding  = questionary.text("Enter rounding value in pixels:",validate=is_integer).ask()
        data['rounding'] = rounding
    if value == "Highlight Color":
        highlight_color  = questionary.text("Enter highlight color in hex (#..):",validate=is_hexcolor).ask()
        data['highlight_color'] = highlight_color
    if value == "Main Color Name":
        main_color  = questionary.text("Enter a color name (ex: red):",validate=is_colorname).ask()
        data['main_color'] = main_color
    if value == "Background Path\n":
        bg_path = questionary.path("Enter the path to a background").ask()
        data['bg_path'] = bg_path
    if value == "Back":
        main_menu()

    with open("saved_values.json", 'w') as json_file:
        json.dump(data, json_file, indent=4)
    enter_settings()
   
def main_menu():
    home_path = os.environ.get('HOME')
    os.system("mkdir -p $HOME/.config/themertui")
    os.chdir(f"{home_path}/.config/themertui")
    answer = questionary.select(
        "Select an option:",
        choices=["Load Settings", "Delete Previous Save", "Show Settings", "Save Current Settings", "Enter New Settings\n", "Exit"],
        use_jk_keys = True
    ).ask()
    
    if answer == "Load Settings":
        load_settings()
    if answer == "Delete Previous Save":
        delete_settings()
    if answer == "Save Current Settings":
        save_settings()
    if answer == "Show Settings":
        show_settings()
    if answer == "Enter New Settings\n":
        enter_settings()
    if answer == "Exit":
        sys.exit()
        
if __name__ == "__main__":
    home_path = os.environ.get('HOME')
    os.system("mkdir -p $HOME/.config/themertui")
    os.chdir(f"{home_path}/.config/themertui")
    if not os.path.isfile("saved_values.json"):
        default_data = {
            "spacing": "10",
            "border_width": "2",
            "active_opacity": "1",
            "inactive_opacity": "1",
            "rounding": "0",
            "highlight_color": "#f93357",
            "main_color": "red",
            "bg_path": ""
        }

        with open('saved_values.json', 'w') as json_file:
            json.dump(default_data, json_file, indent=4)
    
    main_menu()
