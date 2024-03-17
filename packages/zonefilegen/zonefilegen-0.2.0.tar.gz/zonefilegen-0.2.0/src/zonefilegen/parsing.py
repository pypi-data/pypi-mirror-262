import ipaddress
import hashlib
import logging
import pathlib
from typing import List, Tuple

import toml
import zonefilegen
import zonefilegen.core
import zonefilegen.generation


def parse_toml_file(input_file_path: pathlib.Path) -> Tuple[zonefilegen.core.Zone, List[zonefilegen.core.Zone], dict, str]:
    """
    Parses a toml file with DNS records and generates one forward zone and one
    or more reverse zones. Additionally, a dict with info about the SOA record
    and a digest of the source file is returned for embedding in the generated
    files, to detect when serial number needs to be updated.
    """
    with open(input_file_path, 'r') as f:
        data = toml.load(f)
        f.seek(0)
        file_digest = hashlib.sha1(f.read().encode()).hexdigest()

    fwd_zone = zonefilegen.generation.build_fwd_zone(data['origin'], data['rrset'], data['default_ttl'])

    ipv4_ptr_candidates = []
    ipv6_ptr_candidates = []

    rev_ns_records = []
    for rec in fwd_zone.records:
        if rec.record_type == 'A':
            ipv4_ptr_candidates.append((rec.name, rec.ttl, ipaddress.IPv4Address(rec.data)))
        elif rec.record_type == 'AAAA':
            ipv6_ptr_candidates.append((rec.name, rec.ttl, ipaddress.IPv6Address(rec.data)))
        elif rec.record_type == 'NS' and rec.name == fwd_zone.name:
            rev_ns_records.append((rec.name, rec.ttl, rec.data))

    reverse_zones = []
    for network_str in data['networks']:
        network = ipaddress.ip_network(network_str, strict=True)
        if type(network) is ipaddress.IPv4Network:
            if network.prefixlen % 8 != 0:
                logging.fatal("IPv4 network prefix must be divisible by 8")
                exit(1)
            reverse_zones.append(zonefilegen.generation.build_reverse_zone(network,
                                                                           ipv4_ptr_candidates,
                                                                           data['default_ttl'],
                                                                           rev_ns_records))

        elif type(network) is ipaddress.IPv6Network:
            if network.prefixlen % 4 != 0:
                logging.fatal("IPv6 network prefix must be divisible by 4")
                exit(1)
            reverse_zones.append(zonefilegen.generation.build_reverse_zone(network,
                                                                           ipv6_ptr_candidates,
                                                                           data['default_ttl'],
                                                                           rev_ns_records))

    return (fwd_zone, reverse_zones, data['soa'], file_digest)
