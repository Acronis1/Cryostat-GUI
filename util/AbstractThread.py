

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QObject, QThread, pyqtSignal, pyqtSlot



class AbstractThread(QObject):
	"""Abstract thread class to be used with instruments """
    sig_assertion = pyqtSignal(str)

    def __init__(self):
        QThread.__init__(self)
        self.__isRunning = True


    @pyqtSlot() # int
    def work(self):
        """class method which is working all the time while the thread is running
            
        """
        while self.__isRunning:
        	try: 
	        	self.running()
            except AssertionError as assertion: 
                self.sig_assertion.emit(assertion.args[0])	        


    def running(self):
    	"""class method to be implemented """
    	raise NotImplementedError

	@pyqtSlot()
	def stop(self):
		self.__isRunning = False
