# Sigma plugin: Azure EU (Netherlands)

Build a finished Sigma workbook from a conversation. This plugin connects
Claude to your Sigma organization in Azure EU (Netherlands) and adds a skill
that assembles dashboards and data apps from pre-styled components, then
checks its own work with screenshots.

Install the plugin for the region your Sigma organization runs in. To find it,
open **Administration > Account > General Settings** in Sigma and read the
**Cloud** field under **Site**.

## Install

In Claude Code:

```
/plugin marketplace add sigmacomputing/sigma-plugin
/plugin install sigma-build-azure-westeurope-production@sigma-build
```

In Claude or Cowork, open **Customize > Plugins**, add the marketplace
`sigmacomputing/sigma-plugin`, and install this plugin. You can also upload
its `.claude.plugin` file from the
[releases](https://github.com/sigmacomputing/sigma-plugin/releases) page.

After installing, sign in to the `sigma` connector with your Sigma account
when Claude prompts you.

## What it connects to and sends

- One MCP connector, `sigma`, at
  `https://api.eu.azure.sigmacomputing.com/mcp/v2`. You sign in with your
  Sigma account (OAuth), and it acts with your Sigma permissions.
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
