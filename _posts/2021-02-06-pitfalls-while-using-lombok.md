---
layout: blog-post
title: "Pitfalls while using Lombok with Java Development"
excerpt: "Pitfalls while using Lombok with Java Development"
disqus_id: /2021/02/06/pitfalls-while-using-lombok/
tags:
    - Java
---

These days Java developers almost universally prefers
[Lombok](https://projectlombok.org/) because it cuts down on the boilerplate
code you have to write while writing new classes.

Specifically, it allows to generate getters, setters, toString, hashCode and
constructor function automatically.

However, there are some pitfalls which developers must be aware of while using
Lombok:

For example, when we have boolean fields in our class such as follows:

```java
@Getter
@Setter
public class TestBean {

    private String str;

    private boolean isNew;

    private Boolean isOld;
}
```

Here is what the Lombok generates by default:

```java
package lombok;

public class TestBean {
    private String str;
    private boolean isNew;
    private Boolean isOld;

    public TestBean() {
    }

    public String getStr() {
        return this.str;
    }

    public boolean isNew() {
        return this.isNew;
    }

    public Boolean getIsOld() {
        return this.isOld;
    }

    public void setStr(String str) {
        this.str = str;
    }

    public void setNew(boolean isNew) {
        this.isNew = isNew;
    }

    public void setIsOld(Boolean isOld) {
        this.isOld = isOld;
    }
}
```

Notice the different strategy used to generate the `boolean` primitive
getters/setters and boolean object getters/setters.

The `isNew` getter does not have `get` prefixed. The `isNew` setter does not
have `is` keyword which is part of variable.

Whereas, this is not the cause with Object boolean.

This is documented on [Lombok page](https://projectlombok.org/features/GetterSetter)

> For boolean fields that start with is immediately followed by a title-case letter, nothing is prefixed to generate the getter name.

> Any variation on boolean will not result in using the is prefix instead of the get prefix; for example, returning java.lang.Boolean results in a get prefix, not an is prefix.

This is one of the many pitfalls while using Lombok. These discrepancy can cause
serialization / deserialization failures if the developer is not aware of the same.