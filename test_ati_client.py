
from RobotRaconteur.Client import *
import time
import numpy
import sys

def main():

    url='rr+tcp://localhost:59823?service=ati_sensor'
    if (len(sys.argv)>=2):
        url=sys.argv[1]

    #Connect to the service
    cli = RRN.ConnectService(url)

    #Connect a wire connection
    wrench_wire = cli.wrench_sensor_value.Connect()

    #Add callback for when the wire value change
    wrench_wire.WireValueChanged += wrench_wire_cb


def wrench_wire_cb(w,value,time):

    val = w.Invalue

    print("==============")
    print("torque.x",val.torque.x)
    print("torque.y",val.torque.y)
    print("torque.z",val.torque.z)
    print("force.x",val.force.x)
    print("force.y",val.force.y)
    print("force.z",val.force.z)
    print("==============")

if __name__=='__main__':
    main()