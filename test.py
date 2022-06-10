  import json
  import cfnresponse
  import boto3

  ec2_eu_central_1_client = boto3.client('ec2', 'eu-central-1')
  def handler(event, context):
    try:
      if request_type in ["Create", "Update"]:


        print(ec2_eu_central_1_client.describe_vpcs())

        print(event)
        print(event['ResourceProperties']['TransitGatewayID'])
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
      cfnresponse.send(event, context, cfnresponse.FAILED, {})
      raise e
