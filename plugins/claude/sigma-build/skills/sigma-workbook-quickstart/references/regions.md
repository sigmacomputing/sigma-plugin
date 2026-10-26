# Sigma regions and MCP hosts

The `sigma` connector's URL depends on the region the user's Sigma organization
runs in. The user finds their region in Sigma under **Administration > Account >
General Settings**, in the **Cloud** field under **Site**. Users must set the
connector's Server URL to the URL for their own region, from the table below.

| Region | Host | Server URL |
|---|---|---|
| AWS US-West (Oregon) | `aws-api.sigmacomputing.com` | `https://aws-api.sigmacomputing.com/mcp/v2` |
| AWS US-East (N. Virginia) | `api.us-a.aws.sigmacomputing.com` | `https://api.us-a.aws.sigmacomputing.com/mcp/v2` |
| AWS Canada (Central) | `api.ca.aws.sigmacomputing.com` | `https://api.ca.aws.sigmacomputing.com/mcp/v2` |
| AWS EU (Frankfurt) | `api.eu.aws.sigmacomputing.com` | `https://api.eu.aws.sigmacomputing.com/mcp/v2` |
| AWS UK (eu-west-2) | `api.uk.aws.sigmacomputing.com` | `https://api.uk.aws.sigmacomputing.com/mcp/v2` |
| AWS Asia Pacific (Sydney) | `api.au.aws.sigmacomputing.com` | `https://api.au.aws.sigmacomputing.com/mcp/v2` |
| Azure US (Virginia) | `api.us.azure.sigmacomputing.com` | `https://api.us.azure.sigmacomputing.com/mcp/v2` |
| Azure EU (Netherlands) | `api.eu.azure.sigmacomputing.com` | `https://api.eu.azure.sigmacomputing.com/mcp/v2` |
| Azure Canada (Toronto) | `api.ca.azure.sigmacomputing.com` | `https://api.ca.azure.sigmacomputing.com/mcp/v2` |
| Azure UK (London) | `api.uk.azure.sigmacomputing.com` | `https://api.uk.azure.sigmacomputing.com/mcp/v2` |
| Azure Australia (New South Wales) | `api.au.azure.sigmacomputing.com` | `https://api.au.azure.sigmacomputing.com/mcp/v2` |
| GCP US-Central (Iowa) | `api.sigmacomputing.com` | `https://api.sigmacomputing.com/mcp/v2` |
| GCP Saudi Arabia (Dammam) | `api.sa.gcp.sigmacomputing.com` | `https://api.sa.gcp.sigmacomputing.com/mcp/v2` |

Hosts don't follow one pattern (AWS US-West is `aws-api.`, GCP US-Central is the
bare `api.`), so copy a host from the table rather than building one.
