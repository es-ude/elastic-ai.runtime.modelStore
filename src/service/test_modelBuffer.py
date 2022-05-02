import unittest

import ModelBuffer

class test_ModelBuffer(unittest.TestCase):


	def setUp(self):	#Code, der vor jedem Test ausgeführt wird.
		pass

	def test_emptyTest(self):
		self.assertTrue(True)	

	def test_safeEmptyModel(self):
		modelBuffer = ModelBuffer()
		model = ""	#todo: leeres Model soll erzeugt werden.
		self.assertRaises(BaseException, modelBuffer.save(model))	#durch unsere eigene Exception ersetzen

	def test_saveAndLookForModel(self):
		modelBuffer = ModelBuffer()
		model = "Platzhalter"
		modelBuffer.saveModel(model)
		self.assertTrue(modelBuffer.lookFor(model))	#Problem: Model ist Parameter von lookFor()

	def test_safeAndLoadModel(self):
		modelBuffer = ModelBuffer()
		model = "Platzhalter"
		modelBuffer.saveModel(model)
		modelBuffer.lookFor(model)
		self.assertEqual(model, modelBuffer.getModel())	#was ist ein passender Parameter für getModel?

	def test_getModelWithoutLookFor(self):
		modelBuffer = ModelBuffer()
		self.assertRises(BaseException, modelBuffer.getModel())	#todo: passende Exception 
		#Problem: möglicherweise wurde irgendwann lookFor() aufgerufen. Architektur überdenken

	

	def tearDown(self):	#Code, der nach jedem Test ausgeführt wird.
		pass
