"""

This Molotov script has:

- a global setup fixture that sets a global headers dict
- an init worker fixture that sets the session headers
- 3 scenario
- 2 tear downs fixtures

"""


vcode = """
int sleeep(int a){
    for(int i=0;i<a;i++){
        for (int j=0;j<a;j++){}
    }
	return a;
}
"""
import json
from molotov import (
    scenario,
    setup,
    global_setup,
    global_teardown,
    teardown,
    get_context,
)


_API = "http://192.5.86.158:8989"
_HEADERS = {}


# notice that the global setup, global teardown and teardown
# are not a coroutine.
@global_setup()
def init_test(args):
    _HEADERS["accept"] = "application/json"
    _HEADERS["Content-Type"] = "application/json"


@global_teardown()
def end_test():
    print("This is the end")


@setup()
async def init_worker(worker_num, args):
    headers = {}
    headers.update(_HEADERS)
    return {"headers": headers}


@teardown()
def end_worker(worker_num):
    print("This is the end for %d" % worker_num)


# # @scenario(weight=40)
# async def scenario_one(session):
#     async with session.get(_API) as resp:
#         if get_context(session).statsd:
#             get_context(session).statsd.incr("BLEH")
#         res = await resp.json()
#         assert res["result"] == "OK"
#         assert resp.status == 200


@scenario(weight=50)
async def scenario_invoke_func2(session):
    somedata = json.dumps({
		"vargs": {"a":100}
		})
    async with session.post(_API+"/actions/func2/invoke", data=somedata) as resp:
        assert resp.status == 200

@scenario(weight=50)
async def scenario_invoke_func1(session):
    somedata = json.dumps({
		"vargs": {"a":10000}
		})
    async with session.post(_API+"/actions/func1/invoke", data=somedata) as resp:
        assert resp.status == 200