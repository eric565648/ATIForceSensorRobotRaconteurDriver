import RobotRaconteur as RR
RRN = RR.RobotRaconteurNode.s
import RobotRaconteurCompanion as RRC
import argparse
import sys
import platform
import threading
import numpy as np
from RobotRaconteurCompanion.Util.InfoFileLoader import InfoFileLoader
from RobotRaconteurCompanion.Util.DateTimeUtil import DateTimeUtil
from RobotRaconteurCompanion.Util.SensorDataUtil import SensorDataUtil
from RobotRaconteurCompanion.Util.AttributesUtil import AttributesUtil

import rpi_ati_net_ft

class ATIDriver(object):
    def __init__(self, host):
        
        self.host = host
        self.ati_obj = rpi_ati_net_ft.NET_FT(host)

        self.ati_obj.set_tare_from_ft()
        print(self.ati_obj.read_ft_http())
        print(self.ati_obj.try_read_ft_http())
        
        self.ati_obj.start_streaming()
    
    def stream_loop(self):

        res, ft, status = self.ati_obj.try_read_ft_streaming(.1)

    

def main():
    parser = argparse.ArgumentParser(description="ATI force torque sensor driver service for Robot Raconteur")
    parser.add_argument("--sensor-ip", type=str, default="192.168.50.65", help="the ip address of the ati sensor")
    parser.add_argument("--wait-signal",action='store_const',const=True,default=False, help="wait for SIGTERM orSIGINT (Linux only)")

    args,_ = parser.parse_known_args()

    # not yet know what this do
    rr_args = ["--robotraconteur-jumbo-message=true"] + sys.argv

    ati_obj = ATIDriver(args.sensor_ip)

    with RR.ServerNodeSetup("com.robotraconteur.sensor.WrenchSensor",59823,argv=rr_args):
        
        service_ctx = RRN.RegisterService("ati_sensor","com.robotraconteur.sensor.WrenchSensor",ati_obj)
        
        if args.wait_signal:  
            #Wait for shutdown signal if running in service mode          
            print("Press Ctrl-C to quit...")
            import signal
            signal.sigwait([signal.SIGTERM,signal.SIGINT])
        
        else:    
            #Wait for the user to shutdown the service
            if (sys.version_info > (3, 0)):
                input("Server started, press enter to quit...")
            else:
                raw_input("Server started, press enter to quit...")


if __name__ == "__main__":
    main()