---
slug: "unionintersection"
title: Union and Intersection of ArrayList in Java
date: '2014-07-29'
year: '2014'
month: '2014-07'
description: Union and Intersection of ArrayList in Java
tags:
  - Java
draft: false
params:
  disqus_id: /2014/07/22/unionintersection/
  location: 'New Delhi, India'
  time: '9:00 PM'
---


## Intersection

```Java
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class Main
{

	public static void main(String[] args)
	{
		
		 List<String> list1 = new ArrayList<String>(Arrays.asList("A", "B", "C"));
	     List<String> list2 = new ArrayList<String>(Arrays.asList("B", "C", "D", "E", "F"));
	      
	      list1.retainAll(list2) ;
	      	      
	      System.out.println(list1);
	      System.out.println(list2);	     
	}
}
```

```text
[B, C]
[B, C, D, E, F]
```
## Union

```Java
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class Main
{

	public static void main(String[] args)
	{
		
		 List<String> list1 = new ArrayList<String>(Arrays.asList("A", "B", "C"));
	     List<String> list2 = new ArrayList<String>(Arrays.asList("B", "C", "D", "E", "F"));
	      
	      list1.addAll(list2) ;
	      	      
	      System.out.println(list1);
	      System.out.println(list2);	     
	}
}
```

```text
[A, B, C, B, C, D, E, F]
[B, C, D, E, F]
```
