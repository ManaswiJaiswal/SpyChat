from PIL import Image
import os
# pick a .png or .bmp file you have in the working directory
# or give full path name
original_image_file = "picture.png"
#original_image_file = "picture.png"
img = Image.open(original_image_file)
# image mode needs to be 'RGB'
#print(img, img.mode)  # test
# create a new filename for the modified/encoded image
encoded_image_file = "enc_" + original_image_file
messages = {'Sarah' : '', 'Anna' : '', 'Dan':'', 'Becky' : '', 'Will' : ''}

global current_User
current_User = 'Will'
sender = ''
reciever = ''
#friend list
will_friend=[]
sarah_friend=[]
anna_friend=[]
becky_friend=[]
dan_friend=[]

# all users of the application
all_Users = ['Will', 'Anna' ,'Dan', 'Sarah', 'Becky',]

# to insert program in continuous loop
isRunning = True

class User:
    def __init__(self, name, age, rating,status, friend_list):
      self.name = name
      self.age = age
      self.rating = rating
      self.status = status
      self.friend_list = friend_list


emp1 = User('Anna', 28, 3, 'Active', [])
emp2 = User('Dan', 26, 3, 'Active', [])
emp3 = User('Sarah', 37, 4, 'Active',[])
emp4 = User('Becky', 33, 5, 'Active',[])
emp5 = User('Will', 30, 4, 'Inactive',[])

spies = [emp1, emp2, emp3, emp4, emp5 ]

#friends
friends = [emp1,emp2,emp3,emp4]

def encode_image(img, msg):
    length = len(msg)
    # limit length of message to 255
    if length > 255:
        print("text too long! (don't exeed 255 characters)")
        return False
    if img.mode != 'RGB':
        print("image mode needs to be RGB")
        return False
    # use a copy of image to hide the text in
    encoded = img.copy()
    width, height = img.size
    index = 0
    for row in range(height):
        for col in range(width):
            r, g, b = img.getpixel((col, row))
        # first value is length of msg
            if row == 0 and col == 0 and index < length:
                asc = length
            elif index <= length:
                c = msg[index -1]
                asc = ord(c)
            else:
                asc = r
            encoded.putpixel((col, row), (asc, g , b))
            index += 1
    return encoded

def decode_image(img):
    """
     check the red portion of an image (r, g, b) tuple for
    hidden message characters (ASCII values)
    """
    width, height = img.size
    msg = ""
    index = 0
    for row in range(height):
        for col in range(width):
            try:
                r, g, b = img.getpixel((col, row))
            except ValueError:
            # need to add transparency a for some .png files
                r, g, b, a = img.getpixel((col, row))
        # first pixel r value is length of message
            if row == 0 and col == 0:
                length = r
            elif index <= length:
                msg += chr(r)
            index += 1
    return msg

def userchoice():
    choice = ['1. Add Friend', '2. Status', '3. Chat', '4. Rating', '5. Exit', '6. Switch User']
    print(*choice, sep = "\n")
    print('Enter Option')
    user_choice = int(input())
    return  user_choice

def message(to):
    print('Enter your message')
    # don't exceed 255 characters in the message
    secret_msg = input()
    img_encoded = encode_image(img, secret_msg)
    if img_encoded:
    # save the image with the hidden text
        img_encoded.save(encoded_image_file)
    # view the saved file, works with Windows only
    # behaves like double-clicking on the saved file
    if bool(to):
        messages[to] = secret_msg
    else:
        print('Message not sent')
        exit()

def show_message(name):
    img2 = Image.open(encoded_image_file)
    hidden_text = decode_image(img2)

    if name == sender and reciever == current_User:
        print(messages[current_User])
        print("Hidden text:\n{}".format(hidden_text))
        print('See Image?(yes/no)')
        see_image=input()
        if see_image== 'yes':
            os.startfile(encoded_image_file)
        elif see_image=='no':
            pass
    else:
        print('No messages')
    # view the saved file, works with Windows only
    # behaves like double-clicking on the saved file
     # get the hidden text back ...

def chat():
    global reciever
    chosen_friend_name = ''
    print('Chat')
    #sending a message
    print('Choose position of a friend ')
    name = list(set(all_Users) - set([current_User]))
    for i in range(4):
        print('{}.{}'.format(i+1, name[i]))
    chosen_friend = int(input())
    chosen_friend_position = int(chosen_friend) - 1
    if chosen_friend_position < len(friends):
        if chosen_friend==1:
            print(name[0])
            show_message(name[0])
        elif chosen_friend==2:
            print(name[1])
            show_message(name[1])
        elif chosen_friend==3:
            print(name[2])
            show_message(name[2])
        elif chosen_friend==4:
            print(name[3])
            show_message(name[3])
        else:
            print('Invalid choice')
            exit()
    else:
        print ('Invalid Choice')
        reciever = ''
        exit()
    reciever = name[chosen_friend_position]
    chosen_friend_name = name[chosen_friend_position]
    return  chosen_friend_name

def add_friends (user):
    current_spy = ''
    #Print the friend list of active users
    for spy in spies:
        if spy.name == user:
            current_spy = spy
            print("Your Friends : ", spy.friend_list)

    print('Add new friend')
    #print list of available friends
    available_friends = list(set(all_Users) - set([user]))
    for i in range(4):
        print('{0}. {1}'.format(i+1, available_friends[i]))
    selection  = int(input("Select the person : "))
    selected_friend =available_friends[selection-1]

    if selection < 5:
        for spy in list(set(spies) - set([user]) ):
            if spy.rating >= current_spy.rating and not spy.name in current_spy.friend_list and spy.name == selected_friend  :
                current_spy.friend_list.append(spy.name)
                print()
                print('Request sent to {}'.format(spy.name))

            elif spy.name in current_spy.friend_list and spy.name==selected_friend:
                print('Already friends')
            elif spy.name == selected_friend and spy.rating < current_spy.rating:
                print("Request not sent")
            else:
                pass
    else:
        print("Invalid Choice")
    return 1



print('Welcome Will')
while isRunning:
    choice = ['1. Add Friend', '2. Status', '3. Chat', '4. Rating', '5. Exit','6. Switch User']
    print(*choice, sep = "\n")
    #choosing options
    print('Enter Option')
    wchoice = int(input())
    if wchoice == 1:
       add_friends(current_User)
    elif wchoice == 2:
        print('Status')
        wstatus=['1. See', '2. Change']
        print(*wstatus, sep = "\n")
        print('Enter Option')
        wstatuschoice=int(input())
        if wstatuschoice==1:
            print(emp5.status)
        elif wstatuschoice==2:
            emp5.status='Active'
            print(emp5.status)
    elif wchoice == 4:
        print('Rating')
        wrating=['1. See', '2. Change']
        print(*wrating, sep = "\n")
        print('Enter Option')
        wratingchoice=int(input())
        if wratingchoice==1:
            print(emp5.rating)
        elif wratingchoice==2:
            print('enter new rating')
            wredit=int(input())
            emp1.rating=wredit
            print(wredit)
            continue
    elif wchoice == 3:
        chosen_friend = chat()
        message(chosen_friend)
        sender = current_User
    elif wchoice == 5:
        isRunning = False
        exit()

    elif wchoice == 6:
        #switching user so that other user can read the message
        suname = input('Enter Username: ')
        if str(suname)== current_User:
            print('You are already logged in.')
            continue
        elif str(suname)=='Sarah' or 'Dan' or 'Becky' or 'Anna'or 'Will':
            passa=input('Enter password : ')

        else:
            print('Incorrect username')
            continue

        if str(suname)=='Sarah' and passa=='sarahpas':
            current_User = suname
            schoice = userchoice()
            if schoice==1:
               add_friends(current_User)
            elif schoice==2:
                ss=['1. See', '2. Change']
                print(*ss, sep = "\n")
                print('Enter Option')
                ssedit=int(input())
                if ssedit==1:
                    print(emp3.status)
                elif ssedit==2:
                    emp1.status='Inactive'
                    print(emp3.status)
                    exit()
            elif schoice==4:
                sr=['1. See', '2. Change']
                print(*sr, sep = "\n")
                print('Enter Option')
                sratingchoice=int(input())
                if sratingchoice==1:
                    print(emp3.rating)
                    exit()
                elif sratingchoice==2:
                    print('enter new rating')
                    sredit=int(input())
                    emp3.rating=sredit
            elif schoice==3:
                chosen_friend = chat()
                message(chosen_friend)
                sender = current_User

        elif str(suname)=='Anna' and passa=='annapas':
            current_User = suname
            print('Hello Anna')
            ach = userchoice()
            if ach==1:
                add_friends(current_User)
            elif ach==2:
                ans=['1. See', '2. Change']
                print(*ans, sep = "\n")
                print('Enter Option')
                asedit=int(input())
                if asedit==1:
                    print(emp1.status)
                elif asedit==2:
                    emp1.status='Inactive'
                    print(emp1.status)
                    exit()
            elif ach==4:
                ar=['1. See', '2. Change']
                print(*ar, sep = "\n")
                print('Enter Option')
                arch=int(input())
                if arch==1:
                    print(emp1.rating)
                    exit()
                elif arch==2:
                    print('enter new rating')
                    aredit=int(input())
                    emp1.rating=aredit
            elif ach==3:
                chosen_friend = chat()
                message(chosen_friend)
                sender = current_User

        elif str(suname)=='Becky' and passa=='beckypas':
            current_User = suname
            print('Hello Becky')
            bch = userchoice()
            if bch==1:
                add_friends(current_User)
            elif bch==2:
                bs = ['1. See', '2. Change']
                print(*bs, sep = "\n")
                print('Enter Option')
                bsedit=int(input())
                if bsedit==1:
                    print(emp4.status)
                elif bsedit==2:
                    emp4.status='Inactive'
                    print(emp4.status)
                    exit()
            elif bch==4:
                br=['1. See', '2. Change']
                print(*br, sep = "\n")
                print('Enter Option')
                brch=int(input())
                if brch==1:
                    print(emp4.rating)
                    exit()
                elif brch==2:
                    print('enter new rating')
                    bredit=int(input())
                    emp4.rating=bredit
            elif bch==3:
                chosen_friend = chat()
                message(chosen_friend)
                sender = current_User

        elif str(suname)=='Dan' and passa=='danpas':
            current_User = suname
            print('Hello Dan')
            dch = userchoice()
            if dch==1:
                add_friends(current_User)
            elif dch==2:
                ds = ['1. See', '2. Change']
                print(*ds, sep = "\n")
                print('Enter Option')
                dsedit=int(input())
                if dsedit==1:
                    print(emp2.status)
                elif dsedit==2:
                    emp2.status='Inactive'
                    print(emp2.status)
                    exit()
            elif dch==4:
                dr=['1. See', '2. Change']
                print(*dr, sep = "\n")
                print('Enter Option')
                drch=int(input())
                if drch==1:
                    print(emp2.rating)
                    exit()
                elif drch==2:
                    print('enter new rating')
                    aredit=int(input())
                    emp2.rating=aredit
            elif dch==3:
                chosen_friend = chat()
                message(chosen_friend)
                sender = current_User

        elif str(suname)=='Will' and passa=='willpas':
            current_User = suname
            wchoice = userchoice()
            if wchoice==1:
                add_friends(current_User)
            elif wchoice==2:
                ss=['1. See', '2. Change']
                print(*ss, sep = "\n")
                print('Enter Option')
                wsedit=int(input())
                if wsedit==1:
                    print(emp5.status)
                elif wsedit==2:
                    emp1.status='Active'
                    print(emp5.status)
                    exit()
            elif wchoice==4:
                wr=['1. See', '2. Change']
                print(*wr, sep = "\n")
                print('Enter Option')
                wratingchoice=int(input())
                if wratingchoice==1:
                    print(emp5.rating)
                    exit()
                elif wratingchoice==2:
                    print('enter new rating')
                    wredit=int(input())
                    emp5.rating=wredit
            elif wchoice==3:
                chosen_friend = chat()
                message(chosen_friend)
                sender = current_User

        else:
            print('Incorrect Password')


