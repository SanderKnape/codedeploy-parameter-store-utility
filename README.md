# CodeDeploy / Parameter Store integration utility
This repository contains a simple [utility function](/app/scripts/ssm_replacements.py) that fetches secrets from Parameter Store and puts them in the specified configuration file. In addition, through a [CloudFormation](/cloudformation.yaml) file you can fully spin up a working environment to test it out.

The utility is based on a [related blog post by AWS](https://aws.amazon.com/blogs/mt/use-parameter-store-to-securely-access-secrets-and-config-data-in-aws-codedeploy/), but generalised to make it useful for different use cases.

My accompanying blog post explains the utility in more detail, while also going into the design decisions of setting up proper secret management: [Secret management design decisions: theory plus an example](https://sanderknape.com/2018/03/secret-management-design-decisions-theory-plus-an-example).
