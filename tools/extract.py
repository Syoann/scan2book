#! /usr/bin/env python3

import sys

lines_file = sys.argv[1]
resize_factor_pc = sys.argv[2]

FACTOR = 1 / (int(resize_factor_pc) / 100)
MARGIN = 40

class Line:
    def __init__(self, x1, x2, y1, y2, angle, distance=0):
        # Starting coordinates
        self.x1 = int(float(x1))
        self.y1 = int(float(y1))

        # Ending coordinates
        self.x2 = int(float(x2))
        self.y2 = int(float(y2))

        # Angle of the line
        self.angle = int(float(angle))

        # Unused
        self.distance = int(distance)

    def __str__(self):
        return f"{self.x1} {self.x2} {self.y1} {self.y2} angle={self.angle}"

    def get_x(self):
        "Get the mean x"
        return int((self.x1 + self.x2) / 2)

    def get_y(self):
        "Get the mean y"
        return int((self.y1 + self.y2) / 2)



class LineSet:
    def __init__(self, lines=None, width=0, height=0):
        self.lines = []
        self.width = width
        self.height = height

        if lines is not None:
            self.lines = lines

    def get_vertical_lines(self):
        vlines = [ line for line in self.lines if line.angle < 5 or line.angle > 175 ]
        vlines.sort(key=lambda obj: obj.get_x())
        return vlines

    def get_horizontal_lines(self):
        hlines = [ line for line in self.lines if line.angle > 85 and line.angle < 95 ]
        hlines.sort(key=lambda obj: obj.get_y())
        return hlines

    def get_leftmost_line(self):
        leftmost_line = min(self.get_vertical_lines(), key=lambda obj: obj.get_x())

        if leftmost_line.get_x() > self.width * 0.1:
            leftmost_line = Line(0, 0, 0, self.height, angle=0)
        return leftmost_line

    def get_rightmost_line(self):
        rightmost_line = max(self.get_vertical_lines(), key=lambda obj: obj.get_x())

        if rightmost_line.get_x() < self.width * 0.9:
            rightmost_line = Line(self.width, self.width, 0, self.height, angle=0)
        return rightmost_line

    def get_spine_line(self):
        clines = [ line for line in self.get_vertical_lines() if line.get_x() > self.width * 0.1 and line.get_x() < self.width * 0.9 ]

        try:
            return max(clines, key=lambda obj: obj.distance)
        except ValueError:
            return Line(self.width / 2, self.width / 2, 0, self.height, angle=0)

    def get_uppermost_line(self):
        uppermost_line = min(self.get_horizontal_lines(), key=lambda obj: obj.get_y())
        if uppermost_line.get_y() > self.height * 0.1:
            uppermost_line = Line(0, self.width, 0, 0, angle=90)
        return uppermost_line

    def get_bottommost_line(self):
        bottommost_line = max(self.get_horizontal_lines(), key=lambda obj: obj.get_y())
        if bottommost_line.get_y() < self.height * 0.9:
            bottommost_line = Line(0, self.width, self.height, self.height, angle=90)
        return bottommost_line


def parse_lines_file(filename):
    result = {'size': [],
              'lines': []}

    with open(filename) as file_handler:
        for line in file_handler:
            if line.startswith('#'):
                continue

            content = line[:-1].split()

            # Document size
            if line.startswith('viewbox'):
                result['size'] = [int(content[3]), int(content[4])]

            # Line coordinates
            if line.startswith('line'):
                _, origin, destination, separator, count, angle, distance = content
                x1, y1 = origin.split(',')
                x2, y2 = destination.split(',')

                result['lines'].append(Line(x1, x2, y1, y2, angle, distance))

    return result


result = parse_lines_file(lines_file)

lineset = LineSet(result['lines'], result['size'][0], result['size'][1])

left = lineset.get_leftmost_line()
right = lineset.get_rightmost_line()
middle = lineset.get_spine_line()
top = lineset.get_uppermost_line()
bottom = lineset.get_bottommost_line()

width = int((middle.get_x() - left.get_x()) * FACTOR - 2 * MARGIN)
height = int((bottom.get_y() - top.get_y()) * FACTOR - 2 * MARGIN)

print(f"{width}x{height}+{int(left.get_x()*FACTOR+MARGIN)}+{int(top.get_y()*FACTOR+MARGIN)}\t{width}x{height}+{int(middle.get_x()*FACTOR+MARGIN)}+{int(top.get_y()*FACTOR+MARGIN)}")
