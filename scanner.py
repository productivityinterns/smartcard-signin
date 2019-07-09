import nfc
#from nfc.clf import RemoteTarget
from cacbarcode import PDF417Barcode, Code39Barcode

def getEDIPI(data):
    try:
        barcode = PDF417Barcode(data)
        edipi = barcode.edipi
    except:
        # Try the other barcode type
        try:
            barcode = Code39Barcode(data)
            edipi = barcode.edipi
        except:
            # Neither barcode was correct
            # Blink failure light
            # make failure noise
            print("Neither barcode worked!")
    return edipi
#clf = nfc.ContactlessFrontend('usb')
barcode_data = ""
edipi = None
while True:
    barcode_data = input("scan it")
    edipi = getEDIPI(barcode_data)
    # Signin API call here, pass in edipi
    print("EDIPI =", edipi)

    	#tag = clf.connect(rdwr={'on-connect': lambda tag: False})
    	#print(tag)
