from asn1crypto import cms
from datetime import datetime
from cryptography import x509
from cryptography.hazmat.primitives.serialization import pkcs7, Encoding, PublicFormat
from pypomes_core import file_get_data


class CryptoPkcs7:
    """Python code to extract relevant data from a PKCS#7 signature file."""

    def __init__(self, p7s_file: str | bytes) -> None:
        """
        Instantiate the PKCS#7 crypto class, and extract the relevant data.

        :param p7s_file: a p7s file path, or the p7s file bytes
        """
        # instance attributes
        self.payload: bytes                       # the original payload
        self.payload_hash: bytes                  # the payload hash
        self.hash_algorithm: str                  # the algorithm used to calculate the payload hash
        self.signature: bytes                     # the digital signature
        self.signature_algorithm: str             # the algorithm used to generate the signature
        self.signature_timestamp: datetime        # the signature's timestamp
        self.public_key: bytes                    # the serialized public key (in PEM format)
        self.cert_chain: list[bytes]              # the serialized X509 certificate chain (in PEM format)

        # obtain the PKCS#7 file data
        p7s_bytes: bytes = file_get_data(p7s_file)

        # extract the certificate chain and serialize it in PEM format
        certs: list[x509.Certificate] = pkcs7.load_der_pkcs7_certificates(p7s_bytes)
        self.cert_chain = [cert.public_bytes(Encoding.PEM) for cert in certs]

        #  extract the public key and serialize it in PEM format
        cert: x509.Certificate = certs[-1]
        self.public_key = cert.public_key().public_bytes(Encoding.PEM, PublicFormat.SubjectPublicKeyInfo)

        # extract the needed structures
        content_info: cms.ContentInfo = cms.ContentInfo.load(p7s_bytes)
        signed_data: cms.SignedData = content_info["content"]
        signer_info: cms.SignerInfo = signed_data["signer_infos"][0]

        # extract the payload (None if payload is detached)
        self.payload = signed_data["encap_content_info"]["content"].native

        # extract the remaining components
        self.signature = signer_info[""].native
        self.signature_algorithm = signer_info["signature_algorithm"]["algorithm"].native
        self.hash_algorithm = signer_info["digest_algorithm"]["algorithm"].native

        signed_attrs = signer_info["signed_attrs"]
        for signed_attr in signed_attrs:
            match signed_attr["type"].native:
                case "message_digest":
                    self.payload_hash = signed_attr["values"][0].native
                case "signing_time":
                    self.signature_timestamp = signed_attr["values"][0].native
