---
layout: blog-post
title: "Kotlin for Java Developers"
excerpt: "Kotlin for Java Developers"
disqus_id: /2020/07/10/kotlin-for-java-developers/
tags:
    - Java
    - Kotlin
---

I have been learning [Kotlin](https://kotlinlang.org/) in my free time and I must say I have been glued to it since then due to its conciseness and addressing some of the issues which are there in Java.

Hence, In this part I post, we will look at differences between [Kotlin](https://kotlinlang.org/) and [Java](https://www.java.com/en/) from the programmer's perspective.

We will cover the runtime aspects and interoperability in the later posts.


* [Equality differences](#equality)
* [No checked exceptions](#checked)
* [Wrapper classes](#wrapper)
* [Traditional for loop is not more](#forloop)
* [val and var keywords for immutability](#valvar)
* [Ternary operator is removed](#ternary)
* [instanceOf is removed](#instanceof)
* [Template Strings and Inline variables](#template)

<a name="equality"></a>

### Equality differences. In Kotlin, `==` operator checks for structural equality. Instead triple equals === checks for referential equality

This is one of the most important difference I found and hence it the first one. In Kotlin, `==` will check only structural equality. For example,

Consider a POJO In Java

```java
public class Employee {

    private String name;
    private int id;

    public Employee(String name, int id) {
        this.name = name;
        this.id = id;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Employee employee = (Employee) o;
        return id == employee.id &&
                Objects.equals(name, employee.name);
    }
}
```
We can use this class in Kotlin as follows:

```kotlin
var employee2 = Employee("John", 2)
val employee3 = Employee("John", 2)

println(employee2 == employee3)       // true
println(employee2.equals(employee3))  // true
println(employee2 === employee3)        // false
```

<a name="checked"></a>

## No checked exceptions and no throws keyword
How many times in Java we have to decorate the method with `throws` keyword just because the called method inside it throws a checked exception. I have never been fan of this rule. In my opinion, it should be left to developer to decide on he wants to handle the exception or even completely ignore it.

Kotlin gets rid of this uglier aspect of Java.

<a name="wrapper"></a>

### Wrapper classes for convenient methods such as `println()`
Kotlin provides useful wrapper for many of the convenient functions such as now you can do simply `println("myString")` to print out something to console or even `arrayOf(1,2,3)` to create an array.


<a name="forloop"></a>

### Kotlin gets rid of traditional for loop
The traditional for loop has been omitted in Kotlin in favor of below kind of loop.

```kotlin
val names = listOf("Anne", "Peter", "Jeff")
for (name in names) {
    println(name)
}
```
<a name="valvar"></a>

### `val` and `var` keywords for immutability
Just like Swift and JavaScript, `val` can be used to declare immutable (final in java) and `var` for a mutable object. 
Just like Swift, Kotlin compiler can do type inference. Type information is required only if compiler cannot infer type, which results in lot of conciseness

<a name="ternary"></a>

### Ternary operator is removed
Ternary operator is removed in Java. In contrast to this, `if` keyword has been converted to express. So, you can do something like this in Kotlin:

```kotlin
val max = if (a > b) {
    print("Choose a")
    a
} else {
    print("Choose b")
    b
}
```

<a name="instanceof"></a>

### `instanceOf` is removed, Instead use `is`

This is a welcome change along with [smart casting](https://www.javatpoint.com/kotlin-smart-cast)

In Java, you had to use `instanceOf` operator along with cast, for example:

```java
Object something = employee4;
if (something instanceOf Employee) {
    Employee newEmployee  = (Employee)something;
    System.out.println(newEmployee.name);
}
```

In Kotlin, you can simply do:

```kotlin
var something: Any = employee4
if (something is Employee) {
    println("Something is employee")
    println(something.name)
}
```

That means, Kotlin compiler will intelligently figure out that something is an Employee object and allow you to use all the employee properties on that instance variable itself.

This looks like a small change but in reality can open doors to very elegant code especially when combined with [Non null types](https://kotlinlang.org/docs/reference/null-safety.html)

<a name="template"></a>

### Template Strings

This is a feature which every new language is coming up. For example, we can print variables inline and also have multiline strings. For example:

This is a great improvement over Java, where we have to use newlines and escape quotes in these scenarios.

```kotlin
un indentedStringLiteral() =
    """
        First Line
        Second Line
        Third Line
    """

fun unindentedStringLiteral() =
    """
        First Line
        Second Line
        Third Line
    """.trimIndent()


fun printSum(a: Int, b: Int) {
    println("sum of $a and $b is ${a + b}")
}
```


That's it for now. I am still going through rest of the features and excited about using this language in my real world projects. The great thing about Kotlin is that it is interoperable with existing 
Java projects by just adding [Kotlin Standard Library](https://kotlinlang.org/api/latest/jvm/stdlib/) as a runtime dependency.

Watch out this space for the next part of the article

