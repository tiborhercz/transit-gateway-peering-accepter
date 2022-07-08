update-inline-lambda-code:
	aws-cfn-update lambda-inline-code --resource TransitGatewayPeeringAccepter --file transit-gateway-peering-accepter/index.py templates/transit-gateway-peering.yaml
