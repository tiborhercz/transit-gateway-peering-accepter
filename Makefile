deploy-tgw-eu-west-1:
	export REGION=eu-west-1 && \
	aws cloudformation deploy --region $${REGION} --template-file ./transit-gateway.yaml --stack-name transit-gateway
deploy-tgw-eu-central-1:
	export REGION=eu-central-1 && \
	aws cloudformation deploy --region $${REGION} --template-file ./transit-gateway.yaml --stack-name transit-gateway
deploy-tgw-peering-eu-west-1:
	export REGION=eu-west-1 && \
	aws cloudformation deploy --capabilities CAPABILITY_IAM --region $${REGION} --template-file ./transit-gateway-peering.yaml --stack-name transit-gateway-peering
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