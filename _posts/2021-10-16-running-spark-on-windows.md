---
layout: blog-post
title: "Running Spark on Windows"
excerpt: "Running Spark on Windows"
disqus_id: /2021/10/16/running-spark-on-windows/
tags:
    - Spark
---

Assuming you have spark downloaded on machine, you would run `./spark-class org.apache.spark.deploy.master.Master` to run the Spark Master controller

```text
PS D:\spark\spark\bin>  ./spark-class org.apache.spark.deploy.master.Master
Using Spark's default log4j profile: org/apache/spark/log4j-defaults.properties
21/10/16 09:53:02 INFO Master: Started daemon with process name: 4804@DESKTOP-QCP2G4K
21/10/16 09:53:02 WARN Shell: Did not find winutils.exe: {}
21/10/16 09:53:02 WARN NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
21/10/16 09:53:02 INFO SecurityManager: Changing view acls to: user
21/10/16 09:53:02 INFO SecurityManager: Changing modify acls to: user
21/10/16 09:53:02 INFO SecurityManager: Changing view acls groups to:
21/10/16 09:53:02 INFO SecurityManager: Changing modify acls groups to:
21/10/16 09:53:02 INFO SecurityManager: SecurityManager: authentication disabled; ui acls disabled; users  with view permissions: Set(user); groups with view permissions: Set(); users  with modify permissions: Set(user); groups with modify permissions: Set()
21/10/16 09:53:03 INFO Utils: Successfully started service 'sparkMaster' on port 7077.
21/10/16 09:53:03 INFO Master: Starting Spark master at spark://172.21.128.1:7077
21/10/16 09:53:03 INFO Master: Running Spark version 3.1.2
21/10/16 09:53:03 INFO Utils: Successfully started service 'MasterUI' on port 8080.
21/10/16 09:53:03 INFO MasterWebUI: Bound MasterWebUI to 0.0.0.0, and started at http://DESKTOP-QCP2G4K.mshome.net:8080
21/10/16 09:53:03 INFO Master: I have been elected leader! New state: ALIVE
```

The spark UI will now be running at http://localhost:8080

Now, we want to run the spark executor using `./spark-class org.apache.spark.deploy.worker.Worker spark://172.21.128.1:7077`

```text
PS D:\spark\spark\bin> ./spark-class org.apache.spark.deploy.worker.Worker spark://172.21.128.1:7077
Using Spark's default log4j profile: org/apache/spark/log4j-defaults.properties
21/10/16 09:56:12 INFO Worker: Started daemon with process name: 8800@DESKTOP-QCP2G4K
21/10/16 09:56:12 WARN Shell: Did not find winutils.exe: {}
21/10/16 09:56:12 WARN NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
21/10/16 09:56:12 INFO SecurityManager: Changing view acls to: user
21/10/16 09:56:12 INFO SecurityManager: Changing modify acls to: user
21/10/16 09:56:12 INFO SecurityManager: Changing view acls groups to:
21/10/16 09:56:12 INFO SecurityManager: Changing modify acls groups to:
21/10/16 09:56:12 INFO SecurityManager: SecurityManager: authentication disabled; ui acls disabled; users  with view permissions: Set(user); groups with view permissions: Set(); users  with modify permissions: Set(user); groups with modify permissions: Set()
21/10/16 09:56:12 INFO Utils: Successfully started service 'sparkWorker' on port 57088.
21/10/16 09:56:12 INFO Worker: Worker decommissioning not enabled, SIGPWR will result in exiting.
21/10/16 09:56:13 INFO Worker: Starting Spark worker 172.21.128.1:57088 with 12 cores, 30.9 GiB RAM
21/10/16 09:56:13 INFO Worker: Running Spark version 3.1.2
21/10/16 09:56:13 INFO Worker: Spark home: D:\spark\spark\bin\..
21/10/16 09:56:13 INFO ResourceUtils: ==============================================================
21/10/16 09:56:13 INFO ResourceUtils: No custom resources configured for spark.worker.
21/10/16 09:56:13 INFO ResourceUtils: ==============================================================
21/10/16 09:56:13 INFO Utils: Successfully started service 'WorkerUI' on port 8081.
21/10/16 09:56:13 INFO WorkerWebUI: Bound WorkerWebUI to 0.0.0.0, and started at http://DESKTOP-QCP2G4K.mshome.net:8081
21/10/16 09:56:13 INFO Worker: Connecting to master 172.21.128.1:7077...
21/10/16 09:56:13 INFO TransportClientFactory: Successfully created connection to /172.21.128.1:7077 after 21 ms (0 ms spent in bootstraps)
21/10/16 09:56:13 INFO Worker: Successfully registered with master spark://172.21.128.1:7077
```


Spark is now ready to be used in any application such as Java.

```java
@Configuration
public class SparkConfig {

    @Value("${spark.app.name}")
    private String appName;
    @Value("${spark.master}")
    private String masterUri;

    @Bean
    public SparkConf conf() {
        SparkConf conf =
                new SparkConf()
                        .setAppName("local-1634217252353")
                        .setMaster("spark://172.21.128.1:7077");
        return conf;
    }

    @Bean
    public JavaSparkContext sc() {
        JavaSparkContext sc = new JavaSparkContext(conf());
        return sc;
    }
}
```