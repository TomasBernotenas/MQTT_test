from OpenSSL import crypto


class certificate_gen:
    
    
    def __init__(self,args):

        self.issuer=crypto.X509()
        self.reques=crypto.X509Req()
        self.issuerkey=None
        self.key=None
        self.__args=args

    def createKeyPair(self):

        try:

            pkey = crypto.PKey()
            pkey.generate_key(crypto.TYPE_RSA, 2048)
            return pkey

        except:
            print("Failed to generate key")
            exit()

    def cert_gen(self,
        serialNumber=0,
        validityEndInSeconds=10*365*24*60*60,
        KEY_FILE = "certificates/ca.key",
        CERT_FILE="certificates/ca.cert"):

        try:

            cert = crypto.X509()
            cert.set_serial_number(serialNumber)
            cert.gmtime_adj_notBefore(0)
            cert.gmtime_adj_notAfter(validityEndInSeconds)
            cert.set_issuer(self.issuer.get_subject())
            cert.set_subject(self.reques.get_subject())

            if cert.get_subject().CN!="ca":
                cert.add_extensions([crypto.X509Extension(b'subjectAltName',False,b'IP:'+bytes(self.__args.a,'utf-8'))])

            cert.set_pubkey(self.reques.get_pubkey())
            cert.sign(self.issuerkey, 'sha512')

            with open(KEY_FILE, "wt") as f:
                f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, self.key).decode("utf-8"))

            with open(CERT_FILE, "wt") as f:
                f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert).decode("utf-8"))
            
            return cert

        except:
            print("Failed to create certificate")
            exit()

    def request(self,
        emailAddress="Email",
        commonName="ca",
        countryName="LT",
        localityName="Kaunas",
        stateOrProvinceName="Kaunas",
        organizationName="Teltonika",
        organizationUnitName="Teltonika.Networks"):

        try:

            self.reques.get_subject().C = countryName
            self.reques.get_subject().ST = stateOrProvinceName
            self.reques.get_subject().L = localityName
            self.reques.get_subject().O = organizationName
            self.reques.get_subject().OU = organizationUnitName
            self.reques.get_subject().CN = commonName
            self.reques.get_subject().emailAddress = emailAddress
            self.reques.set_pubkey(self.key)
            self.reques.sign(self.key, 'sha512')
            
            return self.reques

        except Exception as e:
            print(e)
            print("Failed to create certificate request")
            exit()

