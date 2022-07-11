import json
from api_executor import APIExecutor 
class GetCIBot:
    def __init__(self):
        self.product = 'nsx-transformers'
        self.branch = 'nsx-jetfire-400-rel'
        self.pipeline = 'gating'
        self.payload_template = {
            "product": "nsx-transformers",
            "nsxbranch": "nsx-jetfire-400-rel",
            "pipeline": "gating",
            "area": "L3",
            "suite": "ESX_L3_NS2Tier_IPv6",
            "count": 1,
            "nsxbuild": 19337070,
            "nsxbuildkind": "ob"
             }
    def get_area_execution(self, build, areas=['L3', 'DFW', 'Edge-L2-L3', 'Operations', 'SmartNIC', 'SmartNIC-L3-UENS']):
        my_res = {}
        for area in areas:
            url_part2 = ('area-execution-summary/?nsxbuild=%s&product=%s&branch=%s&pipeline=%s&area=%s') %(build, self.product, self.branch, self.pipeline, area)
            print(area)
            apiexecutor = APIExecutor()
            response_data = apiexecutor.do_get(str(url_part2))
            print(response_data)
            my_res[area] = response_data['pass_percent']
        print(my_res)
        return my_res

    def get_suite_result_per_area(self, build):
        areas = {'L3': ["ESX_L3_NS2Tier_IPv6", "IPv6_DAD_ESX", "L3_NSXtonVDS"],
                 'DFW': ["VDS_DFW_GATING_ESX", "Policy-DFW-FEAT-GatingTest-01", "DFW.VerifyDataPathAndVmotionWith_L4L7_SSH_ALG_FTP", "DFW.POLICY.VerifyDataPathWith_ICMP_UDP_TCP"],
                 'Operations': ["NSXTonVDS.PortMirror.ERSPAN2Basic", "HeatMap.ESX.P0", "CAT_GATING.WORKFLOW_TRACING", "CAT_GATING.IPFIX_ESX", "nsxt_netopa_tunnellatency_tz", "nsxt_netopa_end2endlatency", "nsxt_netopa_tunnellatency_tz"],
                 'Edge-L2-L3': ["EDGE_L2L3_EVPN", "EDGE_L2L3_Generic_CAT_Suite", "EDGE_L2L3_OSPF", "Edge_L2_L3_Common", "Edge_L2_L3_Multicast"],
                 'SmartNIC-L3-UENS': ['ESX_L3_NS2Tier_IPv6', 'IPv6_DAD_ESX', 'NSX-SmartNIC-TraceFlow', 'SmartNIC-UENS-Netstats'],
                 "SmartNIC": ["NSX-SmartNIC-DFW", "NSX-SmartNIC-IPFIX", "NSX-SmartNIC-L2-L3", "NSX-SmartNIC-PortMirror"]
                }
        if build == '20083974':
            self.payload_template['nsxbranch'] = '"nsx-jetfire'
        with open('areas.json') as json_file:
            data = json.load(json_file)
        areas = data['areas']
        
        my_res = {}
        for area in areas.keys():
            suite_result_list = []
            for suite in areas[area]:
                suite_data = {}

                print("{} {}".format(area, suite))
                self.payload_template['area'] = area
                self.payload_template['suite'] = suite
                self.payload_template['nsxbuild'] = build
                url_part2 = 'testrun/history'
                apiexecutor = APIExecutor()
                response_data = apiexecutor.do_post(str(url_part2), self.payload_template)
                print(response_data)
                if response_data:
                    status = response_data[0].get('status')
                    if status:
                        suite_data[suite] = status
                    else:
                        suite_data[suite] = 'NULL/NOT executed'
                    if response_data[0]['status'] == 'FAIL':
                        suite_data['Triaged'] = response_data[0]['istriaged']
                        if response_data[0]['istriaged']:
                            suite_data['bugs'] = response_data[0]['bugs']
                suite_result_list.append(suite_data)
            my_res[area] = suite_result_list
        print(my_res)
        response = ""
        lines = "--------------------------------------------\n"
        response = response + lines + "\n"
        for area in my_res.keys():
            response = response + "Area:     " + area + "\n"
            for suite in my_res[area]:
                if suite:
                    response = response + "     " + json.dumps(suite) + "\n"
                else:
                    response = response + "no suite executed in this area\n"
                    break
            response = response + lines
        print(response)
        return response
#cibot = GetCIBot()
#cibot.get_area_execution('19337070', ['L3', 'DFW', 'Edge-L2-L3'])
#cibot.get_suite_result_per_area(int('19351349'))
