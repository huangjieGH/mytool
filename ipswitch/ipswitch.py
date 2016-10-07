import wmi
import sys
import configparser 
import argparse
import datetime
from colorama import init,Fore,Back,Style
from __init__ import __version__

conf = configparser.ConfigParser()
conf.read("E:/DATA/F/python/mytool/networkAdapterConf.ini")
networkdesc = conf["public"]["networkdesc"]
subnetmask = conf["public"]["submask"]
wmiobj = wmi.WMI()

def switchNetworkConfiguration(networktype):
    configurations = wmiobj.Win32_NetworkAdapterConfiguration(Description=networkdesc, IPEnabled=True)

    if networktype == "outer":
        ipaddress = conf["interface_outer"]["ipaddress"]
        defaultgateway = conf["interface_outer"]["defaultgateway"]
        dnsserver = conf["interface_outer"]["dnsserver"]
    elif networktype == "inner":
        ipaddress = conf["interface_inner"]["ipaddress"]
        defaultgateway = conf["interface_inner"]["defaultgateway"]
        dnsserver = conf["interface_inner"]["dnsserver"]
    else:
        return False

    ret = configurations[0].SetGateways(DefaultIPGateway=[defaultgateway])
    ret1 = configurations[0].SetDNSServerSearchOrder(DNSServerSearchOrder = [dnsserver])
    ret2 = configurations[0].EnableStatic(IPAddress = [ipaddress], SubnetMask = [subnetmask])

    if (ret[0] == 0 and ret1[0] == 0 and ret2[0] == 0):
        return True
    else:
        print(Fore.RED + Back.YELLOW + "Error:the errorcode are ret:%s,ret1:%s,ret2:%s"%(ret,ret1,ret2))
        return False

def displayNetworkConfiguration():
    sql = "select IPAddress,IPSubnet,DefaultIPGateway,DNSServerSearchOrder from Win32_NetworkAdapterConfiguration where Description=\"" + networkdesc + "\" and IPEnabled=TRUE"
    current_configuration = wmiobj.query(sql)
    print(Fore.GREEN + Back.WHITE + "Now your NetworkAdapter configuration are:")
    #print(current_configuration[0])
    print(Fore.GREEN + Back.BLACK + "DefaultIPGateway:%s"%current_configuration[0].DefaultIPGateway)
    print(Fore.GREEN + Back.BLACK + "DNSServerSearchOrder:%s"%current_configuration[0].DNSServerSearchOrder)
    print(Fore.GREEN + Back.BLACK + "IPAddress:%s"%current_configuration[0].IPAddress)
    print(Fore.GREEN + Back.BLACK + "IPSubnet:%s"%current_configuration[0].IPSubnet)

def get_parser():
    parser = argparse.ArgumentParser(description='switch ip address via the command line')
    parser.add_argument('-t', '--type', type=str, help='the type of the network: inner|oute',choices=['inner','outer'])
    parser.add_argument('-v', '--version', help='displays the current version of ipswitch',action='store_true')
    return parser

def get_datetime():
    return datetime.datetime.now()

def command_line_runner():
    parser = get_parser()
    args = vars(parser.parse_args())

    if args['version']:
        print(__version__)
        return


    if args['type'] in ('inner','outer'):
        networktype = args['type']
        result = switchNetworkConfiguration(networktype)

        if result == True:
            print(Fore.GREEN + Back.WHITE + "Switch NetworkConfiguration success !\n")
            displayNetworkConfiguration()
        else:
            print(Fore.RED + Back.YELLOW + "Switch NetworkConfiguration failed !")

#def _timeit_analyze_(func):
#    from timeit import Timer
#    t1 = Timer("%s()" % func.__name__, "from __main__ import %s" % func.__name__)
#    print("{:<20}{:10.6} s".format(func.__name__ + ":", t1.timeit(1)))

if __name__ == "__main__":
    import timeit
    starttime = get_datetime()
    #初始化 colorama
    init(autoreset = True)
    command_line_runner()
    endtime = get_datetime()
    print('\n' + Fore.RED + Back.YELLOW + 'Total spend:%s'%(endtime - starttime))

    #_timeit_analyze_(command_line_runner)
