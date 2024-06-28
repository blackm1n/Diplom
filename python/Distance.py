import math


class Distance:
    blocks: int
    pixels: int
    subpixels: int
    subsubpixels: int
    subsubsubpixels: int

    def __init__(self, blocks, pixels, subpixels, subsubpixels, subsubsubpixels):
        self.blocks = blocks
        self.pixels = pixels
        self.subpixels = subpixels
        self.subsubpixels = subsubpixels
        self.subsubsubpixels = subsubsubpixels

    def add_distance_d(self, distance):
        if distance.get_distance(5) < 0:
            self.remove_distance_d(distance.reverse())
            return

        self.blocks += distance.get_blocks()
        self.pixels += distance.get_pixels()
        self.subpixels += distance.get_subpixels()
        self.subsubpixels += distance.get_subsubpixels()
        self.subsubsubpixels += distance.get_subsubsubpixels()

        while self.subsubsubpixels >= 16:
            self.subsubsubpixels -= 16
            self.subsubpixels += 1
        while self.subsubpixels >= 16:
            self.subsubpixels -= 16
            self.subpixels += 1
        while self.subpixels >= 16:
            self.subpixels -= 16
            self.pixels += 1
        while self.pixels >= 16:
            self.pixels -= 16
            self.blocks += 1

    def add_distance(self, blocks, pixels, subpixels, subsubpixels, subsubsubpixels):
        self.blocks += blocks
        self.pixels += pixels
        self.subpixels += subpixels
        self.subsubpixels += subsubpixels
        self.subsubsubpixels += subsubsubpixels

        while self.subsubsubpixels >= 16:
            self.subsubsubpixels -= 16
            self.subsubpixels += 1
        while self.subsubpixels >= 16:
            self.subsubpixels -= 16
            self.subpixels += 1
        while self.subpixels >= 16:
            self.subpixels -= 16
            self.pixels += 1
        while self.pixels >= 16:
            self.pixels -= 16
            self.blocks += 1

    def remove_distance_d(self, distance):
        self.blocks -= distance.get_blocks()
        self.pixels -= distance.get_pixels()
        self.subpixels -= distance.get_subpixels()
        self.subsubpixels -= distance.get_subsubpixels()
        self.subsubsubpixels -= distance.get_subsubsubpixels()

        if self.get_distance(5) > 0:
            while self.subsubsubpixels < 0:
                self.subsubsubpixels += 16
                self.subsubpixels -= 1
            while self.subsubpixels < 0:
                self.subsubpixels += 16
                self.subpixels -= 1
            while self.subpixels < 0:
                self.subpixels += 16
                self.pixels -= 1
            while self.pixels < 0:
                self.pixels += 16
                self.blocks -= 1
        else:
            while self.subsubsubpixels <= -16:
                self.subsubsubpixels += 16
                self.subsubpixels -= 1
            while self.subsubpixels <= -16:
                self.subsubpixels += 16
                self.subpixels -= 1
            while self.subpixels <= -16:
                self.subpixels += 16
                self.pixels -= 1
            while self.pixels <= -16:
                self.pixels += 16
                self.blocks -= 1


    def remove_distance(self, blocks, pixels, subpixels, subsubpixels, subsubsubpixels):
        self.blocks -= blocks
        self.pixels -= pixels
        self.subpixels -= subpixels
        self.subsubpixels -= subsubpixels
        self.subsubsubpixels -= subsubsubpixels

        if self.get_distance(5) > 0:
            while self.subsubsubpixels < 0:
                self.subsubsubpixels += 16
                self.subsubpixels -= 1
            while self.subsubpixels < 0:
                self.subsubpixels += 16
                self.subpixels -= 1
            while self.subpixels < 0:
                self.subpixels += 16
                self.pixels -= 1
            while self.pixels < 0:
                self.pixels += 16
                self.blocks -= 1
        else:
            while self.subsubsubpixels <= -16:
                self.subsubsubpixels += 16
                self.subsubpixels -= 1
            while self.subsubpixels <= -16:
                self.subsubpixels += 16
                self.subpixels -= 1
            while self.subpixels <= -16:
                self.subpixels += 16
                self.pixels -= 1
            while self.pixels <= -16:
                self.pixels += 16
                self.blocks -= 1


    def set_blocks(self, blocks):
        self.blocks = blocks

    def set_pixels(self, pixels):
        self.pixels = pixels

    def set_subpixels(self, subpixels):
        self.subpixels = subpixels

    def set_subsubpixels(self, subsubpixels):
        self.subsubpixels = subsubpixels

    def set_subsubsubpixels(self, subsubsubpixels):
        self.subsubsubpixels = subsubsubpixels

    def get_blocks(self):
        return self.blocks

    def get_pixels(self):
        return self.pixels

    def get_subpixels(self):
        return self.subpixels

    def get_subsubpixels(self):
        return self.subsubpixels

    def get_subsubsubpixels(self):
        return self.subsubsubpixels

    def reverse(self):
        return Distance(-self.blocks, -self.pixels, -self.subpixels, -self.subsubpixels, -self.subsubsubpixels)

    def get_distance(self, type):
        if type == 1:
            return 2 * (self.blocks * math.pow(16, 1))
        elif type == 2:
            return 2 * (self.blocks * math.pow(16, 1)) + 2 * (self.pixels * math.pow(16, 0))
        elif type == 3:
            return 2 * (self.blocks * math.pow(16, 1)) + 2 * (self.pixels * math.pow(16, 0)) + 2 * (self.subpixels * math.pow(16, -1))
        elif type == 4:
            return 2 * (self.blocks * math.pow(16, 1)) + 2 * (self.pixels * math.pow(16, 0)) + 2 * (self.subpixels * math.pow(16, -1)) + 2 * (self.subsubpixels * math.pow(16, -2))
        elif type == 5:
            return 2 * (self.blocks * math.pow(16, 1)) + 2 * (self.pixels * math.pow(16, 0)) + 2 * (self.subpixels * math.pow(16, -1)) + 2 * (self.subsubpixels * math.pow(16, -2)) + 2 * (self.subsubsubpixels * math.pow(16, -3))

    def get_distance_d(self):
        return Distance(self.blocks, self.pixels, self.subpixels, self.subsubpixels, self.subsubsubpixels)
