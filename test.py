from cacbarcode import PDF417Barcode, Code39Barcode

# If you want an EDIPI, but aren't sure which barcode is being scanned, do this:
edipi = None

barcode_data = input("scan it")
try:
  barcode = PDF417Barcode(barcode_data)
  # if this was the wrong type, an exception will be thrown
  # otherwise, this was the correct type, so set the edipi
  edipi = barcode.edipi
except:
  # Try the other barcode type
  try:
    barcode = Code39Barcode(barcode_data)
    
    edipi = barcode.edipi
  except:
    # Neither barcode was correct
    print("Neither barcode worked!")
    
print("EDIPI =", edipi)