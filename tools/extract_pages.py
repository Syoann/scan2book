#! /usr/bin/env python3

import cv2
import numpy
import sys


class Block:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def size(self):
        return self.end - self.start + 1

    def display(self, height=0, margin=0):
        return f"{int(self.size() + 2 * margin)}x{int(height)}+{int(max(0, self.start-margin))}+0"

    def __str__(self):
        return f"{self.start}..{self.end} ({self.size()})"


img_name = sys.argv[1]

img = cv2.imread(img_name)

rows, cols, channels = img.shape

# Maximum gap size to stay in the same block
max_gap = max(10, cols * 0.005)

# In grayscale or black and white images, red = green = blue, so we only take the first channel
CHANNEL = 0

intensities = numpy.array([ [sum(img[:,col][:,CHANNEL]) / rows] for col in range(cols) ])

max_intensity = intensities.max(0)[0]
min_intensity_threshold = 10

blocks = []
prev, start = 0, 0
for index, intensity in enumerate(intensities):
    if intensity < 0.98 * max_intensity and intensity > min_intensity_threshold:
        if index - prev > max_gap:
            blocks.append(Block(start, prev))
            start = index
        prev = index

blocks.append(Block(start, prev))

block_sizes = sorted([block.size() for block in blocks], reverse=True)

pages = sorted([block for block in blocks if block.size() >= block_sizes[1]], key=lambda x: x.start)

print(pages[0].display(height=cols, margin=max_gap), pages[1].display(height=cols, margin=max_gap), sep="\t")
