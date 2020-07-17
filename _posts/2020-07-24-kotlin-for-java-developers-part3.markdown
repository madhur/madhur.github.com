---
layout: blog-post
title: "Kotlin for Java Developers - Part 3"
excerpt: "Kotlin for Java Developers"
disqus_id: /2020/07/24/kotlin-for-java-developers-part3/
tags:
    - Java
    - Kotlin
---

Conitnuing article on Kotlin for Java Developers, Let's continue the differences:

## Inheritance

Classes are final by default. We have to use `open` keyword to tell compiler to indicate that class is extensible


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