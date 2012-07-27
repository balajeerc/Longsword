import gamemanager

def log(text):
    gamemanager.GameManager.getInstance().debugText.element.text += text + "  "
    
def clearLog():
    gamemanager.GameManager.getInstance().debugText.element.text = ""