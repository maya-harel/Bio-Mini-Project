class Constraints:

    def __init__(self, const, threshold, window):
        self.const = const
        self.q = threshold
        self.d = window

    def matchConst(self, input):
        print "does this input match the constraint ?"

    def matchWindow(self, windowTemp):
        print "does this input have an according window size ?"

    def matchFreq(self, frequency):
        print "is this input frequent enough ?"

    def match(self, const):
        print "does this input match all the constraints ?"