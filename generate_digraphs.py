import os

KEYS_LIST = [["Oemtilde", "D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9", "D0", "OemMinus", "Oemplus", "Back"],
        ["", "Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "OemOpenBrackets", "Oem6", "Oem5"],
        ["Capital", "A", "S", "D", "F", "G", "H", "J", "K", "L", "Oem1", "Oem7", "Return"],
        ["LShiftKey", "Z", "X", "C", "V", "B", "N", "M", "Oemcomma", "OemPeriod", "OemQuestion", "RShiftKey"],
        ["", "", "", "", "Space", "Space", "Space", "Space", "Space", "", "", "Left", "", "Right"]]

KEYS_FLAT = ["Oemtilde", "D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9", "D0", "OemMinus", "Oemplus", "Back",
        "Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "OemOpenBrackets", "Oem6", "Oem5",
        "Capital", "A", "S", "D", "F", "G", "H", "J", "K", "L", "Oem1", "Oem7", "Return",
        "LShiftKey", "Z", "X", "C", "V", "B", "N", "M", "Oemcomma", "OemPeriod", "OemQuestion", "RShiftKey",
        "Space", "Left", "Right"]


def find_key(key, KEYS_LIST):
    for i in range(len(KEYS_LIST)):
        if key in KEYS_LIST[i]:
            return i, KEYS_LIST[i].index(key)


def parse_file(path, dataset_type, KEYS_LIST, KEYS_FLAT):
    for i in range(0, 3):
        curr_path = f'{path}/s{i}/{dataset_type}'
        for filename in os.listdir(curr_path):
            with open(os.path.join(curr_path, filename)) as f:
                pressed_keys = []
                lines = f.readlines()
                for line in lines:
                    key, action, time = line.split()
                    if key not in KEYS_FLAT:
                        continue
                    x, y = find_key(key, KEYS_LIST)
                    if action == 'KeyDown':
                        pressed_keys.append([key, x, y, time, None])
                    else:
                        for pressed_key in range(len(pressed_keys)-1, -1, -1):
                            if pressed_keys[pressed_key][1] == x and pressed_keys[pressed_key][2] == y:
                                if pressed_keys[pressed_key][4] is None:
                                    pressed_keys[pressed_key][4] = time
                                break

            save_path = f'digraphs/s{i}/{dataset_type}/{filename}'
            with open(save_path, 'w') as f:
                for j in range(1, len(pressed_keys)):
                    try:
                        x = pressed_keys[j-1][1] - pressed_keys[j][1]
                        y = pressed_keys[j-1][2] - pressed_keys[j][2]
                        ht1 = int(pressed_keys[j-1][4]) - int(pressed_keys[j-1][3])
                        ht2 = int(pressed_keys[j][4]) - int(pressed_keys[j][3])
                        ptp = int(pressed_keys[j][3]) - int(pressed_keys[j-1][3])
                        rtp = int(pressed_keys[j][3]) - int(pressed_keys[j-1][4])
                        s = f'{pressed_keys[j-1][0]} {pressed_keys[j][0]} {x} {y} {ht1} {ht2} {ptp} {rtp}'
                        f.write(s + '\n')
                    except:
                        pass
                        # print(curr_path, filename, pressed_keys[j-1], pressed_keys[j])


if __name__ == "__main__":
    if not os.path.exists('digraphs'):
        os.makedirs('digraphs')
    if not os.path.exists('digraphs/s0'):
        os.makedirs('digraphs/s0')
    if not os.path.exists('digraphs/s1'):
        os.makedirs('digraphs/s1')
    if not os.path.exists('digraphs/s2'):
        os.makedirs('digraphs/s2')
    if not os.path.exists('digraphs/s0/baseline'):
        os.makedirs('digraphs/s0/baseline')
    if not os.path.exists('digraphs/s1/baseline'):
        os.makedirs('digraphs/s1/baseline')
    if not os.path.exists('digraphs/s2/baseline'):
        os.makedirs('digraphs/s2/baseline')
    if not os.path.exists('digraphs/s0/rotation'):
        os.makedirs('digraphs/s0/rotation')
    if not os.path.exists('digraphs/s1/rotation'):
        os.makedirs('digraphs/s1/rotation')
    if not os.path.exists('digraphs/s2/rotation'):
        os.makedirs('digraphs/s2/rotation')
    parse_file('UB_keystroke_dataset', 'baseline', KEYS_LIST, KEYS_FLAT)
    parse_file('UB_keystroke_dataset', 'rotation', KEYS_LIST, KEYS_FLAT)