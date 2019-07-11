# from nfc.clf import RemoteTarget
from cacbarcode import PDF417Barcode, Code39Barcode
from attendance import MockAttendance, StatusValues
import graphics
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
	text = graphics.Text(graphics.Point(400, 240), s)
	text.setSize(30)
	text.draw(window)


def drawOut(name, window):
	clearWindow(window)
	time.sleep(.5)
	s = "Goodbye, " + name
	text = graphics.Text(graphics.Point(400, 240), s)
	text.setSize(30)
	text.draw(window)


def drawErr(window):
	clearWindow(window)
	time.sleep(.5)
	s = "Error, failuire to sign in or out"
	text = graphics.Text(graphics.Point(400, 240), s)
	text.setSize(30)
	text.draw(window)


def drawDefault(window):
	clearWindow(window)
	time.sleep(.5)
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
	edipi = None
	print("logic loop starting...")
	while True:
		barcode_data = input()
		edipi = getEDIPI(barcode_data)
		# Signin API call here, pass in edipi
		print("EDIPI =", edipi)
		status = attendance.checkin_checkout(edipi)
		print("Sending status...")
		print(status)
		c.acquire()
		safeStatus = status
		c.notify_all()
		c.release()
		print("status sent...")


if __name__ == "__main__":
	global safeStatus
	safeStatus = None
	print("Graphics thread starting...")
	t = threading.Thread(target=logic)
	t.start()
	window = drawWindow()
	while True:
		c.acquire()
		status = safeStatus
		c.release()
		print(status)
		if status == StatusValues.In:
			drawIn("connor", window)
			print("1")
		elif status == StatusValues.Out:
			drawOut("connor", window)
			print("2")
		elif status == StatusValues.Error:
			drawErr(window)  
			print("3")
		else:
			drawDefault(window)
		


