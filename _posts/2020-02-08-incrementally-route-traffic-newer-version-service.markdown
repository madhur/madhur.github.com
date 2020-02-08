---
layout: blog-post
title: "Incrementally routing traffic to newer version of service"
excerpt: "Incrementally routing traffic to newer version of service"
disqus_id: /2020/02/08/incrementally-route-traffic-newer-version-service/
tags:
- Hashing
- Node.js
---

Recently, I had a requirement to incrementally increase the traffic to a newer version of service we were deploying in production.

We didn't wanted to go with random percentage approach. This is because our users are mobile app users and we didn't want the users to hit the older version and newer verison of service randomly.

That is, we wanted to consistently map the user to either be routed to an older version of newer version based on certain configurable percentage.

[Open diagram in fullscren](/images/hash.png)

<img src='/images/hash.png' height='500px' width='852px' />

Our proxy server was based on node.js 

After evaluatin several algorithms to generate hash based on user id, such as [Base64](https://en.wikipedia.org/wiki/Base64), [MD5](https://en.wikipedia.org/wiki/MD5). I finally zeroed out on [CRC32 algorithm](https://en.wikipedia.org/wiki/Cyclic_redundancy_check).

The simple reason being that output of CRC32 is a simple 32 bit integer which can be easily converted to a percentage value and the performance of crc32 being the fastest among all.

The simple methods below give the gist of algorithm. Our `getHash` function generates the 32 bit integer and `routeRequestBasedonRampUp` method uses this integer to map it to 1..100 buckets. Based on the rampup percentage value, it gives a boolean response which is used by proxy layer.

```javascript
const getHash = userId => {
    return CRC32.str(userId) >>> 0;
};

const routeRequestBasedonRampUp = (userId, rampUpPercent) => {
  const NUM_BUCKETS = 100;
  
  const hash = getHash(userId);
  const bucket = hash % NUM_BUCKETS;

  if (bucket + 1 <= rampUpPercent) {
      return true;
  }
  return false;
};
```

I have used this approach in production with this [crc32 library](https://www.npmjs.com/package/crc-32)

The decisioning time is <1ms and have been serving us really well.

Please let me know in the comments section if you think any better approach is available.