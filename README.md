# Purpose of this script

Delete all of your capacity pools which you created for test purpose, in case you want to delete them all for saving money :D


# How to run the script

1. Clone it locally
    ```powershell
    git clone https://github.com/foe70/anf-auto-deleter.git
    ```
2. Change folder to **.\anf-auto-deleter\src**
3. Install any missing dependencies as needed
    ```bash
    pip install -r ./requirements.txt
    ```
4. Make sure you have the azureauth.json and its environment variable with the path to it defined (as previously described at [prerequisites](https://docs.microsoft.com/en-us/samples/azure-samples/netappfiles-python-sdk-sample/azure-netappfiles-sdk-sample-for-python/))
5. Edit configuration file **.\anf-auto-deleter\conf** and change the variables contents as appropriate.
6. Run the script
    ```powershell
    python ./deleter.py
    ```

# References

- [Azure NetAppFiles SDK Sample for Python](https://docs.microsoft.com/en-us/samples/azure-samples/netappfiles-python-sdk-sample/azure-netappfiles-sdk-sample-for-python/)
- [Azure Active Directory Python Authentication samples](https://github.com/AzureAD/microsoft-authentication-library-for-python/tree/dev/sample)
- [Resource limits for Azure NetApp Files](https://docs.microsoft.com/en-us/azure/azure-netapp-files/azure-netapp-files-resource-limits)
- [Azure Cloud Shell](https://docs.microsoft.com/en-us/azure/cloud-shell/quickstart)
- [Azure NetApp Files documentation](https://docs.microsoft.com/en-us/azure/azure-netapp-files/)
- [Download Azure SDKs](https://azure.microsoft.com/downloads/) 
 
