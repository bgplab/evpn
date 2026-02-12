from box import Box

def cleanup(topology: Box) -> None:
  for n_data in topology.nodes.values():
    if 'vrfs' not in n_data:
      continue
    for vdata in n_data.vrfs.values():
      for rp in ['bgp']:
        vdata.pop(rp,None)
