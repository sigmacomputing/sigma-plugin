# Sigma plugins for AI assistants

Build a finished Sigma workbook from a conversation. Each plugin gives your AI
assistant a connector to your Sigma organization and a skill that assembles
dashboards and data apps from pre-styled components, then checks its own work
with screenshots. The plugins are built for Claude (Claude Code, Claude
and Cowork), Codex and ChatGPT, Cursor, and Cortex Code.

## Pick your region

Sigma hosts each organization in one region. To find yours, open
**Administration > Account > General Settings** in Sigma and read the **Cloud**
field under **Site**.

Claude has one plugin, `sigma-build`, for every region: you set your region's
host on its connector after installing (see the Claude install sections below).
Codex, Cursor and Cortex Code have one plugin per region, so install the one
that matches yours. Those plugins have the same name on each of the three
assistants.

| Region | Claude host | Codex, Cursor and Cortex Code plugin |
|---|---|---|
| AWS US-West (Oregon) | `aws-api.sigmacomputing.com` | `sigma-build-aws-us-west-2-production` |
| AWS US-East (N. Virginia) | `api.us-a.aws.sigmacomputing.com` | `sigma-build-aws-us-east-1-production` |
| AWS Canada (Central) | `api.ca.aws.sigmacomputing.com` | `sigma-build-aws-ca-central-1-production` |
| AWS EU (Frankfurt) | `api.eu.aws.sigmacomputing.com` | `sigma-build-aws-eu-central-1-production` |
| AWS UK (eu-west-2) | `api.uk.aws.sigmacomputing.com` | `sigma-build-aws-eu-west-2-production` |
| AWS Asia Pacific (Sydney) | `api.au.aws.sigmacomputing.com` | `sigma-build-aws-ap-southeast-2-production` |
| Azure US (Virginia) | `api.us.azure.sigmacomputing.com` | `sigma-build-azure-eastus2-production` |
| Azure EU (Netherlands) | `api.eu.azure.sigmacomputing.com` | `sigma-build-azure-westeurope-production` |
| Azure Canada (Toronto) | `api.ca.azure.sigmacomputing.com` | `sigma-build-azure-canadacentral-production` |
| Azure UK (London) | `api.uk.azure.sigmacomputing.com` | `sigma-build-azure-uksouth-production` |
| Azure Australia (New South Wales) | `api.au.azure.sigmacomputing.com` | `sigma-build-azure-australiaeast-production` |
| GCP US-Central (Iowa) | `api.sigmacomputing.com` | `sigma-build-gcp-us-central-1-production` |
| GCP Saudi Arabia (Dammam) | `api.sa.gcp.sigmacomputing.com` | `sigma-build-gcp-me-central2-production` |

After installing, connect the `sigma` connector when your assistant prompts
you and sign in with your Sigma account. Each plugin's folder has a README
that says what it connects to and sends.

Every [release](../../releases) attaches the Claude archive, `sigma-build-<version>.claude.plugin`,
and one archive per region for each of the other assistants, named
`<plugin>-<version>` plus `.codex.zip`, `.cursor.zip` or `.coco.zip`.

## Install in Claude Code

```
/plugin marketplace add sigmacomputing/sigma-plugin
/plugin install sigma-build@sigma-build
```

Set the connector's Server URL to your region's URL; see
[Connect to your region](plugins/claude/sigma-build/README.md#connect-to-your-region).

## Install in Claude or Cowork

Open **Customize > Plugins**, add the marketplace
`sigmacomputing/sigma-plugin`, and install **Sigma**. Then open **Settings > Plugins > Sigma >
Connectors > Connect** and set the **Server URL** to `https://<host>/mcp/v2`
with your region's host from the table above. You can also upload the
`.claude.plugin` file from the [releases](../../releases) page.

## Install in Codex or ChatGPT

Add this repository as a marketplace in the Codex CLI or the ChatGPT desktop
app:

```
codex plugin marketplace add https://github.com/sigmacomputing/sigma-plugin.git
```

Restart the ChatGPT desktop app, open **Plugins** from a Codex session, choose
the `sigma-build` marketplace, and install the plugin for your region. The
Codex IDE extension doesn't support plugins yet.

## Install in Cursor

From the Cursor dashboard, open **Plugins**, import this repository as a team
marketplace, and install the plugin for your region.

To try a plugin in one project instead, download its `.cursor.zip` file from
the [releases](../../releases) page and unzip it. Copy its `skills/` into
`.cursor/skills/` and its `mcp.json` entries into `.cursor/mcp.json`.

## Install in Cortex Code

Install the plugin for your region straight from this repository:

```
cortex plugin install sigmacomputing/sigma-plugin/plugins/coco/<plugin>
```

For example, `cortex plugin install sigmacomputing/sigma-plugin/plugins/coco/sigma-build-aws-us-west-2-production`.

If you need a file instead, download the plugin's `.coco.zip` file from the
[releases](../../releases) page and unzip it. In Cortex Code Desktop, open
**Plugins > Add Local Plugin** and pick the folder that holds
`.cortex-plugin/plugin.json`.

## Try it

- "Build a dashboard of revenue by region and month from my sales data model."
- "Turn this table into an approval queue where reviewers mark each row approved or rejected."
- "Create a scorecard of our top KPIs with a date range filter."

## Support and privacy

- Support: <https://help.sigmacomputing.com/docs/sigma-support>
- Privacy policy: <https://www.sigmacomputing.com/legal/privacy-policy>
- Security: report vulnerabilities as described in [SECURITY.md](SECURITY.md),
  not in issues or pull requests.
- License: Apache-2.0, see [LICENSE](LICENSE)

## Contributing

This repository is published from Sigma's internal source on each release, so
it doesn't accept pull requests. For questions or problems, contact
[Sigma support](https://help.sigmacomputing.com/docs/sigma-support).
