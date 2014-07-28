---
layout: blog-post
title: "Find Nth largest element in an array"
excerpt: "Find Nth largest element in an array"
disqus_id: /2014/07/28/findnthlargest/
location: New Delhi, India
time: 9:00 PM
tags:
- Algorithms
---

Recently, I was asked to write the algorithm for finding nth largest item in an array.

Finding the max is easy:

```Java
public class Main
{

	public static void main(String[] args)
	{
		int array[] =
		{ 10, 20, 30, 25, 50, 55, 90, 10, 20, 30 };

		int max = 0;
		for (int i = 0; i < array.length; ++i)
		{
			if (max < array[i])
				max = array[i];

		}

		System.out.println("The Max is: " + max);

		if (System.console() != null)
			System.console().readLine();

	}
}
```

```
The Max is: 90
```

However, finding the nth largest is bit complicated. It uses the quick select algorithm with complexity `O(n)`


```Java
public class Main
{

	public static void main(String[] args)
	{
		int array[] =
		{ 10, 20, 30, 25, 50, 55, 90, 80, 70, 10, 20, 30 };

		System.out
				.println("The Max is: " + kthLargest(array, array.length - 1));

		System.out.println("The next Max is: "
				+ kthLargest(array, array.length - 2));

		if (System.console() != null)
			System.console().readLine();

	}

	static int kthLargest(int[] list, int k)
	{
		int left = 0;
		int right = list.length - 1;
		while (true)
		{
			int pivIndex = (left + right) / 2;
			int newPiv = partition(list, left, right, pivIndex);
			if (newPiv == k)
				return list[newPiv];
			else if (newPiv < k)
			{
				left = newPiv + 1;
			}
			else
			{
				right = newPiv - 1;
			}
		}
	}

	private static int partition(int[] list, int left, int right, int pivot)
	{
		int pivValue = list[pivot];
		swap(list, pivot, right); // put pivot value on the end
		int storePos = left;
		for (int i = left; i < right; i++)
		{
			if (list[i] < pivValue)
			{
				swap(list, i, storePos);
				storePos++;
			}
		}
		swap(list, storePos, right);
		return storePos;
	}

	private static void swap(int[] list, int a, int b)
	{
		int temp = list[a];
		list[a] = list[b];
		list[b] = temp;

	}
}

```


```text
The Max is: 90
The next Max is: 80
```