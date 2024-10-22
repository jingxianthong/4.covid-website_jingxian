
---

# Malaysia COVID-19 Graph Data Project

## Overview

This project involves downloading COVID-19 data for Malaysia, generating a graph from this data, and serving the graph via a Flask web application.

## Project Structure

- **`download.py`**: Downloads the CSV file containing COVID-19 data from [MOH's Open Data](https://data.moh.gov.my/).
- **`graph.py`**: Draws a graph using the data from the downloaded CSV file.
- **`webapp.py`**: Deploys the graph in a Flask web application for easy access and visualization.

## Getting Started

### Data Source

This project uses official COVID-19 data from the Ministry of Health Malaysia, accessible at [data.moh.gov.my](https://data.moh.gov.my/).

### License

This project is open-source and is licensed under the MIT License.

## Nginx Configuration for External Access

To allow external devices to connect through Nginx, you need to modify the Nginx configuration file. Below is the configuration file:

```
    # Server block for HTTP access on port 80
    server {
        listen       80;
        server_name  your_domain.com;  # Replace with your domain or IP (e.g., 192.168.1.100 or localhost)
        
        # Proxy requests to Dash app running on port 8050
        location / {
            proxy_pass http://127.0.0.1:8050;  # Dash app running on port 8050
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # Handle error pages
        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   C:/Nginx/html;  # Ensure this path exists and contains the error page
        }
    }

    # Optional server block for accessing on port 8008
    server {
        listen 8008;

        # Proxy requests to Dash app running on port 8050
        location / {
            proxy_pass http://localhost:8050;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
    
    # You can add your HTTPS server block here in the future if needed
}
```

### Flask Application Configuration

Ensure that the Flask app is running on the specified port:

```python
if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8050, debug=True)
```

### Finding the IP Address of Your Device

To find the IP address of your device where the Dash app is running:

- **On Windows**:
  1. Open Command Prompt.
  2. Type `ipconfig` and press Enter.
  3. Look for the IPv4 address under your active network connection (e.g., `192.168.1.x`).

### Modifying Nginx Configuration for External Access

Ensure your Nginx server is listening for connections not just on localhost but on all network interfaces (or at least your local network). Update the configuration in your Nginx file as follows:

```nginx
server {
    listen       8050;  # Or any other port you'd like to use
    server_name  _;  # Or use your IP, e.g., 192.168.1.x

    location / {
        proxy_pass http://127.0.0.1:8050;  # Proxy to Dash app
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

This configuration tells Nginx to listen on port 8050 for external traffic and forward it to the Dash app running on `localhost:8050`.

### Firewall and Port Forwarding

Ensure your machine allows incoming connections on port 8050. If you're using a firewall, you may need to open port 8050:

- **Windows Firewall**:
  1. Open the Windows Defender Firewall.
  2. Go to Advanced settings > Inbound Rules.
  3. Create a new rule to allow connections on port 8050.

  Steps to create a new inbound rule:
  1. In the left pane, click `Inbound Rules`.
  2. In the right-hand pane, click `New Rule...`.
  3. Select `Port` as the rule type, and then click `Next`.
  4. Choose `TCP` (since your Dash app is running over TCP).
  5. Select `Specific local ports`, and type `8050` into the field. Click `Next`.
  6. Select `Allow the connection`, and click `Next`.
  7. Choose when this rule should apply:
     - `Domain`: Applies when your computer is connected to a domain.
     - `Private`: Applies when your computer is connected to a private network (e.g., home or work).
     - `Public`: Applies when your computer is connected to a public network (e.g., airport or coffee shop).
     - Check the appropriate boxes based on your environment, then click `Next`.
  8. Name the rule, such as `Allow Port 8050`, and optionally, add a description for future reference. Click `Finish` to create the rule.


My reuslt:
![image](https://github.com/user-attachments/assets/014be716-eb21-4e1c-80f2-12147b6ff7c4)

---

