---
layout: blog-post
title: "Taking memory dump of JVM Applications"
excerpt: "Taking memory dump of JVM Applications"
disqus_id: /2023/04/23/taking-memory-dump-jvm/
tags:
    - Java
---

It seems taking memory dump of JVM applications have changed in recent versions.

Pre java11, heap dump was takn using the jmap command as follows:

```
➜ ~/.sdkman/candidates/java/11.0.12-open/bin/jmap -dump:live, format=b,file=dump.hprof 169213                                                                                                                                                           
Error: More than one non-option argument
Cannot connect to core dump or remote debug server. Use jhsdb jmap instea
```
However, it doesn't work in Java11. The new command is:

```
➜ ~/.jdks/corretto-11.0.13/bin/jhsdb jmap --binaryheap --dumpfile heap.hprof --pid 169213                                                                                                                  
Attaching to process ID 169213, please wait...
Debugger attached successfully.
Server compiler detected.
JVM version is 11.0.13+8-LTS
heap written to heap.hprof
```

There is another error which we have faced while taking heap dump of JVM11 applications

```
Attaching to process ID 226420, please wait...
Debugger attached successfully.
Server compiler detected.
JVM version is 11.0.19+7-LTS
Exception in thread "main" java.lang.IndexOutOfBoundsException: bad SID 0
	at jdk.hotspot.agent/sun.jvm.hotspot.runtime.vmSymbols.symbolAt(vmSymbols.java:58)
	at jdk.hotspot.agent/sun.jvm.hotspot.oops.InstanceKlass.getFieldName(InstanceKlass.java:353)
	at jdk.hotspot.agent/sun.jvm.hotspot.oops.InstanceKlass.<init>(InstanceKlass.java:153)
	at jdk.internal.reflect.GeneratedConstructorAccessor3.newInstance(Unknown Source)
	at java.base/jdk.internal.reflect.DelegatingConstructorAccessorImpl.newInstance(DelegatingConstructorAccessorImpl.java:45)
	at java.base/java.lang.reflect.Constructor.newInstance(Constructor.java:490)
	at jdk.hotspot.agent/sun.jvm.hotspot.runtime.VMObjectFactory.newObject(VMObjectFactory.java:58)
	at jdk.hotspot.agent/sun.jvm.hotspot.runtime.VirtualBaseConstructor.instantiateWrapperFor(VirtualBaseConstructor.java:104)
	at jdk.hotspot.agent/sun.jvm.hotspot.oops.Metadata.instantiateWrapperFor(Metadata.java:73)
	at jdk.hotspot.agent/sun.jvm.hotspot.oops.java_lang_Class.asKlass(java_lang_Class.java:67)
	at jdk.hotspot.agent/sun.jvm.hotspot.utilities.HeapHprofBinWriter.writeClass(HeapHprofBinWriter.java:611)
	at jdk.hotspot.agent/sun.jvm.hotspot.utilities.AbstractHeapGraphWriter$1.doObj(AbstractHeapGraphWriter.java:82)
	at jdk.hotspot.agent/sun.jvm.hotspot.oops.ObjectHeap.iterateLiveRegions(ObjectHeap.java:356)
	at jdk.hotspot.agent/sun.jvm.hotspot.oops.ObjectHeap.iterate(ObjectHeap.java:174)
	at jdk.hotspot.agent/sun.jvm.hotspot.utilities.AbstractHeapGraphWriter.write(AbstractHeapGraphWriter.java:51)
	at jdk.hotspot.agent/sun.jvm.hotspot.utilities.HeapHprofBinWriter.write(HeapHprofBinWriter.java:443)
	at jdk.hotspot.agent/sun.jvm.hotspot.tools.JMap.writeHeapHprofBin(JMap.java:182)
	at jdk.hotspot.agent/sun.jvm.hotspot.tools.JMap.run(JMap.java:97)
	at jdk.hotspot.agent/sun.jvm.hotspot.tools.Tool.startInternal(Tool.java:260)
	at jdk.hotspot.agent/sun.jvm.hotspot.tools.Tool.start(Tool.java:223)
	at jdk.hotspot.agent/sun.jvm.hotspot.tools.Tool.execute(Tool.java:118)
	at jdk.hotspot.agent/sun.jvm.hotspot.tools.JMap.main(JMap.java:176)
	at jdk.hotspot.agent/sun.jvm.hotspot.SALauncher.runJMAP(SALauncher.java:369)
	at jdk.hotspot.agent/sun.jvm.hotspot.SALauncher.main(SALauncher.java:538)

```

It seems this is a known issue filed here [https://bugs.openjdk.org/browse/JDK-8237544](https://bugs.openjdk.org/browse/JDK-8237544)

If anyone knows the resolution for this other than upgrading the JVM version, please let me know in the comments.