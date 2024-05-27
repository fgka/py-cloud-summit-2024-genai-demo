# py-cloud-summit-2024-genai-demo
Python demo for GenAI on Vertex - Cloud Summit 2024

This code is based on the demo application referenced in [Optional: Create a sample application](https://cloud.google.com/code/docs/vscode/write-code-gemini#optional_create_a_sample_application):
1. Command palette: `Cloud Code: New Application`
2. `Kubernetes application`
3. `Python (Flask): Guestbook`: [Guestbook with Cloud Code](https://github.com/GoogleCloudPlatform/cloud-code-samples/tree/v1/python/python-guestbook)

## Enabling Gemini Code

Go to the [Gemini Admin console](https://console.cloud.google.com/gemini-admin) and follow instructions in [Set up Gemini Code Assist for a project](https://cloud.google.com/gemini/docs/discover/set-up-gemini).

Check out [Try Gemini in the Google Cloud console](https://cloud.google.com/gemini/docs/quickstart) to get started.


## Visual Studo Code users

Please follow the instructions in [Code with Gemini Code Assist](https://cloud.google.com/code/docs/vscode/write-code-gemini).


## Remote `minikube`

### **MINIKUBE HOST**

#### Preparation

Check which is the IP address of the remote host and set it:

```bash
MINIKUBE_HOST_IP="<Host IP address that is running minikube>"
```

Example:

```bash
MINIKUBE_HOST_IP="192.168.1.101"
```

#### Start `minikube` in the remote host

```bash
minikube start --vm-driver  docker --memory 8112 --cpus 8 --apiserver-ips=${MINIKUBE_HOST_IP}
```

#### Collect the `minikube` internal IP address

```bash
kubectl config view -o jsonpath='{.clusters[?(@.name == "minikube")].cluster.server}'
```

Expected:

```text
https://192.168.49.2:8443
```

Or:

```bash
kubectl config view -o jsonpath='{.clusters[?(@.name == "minikube")].cluster.server}' \
  | sed -e 's#.*/\(.*\):\(.*\)#MINIKUBE_INTERNAL_IP="\1"\nMINIKUBE_INTERNAL_PORT="\2"\n#'
```

Expected:

```text
MINIKUBE_INTERNAL_IP="192.168.49.2"
MINIKUBE_INTERNAL_PORT="8443"
```

#### Get client keys

```bash
echo "MINIKUBE_CLIENT_CERT=$(kubectl config view -o jsonpath='{.users[?(@.name == "minikube")].user.client-certificate}')"
echo "MINIKUBE_CLIENT_KEY=$(kubectl config view -o jsonpath='{.users[?(@.name == "minikube")].user.client-key}')"
echo "MINIKUBE_CA=$(kubectl config view -o jsonpath='{.clusters[?(@.name == "minikube")].cluster.certificate-authority}')"
```

Expected:

```text
MINIKUBE_CLIENT_CERT=/path/to/home/.minikube/profiles/minikube/client.crt
MINIKUBE_CLIENT_KEY=/path/to/home/.minikube/profiles/minikube/client.key
MINIKUBE_CA=/path/to/home/.minikube/ca.crt
```

### Development host

This is **not** the `minikube` host.

#### Preparation

Remote host running `minikube`:

```bash
MINIKUBE_HOST_IP="<Host IP address that is running minikube>"
```

Remote host username:

```bash
MINIKUBE_HOST_USER="<Username that can SSH into the minikube host>"
```

Or (if it is the case the local user is the same as remote user):

```bash
MINIKUBE_HOST_USER="${USER}"
```

Remote host `minikube` IP (from running `kubectl config view` above):

```bash
MINIKUBE_INTERNAL_IP="<minikube internal IP address in the remote host>"
MINIKUBE_INTERNAL_PORT="<minikube internal port in the remote host>"
```

Local port to use:

```bash
LOCAL_MINIKUBE_PORT=18443
```

#### Get certificates 

See step above to get the paths:

```bash
MINIKUBE_CLIENT_CERT="</minikube_host_path/to/client.crt>"
MINIKUBE_CLIENT_KEY="</minikube_host_path/to/client.key>"
MINIKUBE_CA="</minikube_host_path/to/ca.crt"
```

Copy them over with `scp`:

```bash
MINIKUBE_CERT_DIR="${HOME}/minikube-remote"
mkdir -p ${MINIKUBE_CERT_DIR}
scp -r ${MINIKUBE_HOST_USER}@${MINIKUBE_HOST_IP}:${MINIKUBE_CLIENT_CERT} ${MINIKUBE_CERT_DIR}/
scp -r ${MINIKUBE_HOST_USER}@${MINIKUBE_HOST_IP}:${MINIKUBE_CLIENT_KEY} ${MINIKUBE_CERT_DIR}/
scp -r ${MINIKUBE_HOST_USER}@${MINIKUBE_HOST_IP}:${MINIKUBE_CA} ${MINIKUBE_CERT_DIR}/
ls -l ${MINIKUBE_CERT_DIR}
```

Expected:

```text
-rw-r--r--  1 YOUR_USER  YOUR_GROUP  1147 May 27 15:05 client.crt
-rw-------  1 YOUR_USER  YOUR_GROUP  1675 May 27 15:05 client.key
```

#### Create an SSH tunel

```bash
ssh -N -p 22 ${MINIKUBE_HOST_USER}@${MINIKUBE_HOST_IP} \
  -L 127.0.0.1:${LOCAL_MINIKUBE_PORT}:${MINIKUBE_INTERNAL_IP}:${MINIKUBE_INTERNAL_PORT}
```
