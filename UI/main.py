#########################
# GLOBAL VARIABLES USED #
#########################
import tkinter
from queue import Queue

import pyttsx3 as pyttsx3

ai_name = 'SIGN-BOT'.lower()
EXIT_COMMANDS = ['bye', 'exit', 'quit', 'shut down', 'shutdown']

ownerName = "Cool Boy"
ownerDesignation = "Sir"
ownerPhoto = "1"
rec_email, rec_phoneno = "", ""


avatarChoosen = 0
choosedAvtrImage = None

botChatTextBg = "#007cc7"
botChatText = "white"
userChatTextBg = "#4da8da"

chatBgColor = '#12232e'
background = '#203647'
textColor = 'white'
AITaskStatusLblBG = '#203647'
KCS_IMG = 1  # 0 for light, 1 for dark
voice_id = 0  # 0 for female, 1 for male
ass_volume = 1  # max volume
ass_voiceRate = 200  # normal voice rate

####################################### IMPORTING MODULES ###########################################
""" User Created Modules """
try:
    import normalChat
    import appControl
    import webScrapping
    # import game
    # from userHandler import UserData
    import dictionary


except Exception as e:
    raise e

""" System Modules """
try:
    import os
    # import speech_recognition as sr
    # import pyttsx3
    from tkinter import *
    from tkinter import ttk
    from tkinter import messagebox
    from tkinter import colorchooser
    from PIL import Image, ImageTk
    import cv2
    import numpy as np
    import time
    # import mediapipe as mp
    from threading import Thread
    # from tensorflow.keras.models import Sequential
    # from tensorflow.keras.layers import LSTM, Dense
    # from tensorflow.keras.callbacks import TensorBoard
except Exception as e:
    print(e)

if os.path.exists('userData') == False:
    os.mkdir('userData')


########################################## BOOT UP WINDOW ###########################################



############################################ SET UP VOICE ###########################################
# try:
#     engine = pyttsx3.init()
#     voices = engine.getProperty('voices')
#     engine.setProperty('voice', voices[voice_id].id)  # male
#     engine.setProperty('volume', ass_volume)
# except Exception as e:
#     print(e)


####################################### SET UP TEXT TO SPEECH #######################################
def speak(text, display=False, icon=False):
    AITaskStatusLbl['text'] = 'Speaking...'
    if icon: Label(chat_frame, image=botIcon, bg=chatBgColor).pack(anchor='w', pady=0)
    if display: attachTOframe(text, True)
    print('\n' + ai_name.upper() + ': ' + text)
    # try:
    #     engine.say(text)
    #     engine.runAndWait()
    # except:
    #     print("Try not to type more...")


####################################### SET UP SPEECH TO TEXT #######################################
# def record(clearChat=True, iconDisplay=True):
#     print('\nListening...')
#     AITaskStatusLbl['text'] = 'Listening...'
#     r = sr.Recognizer()
#     r.dynamic_energy_threshold = False
#     r.energy_threshold = 4000
#     with sr.Microphone() as source:
#         r.adjust_for_ambient_noise(source)
#         audio = r.listen(source)
#         said = ""
#         try:
#             AITaskStatusLbl['text'] = 'Processing...'
#             said = r.recognize_google(audio)
#             print(f"\nUser said: {said}")
#             if clearChat:
#                 clearChatScreen()
#             if iconDisplay: Label(chat_frame, image=userIcon, bg=chatBgColor).pack(anchor='e', pady=0)
#             attachTOframe(said)
#         except Exception as e:
#             print(e)
#             # speak("I didn't get it, Say that again please...")
#             if "connection failed" in str(e):
#                 speak("Your System is Offline...", True, True)
#             return 'None'
#     return said.lower()




# TODO: Thread target function
# def voiceMedium():
#     while True:
#         query = record()
#         if query == 'None': continue
#         if isContain(query, EXIT_COMMANDS):
#             speak("Shutting down the System. Good Bye " + ownerDesignation + "!", True, True)
#             break
#         else:
#             main(query.lower())
#     appControl.Win_Opt('close')

# def voiceMedium():
#     while True:
#         query = record()
#         if query == 'None': continue
#         if isContain(query, EXIT_COMMANDS):
#             speak("Shutting down the System. Good Bye " + ownerDesignation + "!", True, True)
#             break
#         else:
#             main(query.lower())
#     appControl.Win_Opt('close')


def keyboardInput(e):
    user_input = UserField.get().lower()
    if user_input != "":
        clearChatScreen()
        if isContain(user_input, EXIT_COMMANDS):
            speak("Bye Bye")
            speak("Shutting down the System. Good Bye " + ownerDesignation + "!", True, True)
        else:
            Label(chat_frame, image=userIcon, bg=chatBgColor).pack(anchor='e', pady=0)
            attachTOframe(user_input.capitalize())
            Thread(target=main, args=(user_input,)).start()
        UserField.delete(0, END)


###################################### TASK/COMMAND HANDLER #########################################
def isContain(txt, lst):
    for word in lst:
        if word in txt:
            return True
    return False


def main(text):



    if isContain(text, ['meaning', 'dictionary', 'definition', 'define']):
        result = dictionary.translate(text)
        # speak(result[0], True, True)
        if result[1] == '': return
        # speak(result[1], True)
        return

    # if 'volume' in text:
    #     appControl.volumeControl(text)
    #     Label(chat_frame, image=botIcon, bg=chatBgColor).pack(anchor='w', pady=0)
    #     attachTOframe('Volume Settings Changed', True)
    #     return

    # if isContain(text, ['timer', 'countdown']):
    #     Thread(target=timer.startTimer, args=(text,)).start()
    #     speak('Ok, Timer Started!', True, True)
    #     return

    if isContain(text, ['search', 'image']):
        if 'image' in text and 'show' in text:
            Thread(target=showImages, args=(text,)).start()
            # speak('Here are the images...', True, True)
            return
        # speak(webScrapping.googleSearch(text), True, True)
        return


    if isContain(text, ['weather']):
        data = webScrapping.weather()
        speak('', False, True)
        showSingleImage("weather", data[:-1])
        speak(data[-1])
        return


    if isContain(text, ['time', 'date']):
        speak(normalChat.chat(text), True, True)
        return

    if 'my name' in text:
        speak('Your name is, ' + ownerName, True, True)
        return


    if isContain(text, ['morning', 'evening', 'noon']) and 'good' in text:
        speak(normalChat.chat("good"), True, True)
        return

    result = normalChat.reply(text)
    if result != "None":
        speak(result, True, True)
    else:
        speak("I couldn't understand your query... ", True, True)
    #speak("Here's what I found on the web... ", True, True)
    # webScrapping.googleSearch(text) #uncomment this if you want to show the result on web, means if nothing found


##################################### DELETE USER ACCOUNT #########################################
def deleteUserData():
    result = messagebox.askquestion('Alert', 'Are you sure you want to exit ?')
    if result == 'no': return
    root.destroy()


#####################
####### GUI #########
#####################

############ ATTACHING BOT/USER CHAT ON CHAT SCREEN ###########
def attachTOframe(text, bot=False):
    if bot:
        botchat = Label(chat_frame, text=text, bg=botChatTextBg, fg=botChatText, justify=LEFT, wraplength=250,
                        font=('Montserrat', 12, 'bold'))
        botchat.pack(anchor='w', ipadx=5, ipady=5, pady=5)
    else:
        userchat = Label(chat_frame, text=text, bg=userChatTextBg, fg='white', justify=RIGHT, wraplength=250,
                         font=('Montserrat', 12, 'bold'))
        userchat.pack(anchor='e', ipadx=2, ipady=2, pady=5)


def clearChatScreen():
    for wid in chat_frame.winfo_children():
        wid.destroy()


### SWITCHING BETWEEN FRAMES ###
def raise_frame(frame):
    frame.tkraise()
    clearChatScreen()


################# SHOWING DOWNLOADED IMAGES ###############
img0, img1, img2, img3, img4 = None, None, None, None, None


def showSingleImage(type, data=None):
    global img0, img1, img2, img3, img4
    try:
        img0 = ImageTk.PhotoImage(Image.open('Downloads/0.jpg').resize((90, 110), Image.Resampling.LANCZOS))
    except:
        pass
    img1 = ImageTk.PhotoImage(Image.open('extrafiles/images/heads.jpg').resize((220, 200), Image.Resampling.LANCZOS))
    img2 = ImageTk.PhotoImage(Image.open('extrafiles/images/tails.jpg').resize((220, 200), Image.Resampling.LANCZOS))
    img4 = ImageTk.PhotoImage(Image.open('extrafiles/images/WeatherImage.png'))

    if type == "weather":
        weather = Frame(chat_frame)
        weather.pack(anchor='w')
        Label(weather, image=img4, bg=chatBgColor).pack()
        Label(weather, text=data[0], font=('Arial Bold', 45), fg='white', bg='#3F48CC').place(x=65, y=45)
        Label(weather, text=data[1], font=('Montserrat', 15), fg='white', bg='#3F48CC').place(x=78, y=110)
        Label(weather, text=data[2], font=('Montserrat', 10), fg='white', bg='#3F48CC').place(x=78, y=140)
        Label(weather, text=data[3], font=('Arial Bold', 12), fg='white', bg='#3F48CC').place(x=60, y=160)

    elif type == "wiki":
        Label(chat_frame, image=img0, bg='#EAEAEA').pack(anchor='w')
    elif type == "head":
        Label(chat_frame, image=img1, bg='#EAEAEA').pack(anchor='w')
    elif type == "tail":
        Label(chat_frame, image=img2, bg='#EAEAEA').pack(anchor='w')
    else:
        img3 = ImageTk.PhotoImage(
            Image.open('extrafiles/images/dice/' + type + '.jpg').resize((200, 200), Image.Resampling.LANCZOS))
        Label(chat_frame, image=img3, bg='#EAEAEA').pack(anchor='w')


def showImages(query):
    global img0, img1, img2, img3
    webScrapping.downloadImage(query)
    w, h = 150, 110
    # Showing Images
    imageContainer = Frame(chat_frame, bg='#EAEAEA')
    imageContainer.pack(anchor='w')
    # loading images
    img0 = ImageTk.PhotoImage(Image.open('Downloads/0.jpg').resize((w, h), Image.Resampling.LANCZOS))
    img1 = ImageTk.PhotoImage(Image.open('Downloads/1.jpg').resize((w, h), Image.Resampling.LANCZOS))
    img2 = ImageTk.PhotoImage(Image.open('Downloads/2.jpg').resize((w, h), Image.Resampling.LANCZOS))
    img3 = ImageTk.PhotoImage(Image.open('Downloads/3.jpg').resize((w, h), Image.Resampling.LANCZOS))
    # Displaying
    Label(imageContainer, image=img0, bg='#EAEAEA').grid(row=0, column=0)
    Label(imageContainer, image=img1, bg='#EAEAEA').grid(row=0, column=1)
    Label(imageContainer, image=img2, bg='#EAEAEA').grid(row=1, column=0)
    Label(imageContainer, image=img3, bg='#EAEAEA').grid(row=1, column=1)


############################# Camera ##################################






######################## CHANGING CHAT BACKGROUND COLOR #########################



chatMode = 1


def changeChatMode():
    global chatMode
    if chatMode == 1:
        # appControl.volumeControl('mute')
        VoiceModeFrame.pack_forget()
        TextModeFrame.pack(fill=BOTH)
        UserField.focus()
        chatMode = 0
    else:
        # appControl.volumeControl('full')
        TextModeFrame.pack_forget()
        VoiceModeFrame.pack(fill=BOTH)
        root.focus()
        chatMode = 1


#####################################  MAIN GUI ####################################################

#### SPLASH/LOADING SCREEN ####
def progressbar():
    s = ttk.Style()
    s.theme_use('clam')
    s.configure("white.Horizontal.TProgressbar", foreground='white', background='white')
    progress_bar = ttk.Progressbar(splash_root, style="white.Horizontal.TProgressbar", orient="horizontal",
                                   mode="determinate", length=303)
    progress_bar.pack()
    splash_root.update()
    progress_bar['value'] = 0
    splash_root.update()

    while progress_bar['value'] < 100:
        progress_bar['value'] += 5
        # splash_percentage_label['text'] = str(progress_bar['value']) + ' %'
        splash_root.update()
        time.sleep(0.1)


def destroySplash():
    splash_root.destroy()

### test ###

# define a function to add frames to the frame_queue
def add_frames():
    while True:
        ret, frame = cap.read() # read a frame from the camera
        if ret:
            frame_queue.put(frame)


# define a function to display frames from the display_queue
def display_frames():
    while True:
        frame = display_queue.get() # get a frame from the display_queue
        # convert the frame from BGR to RGB format
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # create a PIL Image object from the frame
        image = Image.fromarray(frame)
        # create a PhotoImage object from the PIL Image object
        photo = ImageTk.PhotoImage(image)
        # update the cameraRoot widget with the new photo
        cameraRoot.config(image=photo)
        cameraRoot.image = photo

# define a function to add frames to the frame_queue and display frames from the display_queue
def update_camera():
    while True:
        # get a frame from the frame_queue
        frame = frame_queue.get()
        # put the frame in the display_queue
        display_queue.put(frame)
        # sleep for 10 milliseconds
        time.sleep(0.01)



if __name__ == '__main__':
    splash_root = Tk()
    splash_root.configure(bg='#3895d3')
    splash_root.overrideredirect(True)
    splash_label = Label(splash_root, text="Processing...", font=('montserrat', 15), bg='#3895d3', fg='white')
    splash_label.pack(pady=40)
    # splash_percentage_label = Label(splash_root, text="0 %", font=('montserrat',15),bg='#3895d3',fg='white')
    # splash_percentage_label.pack(pady=(0,10))

    w_width, w_height = 400, 200
    s_width, s_height = splash_root.winfo_screenwidth(), splash_root.winfo_screenheight()
    x, y = (s_width / 2) - (w_width / 2), (s_height / 2) - (w_height / 2)
    splash_root.geometry('%dx%d+%d+%d' % (w_width, w_height, x, y - 30))

    progressbar()
    splash_root.after(10, destroySplash)
    splash_root.mainloop()

    root = Tk()
    root.title('SIGN-BOT')
    w_width, w_height = 800, 650
    s_width, s_height = root.winfo_screenwidth(), root.winfo_screenheight()
    x, y = (s_width / 2) - (w_width / 2), (s_height / 2) - (w_height / 2)
    root.geometry('%dx%d+%d+%d' % (w_width, w_height, x, y - 30))  # center location of the screen
    root.configure(bg=background)
    # root.resizable(width=False, height=False)
    root.pack_propagate(0)

    ############test############
    chatRoot = Frame(root, width=550, height=650, bg='white')
    chatRoot.pack(side= tkinter.LEFT)
    cameraRoot = tkinter.Label(root,  width=250, height=650)
    cameraRoot.pack(side= tkinter.RIGHT, padx=10, pady=100, fill=tkinter.X,  expand= True)
    ## Camera ##


    ####################
    root1 = Frame(chatRoot, bg=chatBgColor)
    root2 = Frame(chatRoot, bg=background)
    root3 = Frame(chatRoot, bg=background)
    for f in (root1, root2, root3):
        f.grid(row=0, column=0, sticky='news')

    ################################
    ########  CHAT SCREEN  #########
    ################################

    # Chat Frame
    chat_frame = Frame(root1, width=380, height=551, bg=chatBgColor)
    chat_frame.pack(padx=10)
    chat_frame.pack_propagate(0)

    bottomFrame1 = Frame(root1, bg='#dfdfdf', height=100)
    bottomFrame1.pack(fill=X, side=BOTTOM)
    VoiceModeFrame = Frame(bottomFrame1, bg='#dfdfdf')
    VoiceModeFrame.pack(fill=BOTH)
    TextModeFrame = Frame(bottomFrame1, bg='#dfdfdf')
    TextModeFrame.pack(fill=BOTH)

    #VoiceModeFrame.pack_forget()
    TextModeFrame.pack_forget()

    cblLightImg = PhotoImage(file='extrafiles/images/centralButton.png')
    cblDarkImg = PhotoImage(file='extrafiles/images/centralButton1.png')
    if KCS_IMG == 1: ## Background
        cblimage = cblDarkImg
    else:
        cblimage = cblLightImg
    cbl = Label(VoiceModeFrame, fg='white', image=cblimage, bg='#dfdfdf')
    cbl.pack(pady=17)
    AITaskStatusLbl = Label(VoiceModeFrame, text='    Offline', fg='white', bg=AITaskStatusLblBG,
                            font=('montserrat', 16))
    AITaskStatusLbl.place(x=140, y=32)
    # TODO: Replace
    # # Settings Button <- to be discarded
    # sphLight = PhotoImage(file="extrafiles/images/setting.png")
    # sphLight = sphLight.subsample(2, 2)
    # sphDark = PhotoImage(file="extrafiles/images/setting1.png")
    # sphDark = sphDark.subsample(2, 2)
    # if KCS_IMG == 1:
    #     sphimage = sphDark
    # else:
    #     sphimage = sphLight
    # settingBtn = Button(VoiceModeFrame, image=sphimage, height=30, width=30, bg='#dfdfdf', borderwidth=0,
    #                     activebackground="#dfdfdf", command=lambda: raise_frame(root2))
    # settingBtn.place(relx=1.0, y=30, x=-20, anchor="ne")

    # Keyboard Button
    kbphLight = PhotoImage(file="extrafiles/images/keyboard.png")
    kbphLight = kbphLight.subsample(2, 2)
    kbphDark = PhotoImage(file="extrafiles/images/keyboard1.png")
    kbphDark = kbphDark.subsample(2, 2)
    if KCS_IMG == 1:
        kbphimage = kbphDark
    else:
        kbphimage = kbphLight
    kbBtn = Button(VoiceModeFrame, image=kbphimage, height=30, width=30, bg='#dfdfdf', borderwidth=0,
                   activebackground="#dfdfdf", command=changeChatMode)
    kbBtn.place(x=25, y=30)

    # Mic <- Camera to be placed
    micImg = PhotoImage(file="extrafiles/images/mic.png")
    micImg = micImg.subsample(2, 2)
    micBtn = Button(TextModeFrame, image=micImg, height=30, width=30, bg='#dfdfdf', borderwidth=0,
                    activebackground="#dfdfdf", command=changeChatMode)
    micBtn.place(relx=1.0, y=30, x=-20, anchor="ne")

    # Text Field
    TextFieldImg = PhotoImage(file='extrafiles/images/textField.png')
    UserFieldLBL = Label(TextModeFrame, fg='white', image=TextFieldImg, bg='#dfdfdf')
    UserFieldLBL.pack(pady=17, side=LEFT, padx=10)
    UserField = Entry(TextModeFrame, fg='white', bg='#203647', font=('Montserrat', 16), bd=6, width=22, relief=FLAT)
    UserField.place(x=20, y=30)
    UserField.insert(0, "Ask me anything...")
    UserField.bind('<Return>', keyboardInput)

    # User and Bot Icon
    userIcon = PhotoImage(file="extrafiles/images/avatars/ChatIcons/a" + str(ownerPhoto) + ".png")
    botIcon = PhotoImage(file="extrafiles/images/assistant2.png")
    botIcon = botIcon.subsample(2, 2)

    ###########################
    ########  SETTINGS  #######
    ###########################


    #
    # TODO: When user says bye should shutdown, so we need this
    # try:
    #     # pass
    #      Thread(target=test_show_frame).start()
    # except:
    #      pass
    # try:
    #     # pass
    #     Thread(targe=webScrapping.dataUpdate).start()
    # except Exception as et:
    #     print('System is Offline...')

    root.iconbitmap('extrafiles/images/assistant2.ico')
    raise_frame(root1)
    # create two queues, one for adding frames and one for displaying frames
    frame_queue = Queue()
    display_queue = Queue()
    # cap = cv2.VideoCapture(0)
    # # create two threads, one to add frames and one to display frames
    # add_thread = Thread(target=add_frames)
    # display_thread = Thread(target=display_frames)
    # update_thread = Thread(target=update_camera)
    # add_thread.start()
    # display_thread.start()
    # update_thread.join()
    # add_thread.join()
    # display_thread.join()
    # update_thread.join()
    root.mainloop()
    # cap.release()
    # cv2.destroyAllWindows()

    # start the threads
