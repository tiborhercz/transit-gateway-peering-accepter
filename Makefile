deploy-tgw-eu-west-1:
	export REGION=eu-west-1 && \
	aws cloudformation deploy --region $${REGION} --template-file ./transit-gateway.yaml --stack-name transit-gateway

deploy-tgw-eu-central-1:
	export REGION=eu-central-1 && \
	aws cloudformation deploy --region $${REGION} --template-file ./transit-gateway.yaml --stack-name transit-gateway

deploy-tgw-eu-west-2:
	export REGION=eu-west-2 && \
	aws cloudformation deploy --region $${REGION} --template-file ./transit-gateway.yaml --stack-name transit-gateway

deploy-tgw-peering-eu-west-1:
	export REGION=eu-west-1 && \
	aws cloudformation deploy --capabilities CAPABILITY_IAM --region $${REGION} --template-file ./transit-gateway-peering-eu-west-1-to-eu-central-1.yaml --stack-name transit-gateway-peering

deploy-vpc-ec2:
	export REGION=eu-west-1 && \
	aws cloudformation deploy --capabilities CAPABILITY_IAM --region $${REGION} --parameter-overrides CidrBlock=10.0.0.0/16 SubnetCidrBlock=10.0.1.0/24 KeyName=awsBinx --template-file ./vpc-ec2.yaml --stack-name vpc-ec2

deploy-tgw:
	 sceptre launch demo

update-inline-lambda-code:
	aws-cfn-update lambda-inline-code --resource TransitGatewayPeeringAcceptor --file lambda/index.py templates/transit-gateway-peering.yaml

update-lambda-code-tgw-peering:
	export REGION=eu-west-1 && \
	aws lambda --region $${REGION} update-function-code \
        --function-name custom-resource \
        --s3-bucket lambda-code-bucket-binx-3252 \
        --s3-key lambda-code.zip

zip-lambda-code:
	cd lambda && \
	rm -r package && \
	pip3 install --target ./package -r requirements.txt && \
	cd package && \
	zip -r ../lambda-code.zip . && \
	cd .. && \
	zip -g lambda-code.zip index.py

zip-to-s3-tgw-peering:
	make zip-lambda-code && \
	aws s3 cp ./lambda/lambda-code.zip s3://lambda-code-bucket-binx-3252
