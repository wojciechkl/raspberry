from threading import Thread
import pad
import stepper

PadState = {
    "rstick": 0 
}

class PadListener:
    def jstick(self, axis, fval):
        if(axis == "rx"):
            print "rx %f" % fval
            PadState["rstick"] = fval

    def buttonDown(self, button):
        print "button " + (button)

    def buttonUp(self, button):
        print "button up"

def captureEvents():
    pad.capturePadEvents(PadListener())

padEventLoop = Thread(target=captureEvents)
padEventLoop.daemon = True
padEventLoop.start()

print("Starting steering loop")
stepper.SteeringLoop(PadState)

