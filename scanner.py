#from nfc.clf import RemoteTarget
from cacbarcode import PDF417Barcode, Code39Barcode
from attendance import MockAttendance, StatusValues
import graphics, time, threading
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
    win = graphics.GraphWin("CAC Sign in", 800, 480, autoflush=False)
    win.setBackground("white")
    return win


def clearWindow(win):
    for item in win.items[:]:
	item.undraw()
    win.update()

def drawIn(name, window):
    clearWindow(window)
    time.sleep(.5)
    s = "Welcome, " + name
    text = graphics.Text(graphics.Point(400,240), s)
    text.setSize(30)
    text.draw(window)

def drawOut(name, window):
    clearWindow(window)
    time.sleep(.5)
    s = "Goodbye, " + name
    text = graphics.Text(graphics.Point(400,240), s)
    text.setSize(30)
    text.draw(window)

def drawErr(window):
    clearWindow(window)
    time.sleep(.5)
    s = "Error, failuire to sign in or out"
    text = graphics.Text(graphics.Point(400,240), s)
    text.setSize(30)
    text.draw(window)

def drawDefault(window):
    clearWindow(window)
    time.sleep(.5)
    s = "Scan CAC to sign in or out"
    text = graphics.Text(graphics.Point(400,240), s)
    text.setSize(30)
    text.draw(window)


safeStatus = None
def getSafeStatus():
    return safeStatus

def setSafeStatus(stat):
    safeStatus = stat

def graphicsHandler():
    win = drawWindow()
    thread = None
    while True:
	getSafeStatus()
        if status == StatusValues.In:
           drawIn("connor", window)
	   print("1")
	elif status == StatusValues.Out:
            drawOut("connor",window)
	    print("2")
	elif status == StatusValues.Error:
	    drawErr()  
	    print("3")
	else:
	    drawDefault(window)

if __name__ == "__main__":
	attendance = MockAttendance()
	barcode_data = ""
	edipi = None
	threading.Thread(target=graphicsHandler).start()
	while True:
	
	    barcode_data = input()
	    edipi = getEDIPI(barcode_data)
	    # Signin API call here, pass in edipi
	    print("EDIPI =", edipi)
	    	
	    status = attendance.checkin_checkout(edipi)
	    print(status)
	    setSafeStatus(status)

    	#tag = clf.connect(rdwr={'on-connect': lambda tag: False})
    	#print(tag)
