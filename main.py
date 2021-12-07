from argparse import ArgumentParser
from signal import SIGINT,signal
from modules.data_actions import data_actions


def signal_handler(sig, frame):
    
    print('\n\n\n\n\n\nProcess terminated')
    exit()

def main(args):

        signal(SIGINT, signal_handler)
        data=data_actions(args)
        data.gather_data()


def argument_parser():

    parser = ArgumentParser(description='Connection parameters')

    parser.add_argument('-d', help= "Device name",required=True)
    parser.add_argument('-a', help= "Device address",required=True)
    parser.add_argument('-u', help= "Login name",required=True)
    parser.add_argument('-p', help= "Login password",required=True)
    parser.add_argument('-tel', help= "Phone number",required=True)

    parser.add_argument('-sshp',default=22, help= "SSH connection port")
    parser.add_argument('-tls', help= "TLS type (cert)")
    parser.add_argument('-cp',default=1883, help= "MQTT connection port")
    parser.add_argument('-mqttauth',default="false", help= "MQTT authentificatio (true or false)")

    args = parser.parse_args()

    return args

if __name__=="__main__":

    args = argument_parser()
    main(args)