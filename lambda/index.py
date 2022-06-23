import logging
import time
import cfnresponse
import boto3
from cfn_lambda_handler import Handler

handler = Handler()

logger = logging.getLogger()
logger.setLevel(logging.INFO)

ec2_eu_central_1_resource = boto3.client('ec2', 'eu-central-1')


@handler.create
@handler.update
@handler.delete
def lambda_handler(event, context):
    logger.info(event)
    request_type = event["RequestType"]

    try:
        if request_type in ["Create", "Update"]:
            print(event['ResourceProperties']['TransitGatewayID'])
            time.sleep(80)

            ec2_eu_central_1_resource.accept_transit_gateway_vpc_attachment(
                TransitGatewayAttachmentId=event['ResourceProperties']['TransitGatewayID']
            )

            responseData = {}
            responseData['Data'] = event['ResourceProperties']['TransitGatewayID']

            print(responseData)

            cfnresponse.send(event, context, cfnresponse.SUCCESS, {})
        elif request_type == "Delete":
            # Cleanup
            cfnresponse.send(event, context, cfnresponse.SUCCESS, {})
        else:
            raise ValueError(f"Request type {request_type} not recognised.")
    except Exception as e:
        logger.exception("Operation failed, sending response to CloudFormation")
        cfnresponse.send(event, context, cfnresponse.FAILED, {})
        raise e
