__version__ = 1.0

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'GeneralHelpers'))

def main():
	print(__version__)

if __name__ == "__main__":
	main()
