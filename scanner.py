import nfc
from nfc.clf import RemoteTarget

clf = nfc.ContactlessFrontend('usb')
userInput = ""
while True:
	tag = clf.connect(rdwr={'on-connect': lambda tag: False})
	print(tag)
