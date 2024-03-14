import hashlib
import sys

from asn1crypto.x509 import Certificate
from Crypto.Hash import SHA256
from Crypto.Hash.SHA256 import SHA256Hash
from Crypto.PublicKey.RSA import import_key, RsaKey
from Crypto.Signature import pkcs1_15
from Crypto.Signature.pkcs1_15 import PKCS115_SigScheme
from io import BytesIO
from pathlib import Path
from pyhanko.sign.validation.pdf_embedded import EmbeddedPdfSignature
from pyhanko_certvalidator import ValidationContext
from pyhanko.keys import load_certs_from_pemder, load_certs_from_pemder_data
from pyhanko.pdf_utils.reader import PdfFileReader
from pyhanko.sign.validation import validate_pdf_signature
from pyhanko.sign.validation.status import PdfSignatureStatus
from pypomes_core import APP_PREFIX, env_get_str, exc_format
from typing import Final, BinaryIO

from crypto_pkcs7 import CryptoPkcs7

CRYPTO_HASH_ALGORITHM: Final[str] = env_get_str(f"{APP_PREFIX}_DEFAULT_HASH_ALGORITHM", "sha256")


def crypto_compute_hash(msg: Path | str | bytes, alg: str = CRYPTO_HASH_ALGORITHM) -> bytes:
    """
    Compute the hash of *msg*, using the algorithm specified in *alg*.

    Return *None* if computing the hash not possible.
    Supported algorithms: md5, blake2b, blake2s, sha1, sha224, sha256, sha384 sha512,
    sha3_224, sha3_256, sha3_384, sha3_512, shake_128, shake_256.

    :param msg: The message to calculate the hash for, or a path to a file.
    :param alg: The algorithm to use, or a default value (either 'sha256', or an environment-defined value).
    :return: The hash value obtained, or None if the hash could not be computed.
    """
    hasher = hashlib.new(alg.lower())

    # what is the type of the argument ?
    if isinstance(msg, bytes):
        # argument is type 'bytes'
        hasher.update(msg)

    elif Path.is_file(Path(msg)):
        # argument is the path to a file
        buf_size: int = 128 * 1024
        with Path.open(Path(msg), "rb") as f:
            while True:
                file_bytes: bytes = f.read(buf_size)
                if not file_bytes:
                    break
                hasher.update(file_bytes)

    return hasher.digest()


def crypto_validate_p7s(errors: list[str], p7s_file: str | bytes, p7s_payload: str | bytes = None) -> bool:
    """
    Validate the digital signature of a PKCS#7 file.

    If a *list* is provided in *errors*, the following inconsistencies are reported:
        - No payload found
        - The digital signature is invalid
        - The payload's hash value does not match its content

    :param errors: incidental error messages
    :param p7s_file:  a p7s file path, or the p7s file bytes
    :param p7s_payload:  a payload file path, or the payload bytes
    :return: True if the input data are consistent, False otherwise
    """
    # instantiate the return variable
    result: bool = True

    # instantiate the PKCS7 object
    pkcs7: CryptoPkcs7 = CryptoPkcs7(p7s_file)

    # obtain the payload
    payload: bytes | None = None
    # is the payload detached ?
    if p7s_payload:
        # yes, is the input argument a file path ?
        if isinstance(p7s_payload, str):
            # yes, load payload from file
            with Path.open(Path(p7s_payload), "rb") as f:
                payload = f.read()
        # does it directly holds the payload ?
        elif isinstance(p7s_payload, bytes):
            # yes, use it
            payload = p7s_file
    else:
        # no, retrieve the payload from the p7s file
        payload = pkcs7.payload

    # has the payload been obtained ?
    if payload:
        # yes, validate it
        payload_hash: bytes = crypto_compute_hash(payload, pkcs7.hash_algorithm)
        if payload_hash != pkcs7.payload_hash:
            result = False
            if isinstance(errors, list):
                errors.append("The payload's hash value does not match its content")
    else:
        # no, report the problem
        result = False
        if isinstance(errors, list):
            errors.append("No payload found")

    # where there error ?
    if result:
        # no, verify the signature
        try:
            rsa_key: RsaKey = import_key(pkcs7.public_key)
            # TODO: obtain 'sha256_hash' directly from 'pkcs7.signature'
            sha256_hash: SHA256Hash = SHA256.new(data=payload)
            sig_scheme: PKCS115_SigScheme = pkcs1_15.new(rsa_key)
            # TODO: fix the verification process
            sig_scheme.verify(sha256_hash, pkcs7.signature)
        except ValueError:
            result = False
            if isinstance(errors, list):
                errors.append("The digital signature is invalid")
        except Exception as e:
            if isinstance(errors, list):
                errors.append(exc_format(e, sys.exc_info()))

    return result


def crypto_validate_pdf(errors: list[str],
                        pdf_file: str | bytes, certs_file:  str | bytes = None) -> bool:
    """
    Validate the digital signature of a PDF file.

    If a *list* is provided in *errors*, the following inconsistencies are reported:
        - The file is not digitally signed
        - The digital signature is not valid
        - The certificate used has been revoked
        - The certificate used is not trusted
        - The signature block is not intact
        - A bad seed value found

    :param errors: incidental error messages
    :param pdf_file: a PDF file path, or the PDF file bytes
    :param certs_file: a path to a file containing a PEM/DER-encoded certificate chain, or the bytes thereof
    :return: True if the input data are consistent, False otherwise
    """
    # initialize the return variable
    result: bool = True

    # obtain the PDF data
    if isinstance(pdf_file, bytes):
        # argument is type 'bytes'
        wrapper: BinaryIO = BytesIO(pdf_file)
    else:  # isinstance(pdf_file, str)
        # argumento is a file path
        wrapper: BinaryIO = Path.open(Path(pdf_file), "rb")
    pdf_reader: PdfFileReader = PdfFileReader(wrapper)

    # obtain the validation context
    cert: Certificate | None = None
    if isinstance(certs_file, bytes):
        # argument is type 'bytes'
        cert = load_certs_from_pemder_data(certs_file)
    elif isinstance(certs_file, str):
        # argumento is a file path
        cert = load_certs_from_pemder(certs_file)
    validation_context = ValidationContext(cert)  # 'cert' might be None

    # obtain the list of digital signatures
    signatures: list[EmbeddedPdfSignature] = pdf_reader.embedded_signatures

    # were signatures retrieved ?
    if signatures:
        # yes, verify them
        for signature in signatures:
            error: str | None = None
            status: PdfSignatureStatus = validate_pdf_signature(signature, validation_context)
            if status.revoked:
                error = "The certificate used has been revoked"
            elif not status.intact:
                error = "The signature block is not intact"
            elif not status.trusted and cert:
                error = "The certificate used is not trusted"
            elif not status.seed_value_ok:
                error = "A bad seed value found"
            elif not status.valid:
                error = "The digital signature is not valid"

            # has an error been flagged ?
            if error:
                # yes, report it
                result = False
                errors.append(error)
    else:
        # no, report the problem
        result = False
        errors.append("The file is not digitally signed")

    return result
