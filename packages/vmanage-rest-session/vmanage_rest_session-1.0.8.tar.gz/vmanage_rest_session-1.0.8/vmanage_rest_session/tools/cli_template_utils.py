def filter_cli_config(config):
	config_filter_list = [
		"no daemon-restart",
		"no daemon-reboot",
		"no reboot-on-failure",
		"admin-tech-on-failure",
		"no vrrp-advt-with-phymac"
	]
	config_lines = config.splitlines()
	filter_lines = []
	for line in config_lines:
		if line.strip() not in config_filter_list:
			filter_lines.append(line)

	return "\n".join(filter_lines)
