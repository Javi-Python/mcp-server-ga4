# MCP GA4 Server Setup Guide

This guide explains how to set up and run the MCP Server for Google Analytics 4 (GA4) in your local environment.

---

## 1. Prerequisites

- **Python 3.9+** (recommended: use a virtual environment)
- **Google Cloud SDK (`gcloud`)** installed and authenticated
- **Google Analytics Data API** enabled in your Google Cloud project
- **Access to your GA4 property ID**

---

## 2. Setup Steps

### 2.1. Clone the Repository

```bash
git clone <your-repo-url>
cd <your-repo-folder>
```

### 2.2. Create and Activate a Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2.3. Install Dependencies

```bash
cd mcp-server-ga4
pip install -e ".[dev]"
```

> **Note:** If you use `uv` instead of pip, you can run:  
> `uv pip install -e ".[dev]"`

---

## 3. Google Cloud Authentication

### 3.1. Remove Old Credentials (if troubleshooting)

```bash
rm ~/.config/gcloud/application_default_credentials.json
```

### 3.2. Authenticate with Correct Scopes

```bash
gcloud auth application-default login --scopes=https://www.googleapis.com/auth/cloud-platform,https://www.googleapis.com/auth/analytics.readonly
```

- Log in with the Google account that has access to your GA4 property.
- Make sure the Google Analytics Data API is enabled in your project.

---

## 4. Running the Server

### 4.1. From the Command Line

```bash
mcp-server-ga4 --property-id <YOUR_GA4_PROPERTY_ID>
```

- If `mcp-server-ga4` is not found, use the full path from your virtual environment:
  ```
  /path/to/your/.venv/bin/mcp-server-ga4 --property-id <YOUR_GA4_PROPERTY_ID>
  ```

### 4.2. With Claude Desktop

In your `claude_desktop_config.json`, use the full path to the executable:

```json
"ga4": {
  "command": "/absolute/path/to/your/.venv/bin/mcp-server-ga4",
  "args": ["--property-id", "<YOUR_GA4_PROPERTY_ID>"]
}
```

---

## 5. Troubleshooting

- **403 Insufficient Authentication Scopes:**  
  Make sure you authenticated with both `cloud-platform` and `analytics.readonly` scopes.
- **Permission Denied for Service Account:**  
  Ensure your user has the `Service Account Token Creator` role if impersonating a service account.
- **Command Not Found:**  
  Use the full path to the `mcp-server-ga4` executable from your virtual environment.

---

## 6. Useful Commands

- **Check if `mcp-server-ga4` is available:**
  ```bash
  which mcp-server-ga4
  ```
- **Activate your virtual environment:**
  ```bash
  source /path/to/your/.venv/bin/activate
  ```

---

## 7. References

- [Google Analytics Data API Documentation](https://cloud.google.com/analytics/docs)
- [Google Cloud Authentication](https://cloud.google.com/docs/authentication/provide-credentials-adc)

---

**Keep this README up to date with any changes to your setup or workflow!** 