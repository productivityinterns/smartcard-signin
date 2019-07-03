# smartcard-signin
Application for handling smartcard identities and performing remote check-in

This application will take advantage of a USB NFC reader to obtain smartcard identity, and emit status via a "blink mk2" USB status light.

The general flow of the application is as follows:

* A user scans their ID card with the NFC reader
* If the identity could not be read, flash a blinking red light and make an error sound
* If the identity could be read:
	* Call "Check In/Out" routine and record return value
	* If "In" value is received, turn light solid green for X seconds, play a "Checked In" tone
	* If "Out" Value is received, turn light solid red for X seconds, play a "Checked Out" tone
	* If any other value is received, blink yellow and play an error tone


 
If NFC doesn't pan out, or there are technical issues, an alternative is John's [CACBarcode](https://github.com/jkusner/CACBarcode/pulse) library