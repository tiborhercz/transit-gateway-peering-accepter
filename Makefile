update-inline-lambda-code:
	aws-cfn-update lambda-inline-code --resource TransitGatewayPeeringAcceptor --file transit-gateway-peering-acceptor/index.py templates/transit-gateway-peering.yaml
