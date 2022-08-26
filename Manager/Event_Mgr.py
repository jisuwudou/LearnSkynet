def Singleton(cls):
	_instance={}
	def _singleton(*args,**kwagrs):
		if cls not in  _instance:
			_instance[cls]=cls(*args,**kwagrs)
		return _instance[cls]
	return _singleton

@Singleton
class Evt_Mgr():

	_eventList=[]
	_waitTrigger={}
	def AddEvent(self,sp,handler):
		self._eventList.append([sp,handler])

	def Dispatch(self, sp):
		self._waitTrigger[sp] = 1

	def Run(self):
		for item in self._eventList:
			sp = item[0]
			if sp in self._waitTrigger:
				item[1](sp)

		self._waitTrigger.clear()


def GetMgr():
	return Evt_Mgr()