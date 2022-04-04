from core.actions.BaseAction import BaseAction
from common.utilities.utilities import create_dir, get_dir_path, does_dir_exist
from config.paths import wasp_js_shared_ob_path
from common.error import *
import logging
import time
import ctypes

func_code_template = """
var b64 = {}(####vargs####);
hcall_return(b64);"""

_PWD = get_dir_path()
_CODE_PATH = "{}/virts/js_native".format(_PWD)

VIRTINE_PROC_IDENTIFIER = "virtine"
libname = wasp_js_shared_ob_path
c_lib = ctypes.CDLL(libname)
c_lib.js_x.restype = ctypes.c_char_p


class JSNativeAction(BaseAction):
	def __init__(self):
		super().__init__()
		self.runtime = 'jsnative'
		self.vcode = None

	def insert_code(self, vname, vcode):
		self.action_code = vcode
		func_code = func_code_template.format(vname)
		create_dir("{}/{}/".format(_CODE_PATH, self.action_name))
		vcode += func_code
		with open("{}/{}/func_{}.js".format(_CODE_PATH, self.action_name, self.action_name), 'w') as f:
			f.write(vcode)
		self.vcode = vcode

	def compile_code(self):
		pass

	def call_bin(self, args):
		js_code = self.vcode.replace("####vargs####", args)
		js_code = js_code.encode("utf-8")
		start = time.time()
		ret = c_lib.js_x(js_code)
		end = time.time()

		hits = ctypes.c_uint32()
		misses = ctypes.c_int32()
		c_lib.get_cache_stats(ctypes.byref(misses), ctypes.byref(hits))
		logging.log(logging.CRITICAL, 
		"exec_jsn- ###start###:" + str(start*1000) + \
		", ###end###:" + str(end*1000) + \
		", ###hits###:" + str(hits.value) + \
		", ###misses###:" + str(misses.value) + \
		", ###latency###:" + str((end-start)*1000)
		)
		return ret.decode('utf-8'), (end-start)*1000, misses.value, hits.value

	def execute_code(self, vargs):
		try:
			res, exectime, misses, hits = self.call_bin(str(vargs))
			return {
				"result": res,
				"runTime": exectime,
				"misses": misses,
				"hits": hits
			}
		except Exception as e:
			raise ActionInvokeError(self.action_name, str(e))
