'''
	 Game data utilized in algorithm obtained from Retrosheet.org:
	 	The information used here was obtained free of
     	charge from and is copyrighted by Retrosheet.  Interested
     	parties may contact Retrosheet at "www.retrosheet.org".
'''

__version__ = 1.0

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'GeneralHelpers'))

def main():
	print(__version__)

if __name__ == "__main__":
	main()
