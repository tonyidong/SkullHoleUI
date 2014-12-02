from collections import Counter
import math
import sys

class Curve:
	numPoints = 0
	startPoint = ()
	endPoint = ()
	points = []

	def reverse(self):
		temp = self.startPoint
		self.startPoint = self.endPoint
		self.endPoint = temp
		self.points = reversed(self.points)


def distance(p1, p2):
	return math.sqrt((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2 + (p2[2]-p1[2])**2)

if __name__ == "__main__":
	inFile = sys.argv[1]
	outFile = inFile[:-6] + ".continous.curve"

	# Read in file
	f = open(inFile)
	lines = f.readlines()
	f.close()

	pointList = ["header"]
	edgeList = []

	# Open output file
	outf = open(outFile, 'w')

	numCurves = int(lines[0])
	sumPoints = 0
	curves = []

	curLine = 1
	for i in range(numCurves):
		entries = lines[curLine].split()
		numPoints = int(entries[0])
		sumPoints = sumPoints + numPoints

		curve = Curve()
		curve.numPoints = numPoints
		curve.points = lines[curLine + 1 : curLine + numPoints + 1]
		curve.startPoint = tuple(map(float, lines[curLine + 1].split()))
		curve.endPoint = tuple(map(float, lines[curLine + numPoints].split()))
		curves.append(curve)

		curLine = curLine + numPoints + 1


	outf.write("1\n")
	outf.write(str(sumPoints) + "\n")
	outf.write(str(sumPoints) + "\n")

	i = 0
	while numCurves > 0:
		curve = curves.pop(i)
		for line in curve.points:
			outf.write(line)
		minDistF = 999
		for j in range(len(curves)):
			if distance(curves[j].endPoint, curve.startPoint) < minDistF:
				minDistF = distance(curves[j].startPoint, curve.endPoint)
				minCurveF = j
		minDistR = 999
		for j in range(len(curves)):
			if distance(curves[j].endPoint, curve.startPoint) < minDistR:
				minDistR = distance(curves[j].endPoint, curve.endPoint)
				minCurveR = j
		if minDistF <= minDistR:
			i = minCurveF
		else:
			i = minCurveR
			curves[i].reverse()
		numCurves = numCurves - 1

	outf.close()