class Constraints:

    def __init__(self, const, threshold, window):
        self.const = const
        self.q = threshold
        self.d = window

    def evaluate(self, const):
        print "checking : does this input match all the constraints ?"

