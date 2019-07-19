import time
import keyboard
import mouse
from PIL import Image, ImageGrab, ImageOps

#background = (18, 18, 18)
#red = (196, 40, 31)
#black = (2, 2, 2)
#green = (64, 158, 63)

#Assuming 2560x1080, windowed fullscreen
x_pad = 909
y_pad = 294
bet_amount = [0, 9, 19, 39, 78, 156, 312, 625, 1250, 2500, 5000, 0, 0, 0, 0, 0, 0]
wait = 1
round_count = 0

class coord:
    map_change_gmod = (1270, 401, 1291, 417) # sum = 575
    map_change_moat = (1224, 805, 1317, 836) #sum = 3563

    welcome_screen = (721, 528, 767, 541) #sum = 2909
    close_welcome_screen_x = 249
    close_welcome_screen_y = 979

    round_end_screen = (1515, 757, 1614, 781) #sum = 9256
    close_round_end_screen_x = 1567
    close_round_end_screen_y = 771

    map_vote_screen = (1179, 766, 1270, 804) #sum = 6174

    roulette_screen = (1153, 433, 1204, 474) #sum = 4427
    close_roulette_screen_x = 1641
    close_roulette_Screen_y = 277

    new_spin = (1465, 498, 1512, 530) #sum = 13625

    last_round = (913, 699, 951, 709) #sum = 2121

    rest_x = 1720
    rest_y = 400

    bet_amount_right_x = 1233
    bet_amount_right_y = 407

    bet_amount_left_x = 1155
    bet_amount_left_y = 407

    bet_red_x = 1200
    bet_red_y = 510

    bet_black_x = 1200
    bet_black_y = 610

    recent_spin = (1384, 355)

def last_round_check():
    if get_coord_sum(coord.last_round) == 2121:
        sleep(180)

def make_bet(color, amount):
    mouse.move(coord.bet_amount_right_x - 5, coord.bet_amount_right_y, True, 0.1)
    time.sleep(0.1)
    mouse.drag(coord.bet_amount_right_x, coord.bet_amount_right_y, coord.bet_amount_left_x, coord.bet_amount_left_y, True, 0.5)
    time.sleep(0.5)
    keyboard.write(str(amount), 0.5)
    keyboard.press_and_release('enter')
    time.sleep(0.25)
    if color == "red":
        mouse.move(coord.bet_red_x, coord.bet_red_y, True, 0.2)
        mouse.double_click('left')
        time.sleep(0.5)
        mouse.move(coord.rest_x, coord.rest_y + 50, True, 1)
        time.sleep(4)
    elif color == 'black':
        mouse.move(coord.bet_black_x, coord.bet_black_y, True, 0.2)
        mouse.double_click('left')
        time.sleep(0.5)
        mouse.move(coord.rest_x, coord.rest_y + 50, True, 1)
        time.sleep(4)

def check_recent_spin(coordinates):
    img = ImageGrab.grab()
    #img = Image.open("green.png")
    return img.getpixel(coordinates)

def get_coord_sum(coordinates, debug = 0):
    sum = 0
    img = ImageGrab.grab(coordinates)
    img = ImageOps.grayscale(img)
    if debug == 1:
        img.save(str(int(time.time())) + ".png", "PNG") #for debug
    a = img.getcolors()
    for numbers in a:
        for x in numbers:
            sum += x
    return sum

def main(round_count):
    red_count = 0
    black_count = 0
    green_count = 0
    run = True
    while run:
        if get_coord_sum(coord.roulette_screen) != 4427:
            if get_coord_sum(coord.round_end_screen) == 9256:
                #close round end screen if it's open
                print("Round end screen is open")
                round_count += 1
                print("Round " + str(round_count))
                mouse.move(coord.close_round_end_screen_x, coord.close_round_end_screen_y, True, 0.1)
                mouse.click('left')
                print("Round end screen is closed")
            elif get_coord_sum(coord.welcome_screen) == 2909:
                #close welcome screen if it's open
                print("Welcome screen is open")
                mouse.move(coord.close_welcome_screen_x, coord.close_welcome_screen_y, True, 0.1)
                mouse.click('left')
                print("Welcome screen is closed")
            #elif get_coord_sum(coord.map_vote_screen) == 6174:
            #    print("Map vote screen is open..")
            #    time.sleep(10)
            elif get_coord_sum(coord.map_change_moat) == 3563:
                round_count = 0
                time.sleep(10)
            else:
                #if no windows are open, try opening the roulette screen
                mouse.move(coord.close_roulette_screen_x, coord.close_roulette_Screen_y, True, 0.1)
                mouse.click('left')
                keyboard.press('i')
                mouse.move(1215, 283, True, 1)
                mouse.click('left')
                keyboard.release('i')
                mouse.move(1350, 318, True, 1)
                mouse.click('left')
                time.sleep(5)
                #mouse.move(coord.rest_x, coord.rest_y, True, 1)
                #time.sleep(5)
        else:
            if round_count == 19 or get_coord_sum(coord.map_vote_screen) == 6174:
                round_count = 0
                nextmap = True
                while nextmap:
                    if get_coord_sum(coord.map_change_moat) == 3563:
                        nextmap = False
                    print("Waiting until next map...")
                    time.sleep(10)
                print("red count: " + str(red_count))
                print("black count: " + str(black_count))
            elif get_coord_sum(coord.new_spin) == 13625:
                time.sleep(1)
                if check_recent_spin(coord.recent_spin) == (196, 40, 31):
                    print("Red")
                    red_count += 1
                    red_count += green_count
                    black_count = 0
                    green_count = 0
                    print("Red count is " + str(red_count))
                    if red_count >= wait:
                        print("Betting on black..")
                        make_bet('black', bet_amount[red_count])
                elif check_recent_spin(coord.recent_spin) == (2, 2, 2):
                    print("Black")
                    black_count += 1
                    black_count += green_count
                    red_count = 0
                    green_count = 0
                    print("Black count is " + str(black_count))
                    if black_count >= wait:
                        print("Betting on red..")
                        make_bet('red', bet_amount[black_count])
                elif check_recent_spin(coord.recent_spin) == (58, 151, 57):
                    print("Green")
                    if black_count > 0:
                        black_count += 1
                        print("Black count is " + str(black_count))
                        if black_count >= wait:
                            print("Betting on red..")
                            make_bet('red', bet_amount[black_count])
                    elif red_count > 0:
                        red_count += 1
                        print("Red count is " + str(red_count))
                        if red_count >= wait:
                            print("Betting on black..")
                            make_bet('black', bet_amount[red_count])
                    else:
                        green_count += 1
while True:
        if keyboard.is_pressed("ctrl+r"):
            print("Bot running!")
            main(round_count)
        elif keyboard.is_pressed("ctrl+t"):
            time.sleep(0.35)
            round_count += 1
            print("Round " + str(round_count))

#while True:
#    if keyboard.is_pressed("space"):
#        print(check_recent_spin(coord.recent_spin))