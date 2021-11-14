from nickname import randoum
nickname = randoum()

users = 0
tabinfo = 0
letterColorIndex = 0
messageYOffset = 5
rows = 0
cols = 0

pomodoroRunning = False
pauseRunning = False
pomodoroCount = 0
pomodoroLength = 60 * 25
pomodoroEnd = ""
# pomodoroLength = 3
pomodoroStart = ""
pauseStart = ""
pauseLength = 60 * 5
# pauseLength = 3

activities = {}
activity = "chat"
messages = []
history = []
todos = []

emojisNames = ["shrug", "wave", "raslefion", "nonmerci", "kill", "bizarre"]
radioCommands = ["metal", "culture", "nolife", "japon", "mongol", "stop"]

nicknameRequestString = 'NICKNAME'
nbUserRequestString = "NUMBEROFUSERS"
systemMessageSplitString = "####"
userMessageSplitString = "::::"
encodingMethod = "utf-8"
alecoute = "rien"
songTitle = ""

audioClient = ""
audioMode = False
#notify = DesktopNotifier()
