from argparse import ArgumentParser
from signal import SIGINT, SIGTERM,signal
from modules.data_actions import data_actions


def signal_handler(sig, frame):
    
    print('\n\n\n\n\n\nProcess terminated')
    exit()

def main(args):

        signal(SIGINT, signal_handler)
        signal(SIGTERM, signal_handler)
        data=data_actions(args)
        data.gather_data()


def argument_parser():

    parser = ArgumentParser(description='Connection parameters')
    parser._action_groups.pop()

    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')

    required.add_argument('-d', help= "Device name",required=True)
    required.add_argument('-a', help= "Device address",required=True)
    required.add_argument('-u', help= "Login name",required=True)
    required.add_argument('-p', help= "Login password",required=True)
    required.add_argument('-tel', help= "Phone number",required=True)

    optional.add_argument('-sshp',default=22, help= "SSH connection port",required=False)
    optional.add_argument('-tls', help= "TLS type (cert)",required=False)
    optional.add_argument('-cp',default=1883, help= "MQTT connection port",required=False)
    optional.add_argument('-mqttauth',default="false", help= "MQTT authentificatio (true or false)",required=False)

    args = parser.parse_args()

    return args

if __name__=="__main__":

    args = argument_parser()
    main(args)