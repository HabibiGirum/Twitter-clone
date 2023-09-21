# Define the osquery query
$osquery_query = "SELECT * FROM time;"

# Define the API endpoint where you want to send the data
$endpoint_url = "https://api.vistar.cloud/api/v1/computers/osquery_log_data/"

# Specify the interval (in seconds) between data sends (e.g., every 1 hour)
$interval_seconds = 30  # 1 hour

while ($true) {
    # Run the osquery command and capture the output
    try {
        $osquery_output = & "C:\Program Files\osquery\osqueryi.exe" "--json" $osquery_query
        $osquery_data = $osquery_output | ConvertFrom-Json
    }
    catch {
        Write-Host "Error running osquery: $_"
        $osquery_data = @()
    }

    # Prepare the data to send (you may need to format it based on your endpoint requirements)
    $data_to_send = @{
        "query"   = $osquery_query
        "results" = $osquery_data
    }

    # Send the data to the endpoint using Invoke-RestMethod
    try {
        $response = Invoke-RestMethod -Uri $endpoint_url -Method Post -ContentType "application/json" -Body ($data_to_send | ConvertTo-Json)
        if ($response.StatusCode -eq 200) {
            Write-Host "Data sent successfully"
        }
        else {
            Write-Host "Failed to send data. Status code: $($response.StatusCode)"
        }
    }
    catch {
        Write-Host "Error sending data: $_"
    }

    # Sleep for the specified interval before the next run
    Start-Sleep -Seconds $interval_seconds
}
