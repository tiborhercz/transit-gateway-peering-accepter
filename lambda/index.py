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

    ec2_resource = boto3.client('ec2', event['ResourceProperties']['PeerRegion'])

    try:
        if request_type in ["Create", "Update"]:

            wait_for_attachment_state('pendingAcceptance', event['ResourceProperties']['TransitGatewayID'],
                                      ec2_resource, 30)

            response = ec2_resource.accept_transit_gateway_peering_attachment(
                TransitGatewayAttachmentId=event['ResourceProperties']['TransitGatewayID']
            )

            print("Transit Gateway Peering Attachment accept response:")
            print(response)

            wait_for_attachment_state('available', event['ResourceProperties']['TransitGatewayID'],
                                      ec2_resource, 10)

            cfnresponse.send(event, context, cfnresponse.SUCCESS, {})
        elif request_type == "Delete":
            # No action needed because this custom resource only executes an accept request
            # and doesn't manage a physical resource therefore nothing can be deleted
            cfnresponse.send(event, context, cfnresponse.SUCCESS, {})
        else:
            raise ValueError(f"Request type {request_type} not recognised.")
    except Exception as e:
        logger.exception("Operation failed, sending response to CloudFormation")
        cfnresponse.send(event, context, cfnresponse.FAILED, {})
        raise e


def wait_for_attachment_state(state, transit_gateway_attachment_id, ec2_resource, sleep_time):
    print("Waiting for %s to become state " %(transit_gateway_attachment_id,state))

    complete = False
    while not complete:
        response = ec2_resource.describe_transit_gateway_peering_attachments(
            TransitGatewayAttachmentIds=[transit_gateway_attachment_id]
        )

        print("Transit Gateway Peering Attachment describe response:")
        print(response)

        if response["TransitGatewayPeeringAttachments"][0]["State"] == state:
            complete = True
        sleep(sleep_time)


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
