#!/usr/bin/env python
import re
import subprocess
import boto3

#aws ssm get-parameters --names #{FOX_ENV}.#{FOX_BU}.splunk_web_password --with-decryption --region us-west-2 | jq -r '.Parameters[0].Value

def getParameter(parameter):
    """
    Reads a secure parameter from AWS SSM service and fetch the Passwd.
    """
    ssm = boto3.client('ssm',
        region_name='us-west-2'
    )
    response = ssm.get_parameters(
        Names=[
            parameter,
        ],
        WithDecryption=True
    )
    credentials = response['Parameters'][0]['Value']
    return credentials

def get_bu():
    '''
    gets bu of current node
    '''
    bashCommand = "source /etc/ec2-tags; echo -n $BUSINESSUNIT"
    bu = subprocess.check_output(bashCommand, shell=True)
    return bu


def all_bus():
    '''
    queries consul for all bus. returns a list of bus
    '''
    bashCommand = "curl --silent localhost:8500/v1/catalog/nodes | jq --raw-output '.[].Meta.businessunit | select(. != null)' | sort | uniq"
    bus = subprocess.check_output(bashCommand, shell=True).split("\n")
    bus = [x for x in bus if x]
    return bus


def get_splunk_nodes():
    '''
    This function will retrieve all nodes associated with
    Runs splun klist serach-servers and returns a list of ips
    '''
    ip_pattern = re.compile('(\d+\.){3}\d+:\d+')
    bashCommand = "/opt/splunk/bin/splunk list search-server -auth admin:splunk"
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    output = output.split(' ')
    output = [x.replace(
               '"', '') for x in output if re.match('"(\d+\.){3}\d+:\d+"', x)]

    return output


def get_consul_nodes():
    '''
    Runs consul service lookup comnads to get the nodes that are online that
    the DMC needs to monitor, returns a list of ips. The roles array is used to
    traverse over each tag that the nodes used to register with consul. The
    output list is the same format as the list returned in get_splunk_nodes()
    '''
    output = []
    roles = ['searchhead', 'deployer', 'clustermaster',
             'deployment-server', 'essearchhead', 'hec']
    if get_bu() == 'federated':
        bus = all_bus()
    else:
        bus = [get_bu()]
    for bu in bus:
        for role in roles:
            bashCommand = "consul catalog nodes -node-meta=role=" + role + " -node-meta=businessunit=" + bu
            process = subprocess.Popen(
                      bashCommand.split(), stdout=subprocess.PIPE)
            tmp_output, error = process.communicate()
            tmp_output = tmp_output.split(' ')
            output += tmp_output
    output = [x.replace(
              '"', '') for x in output if re.match('(\d+\.){3}\d+', x)]
    output = [ip + ":8089" for ip in output]
    return output


def diff():
    '''
    diff and invertdiff are functions that determine the difference of two
    lists
    '''
    splunk_ip_list = get_splunk_nodes()
    consul_ip_list = get_consul_nodes()
    diff_list = list(set(consul_ip_list) - set(splunk_ip_list))
    return diff_list


def invertdiff():
    splunk_ip_list = get_splunk_nodes()
    consul_ip_list = get_consul_nodes()
    diff_list = list(set(splunk_ip_list) - set(consul_ip_list))
    return diff_list


def add_node():
    '''
    Adds node to splunk using the add seatch-server command. This function takes the difference
    between the two lists built in get_splunk_nodes and get_consul_nodes
    '''
    iplist = diff()
    for ip in iplist:
        slackPasswd = getParameter(parameter)
        bashCommand = "/opt/splunk/bin/splunk add search-server " + ip + " -auth admin:splunk -remoteUsername admin -remotePassword set(slackPasswd)"
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        tmp_output, error = process.communicate()


def remove_node():
    '''
    Similar to add node, uses diff to get the diff and remove downed DMC
    members
    '''
    ipList = invertdiff()
    slackPasswd = getParameter(parameter)
    for ip in ipList:
        bashCommand = "/opt/splunk/bin/splunk remove search-server " + ip + " -auth admin:splunk -remoteUsername admin -remotePassword set(slackPasswd)"
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        tmp_output, error = process.communicate


# Main program
def main():
    add_node()
    remove_node()


if __name__ == '__main__':
    main()
