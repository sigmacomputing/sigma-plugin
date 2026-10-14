# Sigma plugin: AWS US-West (Oregon)

Build a finished Sigma workbook from a conversation. This plugin connects
Cursor to your Sigma organization in AWS US-West (Oregon) and adds a skill
that assembles dashboards and data apps from pre-styled components, then
checks its own work with screenshots.

Install the plugin for the region your Sigma organization runs in. To find it,
open **Administration > Account > General Settings** in Sigma and read the
**Cloud** field under **Site**.

## Install

From the Cursor dashboard, open **Plugins**, import the
`sigmacomputing/sigma-plugin` repository as a team marketplace, and install
this plugin.

To try it in one project instead, download its `.cursor.zip` file from the
[releases](https://github.com/sigmacomputing/sigma-plugin/releases) page and
unzip it. Copy its `skills/` into `.cursor/skills/` and its `mcp.json` entries
into `.cursor/mcp.json`.

After installing, sign in to the `sigma` connector with your Sigma account
when Cursor prompts you.

## What it connects to and sends

- One MCP connector, `sigma`, at `https://aws-api.sigmacomputing.com/mcp/v2`.
  You sign in with your Sigma account (OAuth), and it acts with your Sigma
  permissions.
- Cursor sends it your requests and the workbook programs it writes. Sigma
  builds the workbooks in your organization and returns screenshots so Cursor
  can check its work.
- The skill includes two Python helper scripts that Cursor can run to check a
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
