import ledcube
import time
import random

class RainCube(ledcube.Cube):
    def __init__(self, **kwargs):
        super(RainCube, self).__init__(self, **kwargs)

    def run(self, dt=0.5):
        i, j, k = (0,0,0)
        while True:
            # Check if the active LED is falling
            falling = True
            if not RainCube.__checkIndex__(i,j,k-1):
                falling = False
            elif self.get(i,j,k-1):
                falling = False

            # Do the falling
            if falling:
                self.set(i, j, k, False, False)
                k -= 1
                self.set(i, j, k, True, False)
                self.update()
            else:
                if self.checkFull():
                    self.clear()

                while self.get(i, j, k):
                    i = random.choice(range(4))
                    j = random.choice(range(4))
                    k = 3
                self.set(i, j, k)

            # Wait
            time.sleep(dt)

    def checkFull(self):
        for val in self.state:
            if val == False:
                return False
        return True

if __name__ == '__main__':
    cube = RainCube()
    cube.run()

