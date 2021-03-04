from scan_web_server.utils import *
from .Parameters import Parameters
from .PType import PType


class Certificate(Parameters):

    def __init__(self, certificate):
        # Create a dictionary for certificate parameters with PType keys
        super().__init__()
        self.parameters = {enum: {} for enum in PType if enum.is_certificate and enum.is_ratable}
        self.non_parameters = {enum: [] for enum in PType if enum.is_certificate and not enum.is_ratable}
        self.certificate = certificate

    def parse_certificate(self):
        """
        Parse information from a certificate and into a dictionary.
        """
        self.parameters[PType.cert_pub_key_algorithm][pub_key_alg_from_cert(self.certificate.public_key())] = 0
        self.parameters[PType.cert_pub_key_length][str(self.certificate.public_key().key_size)] = 0

        hash_function = str(self.certificate.signature_hash_algorithm.name).upper()
        self.parameters[PType.cert_sign_algorithm_hash_function][hash_function] = 0

        sign_algorithm = get_sig_alg_from_oid(self.certificate.signature_algorithm_oid)
        self.parameters[PType.cert_sign_algorithm][sign_algorithm] = 0

        self.non_parameters[PType.cert_version].append(str(self.certificate.version.value))
        self.non_parameters[PType.cert_serial_number].append(str(self.certificate.serial_number))
        self.non_parameters[PType.cert_not_valid_before].append(str(self.certificate.not_valid_before.date()))
        self.non_parameters[PType.cert_not_valid_after].append(str(self.certificate.not_valid_after.date()))
        self.non_parameters[PType.cert_alternative_names] = self.parse_alternative_names()
        self.non_parameters[PType.cert_subject] = self.parse_name(self.certificate.subject)
        self.non_parameters[PType.cert_issuer] = self.parse_name(self.certificate.issuer)

    def parse_alternative_names(self):
        """
        Parse the alternative names from the certificate extensions.

        :return: list of alternative names
        """
        try:
            extension = self.certificate.extensions.get_extension_for_class(x509.SubjectAlternativeName)
        except x509.extensions.ExtensionNotFound:
            return []
        return extension.value.get_values_for_type(x509.DNSName)

    @staticmethod
    def parse_name(name):
        """
        Parse subject and issuer information and return as list.

        :param name: objects that is parsed
        :return:
        """
        name_info = []
        for attribute in name:
            name_info.append(f'{attribute.oid._name}={attribute.value}')
        return name_info[:-1]

    def rate_certificate(self):
        """
        Rate all valid certificate parameters.
        """
        rateable_parameters = list(self.parameters.keys())
        key_types = [PType.cert_pub_key_length]
        self.rate_parameters(rateable_parameters, key_types)

    def rate(self):
        self.parse_certificate()
        self.rate_certificate()
        return self.rating
