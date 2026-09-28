import httpx

# Replace with your actual deployment ID after registration
deployment_id = "78200bd5-b0b5-4271-98c4-0a0e093ea889"

# Local Prefect API URL
url = f"http://localhost:4200/api/deployments/{deployment_id}/create_flow_run"

# Parameters to pass to the flow
payload = {
    "parameters": {
        "user_id": 203  # Example user ID
    }
}

# Make the API request
response = httpx.post(
    url=url,
    json=payload
    )

# Check the response
if response.status_code in (200, 201):
    print("Flow run triggered successfully:", response.json())
else:
    print("Error triggering flow run:", response.status_code, response.text)