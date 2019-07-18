import deepsecurity as api
from deepsecurity.rest import ApiException as api_exception


def get_anti_malware_status_for_computers(api, configuration, api_version, api_exception):
    """Obtains agent and appliance status for the Anti-Malware module of all computers.
    Returns the status information of all computers that have the Anti-Malware module turned off,
    or where the status of the module is not active as comma-separated values.
    :param api: The Deep Security API modules.
    :param configuration: Configuration object to pass to the api client.
    :param api_version: The version of the API to use.
    :param api_exception: The Deep Security API exception module.
    :return: A string that can be saved as a CSV file.
    """
    # Add column titles to comma-separated values string
    csv = "Host Name,Module State,Agent or Appliance,Status,Status Message\r\n"
    # Include Anti-Malware information in the returned Computer objects
    expand = api.Expand(api.Expand.anti_malware)
    try:
        computers_api = api.ComputersApi(api.ApiClient(configuration))
        computers = computers_api.list_computers(api_version, expand=expand.list(), overrides=False)
        print('1')
        # Get the list of computers and iterate over it
        for computer in computers.computers:
            # Module information to add to the CSV string
            module_info = []
            # Check that the computer has a an agent or appliance status
            if computer.anti_malware.module_status:
                agent_status = computer.anti_malware.module_status.agent_status
                appliance_status = computer.anti_malware.module_status.appliance_status
            else:
                agent_status = None
                appliance_status = None
            # Agents that are not active for the module
            if agent_status and agent_status != "inactive":
                # Host name
                module_info.append(computer.host_name)
                # Module state
                module_info.append(computer.anti_malware.state)
                # Agent status and status message
                module_info.append("Agent")
                module_info.append(agent_status)
                module_info.append(computer.anti_malware.module_status.agent_status_message)
                # Add the module info to the CSV string
                csv_line = ""
                for num, item in enumerate(module_info):
                    csv_line += item
                    if num != (len(module_info) - 1):
                        csv_line += ","
                    else:
                        csv_line += "\r\n"
                csv += csv_line
            # Appliances that are not active for the module
            if appliance_status and appliance_status != "inactive":
                # Host name
                module_info.append(computer.host_name)
                # Module state
                module_info.append(computer.anti_malware.state)
                # Appliance status and status message
                module_info.append("Appliance")
                module_info.append(appliance_status)
                module_info.append(computer.anti_malware.module_status.appliance_status_message)
                # Add the module info to the CSV string
                csv_line = ""
                for num, item in enumerate(module_info):
                    csv_line += item
                    if num != (len(module_info) - 1):
                        csv_line += ","
                    else:
                        csv_line += "\r\n"
                csv += csv_line
        return csv
    except api_exception as e:
        return "Exception: " + str(e)


if __name__ == '__main__':
    # Add Deep Security Manager host information to the api client configuration
    configuration = api.Configuration()
    configuration.host = 'https://app.deepsecurity.trendmicro.com/api'
    # Authentication
    configuration.api_key['api-secret-key'] = '#CHANGE_TO_TRENDMICRO_API'
    # Version
    api_version = 'v1'
    # print(get_policies_list(api, configuration, api_version, api_exception))
    print(get_anti_malware_status_for_computers(api, configuration, api_version, api_exception))