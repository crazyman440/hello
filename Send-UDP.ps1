$TargetIP = "192.168.1.232"
$TargetPort = 12345
$Message = "test packet"

# Create a UDP client
$UdpClient = New-Object System.Net.Sockets.UdpClient
$Bytes = [System.Text.Encoding]::UTF8.GetBytes($Message)

# Send the UDP packet
$UdpClient.Send($Bytes, $Bytes.Length, $TargetIP, $TargetPort)

Write-Host "Sent UDP packet to ${TargetIP}:${TargetPort} with message: ${Message}"

# Close the client
$UdpClient.Close()
