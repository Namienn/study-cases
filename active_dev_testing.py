"""This file is directed at active development testing and debugging

Due to the nature of the framework, execs through 'if __name__ == "__main__":' 
Don't work, so i have to import the frame into an external file (this one)
in order to actually run active debugging tests on the code.

Ultimately, this is a workflow facilitator."""

from pathlib import Path
this_directory = Path(__file__).parent

import sys
sys.path.append(str(this_directory))

import ChasmSystem as chs

print('Done!')