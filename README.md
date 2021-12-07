# MQTT_Test
## Setup
**Python version:** 3.9.5 <br>
<br>
**Paramiko library:**<br>
used to communicate with the device using SSH protocol ```$ pip install paramiko```<br>
<br>
**OpenSSL library:**<br>
used to generate certificates ```$ pip install pyOpenSSL```<br>
<br>
**paho-mqtt library:**<br>
used to communicate with MQTT ```$ pip install paho-mqtt```<br>
<br>
## Configuration file usage
Configuration file is used to define devices with their MQTT topics and commands for router info retrieval.<br>
<br>
All information has to be stored inside ```"devices":``` json object array.<br>
<br>
**Device structure**<br>
<br>
```"device":``` Device name for which the configuration is being created.<br>
```"topics":``` Topics and commands for the specified device.<br>
<br>
**Topic structure**<br>
<br>
```"topic":``` Topic to witch will be subscirbed and published.<br>
```"config_command":``` Command to get information from routers configuration files.<br>
<br>
**Example**
```json
{ 
    "devices":[
        {
            "device":"rutx11",
            "topics":[
                    {
                        "topic":"temperature",
                        "config_command":"gsmctl -c"
                    },
                    {
                        "topic":"operator",
                        "config_command":"gsmctl -o"
                    },
                    {
                        "topic":"signal",
                        "config_command":"gsmctl -q"
                    },
                    {
                        "topic":"network",
                        "config_command":"gsmctl -g"
                    },
                    {
                        "topic":"connection",
                        "config_command":"gsmctl -t"
                    },
                    {
                        "topic":"wan",
                        "config_command":". /lib/functions/network.sh; network_find_wan NET_IF; network_get_ipaddr NET_ADDR ${NET_IF} ; echo ${NET_ADDR}"
                    },
                    {
                        "topic":"uptime",
                        "config_command":"ubus -S call system info"
                    },
                    {
                        "topic":"name",
                        "config_command":"uci get system.system.device_code"
                    },
                    {
                        "topic":"pin3",
                        "config_command":"uci get ioman.din1.value"
                    },
                    {
                        "topic":"pin4",
                        "config_command":"uci get ioman.dout1.value"
                    }  
                ]
        }
    ]
}
```


## Starting the script
Script is started using **main.py** module but it requires some parameters depending on the desired configuration.<br>
<br>
**Parameters**<br>
+ Required parameters<br>
```-d``` Device name that will be tested.<br>
```-a``` Device ip address.<br>
```-u``` Username for SSH connection athentification..<br>
```-p``` Password for SSH connection authentification.<br>
```-tel``` Phone number to which you want to get SMS notification if test failed.<br>
+ Optional parameters<br>
```-sshp``` Port for SSH connection (default=22).<br>
```-cp``` Connection port for MQTT client (default=1883).<br>
```-tls``` Type of tls to use (cert or dont include).<br>
```-mqttauth``` MQTT username and password usage (true or false, default=false).<br>

**Example**<br>

* Example for base MQTT setup<br>
```python3 main.py -d rutx11 -a 192.168.1.1 -u root -p admin01 -tel +37000000000```<br><br>

* Example for MQTT setup with certificates<br>
```python3 main.py -d rutx11 -a 192.168.1.1 -u root -p admin01 -tel +37000000000 -tls cert```<br><br>

* Example for MQTT setup with certificates and custom MQTT port<br>
```python3 main.py -d rutx11 -a 192.168.1.1 -u root -p admin01 -tel +37000000000 -tls cert -cp 8883```<br><br>

* Example for MQTT setup with certificates and MQTT authentification<br>
```python3 main.py -d rutx11 -a 192.168.1.1 -u root -p admin01 -tel +37000000000 -tls cert -mqttauth true```<br><br>
