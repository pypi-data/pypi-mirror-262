# Generated using abnf-to-regex 1.1.2

alphanum = '[a-zA-Z0-9]'
ldh = f'({alphanum}|-)'
nid = f'{alphanum}({ldh}){{30}}{alphanum}'
unreserved = '[a-zA-Z0-9\\-._~]'
pct_encoded = '%[0-9A-Fa-f][0-9A-Fa-f]'
sub_delims = "[!$&'()*+,;=]"
pchar = f'({unreserved}|{pct_encoded}|{sub_delims}|[:@])'
nss = f'{pchar}({pchar}|/)*'
assigned_name = f'urn:{nid}:{nss}'
fragment = f'({pchar}|[/?])*'
f_component = f'{fragment}'
r_component = f'{pchar}({pchar}|[/?])*'
q_component = f'{pchar}({pchar}|[/?])*'
rq_components = f'(\\?\\+{r_component})?(\\?={q_component})?'
namestring = f'{assigned_name}({rq_components})?(\\#{f_component})?'
