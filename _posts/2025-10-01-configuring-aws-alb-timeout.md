---
layout: blog-post
title: "Configuring AWS ALB Timeouts"
excerpt: "Configuring AWS ALB Timeouts"
disqus_id: /2025/10/01/configuring-aws-alb-timeout/
tags:
    - Timeout
---

> **Author's Note:** I recently encountered this exact library issue. After solving it, I used Claude AI to help me structure this troubleshooting guide based on my experience. The problem and solution are genuine - I just wanted to create a quick resource that others could benefit from.

### ALB Idle Timeout Configuration: Best Practices to Prevent 5xx Errors

If you've ever encountered mysterious 502 Bad Gateway or 504 Gateway Timeout errors from your AWS Application Load Balancer (ALB), you're not alone. Many of these issues stem from improperly configured timeout settings between your ALB and backend applications. In this article, we'll explore the best practices for configuring ALB idle timeouts.


## Understanding the Problem

AWS Application Load Balancers manage connections between clients and your backend applications. When timeout configurations are misaligned, you create race conditions that result in intermittent 5xx errors and degraded user experience.

The root cause typically involves two types of timeouts that must work in harmony:
- **Request timeouts**: How long to wait for a single request/response cycle
- **Keep-alive (idle) timeouts**: How long to maintain connections between requests

## Request Timeout Best Practices

### The Golden Rule: Application Timeout < ALB Timeout

Your application's request timeout should always be shorter than your ALB's timeout. Here's the recommended hierarchy:

```
ALB Request Timeout: 60 seconds (default)
Application Timeout: 50-55 seconds
Database/External API Timeout: 45 seconds or less
```

### Why This Matters

When your application timeout equals or exceeds the ALB timeout, you create a dangerous race condition:

1. **Request arrives** at ALB and forwards to your application
2. **Both timers start** counting down simultaneously
3. **Application timeout hits first** and closes the connection
4. **ALB is still waiting** for a response when connection terminates
5. **ALB generates 5xx error** instead of receiving your application's graceful error response



## Keep-Alive Timeout Best Practices

### The Reverse Rule: Application Keep-Alive > ALB Idle Timeout

Unlike request timeouts, keep-alive timeouts follow the opposite pattern:

```
ALB Idle Timeout: 60 seconds (default)
Application Keep-Alive: 65+ seconds
Database Connection Pool Idle: 70+ seconds
```

### Why Application Keep-Alive Should Be Higher

If your application's keep-alive timeout is shorter than ALB's idle timeout:

1. **Client completes request** through ALB to application
2. **Application closes connection** after its shorter keep-alive period
3. **ALB still considers connection active** and attempts reuse
4. **Next request fails** with 502 Bad Gateway because connection is closed


## Advanced Configuration Scenarios

### High-Traffic Applications

For applications handling high request volumes:

```
ALB Idle Timeout: 30 seconds (reduced)
Application Keep-Alive: 35 seconds
Request Timeout: 25 seconds
```

Shorter timeouts free up connections faster and improve resource utilization.

### Long-Running Operations

For applications with legitimate long-running operations:

```
ALB Request Timeout: 300 seconds (5 minutes)
Application Timeout: 280 seconds
Keep-Alive: 310 seconds
```

Consider moving truly long operations to asynchronous processing with status polling endpoints.

### Microservices Architecture

For service-to-service communication:

```
External ALB (Internet-facing):
  - Request Timeout: 60s
  - Idle Timeout: 60s

Internal ALB (Service-to-service):
  - Request Timeout: 30s
  - Idle Timeout: 30s

Application Configuration:
  - Request Timeout: 25s
  - Keep-Alive: 35s
```

## Monitoring and Troubleshooting

### Key Metrics to Monitor

**ALB CloudWatch Metrics**:
- `HTTPCode_ELB_5XX_Count`: Track 5xx errors from ALB
- `TargetResponseTime`: Monitor backend response times
- `ActiveConnectionCount`: Watch connection patterns

**Application Metrics**:
- Connection pool utilization
- Request timeout occurrences
- Keep-alive connection reuse rates

### Common Error Patterns

**502 Bad Gateway**:
- Often indicates application closed connection unexpectedly
- Check: Application keep-alive < ALB idle timeout
- Check: Application crashed or became unresponsive

**504 Gateway Timeout**:
- ALB timeout expired waiting for response
- Check: Application timeout ≥ ALB request timeout
- Check: Long-running operations without proper timeout handling

### Debugging Commands

**Test connection behavior**:
```bash
# Test keep-alive behavior
curl -H "Connection: keep-alive" -v http://your-alb-endpoint/

# Monitor connection reuse
curl -H "Connection: keep-alive" -v \
  http://your-alb-endpoint/endpoint1 \
  http://your-alb-endpoint/endpoint2
```

**Check ALB configuration**:
```bash
aws elbv2 describe-load-balancer-attributes \
  --load-balancer-arn arn:aws:elasticloadbalancing:...
```

## Best Practices Summary

1. **Request Timeouts**: Application timeout should be 10-15% shorter than ALB timeout
2. **Keep-Alive Timeouts**: Application keep-alive should be 5-10 seconds longer than ALB idle timeout
3. **Monitor Religiously**: Set up alerts for 5xx error rates and connection metrics
4. **Test Thoroughly**: Use load testing tools to validate timeout behavior under various conditions
5. **Document Configuration**: Maintain clear documentation of timeout values across your infrastructure
6. **Gradual Changes**: Modify timeout values incrementally and monitor impact

## Conclusion

Proper timeout configuration is crucial for maintaining reliable web applications behind AWS Application Load Balancers. By following the principles outlined in this guide—keeping application request timeouts shorter than ALB timeouts and application keep-alive timeouts longer than ALB idle timeouts—you can eliminate most timeout-related 5xx errors.

Remember that timeout configuration is not a one-size-fits-all solution. Consider your application's specific requirements, traffic patterns, and operational constraints when implementing these best practices. Regular monitoring and testing will help you fine-tune these settings for optimal performance and reliability.

The investment in properly configuring these timeouts will pay dividends in improved user experience, reduced operational overhead, and fewer 3 AM troubleshooting sessions.