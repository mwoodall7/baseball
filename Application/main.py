'''
Copyright © Matthew Woodall (mwoodall7 on Github). All Worldwide Rights Reserved.

This material is the property of Matthew Woodall a.k.a. sparePartsBud on Github.
All use, alterations, disclosure, dissemination, and/or reproduction not specifically
authorized by sparePartsBud is prohibited.
'''

__version__ = "0.0.0"

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'GeneralHelpers'))

def main():
	print(__version__)

if __name__ == "__main__":
	main()
