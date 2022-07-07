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

    ec2 = boto3.client('ec2', event['ResourceProperties']['PeerRegion'])

    try:
        if request_type in ["Create", "Update"]:
            complete = False
            sleep_time = 10
            while not complete:
                response = ec2.describe_transit_gateway_peering_attachments(
                    TransitGatewayAttachmentIds=[event['ResourceProperties']['TransitGatewayID']]
                )

                state = response["TransitGatewayPeeringAttachments"][0]["State"]

                if state in ["pending", "initiating", "initiatingRequest"]:
                    print("TGW Attachment state is %s. Waiting for it to become available"
                          % state)

                elif state == "pendingAcceptance":
                    print("TGW Attachment state is %s. Accepting peering attachment"
                          % state)
                    response = ec2.accept_transit_gateway_peering_attachment(
                        TransitGatewayAttachmentId=event['ResourceProperties']['TransitGatewayID']
                    )

                    print("Transit Gateway Peering Attachment accept response:")
                    print(response)
                    sleep_time = 30

                elif state == "available":
                    print("TGW Attachment state is %s. Sending success response to CloudFormation"
                          % state)
                    complete = True

                else:
                    raise Exception("cannot accept TransitGatewayPeeringAttachments from state %s."
                                    % state)

                if not complete:
                    sleep(sleep_time)

            cfnresponse.send(event, context, cfnresponse.SUCCESS, {})
        elif request_type == "Delete":
            # No action needed because this custom resource only executes an accept request
            # and doesn't manage a physical resource therefore nothing can be deleted
            cfnresponse.send(event, context, cfnresponse.SUCCESS, {})
        else:
            raise ValueError(f"Request type {request_type} not recognised.")
    except Exception as e:
        print(e)
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
