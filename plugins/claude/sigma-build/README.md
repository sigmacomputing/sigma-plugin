# Sigma Build Plugin

Build a finished Sigma workbook from a conversation. This plugin connects
Claude to your Sigma organization and adds a skill that assembles dashboards
and data apps from pre-styled components, then checks its own work with
screenshots.

One plugin serves every Sigma region. After installing, set the connector's
Server URL to your region's URL (see below).

## Find your region

Open **Administration > Account > General Settings** in Sigma and read the
**Cloud** field under **Site**. Then find your row:

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

## Install

In Claude Code:

```
/plugin marketplace add sigmacomputing/sigma-plugin
/plugin install sigma-build@sigma-build
```

In Claude or Cowork, open **Customize > Plugins**, add the marketplace
`sigmacomputing/sigma-plugin`, and install **Sigma**. You can also upload its
`.claude.plugin` file from the
[releases](https://github.com/sigmacomputing/sigma-plugin/releases) page.

## Connect to your region

In Claude or Cowork, open **Settings > Plugins > Sigma > Connectors >
Connect**, set the **Server URL** to `https://<host>/mcp/v2` using the host
from your row above, and sign in with your Sigma account.

In Claude Code there is no connect form, so add the connector yourself with
your region's URL:

```
claude mcp add --transport http sigma https://<host>/mcp/v2
```

## What it connects to and sends

- One MCP connector, `sigma`, at `https://<host>/mcp/v2` for your region. You
  sign in with your Sigma account (OAuth), and it acts with your Sigma
  permissions.
- Claude sends it your requests and the workbook programs it writes. Sigma
  builds the workbooks in your organization and returns screenshots so Claude
  can check its work.
- The skill includes two Python helper scripts that Claude can run to check a
  program before sending it. They use only the Python standard library and
  make no network calls.
- The plugin sends nothing anywhere else.

## Try it

- "Build a dashboard of revenue by region and month from my sales data model."
- "Turn this table into an approval queue where reviewers mark each row
  approved or rejected."
- "Create a scorecard of our top KPIs with a date range filter."

## Support and privacy

- Support: <https://help.sigmacomputing.com/docs/sigma-support>
- Privacy policy: <https://www.sigmacomputing.com/legal/privacy-policy>
- License: Apache-2.0, see [LICENSE](LICENSE)
