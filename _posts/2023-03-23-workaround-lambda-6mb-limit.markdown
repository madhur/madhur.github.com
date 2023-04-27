---
layout: blog-post
title: "Workaround AWS Lambda 6 MB Response size limit"
excerpt: "Workaround AWS Lambda 6 MB Response size limit"
disqus_id: /2023/03/23/workaround-lambda-6mb-limit/
tags:
    - AWS
    - NodeJs
---

[AWS Lambda](https://aws.amazon.com/lambda/) is a great way to build serverless applications.

However, there lot of limitations imposed by AWS Lambda.

For example, [one of the limitations is that the payload size of the lambda is restricted to 6 MB, when using it synchronously](https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-limits.html)

This makes, Lambda ineffective to serve binary files such as videos, PDF's etc.

However, there is nifty workaround for this limitation, which is using [S3 pre-signed URL's](https://docs.aws.amazon.com/AmazonS3/latest/userguide/ShareObjectPreSignedURL.html)

The idea is to upload the object to S3, generate the pre-signed URL and send it back to client. This is what we did for one of our use cases and it worked really well.

The following code snippet demonstrates the idea:


```javascript
import {
  getSignedUrl,
} from "@aws-sdk/s3-request-presigner";
import { S3Client, GetObjectCommand } from "@aws-sdk/client-s3";

const createPresignedUrlWithClient = ({ key }) => {
  const client = new S3Client({ REGION });
  const command = new GetObjectCommand({ Bucket: BUCKET_NAME, Key: key });
  return getSignedUrl(client, command, { expiresIn: 3600 });
};

export const directoryLister = async (event, context, callback) => {
    let path = event.queryStringParameters.file;
    let params = {
      Bucket: BUCKET_NAME,
      Key: path,
      ResponseContentDisposition: "inline",
    };
    const command = new GetObjectCommand(params);
    const data = await client.send(command);
    if (data.ContentLength > SIZE_THRESHOLD) {
		// If the size is greater than threshold, generate pre-signed url
      const clientUrl = await createPresignedUrlWithClient({
        key: params.Key,
      });
      const response = {
        statusCode: 301,
        headers: {
          Location: clientUrl,
        }
      };
      context.succeed(response);
      return;
    }

    // Convert Body from a Buffer to a String
    const content = await streamToBuffer(data.Body);
    let base64 = content.toString("base64");

    const response = {
      statusCode: 200,
      body: base64,
      isBase64Encoded: true,
      headers: {
        "Content-disposition": "inline",
        "content-type": "application/pdf",
      },
    };
    context.succeed(response);
}
```






