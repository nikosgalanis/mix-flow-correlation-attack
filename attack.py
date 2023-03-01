"""
Step 1: Data Collection
-Get input packets time of entering mix network
-Get output packets time of arriving at node

Step 2: Flow Pattern Extraction
-Transform list of input packets and output packets into pattern vectors

Step 3: Distance Function Selection
-Determine the distance between the pattern vectors
-Distance Function 1: Mutual Information
-Distance Function 2: Frequency-spectrum-based matched filter

Step 4: Flow Correlation
-Selecting the OUTPUT link whose traffic has the minimum distance to INPUT flow pattern vector
"""
import struct
import random
from datetime import datetime, timedelta




def dataCollection():

	result_file = open('output.txt', 'r')

	lines = (line.strip().split('\t') for line in result_file)

	# dictionary of lists. ex A[192.32....] = []
	A = {}
	B = {}

	for [src, dest, in_time_str, _, out_time_str, _] in lines:
		A.setdefault(src, []).append(in_time_str)
		B.setdefault(dest, []).append(out_time_str)
	
	return A, B

dataCollection()

def flowPatternExtraction():
	# TODO: Implement Flow Pattern Extraction
	pass


def dist_mutual_info():
	# TODO: Implement Mutual Information distance function
	pass


def dist_fsb_matched_filter():
	# TODO: Implement Frequency-Spectrum-Based matched filter distance function
	pass


def distanceFunctionSelection():
	# TODO: Implement Distance Function Selection
	pass


def flowCorrelationAttack():
	# TODO: Implement Attack
	pass
