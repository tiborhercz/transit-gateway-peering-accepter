import logging
import sys
from time import sleep

import cfnresponse
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
    logger.info(event)
    request_type = event["RequestType"]

    ec2_eu_central_1_resource = boto3.client('ec2', 'eu-central-1')

    try:
        if request_type in ["Create", "Update"]:

            complete = False
            while not complete:
                response = ec2_eu_central_1_resource.describe_transit_gateway_peering_attachments(
                    TransitGatewayAttachmentIds=[event['ResourceProperties']['TransitGatewayID']]
                )

                print("TransitGatewayPeeringAttachments-State=" + response["TransitGatewayPeeringAttachments"][0]["State"])

                if response["TransitGatewayPeeringAttachments"][0]["State"] == 'pendingAcceptance':
                    complete = True
                sleep(10)

            response = ec2_eu_central_1_resource.accept_transit_gateway_peering_attachment(
                TransitGatewayAttachmentId=event['ResourceProperties']['TransitGatewayID']
            )

            responseData = {}
            responseData['PhysicalResourceId'] = event['ResourceProperties']['TransitGatewayID']

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


if __name__ == "__main__":
    handler({
        "RequestType": "Create",
        "ResponseURL": "https://httpbin.org",
        "ResourceProperties": {
            "Region": sys.argv[1],
            "TransitGatewayID": sys.argv[2]
        }},
        {}
    )
