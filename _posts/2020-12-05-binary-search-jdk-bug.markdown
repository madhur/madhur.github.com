---
layout: blog-post
title: "Binary Search bug in JDK"
excerpt: "Binary Search bug in JDK"
disqus_id: /2020/12/05/binary-search-jdk-bug/
tags:
    - Binary Search
---

There was a [famous bug](https://ai.googleblog.com/2006/06/extra-extra-read-all-about-it-nearly.html) which existed in JDK implementation of [Binary Search](https://en.wikipedia.org/wiki/Binary_search_algorithm)


Randomly, I tried to reproduce the issue this weekend.

Here is the flawed implementation

```java
public int search(int[] arr, int target) {
    int low = 0;
    int high = arr.length - 1;

    while (low <= high) {
        int mid = (high + low) / 2;

        if(arr[mid] == target) {
            return mid;
        }
        else if (arr[mid] < target) {
            low = mid + 1;
        }
        else {
            high = mid - 1;
        }
    }
    return -1;
}
```

If we execute this algorithm with following code:

```java
BinarySearch binarySearch = new BinarySearch();
int[] newArr = new int[(int) Math.pow(2, 30) + 100];
System.out.println(binarySearch.search(newArr, (int) Math.pow(2, 30)));
```

We see the following exception

```console
Exception in thread "main" java.lang.ArrayIndexOutOfBoundsException: -1073741788
	at binarysearch.BinarySearch.search(BinarySearch.java:14)
	at binarysearch.BinarySearch.main(BinarySearch.java:31)

Process finished with exit code 1
```

The issue is in calculation of `mid` variable. The value `high+low` overflows
the maximum range of `int` and ultimately results in negative value.

To fix this, we simply need to change the calculation of `mid` as follows:

```java
int mid = low + (high - low)/2;
```

This will give us the correct value of `-1` which indicates that value doesn't
exist in the array.

Its amazing how simplest of bugs can remain undetected for years. This one
remain undetected for nine years.

