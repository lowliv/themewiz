def change_values(spacing,border_width,active_opacity,inactive_opacity,rounding,highlight_color,main_color,bg_path):
    import re
    import json
    import os
    import subprocess
    
    hex_string = highlight_color # Your Hex
    
    match = re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', hex_string)
    
    if match:                      
        hex_check = True
    else:
        hex_check = False
    home = os.getenv("HOME")
    os.chdir(f"{home}/.config")
    if os.path.isfile("hypr/hyprland.conf"):
        f = open("hypr/hyprland.conf", "r")
        l = f.readlines()
        f.close()
        for n in l:
            if n.find("border_size") >= 0:
                l[l.index(n)] = "    border_size = " + str(border_width) + "\n"
            elif n.find("rounding") >= 0:
                l[l.index(n)] = "    rounding = " + str(rounding) + "\n"
            elif n.find("gaps_in") >= 0:
                l[l.index(n)] = "    gaps_in = " + str(int(int(spacing)/2)) + "\n"
            elif n.find("gaps_out") >= 0:
                l[l.index(n)] = "    gaps_out = " + str(spacing) + "\n"
            elif n.find("inactive_opacity") >= 0:
                l[l.index(n)] = "    inactive_opacity = " + str(inactive_opacity) + "\n"
            elif n.find("active_opacity") >= 0:
                l[l.index(n)] = "    active_opacity = " + str(active_opacity) + "\n"
            elif n.find("col.active_border") >= 0 and hex_check == True:
                l[l.index(n)] = "    col.active_border = " + "0xee" + highlight_color[1:] + "\n"
        
        f = open("hypr/hyprland.conf", "w")
        f.writelines(l)
        f.close()
    
    if os.path.isfile("rofi/themes/rectangle.rasi"):
        f = open("rofi/themes/rectangle.rasi", "r")
        l = f.readlines()
        f.close()
        for n in l:
            if n.find("bg1:") >= 0:
                l[l.index(n)] = "    bg1: " + highlight_color + "EE;\n"
            elif n.find("fg3:") >= 0:
                l[l.index(n)] = "    fg3: " + highlight_color + "50;\n"
            elif n.find("border-radius") >= 0:
                l[l.index(n)] = "    border-radius: " + str(rounding) + ";\n"
            elif n.find("border:") >= 0:
                l[l.index(n)] = "    border: " + str(border_width) + "px;\n"
        
        f = open("rofi/themes/rectangle.rasi", "w")                
        f.writelines(l)
        f.close()
    
    if os.path.isfile("waybar/config-icons"):
        f = open("waybar/config-icons", "r")
        l = f.readlines()
        f.close()
        for n in l:
            if n.find("margin-left") >= 0:
                l[l.index(n)] = '    "margin-left": ' + str(spacing) + ",\n"
            elif n.find("margin-right") >= 0:
                l[l.index(n)] = '    "margin-right": ' + str(spacing) + ",\n"
            elif n.find("margin-top") >= 0:
                l[l.index(n)] = '    "margin-top": ' + str(int(int(spacing)/2)) + ",\n"
        
        f = open("waybar/config-icons", "w")
        f.writelines(l)
        f.close()
        
    if os.path.isfile("waybar/config-numbers"):
        f = open("waybar/config-numbers", "r")
        l = f.readlines()
        f.close()
        for n in l:
            if n.find("margin-left") >= 0:
                l[l.index(n)] = '    "margin-left": ' + str(spacing) + ",\n"
            elif n.find("margin-right") >= 0:
                l[l.index(n)] = '    "margin-right": ' + str(spacing) + ",\n"
            elif n.find("margin-top") >= 0:
                l[l.index(n)] = '    "margin-top": ' + str(int(int(spacing)/2)) + ",\n"
        
        f = open("waybar/config-numbers", "w")
        f.writelines(l)
        f.close()
    
    if os.path.isfile("waybar/style.css"):
        f = open("waybar/style.css", "r")
        l = f.readlines()
        f.close()
        for n in l:
            if n.find("border-radius") >= 0:
                l[l.index(n)] = '    border-radius: ' + str(rounding) + ";\n"
            elif n.find("background-color") >= 0:
                l[l.index(n)] = '    background-color: ' + highlight_color + ";\n"
        f = open("waybar/style.css", "w")
        f.writelines(l)
        f.close()
    
    os.system("killall waybar")
    command = "waybar -c $HOME/.config/waybar/config-icons &"
    subprocess.Popen(
        command, shell=True, preexec_fn=os.setpgrp, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
    
    
    if os.path.isfile("kitty/kitty.conf"):
        f = open("kitty/kitty.conf", "r")
        l = f.readlines()
        f.close()
        
        # default = blue
        color_num = 0
        color_names = [ "red", "green", "yellow", "blue", "magenta", "cyan"]
        for n in color_names:
            if main_color == n:
                color_num = color_names.index(n)+1
        
        if color_num == 0:
            print("color name didn't match one of the options so the colors won't be changed")
            quit()
        color_list = [5,1,3,2,6,4]
        color_map = ["123456","362514","246135","654321","415263","531642"]
        changed = 0
        red_num = 1
        for n in l:
            for c in color_list:
                if n.find("color" + str(c) + "  ") >= 0 and changed == 0 and not n.find(":") >= 0:
                    red_num = c
                    for q in color_map:
                        if q.find(str(red_num)) == 0:
                            current_color_map_index = color_map.index(q)
                            print(current_color_map_index)
                    for q in color_map:
                        if q.find("4") + 1 == color_num:
                            target_color_map_index = color_map.index(q)
                    
                    shifter = target_color_map_index - current_color_map_index
                    
                    changed +=1
                    l[l.index(n)] = 'color' + str(color_list[(color_list.index(c)+shifter) % 6]) + " " + n[7:]
                elif n.find("color" + str(c) + "  ") >= 0 and changed > 0 and not n.find(":") >= 0:
                    l[l.index(n)] = 'color' + str(color_list[(color_list.index(c)+shifter) % 6]) + " " + n[7:]
                elif n.find("color" + str(c+8)) >= 0 and changed > 0 and not n.find(":") >= 0:
                    l[l.index(n)] = 'color' + str(color_list[(color_list.index(c)+shifter) % 6] + 8) + " " + n[len(str(color_list[(color_list.index(c)+shifter) %6] +8))+len("color")+1:]
        
        f = open("kitty/kitty.conf", "w")
        f.writelines(l)
        f.close()
    
    
    if os.path.isfile("zellij/config.kdl"):
        f = open("zellij/config.kdl", "r")
        l = f.readlines()
        f.close()
        
        # default = blue
        color_num = 0
        color_names = [ "red", "green", "yellow", "blue", "magenta", "cyan", "orange"]
        for n in color_names:
            if main_color == n:
                color_num = color_names.index(n)+1
        
        if color_num == 0:
            print("color name didn't match one of the options so the colors won't be changed")
            quit()
        color_list = [5,1,7,3,2,6,4]
        color_map = ["1234567","7625143","3461752","2547316","6153274","4712635", "5376421"]
        changed = 0
        red_num = 1
        for n in l:
            for c in color_list:
                if n.find(" " + color_names[c-1] + " ") >= 0 and n.find("249 51 87") and changed == 0:
                    red_num = c
                    print("target green", color_num)
                    print("current red", red_num)
                    for q in color_map:
                        if q.find(str(red_num)) == 0:
                            current_color_map_index = color_map.index(q)
                            print(current_color_map_index)
                    for q in color_map:
                        if q.find("2") + 1 == color_num:
                            target_color_map_index = color_map.index(q)
                    print(target_color_map_index)
                    
                    shifter = target_color_map_index - current_color_map_index
                    print(shifter)
                    print((color_list.index(c)+shifter) % 7)
                    print(color_list[(color_list.index(c)+shifter) % 7])
                    
                    changed +=1
                    l[l.index(n)] = "        " + color_names[color_list[(color_list.index(c)+shifter) % 7]-1] + " " + n[len(color_names[c-1])+8:]
                elif n.find(" " + color_names[c-1] + " ") >= 0 and changed > 0:
                    l[l.index(n)] = "        " + color_names[color_list[(color_list.index(c)+shifter) % 7]-1] + " " + n[len(color_names[c-1])+8:]
        
        f = open("zellij/config.kdl", "w")
        f.writelines(l)
        f.close()
    
    
    if os.path.isfile("dunst/dunstrc"):
        f = open("dunst/dunstrc", "r")
        l = f.readlines()
        f.close()
        for n in l:
            if n.find("    frame_width = ") >= 0:
                l[l.index(n)] = '    frame_width = ' + str(border_width) + '\n'
            elif n.find("    frame_color = ") >= 0: 
                l[l.index(n)] = '    frame_color = "' + highlight_color + '"\n'
            elif n.find("    corner_radius = ") >= 0: 
                l[l.index(n)] = '    corner_radius = ' + str(rounding) + '\n'
            elif n.find("    offset = ") >= 0:
                l[l.index(n)] = '    offset = ' + str(2*spacing) + "x" + str(2*spacing) + '\n'
                
        f = open("dunst/dunstrc", "w")
        f.writelines(l)
        f.close()
    os.system("killall dunst-wb")
    os.system("killall dunstctl")
    os.system("pkill dunst")
    command = "dunst &"
    subprocess.Popen(
        command, shell=True, preexec_fn=os.setpgrp, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
    
    if int(rounding) > 21:
        rounding = str(21)
    
    if os.path.isfile("smartbot/config.json"):
        with open("smartbot/config.json", "r") as f:
            config = json.load(f)
       
        config["Style"]["ok_button"] = f"QPushButton {{ border-radius: {rounding}px; background-color: {highlight_color}; color: white; font-size: 16px; padding: 10px; border: none; }}"
        config["Style"]["cancel_button"] = f"QPushButton {{ border-radius: {rounding}px; background-color: {highlight_color}; color: white; font-size: 16px; padding: 10px; border: none; }}"
        
        with open("smartbot/config.json", "w") as f:
            json.dump(config, f, indent=4)
    os.system("pkill swaybg")
    command = "swaybg -i " + bg_path + " &"
    subprocess.Popen(
        command, shell=True, preexec_fn=os.setpgrp, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )    
    return
    # if os.path.isfile("smartbot/config.json"):
    #     f = open("smartbot/config.json", "r")
    #     l = f.readlines()
    #     f.close()
    #     for n in l:
    #         print(n)
    #         if n.find('    "ok_button": "QPushButton ') >= 0:
    #             print("found ok")
    #             l[l.index(n)] = '    "ok_button": "QPushButton { border-radius: ' + str(rounding) + 'px; background-color: ' + highlight_color + '; color: white; font-size: 16px; padding: 10px; border: none; }",'
    #         if n.find('    "cancel_button": "QPushButton ') >= 0:
    #             print("found ok")
    #             l[l.index(n)] = '    "cancel_button": "QPushButton { border-radius: ' + str(rounding) + 'px; background-color: ' + highlight_color + '; color: white; font-size: 16px; padding: 10px; border: none; }"'
    #     f = open("smartbot/config.json", "w")
    #     f.writelines(l)
    #     f.close()
    
def change_values(spacing,border_width,active_opacity,inactive_opacity,rounding,highlight_color,main_color,bg_path):
    import re
    import json
    import os
    
    hex_string = highlight_color # Your Hex
    
    match = re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', hex_string)
    
    if match:                      
        hex_check = True
    else:
        hex_check = False
        print("highlight_color is not a valid hex color so it won't be changed")
    home = os.getenv("HOME")
    os.chdir(f"{home}/.config")
    if os.path.isfile("hypr/hyprland.conf"):
        f = open("hypr/hyprland.conf", "r")
        l = f.readlines()
        f.close()
        for n in l:
            if n.find("border_size") >= 0:
                l[l.index(n)] = "    border_size = " + str(border_width) + "\n"
            elif n.find("rounding") >= 0:
                l[l.index(n)] = "    rounding = " + str(rounding) + "\n"
            elif n.find("gaps_in") >= 0:
                l[l.index(n)] = "    gaps_in = " + str(int(int(spacing)/2)) + "\n"
            elif n.find("gaps_out") >= 0:
                l[l.index(n)] = "    gaps_out = " + str(spacing) + "\n"
            elif n.find("inactive_opacity") >= 0:
                l[l.index(n)] = "    inactive_opacity = " + str(inactive_opacity) + "\n"
            elif n.find("active_opacity") >= 0:
                l[l.index(n)] = "    active_opacity = " + str(active_opacity) + "\n"
            elif n.find("col.active_border") >= 0 and hex_check == True:
                l[l.index(n)] = "    col.active_border = " + "0xee" + highlight_color[1:] + "\n"
        
        f = open("hypr/hyprland.conf", "w")
        f.writelines(l)
        f.close()
    
    if os.path.isfile("rofi/themes/rectangle.rasi"):
        f = open("rofi/themes/rectangle.rasi", "r")
        l = f.readlines()
        f.close()
        for n in l:
            if n.find("bg1:") >= 0:
                l[l.index(n)] = "    bg1: " + highlight_color + "EE;\n"
            elif n.find("fg3:") >= 0:
                l[l.index(n)] = "    fg3: " + highlight_color + "50;\n"
            elif n.find("border-radius") >= 0:
                l[l.index(n)] = "    border-radius: " + str(rounding) + ";\n"
            elif n.find("border:") >= 0:
                l[l.index(n)] = "    border: " + str(border_width) + "px;\n"
        
        f = open("rofi/themes/rectangle.rasi", "w")                
        f.writelines(l)
        f.close()
    
    if os.path.isfile("waybar/config-icons"):
        f = open("waybar/config-icons", "r")
        l = f.readlines()
        f.close()
        for n in l:
            if n.find("margin-left") >= 0:
                l[l.index(n)] = '    "margin-left": ' + str(spacing) + ",\n"
            elif n.find("margin-right") >= 0:
                l[l.index(n)] = '    "margin-right": ' + str(spacing) + ",\n"
            elif n.find("margin-top") >= 0:
                l[l.index(n)] = '    "margin-top": ' + str(int(int(spacing)/2)) + ",\n"
        
        f = open("waybar/config-icons", "w")
        f.writelines(l)
        f.close()
        
    if os.path.isfile("waybar/config-numbers"):
        f = open("waybar/config-numbers", "r")
        l = f.readlines()
        f.close()
        for n in l:
            if n.find("margin-left") >= 0:
                l[l.index(n)] = '    "margin-left": ' + str(spacing) + ",\n"
            elif n.find("margin-right") >= 0:
                l[l.index(n)] = '    "margin-right": ' + str(spacing) + ",\n"
            elif n.find("margin-top") >= 0:
                l[l.index(n)] = '    "margin-top": ' + str(int(int(spacing)/2)) + ",\n"
        
        f = open("waybar/config-numbers", "w")
        f.writelines(l)
        f.close()
    
    if os.path.isfile("waybar/style.css"):
        f = open("waybar/style.css", "r")
        l = f.readlines()
        f.close()
        for n in l:
            if n.find("border-radius") >= 0:
                l[l.index(n)] = '    border-radius: ' + str(rounding) + ";\n"
            elif n.find("background-color") >= 0:
                l[l.index(n)] = '    background-color: ' + highlight_color + ";\n"
        f = open("waybar/style.css", "w")
        f.writelines(l)
        f.close()
    
    os.system("killall waybar")
    os.system("waybar -c $HOME/.config/waybar/config-icons > /dev/null 2>&1 &")
    
    
    if os.path.isfile("kitty/kitty.conf"):
        f = open("kitty/kitty.conf", "r")
        l = f.readlines()
        f.close()
        
        # default = blue
        color_num = 0
        color_names = [ "red", "green", "yellow", "blue", "magenta", "cyan"]
        for n in color_names:
            if main_color == n:
                color_num = color_names.index(n)+1
        
        if color_num == 0:
            print("color name didn't match one of the options so the colors won't be changed")
            quit()
        color_list = [5,1,3,2,6,4]
        color_map = ["123456","362514","246135","654321","415263","531642"]
        changed = 0
        red_num = 1
        for n in l:
            for c in color_list:
                if n.find("color" + str(c) + "  ") >= 0 and changed == 0 and not n.find(":") >= 0:
                    red_num = c
                    for q in color_map:
                        if q.find(str(red_num)) == 0:
                            current_color_map_index = color_map.index(q)
                            print(current_color_map_index)
                    for q in color_map:
                        if q.find("4") + 1 == color_num:
                            target_color_map_index = color_map.index(q)
                    
                    shifter = target_color_map_index - current_color_map_index
                    
                    changed +=1
                    l[l.index(n)] = 'color' + str(color_list[(color_list.index(c)+shifter) % 6]) + " " + n[7:]
                elif n.find("color" + str(c) + "  ") >= 0 and changed > 0 and not n.find(":") >= 0:
                    l[l.index(n)] = 'color' + str(color_list[(color_list.index(c)+shifter) % 6]) + " " + n[7:]
                elif n.find("color" + str(c+8)) >= 0 and changed > 0 and not n.find(":") >= 0:
                    l[l.index(n)] = 'color' + str(color_list[(color_list.index(c)+shifter) % 6] + 8) + " " + n[len(str(color_list[(color_list.index(c)+shifter) %6] +8))+len("color")+1:]
        
        f = open("kitty/kitty.conf", "w")
        f.writelines(l)
        f.close()
    
    
    if os.path.isfile("zellij/config.kdl"):
        f = open("zellij/config.kdl", "r")
        l = f.readlines()
        f.close()
        
        # default = blue
        color_num = 0
        color_names = [ "red", "green", "yellow", "blue", "magenta", "cyan", "orange"]
        for n in color_names:
            if main_color == n:
                color_num = color_names.index(n)+1
        
        if color_num == 0:
            print("color name didn't match one of the options so the colors won't be changed")
            quit()
        color_list = [5,1,7,3,2,6,4]
        color_map = ["1234567","7625143","3461752","2547316","6153274","4712635", "5376421"]
        changed = 0
        red_num = 1
        for n in l:
            for c in color_list:
                if n.find(" " + color_names[c-1] + " ") >= 0 and n.find("249 51 87") and changed == 0:
                    red_num = c
                    print("target green", color_num)
                    print("current red", red_num)
                    for q in color_map:
                        if q.find(str(red_num)) == 0:
                            current_color_map_index = color_map.index(q)
                            print(current_color_map_index)
                    for q in color_map:
                        if q.find("2") + 1 == color_num:
                            target_color_map_index = color_map.index(q)
                    print(target_color_map_index)
                    
                    shifter = target_color_map_index - current_color_map_index
                    print(shifter)
                    print((color_list.index(c)+shifter) % 7)
                    print(color_list[(color_list.index(c)+shifter) % 7])
                    
                    changed +=1
                    l[l.index(n)] = "        " + color_names[color_list[(color_list.index(c)+shifter) % 7]-1] + " " + n[len(color_names[c-1])+8:]
                elif n.find(" " + color_names[c-1] + " ") >= 0 and changed > 0:
                    l[l.index(n)] = "        " + color_names[color_list[(color_list.index(c)+shifter) % 7]-1] + " " + n[len(color_names[c-1])+8:]
        
        f = open("zellij/config.kdl", "w")
        f.writelines(l)
        f.close()
    
    
    if os.path.isfile("dunst/dunstrc"):
        f = open("dunst/dunstrc", "r")
        l = f.readlines()
        f.close()
        for n in l:
            if n.find("    frame_width = ") >= 0:
                l[l.index(n)] = '    frame_width = ' + str(border_width) + '\n'
            elif n.find("    frame_color = ") >= 0: 
                l[l.index(n)] = '    frame_color = "' + highlight_color + '"\n'
            elif n.find("    corner_radius = ") >= 0: 
                l[l.index(n)] = '    corner_radius = ' + str(rounding) + '\n'
            elif n.find("    offset = ") >= 0:
                l[l.index(n)] = '    offset = ' + str(2*spacing) + "x" + str(2*spacing) + '\n'
                
        f = open("dunst/dunstrc", "w")
        f.writelines(l)
        f.close()
    os.system("killall dunst-wb")
    os.system("killall dunstctl")
    os.system("pkill dunst")
    os.system("dunst > /dev/null 2>&1 &")
    
    if int(rounding) > 21:
        rounding = str(21)
    
    if os.path.isfile("smartbot/config.json"):
        with open("smartbot/config.json", "r") as f:
            config = json.load(f)
       
        config["Style"]["ok_button"] = f"QPushButton {{ border-radius: {rounding}px; background-color: {highlight_color}; color: white; font-size: 16px; padding: 10px; border: none; }}"
        config["Style"]["cancel_button"] = f"QPushButton {{ border-radius: {rounding}px; background-color: {highlight_color}; color: white; font-size: 16px; padding: 10px; border: none; }}"
        
        with open("smartbot/config.json", "w") as f:
            json.dump(config, f, indent=4)
    os.system("pkill swaybg")
    os.system("swaybg -i " + bg_path + " > /dev/null 2>&1 &")
    os.system("disown")
    return
    # if os.path.isfile("smartbot/config.json"):
    #     f = open("smartbot/config.json", "r")
    #     l = f.readlines()
    #     f.close()
    #     for n in l:
    #         print(n)
    #         if n.find('    "ok_button": "QPushButton ') >= 0:
    #             print("found ok")
    #             l[l.index(n)] = '    "ok_button": "QPushButton { border-radius: ' + str(rounding) + 'px; background-color: ' + highlight_color + '; color: white; font-size: 16px; padding: 10px; border: none; }",'
    #         if n.find('    "cancel_button": "QPushButton ') >= 0:
    #             print("found ok")
    #             l[l.index(n)] = '    "cancel_button": "QPushButton { border-radius: ' + str(rounding) + 'px; background-color: ' + highlight_color + '; color: white; font-size: 16px; padding: 10px; border: none; }"'
    #     f = open("smartbot/config.json", "w")
    #     f.writelines(l)
    #     f.close()
    
def change_values(spacing,border_width,active_opacity,inactive_opacity,rounding,highlight_color,main_color,bg_path):
    import re
    import json
    import os
    
    hex_string = highlight_color # Your Hex
    
    match = re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', hex_string)
    
    if match:                      
        hex_check = True
    else:
        hex_check = False
        print("highlight_color is not a valid hex color so it won't be changed")
    home = os.getenv("HOME")
    os.chdir(f"{home}/.config")
    if os.path.isfile("hypr/hyprland.conf"):
        f = open("hypr/hyprland.conf", "r")
        l = f.readlines()
        f.close()
        for n in l:
            if n.find("border_size") >= 0:
                l[l.index(n)] = "    border_size = " + str(border_width) + "\n"
            elif n.find("rounding") >= 0:
                l[l.index(n)] = "    rounding = " + str(rounding) + "\n"
            elif n.find("gaps_in") >= 0:
                l[l.index(n)] = "    gaps_in = " + str(int(int(spacing)/2)) + "\n"
            elif n.find("gaps_out") >= 0:
                l[l.index(n)] = "    gaps_out = " + str(spacing) + "\n"
            elif n.find("inactive_opacity") >= 0:
                l[l.index(n)] = "    inactive_opacity = " + str(inactive_opacity) + "\n"
            elif n.find("active_opacity") >= 0:
                l[l.index(n)] = "    active_opacity = " + str(active_opacity) + "\n"
            elif n.find("col.active_border") >= 0 and hex_check == True:
                l[l.index(n)] = "    col.active_border = " + "0xee" + highlight_color[1:] + "\n"
        
        f = open("hypr/hyprland.conf", "w")
        f.writelines(l)
        f.close()
    
    if os.path.isfile("rofi/themes/rectangle.rasi"):
        f = open("rofi/themes/rectangle.rasi", "r")
        l = f.readlines()
        f.close()
        for n in l:
            if n.find("bg1:") >= 0:
                l[l.index(n)] = "    bg1: " + highlight_color + "EE;\n"
            elif n.find("fg3:") >= 0:
                l[l.index(n)] = "    fg3: " + highlight_color + "50;\n"
            elif n.find("border-radius") >= 0:
                l[l.index(n)] = "    border-radius: " + str(rounding) + ";\n"
            elif n.find("border:") >= 0:
                l[l.index(n)] = "    border: " + str(border_width) + "px;\n"
        
        f = open("rofi/themes/rectangle.rasi", "w")                
        f.writelines(l)
        f.close()
    
    if os.path.isfile("waybar/config-icons"):
        f = open("waybar/config-icons", "r")
        l = f.readlines()
        f.close()
        for n in l:
            if n.find("margin-left") >= 0:
                l[l.index(n)] = '    "margin-left": ' + str(spacing) + ",\n"
            elif n.find("margin-right") >= 0:
                l[l.index(n)] = '    "margin-right": ' + str(spacing) + ",\n"
            elif n.find("margin-top") >= 0:
                l[l.index(n)] = '    "margin-top": ' + str(int(int(spacing)/2)) + ",\n"
        
        f = open("waybar/config-icons", "w")
        f.writelines(l)
        f.close()
        
    if os.path.isfile("waybar/config-numbers"):
        f = open("waybar/config-numbers", "r")
        l = f.readlines()
        f.close()
        for n in l:
            if n.find("margin-left") >= 0:
                l[l.index(n)] = '    "margin-left": ' + str(spacing) + ",\n"
            elif n.find("margin-right") >= 0:
                l[l.index(n)] = '    "margin-right": ' + str(spacing) + ",\n"
            elif n.find("margin-top") >= 0:
                l[l.index(n)] = '    "margin-top": ' + str(int(int(spacing)/2)) + ",\n"
        
        f = open("waybar/config-numbers", "w")
        f.writelines(l)
        f.close()
    
    if os.path.isfile("waybar/style.css"):
        f = open("waybar/style.css", "r")
        l = f.readlines()
        f.close()
        for n in l:
            if n.find("border-radius") >= 0:
                l[l.index(n)] = '    border-radius: ' + str(rounding) + ";\n"
            elif n.find("background-color") >= 0:
                l[l.index(n)] = '    background-color: ' + highlight_color + ";\n"
        f = open("waybar/style.css", "w")
        f.writelines(l)
        f.close()
    
    os.system("killall waybar")
    os.system("waybar -c $HOME/.config/waybar/config-icons > /dev/null 2>&1 &")
    
    
    if os.path.isfile("kitty/kitty.conf"):
        f = open("kitty/kitty.conf", "r")
        l = f.readlines()
        f.close()
        
        # default = blue
        color_num = 0
        color_names = [ "red", "green", "yellow", "blue", "magenta", "cyan"]
        for n in color_names:
            if main_color == n:
                color_num = color_names.index(n)+1
        
        if color_num == 0:
            print("color name didn't match one of the options so the colors won't be changed")
            quit()
        color_list = [5,1,3,2,6,4]
        color_map = ["123456","362514","246135","654321","415263","531642"]
        changed = 0
        red_num = 1
        for n in l:
            for c in color_list:
                if n.find("color" + str(c) + "  ") >= 0 and changed == 0 and not n.find(":") >= 0:
                    red_num = c
                    for q in color_map:
                        if q.find(str(red_num)) == 0:
                            current_color_map_index = color_map.index(q)
                            print(current_color_map_index)
                    for q in color_map:
                        if q.find("4") + 1 == color_num:
                            target_color_map_index = color_map.index(q)
                    
                    shifter = target_color_map_index - current_color_map_index
                    
                    changed +=1
                    l[l.index(n)] = 'color' + str(color_list[(color_list.index(c)+shifter) % 6]) + " " + n[7:]
                elif n.find("color" + str(c) + "  ") >= 0 and changed > 0 and not n.find(":") >= 0:
                    l[l.index(n)] = 'color' + str(color_list[(color_list.index(c)+shifter) % 6]) + " " + n[7:]
                elif n.find("color" + str(c+8)) >= 0 and changed > 0 and not n.find(":") >= 0:
                    l[l.index(n)] = 'color' + str(color_list[(color_list.index(c)+shifter) % 6] + 8) + " " + n[len(str(color_list[(color_list.index(c)+shifter) %6] +8))+len("color")+1:]
        
        f = open("kitty/kitty.conf", "w")
        f.writelines(l)
        f.close()
    
    
    if os.path.isfile("zellij/config.kdl"):
        f = open("zellij/config.kdl", "r")
        l = f.readlines()
        f.close()
        
        # default = blue
        color_num = 0
        color_names = [ "red", "green", "yellow", "blue", "magenta", "cyan", "orange"]
        for n in color_names:
            if main_color == n:
                color_num = color_names.index(n)+1
        
        if color_num == 0:
            print("color name didn't match one of the options so the colors won't be changed")
            quit()
        color_list = [5,1,7,3,2,6,4]
        color_map = ["1234567","7625143","3461752","2547316","6153274","4712635", "5376421"]
        changed = 0
        red_num = 1
        for n in l:
            for c in color_list:
                if n.find(" " + color_names[c-1] + " ") >= 0 and n.find("249 51 87") and changed == 0:
                    red_num = c
                    print("target green", color_num)
                    print("current red", red_num)
                    for q in color_map:
                        if q.find(str(red_num)) == 0:
                            current_color_map_index = color_map.index(q)
                            print(current_color_map_index)
                    for q in color_map:
                        if q.find("2") + 1 == color_num:
                            target_color_map_index = color_map.index(q)
                    print(target_color_map_index)
                    
                    shifter = target_color_map_index - current_color_map_index
                    print(shifter)
                    print((color_list.index(c)+shifter) % 7)
                    print(color_list[(color_list.index(c)+shifter) % 7])
                    
                    changed +=1
                    l[l.index(n)] = "        " + color_names[color_list[(color_list.index(c)+shifter) % 7]-1] + " " + n[len(color_names[c-1])+8:]
                elif n.find(" " + color_names[c-1] + " ") >= 0 and changed > 0:
                    l[l.index(n)] = "        " + color_names[color_list[(color_list.index(c)+shifter) % 7]-1] + " " + n[len(color_names[c-1])+8:]
        
        f = open("zellij/config.kdl", "w")
        f.writelines(l)
        f.close()
    
    
    if os.path.isfile("dunst/dunstrc"):
        f = open("dunst/dunstrc", "r")
        l = f.readlines()
        f.close()
        for n in l:
            if n.find("    frame_width = ") >= 0:
                l[l.index(n)] = '    frame_width = ' + str(border_width) + '\n'
            elif n.find("    frame_color = ") >= 0: 
                l[l.index(n)] = '    frame_color = "' + highlight_color + '"\n'
            elif n.find("    corner_radius = ") >= 0: 
                l[l.index(n)] = '    corner_radius = ' + str(rounding) + '\n'
            elif n.find("    offset = ") >= 0:
                l[l.index(n)] = '    offset = ' + str(2*spacing) + "x" + str(2*spacing) + '\n'
                
        f = open("dunst/dunstrc", "w")
        f.writelines(l)
        f.close()
    os.system("killall dunst-wb")
    os.system("killall dunstctl")
    os.system("pkill dunst")
    os.system("dunst > /dev/null 2>&1 &")
    
    if int(rounding) > 21:
        rounding = str(21)
    
    if os.path.isfile("smartbot/config.json"):
        with open("smartbot/config.json", "r") as f:
            config = json.load(f)
       
        config["Style"]["ok_button"] = f"QPushButton {{ border-radius: {rounding}px; background-color: {highlight_color}; color: white; font-size: 16px; padding: 10px; border: none; }}"
        config["Style"]["cancel_button"] = f"QPushButton {{ border-radius: {rounding}px; background-color: {highlight_color}; color: white; font-size: 16px; padding: 10px; border: none; }}"
        
        with open("smartbot/config.json", "w") as f:
            json.dump(config, f, indent=4)
    os.system("pkill swaybg")
    os.system("swaybg -i " + bg_path + " > /dev/null 2>&1 &")
    os.system("disown")
    return
    # if os.path.isfile("smartbot/config.json"):
    #     f = open("smartbot/config.json", "r")
    #     l = f.readlines()
    #     f.close()
    #     for n in l:
    #         print(n)
    #         if n.find('    "ok_button": "QPushButton ') >= 0:
    #             print("found ok")
    #             l[l.index(n)] = '    "ok_button": "QPushButton { border-radius: ' + str(rounding) + 'px; background-color: ' + highlight_color + '; color: white; font-size: 16px; padding: 10px; border: none; }",'
    #         if n.find('    "cancel_button": "QPushButton ') >= 0:
    #             print("found ok")
    #             l[l.index(n)] = '    "cancel_button": "QPushButton { border-radius: ' + str(rounding) + 'px; background-color: ' + highlight_color + '; color: white; font-size: 16px; padding: 10px; border: none; }"'
    #     f = open("smartbot/config.json", "w")
    #     f.writelines(l)
    #     f.close()
    