from netsim.augment import devices
from box import Box

def pre_transform(topology: Box) -> None:
  f_list = []

  for node,n_data in topology.nodes.items():
    if 'evpn' not in n_data.get('module',[]):
      continue

    features = devices.get_device_features(n_data,topology.defaults)
    if 'evpn' in features:
      continue

    f_list += [ f'{node}({n_data.device})' ]
    n_data.module = [ m for m in n_data.module if m not in ('evpn','vxlan') ]
    n_data.pop('evpn',None)
    n_data.pop('vxlan',None)

  if not f_list:
    return

  if 'message' not in topology:
    topology.message = ''

  topology.message += f'''
netlab cannot configure EVPN on {", ".join(f_list)}.
You'll have to configure VXLAN and EVPN manually.
'''
