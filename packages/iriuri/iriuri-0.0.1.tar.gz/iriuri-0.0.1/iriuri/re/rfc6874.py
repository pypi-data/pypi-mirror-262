# Generated using abnf-to-regex 1.1.2

dec_octet = '([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])'
h16 = '[0-9A-Fa-f]{1,4}'
ipv4address = f'{dec_octet}\\.{dec_octet}\\.{dec_octet}\\.{dec_octet}'
ls32 = f'({h16}:{h16}|{ipv4address})'
ipv6address = (
    f'(({h16}:){{6}}{ls32}|::({h16}:){{5}}{ls32}|({h16})?::({h16}:){{4}}'
    f'{ls32}|(({h16}:)?{h16})?::({h16}:){{3}}{ls32}|(({h16}:){{2}}{h16})?::'
    f'({h16}:){{2}}{ls32}|(({h16}:){{3}}{h16})?::{h16}:{ls32}|(({h16}:){{4}}'
    f'{h16})?::{ls32}|(({h16}:){{5}}{h16})?::{h16}|(({h16}:){{6}}{h16})?::)'
)
unreserved = '[a-zA-Z0-9\\-._~]'
pct_encoded = '%[0-9A-Fa-f][0-9A-Fa-f]'
zoneid = f'({unreserved}|{pct_encoded})+'
ipv6addrz = f'{ipv6address}%25{zoneid}'
sub_delims = "[!$&'()*+,;=]"
ipvfuture = f'[vV][0-9A-Fa-f]+\\.({unreserved}|{sub_delims}|:)+'
ip_literal = f'\\[({ipv6address}|{ipv6addrz}|{ipvfuture})\\]'
