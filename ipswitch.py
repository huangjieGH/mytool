import wmi
import sys
import configparser 
from colorama import init,Fore,Back,Style

def usage():
    print(Fore.GREEN + Back.WHITE + Style.DIM + '''Usage:
             ipswitch outer|inner
            ''')

def switchNetworkConfiguration(networktype):
    wmiobj = wmi.WMI()
    configurations = wmiobj.Win32_NetworkAdapterConfiguration(Description='Intel(R) Ethernet Connection (3) I218-LM', IPEnabled=True)

    conf = configparser.ConfigParser()
    conf.read("F:/python/mytool/networkAdapterConf.ini")

    subnetmask = conf["public"]["submask"]

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
    wmiobj = wmi.WMI()
    sql = "select IPAddress,IPSubnet,DefaultIPGateway,DNSServerSearchOrder from Win32_NetworkAdapterConfiguration where Description=\"Intel(R) Ethernet Connection (3) I218-LM\" and IPEnabled=TRUE"
    current_configuration = wmiobj.query(sql)
    print(Fore.GREEN + Back.WHITE + "Now your NetworkAdapter configuration are:")
    #print(current_configuration[0])
    print(Fore.GREEN + Back.BLACK + "DefaultIPGateway:%s"%current_configuration[0].DefaultIPGateway)
    print(Fore.GREEN + Back.BLACK + "DNSServerSearchOrder:%s"%current_configuration[0].DNSServerSearchOrder)
    print(Fore.GREEN + Back.BLACK + "IPAddress:%s"%current_configuration[0].IPAddress)
    print(Fore.GREEN + Back.BLACK + "IPSubnet:%s"%current_configuration[0].IPSubnet)

def main():
    if (len(sys.argv) == 2):
        if (sys.argv[1] != "outer" and sys.argv[1] != "inner"):
            usage()
            exit()
        else:
            networktype = sys.argv[1]
    else:
        usage()
        exit()

    result = switchNetworkConfiguration(networktype)

    if result == True:
        print(Fore.GREEN + Back.WHITE + "Switch NetworkConfiguration success !\n")
        displayNetworkConfiguration()
    else:
        print(Fore.RED + Back.YELLOW + "Switch NetworkConfiguration failed !")

if __name__ == "__main__":
    #初始化 colorama
    init(autoreset = True)
    main()
