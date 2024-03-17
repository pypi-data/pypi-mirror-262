import ipaddress

RECORD_CLASSES = [
    'IN',
    'CH',
    'HS',
]

RECORD_TYPES = [
    'A',
    'NS',
    'MD',
    'MF',
    'CNAME',
    'SOA',
    'WKS',
    'PTR',
    'HINFO',
    'MINFO',
    'MX',
    'TXT',
    'RP',
    'AFSDB',
    'X25',
    'ISDN',
    'RT',
    'NSAP',
    'NSAP-PTR',
    'SIG',
    'KEY',
    'PX',
    'GPOS',
    'AAAA',
    'LOC',
    'NXT',
    'EID',
    'NIMLOC',
    'SRV',
    'ATMA',
    'NAPTR',
    'KX',
    'CERT',
    'A6',
    'DNAME',
    'SINK',
    'OPT',
    'APL',
    'DS',
    'SSHFP',
    'IPSECKEY',
    'RRSIG',
    'NSEC',
    'DNSKEY',
    'DHCID',
    'NSEC3',
    'NSEC3PARAM',
    'TLSA',
    'SMIMEA',
    'HIP',
    'NINFO',
    'RKEY',
    'TALINK',
    'CDS',
    'CDNSKEY',
    'OPENPGPKEY',
    'CSYNC',
    'ZONEMD',
    'VCB',
    'SVCB',
    'HTTPS',
    'SPF',
    'UINFO',
    'UID',
    'GID',
    'UNSPEC',
    'NID',
    'L32',
    'L64',
    'LP',
    'EUI48',
    'EUI64',
    'TKEY',
    'TSIG',
    'IXFR',
    'AXFR',
    'MAILB',
    'MAILA',
    '*',
    'URI',
    'CAA',
    'AVC',
    'DOA',
    'AMTRELAY',
    'TA',
    'DLV',
]


class ResourceRecord():
    def __init__(self):
        self.name = None
        self.ttl = None
        self.record_class = None
        self.record_type = None
        self.data = None

    def to_line(self):
        ttl_str = str(self.ttl) if self.ttl else ''
        record_class_str = str(self.record_class) if self.record_class else ''
        return f"{self.name} {ttl_str} {record_class_str} {self.record_type} {self.data}"


class Zone():
    def __init__(self, name: str, default_ttl: int):
        self.name = name
        self.default_ttl = default_ttl
        self.records = []

    def generate_origin(self):
        return f"$ORIGIN {self.name}"

    def generate_ttl(self):
        return f"$TTL {self.default_ttl}"


def get_rev_zone_name(network) -> str:
    """
    Cuts off the first few blocks of a reverse pointer for a network address
    to create a suitable reverse zone name for a certain prefix length.
    """
    if type(network) is ipaddress.IPv4Network:
        divisor = 8
        address_len = 32
    elif type(network) is ipaddress.IPv6Network:
        divisor = 4
        address_len = 128
    else:
        raise Exception(f"Invalid network type: {network}")

    blocks_to_cut = int((address_len - network.prefixlen) / divisor)
    return '.'.join(network.network_address.reverse_pointer.split('.')[blocks_to_cut:None]) + '.'


def get_rev_ptr_name(address, prefix_len) -> str:
    """
    Cuts off the last few blocks of a reverse pointer for an address
    to create a suitable reverse pointer name for a certain prefix length.
    """
    if type(address) is ipaddress.IPv4Address:
        divisor = 8
        address_len = 32
    elif type(address) is ipaddress.IPv6Address:
        divisor = 4
        address_len = 128
    else:
        raise Exception(f"Invalid address type: {address}")

    blocks_to_cut = int(((address_len - prefix_len) / divisor))
    return '.'.join(address.reverse_pointer.split('.')[None:blocks_to_cut])
