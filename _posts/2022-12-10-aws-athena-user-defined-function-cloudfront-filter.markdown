---
layout: blog-post
title: "User Defined function(UDF) to filter cloudfront IP Addresses from AWS Athena Logs"
excerpt: "User Defined function(UDF) to filter cloudfront IP Addresses from AWS Athena Logs"
disqus_id: /2022/12/10/aws-athena-user-defined-function-cloudfront-filter/
tags:
    - Athena
	- Java
	- Lambda
---

Recently, I was faced with a situation where I had to query [AWS ALB Logs](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-access-logs.html) for the rows not coming from the [cloudfront](https://aws.amazon.com/cloudfront/) IP as the source.

To give some perspective, we use [cloudfront CDN](https://aws.amazon.com/cloudfront/) in front of our ALB, however, some of our traffic was also coming to [ALB](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/introduction.html) directly.

I wanted to query the traffic directly coming from users in [AWS Athena](https://www.amazonaws.cn/en/athena/) and there was no easy way to do that.

That's where I decided to write [User defined function (UDFS)](https://docs.aws.amazon.com/athena/latest/ug/querying-udf.html)

All the AWS IP ranges are mentioned in this url [https://ip-ranges.amazonaws.com/ip-ranges.json](https://ip-ranges.amazonaws.com/ip-ranges.json)

What we can do is simply write a function, which will query the row and filter it out if the source IP Address lies in this range.

Here is the simple snippet for the same:


```java
public class CloudFrontFilterUDFS extends UserDefinedFunctionHandler {
    private static final String SOURCE_TYPE = "Custom";
    static ObjectMapper mapper = new ObjectMapper();
    static List<SubnetUtils.SubnetInfo> subnetUtils;

    static {
        mapper.configure(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES, false);
        InputStream in = Thread.currentThread().getContextClassLoader().getResourceAsStream("cloudfront.json");
        CloudFront cloudfront = null;
        try {
            cloudfront = mapper.readValue(in, CloudFront.class);
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
        subnetUtils = cloudfront.getPrefixes().stream().map(prefix -> new SubnetUtils(prefix.getIp_prefix()).getInfo()).collect(Collectors.toList());
    }

    public CloudFrontFilterUDFS() {
        super(SOURCE_TYPE);
    }

    public String iscloudfrontip(String ipAddress) {
        if(StringUtils.isEmpty(ipAddress)) {
            return String.valueOf(false);
        }
        return String.valueOf(subnetUtils.stream().anyMatch(s-> s.isInRange(ipAddress)));
    }
}
```

All needs to be done is, package this in a jar file and deploy it to [AWS Lambda](https://aws.amazon.com/lambda/) as a function.

Once its deployed, its easy to query AWS athena as follows:


```sql
USING EXTERNAL FUNCTION IsCloudFrontIP(ip varchar)
RETURNS varchar
LAMBDA 'cloudfront-filter-udfs'
SELECT  request_url, approx_percentile(target_processing_time, 0.99) as p99
FROM "alb_logs"."alb_ext_logs"
where year = '2023'
	and month = '06'
	and day = '14'
	and IsCloudFrontIP(client_ip)='false'
    and target_status_code='200'
	group by request_url order by p99 desc
```

In the above query, `cloudfront-filter-udfs` is the exact name of the lambda function which is deployed.

You can checkout the entire the UDFS code in [my github repository](https://github.com/madhur/cloudfront-filter-udfs)