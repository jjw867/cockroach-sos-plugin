from sos.report.plugins import Plugin, IndependentPlugin

class Cockroach(Plugin, IndependentPlugin):

    short_desc = 'Cockroach RDBMS'

    plugin_name = "cockroach"
    profiles = ('services',)

    packages = ('cockroach')

    def setup(self):
        env_vars = {}
        config_file = "/etc/cockroach/cockroach.conf"

# Defaults in case there is no configuration file

        cockroach_log_config = "/etc/cockroach/cockroach-logs.yaml"
        cockroach_storage = "/var/lib/cockroach"
        cockroach_log = "/var/log/cockroach"
        cockroach_ui = "localhost:8080"

        try:
            with open(config_file) as f:
                for line in f:
                    if line.startswith('#') or not line.strip():
                        continue
                    key, value = line.strip().split('=', 1)
                    # os.environ[key] = value  # Load to local environ
                    # env_vars[key] = value # Save to a dict, initialized env_vars = {}
                    # env_vars.append({'name': key, 'value': value}) # Save to a list
                    item = {key: value}
                    env_vars.update(item)
                cockroach_log_config = env_vars.get("COCKROACH_LOG_CONFIG")
                cockroach_storage = env_vars.get("COCKROACH_STORAGE1")
                cockroach_log = env_vars.get("COCKROACH_LOG")
                cockroach_ui = env_vars.get("COCKROACH_UI_PORT")

        except FileNotFoundError:
            print('Cockroach configuration file not present')

        self.add_copy_spec([
            cockroach_log + "/*.log",
            config_file,
            cockroach_log_config
            ])

        self.add_cmd_output("cockroach version")
        self.add_cmd_output("du -sh " + cockroach_storage)
        self.add_cmd_output("curl -k https://" + cockroach_ui + "/_status/vars")
        self.add_cmd_output("curl -k https://" + cockroach_ui + "/api/v2/rules")
        self.add_cmd_output("curl -k https://" + cockroach_ui + "/health")
        self.add_cmd_output("systemctl show cockroach")
        self.add_cmd_output("systemctl status cockroach")
