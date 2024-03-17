import zonefilegen.parsing


def test_simple_parsing():
    input_file = "docs/sample.toml"

    (fwd_zone, reverse_zones, soa_dict, input_digest) = zonefilegen.parsing.parse_toml_file(input_file)
    assert fwd_zone.name == "example.com."
    assert fwd_zone.default_ttl == 3600

    found_mail1 = False
    for rec in fwd_zone.records:
        if rec.name == 'mail1.example.com.':
            found_mail1 = True
            assert rec.record_class == 'IN'
            assert rec.record_type == 'A'
            assert rec.data == '198.51.100.3'
            assert rec.ttl == 300

    assert found_mail1
