emojis = {
    "shrug": "¯\\_(ツ)_/¯",
    "wave": "°º¤ø,¸¸,ø¤º°`°º¤ø,¸,ø¤°º¤ø,¸¸,ø¤º°`°º¤ø,",
    "raslefion": "(╯°□°）╯ ︵ ┻━┻",
    "nonmerci": "╭∩╮（︶︿︶）╭∩╮",
    "kill": "(╯°□°)--︻╦╤─ - - -",
    "bizarre": "(ノಠ益ಠ)ノ彡",
}

def emoj(nickname, emoji, client):
	client.send('{}::::{}'.format(nickname, emojis[emoji]).encode("utf8"))
