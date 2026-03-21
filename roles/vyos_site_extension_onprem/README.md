# vyos_site_extension_onprem

Configures the on-prem VyOS site-extension layer that peers with the shared
Hetzner edge and advertises approved on-prem prefixes upstream.

This role also supports an optional consumer SNAT path for burst or DR
consumers when downstream on-prem subnets do not return cloud prefixes through
the site extension edge.
