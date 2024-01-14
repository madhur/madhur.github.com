---
layout: blog-post
title: "Generic traffic splitting algorithm"
excerpt: "Generic traffic splitting algorithm"
disqus_id: /2020/11/13/generic-traffic-splitting-algorithm/
tags:
    - Algorithm
---

In one our recent requirements, we were required to very accurately split the
incoming traffic into multiple distribution patterns. This is a very common
algorithm requirement in use cases such as load balancer where you would assign
the weight to each resource and load balancer would split the incoming traffic
into the resources based on the desired weightages.

I had written the article [Incrementally routing traffic to newer version of service]({% post_url
2020-02-08-incrementally-route-traffic-newer-version-service %}) and an astute
follower / reader might question that we could have used the similar logic here.

The main difference between the that article and requirement here is the
accuracy. That algorithm was based on the probabilities and result was the
approximation of the desired split.

But in this case, we require the exact split and hence we cannot rely on
probabilities. We will need to maintain the state.

To state the problem simply as a test case below:

```java
@Test
public void splitTest() {
        List<BucketInfo> bucketInfoList = new ArrayList<>();
        bucketInfoList.add(new BucketInfo('a', 5));
        bucketInfoList.add(new BucketInfo('b', 2));
        bucketInfoList.add(new BucketInfo('c', 3));

        Distributor distributor = new Distributor(bucketInfoList);
        int aBucketCount = 0, bBucketCount = 0, cBucketCount = 0;
        for(int i=0;i<100;++i) {
            char bucket = distributor.getNextBucket();
            switch (bucket) {
                case 'a':
                    aBucketCount++;
                    break;
                case 'b':
                    bBucketCount++;
                    break;
                case 'c':
                    cBucketCount++;
                    break;
            }
        }
        Assert.assertEquals(50, aBucketCount);
        Assert.assertEquals(20, bBucketCount);
        Assert.assertEquals(30, cBucketCount);
}
```
Bucket definition:

```java
public class BucketInfo {
    private final int weight;
    private final char bucketId;

    public BucketInfo(char bucketId, int weight) {
        this.bucketId = bucketId;
        this.weight = weight;
    }
    public char getBucketId() {
        return bucketId;
    }
    public int getWeight() {
        return weight;
    }
}
```


We define n number of buckets (identified by a char here) and an integer
weightage. We need to split the infinite requests into the weightage. For
example in this case, we have 3 buckets (a, b and c) with weights 5, 2 and 3.

If we are firing 100 requests, there should be exactly, 50 requests served by a,
20 by b and 30 by c.

Simply, it comes down to identifying the bucket to be used for the request and
needless to say it should be O(1)

Our implementation requires implementing just one interface

```java
public interface IDistributor {
    char getNextBucket();
}
```

My solution was implemented using an array of length equal to total number of
buckets and assigning each array index to the bucket in proportion to their
weightage.

Now, the identifying the next bucket is simply, choosing the index in this array
with equal probability. To solve the equal probability equation, we will need to
store the last index used in memory and just increment the index considering the
array to be circular.

```java
@Override
public char getNextBucket() {
        this.nextBucketIndex++;
        this.nextBucketIndex = (this.nextBucketIndex == this.senderBuckets.length)? 0: this.nextBucketIndex;
        return senderBuckets[nextBucketIndex];
    }
```

The full code is available in the [gist here](https://gist.github.com/madhur/8e84a839f9772b2e0ede429f6e0fa770)