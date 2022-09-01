

from enum import Enum
class ESYS(Enum):
	DefaultSys = 0
	MovementSys = 1

class ECMD(Enum):

	cMovePos = 1

	sCreateMainPlayer = 1
	sCreateOtherPlayer = 2
	sOtherPos = 3