# CloudFormation custom resource - Transit Gateway Peering Attachment acceptor

In this repository you will find a CloudFormation Custom Resource which accepts a 
Transit Gateway Peering Attachment.

A Transit Gateway Attachment can be accepted if the state is `pendingAcceptance` after accepting
the attachment it will go into the `pending` state if successful the attachment becomes `available` after 2-5 minutes. 

See image below for the whole lifecycle of the attachment:

![](peering-attachment-lifecycle.png)


# Lambda Custom Resource

The Lambda custom resource will wait for the attachment states. The states are handled as follows:

- **pendingAcceptance**: Accept the peering attachment
- **pending, initiating, initiatingRequest**: Wait for pendingAcceptance or a failure
- **available**: Send a `SUCCESS` response to CloudFormation
- **Other states**: Throw an exception and send `FAILED` response to CloudFormation

# CloudFormation Examples

You can find two CloudFormation examples that implement the custom resource.
Two stacks can be found a minimal stack and a full stack.

- **transit-gateway-peering-minimal**: This is a minimal stack, which only has the Transit Gateway, Peering Attachment and the custom resource peering attachment acceptor.
- **transit-gateway-peering-minimal**: This is a full stack, which includes everything from the minimal stack and adds a VPC, EC2 and routes to be able to perform a ping test from both the EC2 instances.

## Deploy the stacks
For deployment of the stacks [Sceptre](https://github.com/Sceptre/sceptre) is used.

### Minimal
Deploy the minimal stack
```shell
sceptre launch transit-gateway-peering-minimal
```

Destroy the minimal stack
```shell
sceptre delete transit-gateway-peering-minimal
```

### Full
Deploy the Full stack
```shell
sceptre launch transit-gateway-peering-full
```

Destroy the Full stack
```shell
sceptre delete transit-gateway-peering-full
```