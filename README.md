---

# Malaysia COVID-19 Graph Data Project

## Overview

This project aims to download COVID-19 data for Malaysia, generate a graph from this data, and serve the graph using a Flask web application. It provides an easy way to visualize the pandemic trends.

## Project Structure

- **`download.py`**: Script for downloading the COVID-19 data in CSV format from [MOH's Open Data](https://data.moh.gov.my/).
- **`graph.py`**: Generates a graph from the downloaded data.
- **`webapp.py`**: Hosts the graph in a Flask-based web application.

## Getting Started

### Data Source

The project uses official COVID-19 data provided by the Ministry of Health Malaysia, available at [data.moh.gov.my](https://data.moh.gov.my/).

### License

This project is open-source and licensed under the MIT License.

---

## Nginx Configuration for External Access

To allow external access to the web app through Nginx, the Nginx configuration must be set up properly. Below is a sample configuration for proxying requests to the Flask app:

### Example Nginx Configuration

```nginx
# HTTP server block
server {
    listen       80;
    server_name  your_domain.com;  # Replace with your domain or IP (e.g., 192.168.1.100)

    # Proxying requests to the Flask app on port 8050
    location / {
        proxy_pass http://127.0.0.1:8050;  # Dash/Flask app running on port 8050
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Error page handling
    error_page   500 502 503 504  /50x.html;
    location = /50x.html {
        root   /usr/share/nginx/html;  # Adjust path if needed
    }
}

# Optional server block for port 8008
server {
    listen 8008;

    # Proxying requests to the Flask app
    location / {
        proxy_pass http://localhost:8050;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Flask Application Configuration

Ensure your Flask application is listening on the correct interface and port. The following code ensures the Flask app runs on port 8050, accessible from any IP:

```python
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8050, debug=True)
```

---

## Accessing the Application

### Finding the IP Address

To access the Flask app from other devices, you need to find the IP address of your device.

- **On Windows**:
  1. Open the Command Prompt.
  2. Type `ipconfig` and press Enter.
  3. Look for the IPv4 address under your active network connection (e.g., `192.168.1.x`).

### Updating Nginx Configuration

Make sure Nginx is configured to accept external traffic on the relevant port, by modifying the configuration as follows:

```nginx
server {
    listen       8050;  # The port to listen for external connections
    server_name  _;  # Use your IP or domain name

    location / {
        proxy_pass http://127.0.0.1:8050;  # Proxy to the local Flask app
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

## Firewall and Port Forwarding

If your device has a firewall, ensure port 8050 is open to allow incoming connections.

### Opening Port 8050 on Windows Firewall

To allow connections on port 8050, follow these steps:

1. Open Windows Defender Firewall.
2. Navigate to **Advanced Settings** > **Inbound Rules**.
3. Create a new rule for port 8050.

Steps for adding a new inbound rule:
1. Click **Inbound Rules**.
2. Select **New Rule...** from the right-hand pane.
3. Choose **Port** as the rule type, and select **Next**.
4. Enter `8050` under **Specific local ports**, then click **Next**.
5. Select **Allow the connection**.
6. Choose the network profile (Domain, Private, or Public) based on where the app will run.
7. Name the rule (e.g., `Allow Port 8050`) and click **Finish**.

Now, your application should be accessible from external devices.

---

