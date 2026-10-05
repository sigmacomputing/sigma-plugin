# Sigma plugin for Claude

Build a finished Sigma workbook from a conversation. The plugin gives Claude a
connector to your Sigma organization and a skill that assembles dashboards and
data apps from pre-styled components, then checks its own work with
screenshots.

## Install

Sigma hosts each organization in one region, so install the plugin that
matches yours. To find it, open **Administration > Account > General Settings**
in Sigma and read the **Cloud** field under **Site**.

| Region | Plugin |
|---|---|
| AWS US-West (Oregon) | `sigma-build-aws-us-west-2-production` |
| AWS US-East (N. Virginia) | `sigma-build-aws-us-east-1-production` |
| AWS Canada (Central) | `sigma-build-aws-ca-central-1-production` |
| AWS EU (Frankfurt) | `sigma-build-aws-eu-central-1-production` |
| AWS UK (eu-west-2) | `sigma-build-aws-eu-west-2-production` |
| AWS Asia Pacific (Sydney) | `sigma-build-aws-ap-southeast-2-production` |
| Azure US (Virginia) | `sigma-build-azure-eastus2-production` |
| Azure EU (Netherlands) | `sigma-build-azure-westeurope-production` |
| Azure Canada (Toronto) | `sigma-build-azure-canadacentral-production` |
| Azure UK (London) | `sigma-build-azure-uksouth-production` |
| Azure Australia (New South Wales) | `sigma-build-azure-australiaeast-production` |
| GCP US-Central (Iowa) | `sigma-build-gcp-us-central-1-production` |
| GCP Saudi Arabia (Dammam) | `sigma-build-gcp-me-central2-production` |

In Claude Code:

```
/plugin marketplace add sigmacomputing/sigma-plugin
/plugin install <plugin>@sigma-build
```

In Claude or Cowork, open **Customize > Plugins**, add the marketplace
`sigmacomputing/sigma-plugin`, and install the plugin for your region. You can
also upload a `.plugin` file from the [releases](../../releases) page.

After installing, connect the `sigma_*` connector when Claude prompts you and
sign in with your Sigma account.

Each plugin's folder has a README that says what it connects to and sends.

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
