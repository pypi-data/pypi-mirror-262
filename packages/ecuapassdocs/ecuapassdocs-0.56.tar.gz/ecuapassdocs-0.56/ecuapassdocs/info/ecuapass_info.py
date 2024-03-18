
import os, json, re

from .ecuapass_data import EcuData
from .ecuapass_extractor import Extractor
from .ecuapass_utils import Utils

# Base class for all info document clases: CartaporteInfo (CPI), ManifiestoInfo (MCI), EcuDCL (DTAI)
class EcuInfo:
	def __init__ (self, fieldsJsonFile, runningDir):
		self.fieldsJsonFile      = fieldsJsonFile
		self.runningDir          = runningDir
		self.resourcesPath       = os.path.join (runningDir, "resources", "data_cartaportes") 
		self.fields              = json.load (open (fieldsJsonFile))
		self.fields ["jsonFile"] = fieldsJsonFile
		self.ecudoc              = {}

	#-- For all types of documents (fixed fro NTA and BYZA, check the others)
	def getNumeroDocumento (self):
		text   = Utils.getValue (self.fields, "00b_Numero")
		numero = Extractor.getNumeroDocumento (text)

		codigo = self.getCodigoPais (numero)
		self.fields ["00_Pais"] = {"value":codigo, "content":codigo}
		return numero

	#-- Returns the first two letters from document number
	def getCodigoPais (self, numero):
		try:
			if numero.startswith ("CO"): 
				return "CO"
			elif numero.startswith ("EC"): 
				return "EC"
		except:
			print (f"ALERTA: No se pudo determinar código del pais desde el número: '{numero}'")
		return ""

	#-- Return updated PDF document fields
	def getDocFields (self):
		return self.fields

	#-- Get id (short name)
	def getIdEmpresa (self):
		return self.empresa ["id"]

	#-- Get data and value from document main fields"""
	def getNombreEmpresa (self):
		return self.empresa ["nombre"]

	def getDireccionEmpresa (self):
		return self.empresa ["direccion"]

	#-----------------------------------------------------------
	#-- Return IMPORTACION or EXPORTACION
	#-----------------------------------------------------------
	def getTipoProcedimiento (self):
		return "IMPORTACION||LOW"

	def getTipoProcedimiento (self):
		tipoProcedimiento = None
		procedimientosNTA   = {"CO":"IMPORTACION", "EC":"EXPORTACION"}
		procedimientosBYZA  = {"CO":"EXPORTACION", "EC":"IMPORTACION"}

		try:
			if self.empresa ["id"] == "NTA":
				procedimientos = procedimientosNTA
			elif self.empresa ["id"] == "BYZA":
				procedimientos = procedimientosBYZA

			numero            = self.getNumeroDocumento ()
			codigoPais        = self.getCodigoPais (numero)
			tipoProcedimiento = procedimientos [codigoPais]
		except:
			Utils.printException ("No se pudo determinar tipo de procedimiento (Importación/Exportación)")
			tipoProcedimiento = "IMPORTACION||LOW"

		return tipoProcedimiento

	#-----------------------------------------------------------
	# Get info from mercancia: INCONTERM, Ciudad, Precio, Tipo Moneda
	#-----------------------------------------------------------
	def getIncotermInfo (self, text):
		info = {"incoterm":None, "precio":None, "moneda":None, "pais":None, "ciudad":None}

		try:
			text = text.replace ("\n", " ")

			# Precio
			text, precio    = Extractor.getRemoveNumber (text)
			info ["precio"] = Utils.checkLow (Utils.convertToAmericanFormat (precio))
			text = text.replace (precio, "") if precio else text

			# Incoterm
			termsString = Extractor.getDataString ("tipos_incoterm.txt", 
			                                        self.resourcesPath, From="keys")
			reTerms = rf"\b({termsString})\b" # RE for incoterm
			incoterm = Utils.getValueRE (reTerms, text)
			info ["incoterm"] = Utils.checkLow (incoterm)
			text = text.replace (incoterm, "") if incoterm else text

			# Moneda
			info ["moneda"] = "USD"
			text = text.replace ("USD", "")
			text = text.replace ("$", "")

			# Get ciudad from text and Search 'pais' in previos boxes
			ciudadPais   = Extractor.extractCiudadPais (text, self.resourcesPath) 
			ciudad, pais = ciudadPais ["ciudad"], ciudadPais ["pais"]

			info ["ciudad"], info ["pais"] = self.searchPaisPreviousBoxes (ciudad, pais)
			if not info ["pais"]:
				info ["pais"]   = Utils.checkLow (info["pais"])
				info ["ciudad"] = Utils.addLow (info ["ciudad"])
			elif info ["pais"] and not info ["ciudad"]:
				info ["ciudad"] = Utils.addLow (info ["ciudad"])

		except:
			Utils.printException ("Obteniendo informacion de 'mercancía'")

		return info

	#-----------------------------------------------------------
	# Clean watermark: depending for each "company" class
	#-----------------------------------------------------------
	def cleanWaterMark (self, text):
		if self.empresa ['id'] == "NTA":
			w1, w2, w3, w4 = "N\.T\.A\.", "CIA\.", "LTDA.", "N\.I\.A\."
			expression = rf'(?:{w1}\s+{w2}\s+{w3}|{w2}\s+{w3}\s+{w1}|{w3}\s+{w1}\s+{w2}|{w4}\s+{w2}\s+{w3}|{w2}\s+{w3}\s+{w4}|{w3}\s+{w4}\s+{w2}|{w1}\s+{w2}\s+{w3}|{w2}\s+{w3}\s+{w1}|{w3}\s+{w1}\s+{w2}|{w4}\s+{w2}\s+{w3}|{w2}\s+{w3}\s+{w4}|{w3}\s+{w4}\s+{w2})'

		elif self.empresa ['id'] == 'BYZA':
			w1, w2, w3, w4, w5, w6 = "By", "za", "soluciones", "que.", "facilitan", "tu", "vida"
			expression = rf'{w1}\s+{w2}\s+{w3}\s+{w4}\s+{w5}\s+{w6}'
		else:
			return text

		pattern = re.compile (expression)
		text = re.sub (pattern, '', text)

		return text.strip()

