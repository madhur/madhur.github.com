---
layout: blog-post
title: "Kotlin for Java Developers - Part 2"
excerpt: "Kotlin for Java Developers"
disqus_id: /2020/07/17/kotlin-for-java-developers-part2/
tags:
    - Java
    - Kotlin
---

Continuing article on Kotlin for Java Developers, Let's continue the differences:


* [Access Modifiers](#access)
* [Defining Classes and Constructors](#defining)
* [Multiple constructors](#multiple)
* [Generate Getters and Setters](#generate)
* [Data classes](#data)
* [Extension Functions](#extension)

<a name="access"></a>

## Access Modifiers

Default top level visibility is public whereas its package private in java

There is no restriction to have class names and filenames so its possible to declare multiple 
public classes in single Kotlin file

There is something called private class in Kotlin which means only classes within that file can use it.

```kotlin
fun main () {
    val emp = PEmployee()
    println(emp)
}

private class PEmployee {
    
}
```

Kotlin has fourth access modifier called [internal](https://kotlinlang.org/docs/reference/visibility-modifiers.html), which means internal to the [module](https://kotlinlang.org/docs/reference/visibility-modifiers.html)

Kotlin classes can't see private properties defined in inner classes

It is interested to note that since Kotlin runs on JVM, the code must be compiled to access modifiers which JVM can understand.
private is compiled to package private
internal is compiled to public

<a name="defining"></a>

## Defining Classes and Constructors

```java
public class JavaEmployee {

    private final String firstname;

    public JavaEmployee(String firstname) {
        this.firstname = firstname;
    }
}
```

```kotlin
class PEmployee constructor(firstName: String) {

    val firstName: String

    init {
        this.firstName = firstName
    }
}
```

This can be shortened to 
```kotlin
class PEmployee constructor(firstName: String) {
    val firstName: String = firstName
}
```

And can be even shortened to,

```kotlin
class PEmployee (val firstName: String) {
}

```

Kotlin has the notion of primary and secondary constructors.
[init](https://kotlinlang.org/docs/reference/classes.html) block is not a constructor. It is used in conjunction with primary constructors. It is like an init body for primary constructor.

<a name="multiple"></a>

## Multiple constructors

```java
public class JavaEmployee {

    private final String firstName;
    private final boolean fullTime;

    public JavaEmployee(String firstName) {
        this.firstName = firstName;
        this.fullTime = true;
    }

    public JavaEmployee(String firstName, boolean fullTime) {
        this.firstName = firstName;
        this.fullTime = fullTime;
    }

}
```

The initial equivalent code in Kotlin will be:
```kotlin
class PEmployee (val firstName: String) {
    var fullTime: Boolean = true
    constructor(firstName: String, fullTime: Boolean): this(firstName) {
        this.fullTime = fullTime
    }
}
```

Which can be even shortened by providing default parameter values, which is something not possible in Java.
```kotlin

class PEmployee (val firstName: String, var fullTime: Boolean = true) {
}
```
<a name="generate"></a>

## Generate Getters and Setters
There is interesting philosophy of Getters and Setters w.r.t. Kotlin

In Kotlin, getters and setters are automatically generated, however their visibility is same as that of variable visibility.

For ex, if variable is declared private, its getters and setter will be also private, which means you won't be able to access it from outside the class. Sounds strange and counter-intuitive to Java world. Right?

But that's how it is.

```java
public class JavaEmployee {

    private final String firstName;
    private  boolean fullTime;

    public JavaEmployee(String firstName) {
        this.firstName = firstName;
        this.fullTime = true;
    }

    public JavaEmployee(String firstName, boolean fullTime) {
        this.firstName = firstName;
        this.fullTime = fullTime;
    }

    public String getFirstName() {
        return firstName;
    }

    public boolean isFullTime() {
        return fullTime;
    }

    public void setFullTime(boolean fullTime) {
        this.fullTime = fullTime;
    }


}
```

Equivalent code will be

```kotlin
class PEmployee (val firstName: String,  fullTime: Boolean = true) {

    var fullTime = fullTime
    get() {
        println("Running the custom get")
        return field
    }
    set(value) {
        println("Running the custom set")
        field = value
    }
}
```

Not that getters and setters will be automatically called while referring the variables

```kotlin
fun main () {
    val emp = PEmployee("John")
    println(emp.firstName)
    emp.fullTime = false

    val emp2 = PEmployee("Madhur")
    println(emp2.fullTime);

    val emp3 = PEmployee("Ahuja", false)
    println(emp3.fullTime)
}
```

```console
John
Running the custom set
Running the custom get
true
Running the custom get
false
```

<a name="data"></a>

## Data classes

Data classes are equivalent to POJO

It comes with free [equals](https://kotlinlang.org/docs/reference/equality.html) and [toString](https://kotlinlang.org/docs/reference/data-classes.html) function, very similar to [Lombok](https://projectlombok.org/)

It also comes with a [copy](https://kotlinlang.org/docs/reference/data-classes.html) function as well.

<a name="extension"></a>

## Extension Functions

Syntactic sugar to extend classes with more functions. It doesn't actually extend any class.

```kotlin

fun String.upperFirstAndLast() : String {
    val upperFirst = this.substring(0, 1).toUpperCase() + this.substring(1)
    return upperFirst.substring(0, upperFirst.length - 1) +
            upperFirst.substring(upperFirst.length -1, upperFirst.length).toUpperCase()
}

val s = "this is all in lowercase"
println(s.upperFirstAndLast())
```

Kotlin uses extension functions extensively inside Kotlin Standard Library