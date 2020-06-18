import os
import sample_utils
import resource_uri_utils
import azure.mgmt.netapp.models
from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.netapp import AzureNetAppFilesManagementClient
from azure.mgmt.netapp.models import NetAppAccount, \
    CapacityPool, \
    Volume
from azure.mgmt.resource import ResourceManagementClient
from msrestazure.azure_exceptions import CloudError
from sample_utils import console_output, print_header, resource_exists
import configparser

RESOURCE_GROUP_NAME = 'ANF-RG'
acname = []
poid = []
void = []
conf= configparser.ConfigParser()

def readConf():
    root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    conf.read(root_path + '/conf/config.conf')  # 文件路径
    name = conf.get("resource_group", "name")  # 获取指定section 的option值
    console_output("Resource group: {} ".format(name))
    return name

# get anf account name list

def List_ANF_account(anf_client, rg_id):
    result = anf_client.accounts.list(resource_uri_utils.get_resource_name(rg_id))
    global acname
    for re in result:
        acname.append(re.name)
    return acname    

# get pool id list 

def List_ANF_pool_id(anf_client,resource_group_name,account_name_list):
    global poid
    for account_name in account_name_list:
        result = anf_client.pools.list(resource_group_name,account_name)
        for re in result:
            poid.append(re.id)
    return poid

# get volume id list

def List_ANF_vol_id(anf_client,resource_group_name,pool_id_list):
    global void
    for pool_id in pool_id_list:
        result = anf_client.volumes.list(resource_group_name,pool_id.split('/')[8],pool_id.split('/')[10])
        for re in result:
            void.append(re.id)
    return void

def run_deleter():
    
    conf= configparser.ConfigParser()
    RESOURCE_GROUP_NAME = readConf()
    
    # get client and credential

    credentials, subscription_id = sample_utils.get_credentials()
    anf_client = AzureNetAppFilesManagementClient(
        credentials, subscription_id)

    RG_ID='/subscriptions/{}/resourceGroups/{}'.format(subscription_id, RESOURCE_GROUP_NAME)
    ANF_ACCOUNT_NAME_LIST = List_ANF_account(anf_client,RG_ID)
    POOL_ID_LIST = List_ANF_pool_id(anf_client,RESOURCE_GROUP_NAME,ANF_ACCOUNT_NAME_LIST)
    VOL_ID_LIST = List_ANF_vol_id(anf_client,RESOURCE_GROUP_NAME,POOL_ID_LIST)

    if ANF_ACCOUNT_NAME_LIST:
        if POOL_ID_LIST:
            if VOL_ID_LIST:
                # Clearning up volume
                try:
                    for pool_id in POOL_ID_LIST:
                        for volume_id in VOL_ID_LIST:
                            if pool_id.split('/')[10] == volume_id.split('/')[10]:
                                console_output("\t\tDeleting {}".format(resource_uri_utils.get_anf_volume(volume_id)))
                                anf_client.volumes.delete(RESOURCE_GROUP_NAME,
                                            pool_id.split('/')[8],
                                            resource_uri_utils.get_anf_capacity_pool(
                                            pool_id),
                                            resource_uri_utils.get_anf_volume(
                                            volume_id)
                                            ).wait()
                                sample_utils.wait_for_no_anf_resource(anf_client, volume_id)
                                console_output('\t\tDeleted Volume: {}'.format(volume_id))

                except CloudError as ex:
                    console_output(
                        'An error ocurred. Error details: {}'.format(ex.message))
                    raise

                # Cleaning up Capacity Pool
                for pool_id in POOL_ID_LIST:
                    console_output("\tDeleting Capacity Pool {} ...".format(
                        resource_uri_utils.get_anf_capacity_pool(pool_id)))
                    try:
                        anf_client.pools.delete(RESOURCE_GROUP_NAME,pool_id.split('/')[8],resource_uri_utils.get_anf_capacity_pool(pool_id)).wait()

                        sample_utils.wait_for_no_anf_resource(anf_client, pool_id)

                        console_output(
                            '\t\tDeleted Capacity Pool: {}'.format(pool_id))
                    except CloudError as ex:
                        console_output(
                            'An error ocurred. Error details: {}'.format(ex.message))
                        raise
            else:
                console_output("No volume detected!")
        else:
            console_output("No capacity pool detected!")
    else:
        console_output("No ANF account detected in RG {}".format(RESOURCE_GROUP_NAME))
        

if __name__ == "__main__":

    run_deleter()



