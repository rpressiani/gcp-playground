# flask-vm
Based on GCP's tutorial [Get started with Terraform](https://cloud.google.com/docs/terraform/get-started-with-terraform).

### Apply infrastructure
```bash
$ terraform fmt
$ terraform validate
$ terraform apply
```

### Launch Flask webserver
- Open GCP console and connect to the VM with SSH
- Create `app.py`
- Copy/paste the `app.py` code
- Launch the server with
  
  ```bash
  $ python app.py
  ```

### Test webserver
- Get the external IP using Terraform output
  
  ```bash 
  $ terraform output
  ```
- Run `curl` to confirm the webserver is up and running

  ```bash 
  $ curl http://<EXTERNAL_IP_ADDRESS>:5000
  ```

### Destroy infrastrucure
```bash
$ terraform destroy
```
