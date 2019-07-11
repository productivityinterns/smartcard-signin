# from nfc.clf import RemoteTarget
from cacbarcode import PDF417Barcode, Code39Barcode
from attendance import MockAttendance, StatusValues
import graphics, sys, random
import time
import threading


def getEDIPI(data):
    edipi = ""
    try:
        barcode = PDF417Barcode(data)
        edipi = barcode.edipi
    except:
        # Try the other barcode type
        try:
            barcode = Code39Barcode(data)
            edipi = barcode.edipide
        except:
            # Neither barcode was correct
            # Blink failure light
            # make failure noise
            print("Neither barcode worked!")
    return edipi


def drawWindow():
    win = graphics.GraphWin("CAC Sign in", 800, 480)
    win.setBackground("white")
    return win


def clearWindow(win):
    for item in win.items[:]:
        item.undraw()
    #win.update()


def drawIn(name, window):
    clearWindow(window)
    print("DRAW IN")
    window.setBackground("green")
    #time.sleep(.5)
    s = "Welcome, " + name
    text = graphics.Text(graphics.Point(400, 240), s)
    text.setSize(30)
    text.draw(window)
    
    print("DRAW IN done")

def drawOut(name, window):
    print("DRAW Out")
    clearWindow(window)
    window.setBackground("red")
    #time.sleep(.5)
    s = "Goodbye, " + name
    text = graphics.Text(graphics.Point(400, 240), s)
    text.setSize(30)
    text.draw(window)
    
    print("DRAW out done")

def drawErr(window):
    print("DRAW E")
    clearWindow(window)
  
    window.setBackground("yellow")
    s = "Error, failuire to sign in or out"
    text = graphics.Text(graphics.Point(400, 240), s)
    text.setSize(30)
    text.draw(window)
 
    print("DRAW e done")

def drawDefault(window):
    print("DRAW nothin")
    clearWindow(window)   
    s = "Scan CAC to sign in or out"
    text = graphics.Text(graphics.Point(400, 240), s)
    text.setSize(30)
    text.draw(window)
  


#safeStatus = None
c = threading.Condition()


def logic():
    attendance = MockAttendance()
    barcode_data = ""
    global safeStatus
    global userName
    edipi = None
    print("logic loop starting...")
    while True:
                
        barcode_data = sys.stdin.readline() 
        edipi = getEDIPI(barcode_data)        
        # Signin API call here, pass in edipi
        print("EDIPI =", edipi)
        (status,name) = attendance.checkin_checkout(edipi)
        print("Sending status...")
        print(status)
        c.acquire()
        safeStatus = status
        userName = name
        c.notify_all()
        c.release()
        print("status sent...")


if __name__ == "__main__":
    global safeStatus
    global userName
    safeStatus = None
    oldName = None
    userName = ""
    print("Graphics thread starting...")
    t = threading.Thread(target=logic)
    t.start()
    window = drawWindow()
    oldStatus = None
    while True:       
        c.acquire()
        status = safeStatus
        name = userName
        c.release()
        if oldStatus != status or oldName != name:
            print(status)
            if status == StatusValues.In:
                drawIn(name, window)
                print("1")
            elif status == StatusValues.Out:
                drawOut(name, window)
                print("2")
            elif status == StatusValues.Error:
                drawErr(window)  
                print("3")
            else:
                drawDefault(window)
        oldStatus = safeStatus
        oldName = name
        time.sleep(0.1)
        


