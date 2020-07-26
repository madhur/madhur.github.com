---
layout: blog-post
title: "Kotlin for Java Developers - Part 3"
excerpt: "Kotlin for Java Developers"
disqus_id: /2020/07/26/kotlin-for-java-developers-part3/
tags:
    - Java
    - Kotlin
---

Continuing article on Kotlin for Java Developers, Let's continue the differences:

* [Inheritance](#inheritance)
* [Singletons](#singletons)
* [when instead of switch](#when)
* [Mutable variables inside lambda](#mutable)
* [With keyword](#with)


<a name="inheritance"></a>

## Inheritance

Classes are final by default. We have to use `open` keyword to tell compiler to indicate that class is extensible

<a name="singletons"></a>

## Singletons

In Kotlin, singletons can be simply defined using object keyword

```kotlin
object CompanyCommunications {

    val currentYear = Year.now().value

    fun getTagLine() = "Our company rocks"
    fun getCopyrihtLine() = "Copyright";
}
```

Static keyword doesn't exist in Kotlin. 

`object` keyword can also be used to emulate static variables

```kotlin
class SomeClass {
    companion object {
        private val privateVar = 6

        fun accessPrivateVar() {
            println("I am printing $privateVar")
        }
    }
}
```

<a name="when"></a>

## when instead of switch

Kotlin doesn't have `switch` keyword, instead it introduced `when` keyword

```kotlin
val z = when (something) {
    is String ->{
        println(something.toUpperCase())
        1
    }
    is BigDecimal -> {
        println(something.remainder(BigDecimal(10.5)))
        2
    }
    is Int -> {
        println("${something - 22}")
        3
    }
    else -> {
        println("Doesn't match anything")
        -1
    }
}
```
<a name="mutable"></a>

## Mutable variables inside lambda

In Kotlin, mutable variables can be accessed inside a lambda function

<a name="with"></a>

## With keyword

[with](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin/with.html) keyword can be used in Kotlin to make code more concise when lot of operations are done on a variable
For example,

```kotlin
fun countTo100(): String {
    val numbers = StringBuilder()
    for (i in 1..99) {
        numbers.append(i)
        numbers.append(", ")
    }
    numbers.append(100)
    return numbers.toString()
}
```
Can be written as, 

```kotlin
fun countTo100With() =
     with(StringBuilder()) {
        for (i in 1..99) {
            append(i)
            append(", ")
        }
        append(100)
        toString()
    }
```

