from enum import Enum, auto


class PType(Enum):
    """
    Enum type class that defines parameter types for cipher suite and certificate parameters.
    """
    protocol = auto()
    kex_algorithm = auto()
    cert_pub_key_algorithm = auto()
    cert_pub_key_length = auto()
    sym_enc_algorithm = auto()
    sym_enc_algorithm_key_length = auto()
    sym_enc_algorithm_block_mode = auto()
    sym_ecn_algorithm_block_mode_number = auto()
    hash_function = auto()
    cert_sign_algorithm = auto()
    cert_sign_algorithm_hash_function = auto()
    hmac_function = auto()
    cert_version = auto()
    cert_serial_number = auto()
    cert_not_valid_before = auto()
    cert_not_valid_after = auto()
    cert_subject = auto()
    cert_issuer = auto()
    cert_alternative_names = auto()

    @property
    def key_pair(self):
        """
        Defines the algorithm to which the algorithm length belongs to.

        :return: algorithm type
        """
        pairs = {
            self.sym_enc_algorithm_key_length: self.sym_enc_algorithm,
            self.cert_pub_key_length: self.cert_pub_key_algorithm,
            self.sym_ecn_algorithm_block_mode_number: self.sym_enc_algorithm_block_mode
        }
        return pairs[self]

    @property
    def string_alias(self):
        """
        Defines a string alias of a specific parameter

        :return: string
        """
        aliases = {
            self.protocol: 'Typ a verzia protokolu',
            self.kex_algorithm: 'Algoritmus výmenu kľúčov',
            self.cert_pub_key_algorithm: 'Algoritmus verejného kľúča',
            self.cert_pub_key_length: 'Veľkosť verejného kľúča',
            self.sym_enc_algorithm: 'Algoritmus symetrickej šifry',
            self.sym_enc_algorithm_key_length: 'Veľkosť kľúča symetrickej šifry',
            self.sym_enc_algorithm_block_mode: 'Blokový mód symetrickej šifry',
            self.sym_ecn_algorithm_block_mode_number: 'Dodatočná inoformácia k blokovému módu',
            self.hash_function: 'Hash funkcia',
            self.cert_sign_algorithm: 'Algoritmus podpisu certifikátu',
            self.cert_sign_algorithm_hash_function: 'Hash funkcia pre podpis certifikátu',
            self.hmac_function: 'Hmac funkcia',
        }
        return aliases[self]

    @property
    def is_cipher_suite(self):
        """
        Defines which parameters are parsable from a cipher suite

        :return: true if a parameter is parsable
        """
        cipher_suite_parameters = [
            self.kex_algorithm,
            self.sym_enc_algorithm,
            self.sym_enc_algorithm_key_length,
            self.sym_enc_algorithm_block_mode,
            self.sym_ecn_algorithm_block_mode_number,
            self.hash_function,
            self.hmac_function
        ]
        return self in cipher_suite_parameters

    @property
    def is_certificate(self):
        """
        Defines which parameters are parsable from a certificate.

        :return: true if a parameter is parsable
        """
        certificate_parameters = [
            self.cert_pub_key_algorithm,
            self.cert_pub_key_length,
            self.cert_sign_algorithm,
            self.cert_sign_algorithm_hash_function,
            self.cert_version,
            self.cert_serial_number,
            self.cert_not_valid_before,
            self.cert_not_valid_after,
            self.cert_subject,
            self.cert_issuer,
            self.cert_alternative_names
        ]
        return self in certificate_parameters

    @property
    def is_ratable(self):
        """
        Defines which parameter can be rated.

        :return: true if a parameter can be rated
        """
        rateable_parameters = [
            self.kex_algorithm,
            self.sym_enc_algorithm,
            self.sym_enc_algorithm_key_length,
            self.sym_enc_algorithm_block_mode,
            self.sym_ecn_algorithm_block_mode_number,
            self.hash_function,
            self.hmac_function,
            self.cert_pub_key_algorithm,
            self.cert_pub_key_length,
            self.cert_sign_algorithm,
            self.cert_sign_algorithm_hash_function,
        ]
        return self in rateable_parameters
