---
layout: blog-post
title: "Must have Java code analysis Tools - Part 2"
excerpt: "Must have Java code analysis Tools - Part 2"
disqus_id: /2020/02/02/must-have-java-code-analysis-tools-part2/
tags:
- Java
---

In the last post, we looked at [checkstyle](https://github.com/checkstyle/checkstyle), which focuses on the code linting at the source level.

In this post, we will look at [SpotBugs](https://spotbugs.github.io/), which is a successor of [FindBugs](http://findbugs.sourceforge.net/). SpotBugs works at the bytecode level instead of the source level. Hence it is able, to find out possible bugs in your java code.

The list of entire checks which SpotBugs finds can be found [here](https://spotbugs.readthedocs.io/en/latest/bugDescriptions.html)

## Running with build process

Again, SpotBugs is most useful when integrated with build tool such as Maven or Gradle.

For example, We use the following section in [pom.xml](https://maven.apache.org/guides/introduction/introduction-to-the-pom.html) to run SpotBugs as part of build process


```xml
<plugin>
	<groupId>com.github.spotbugs</groupId>
	<artifactId>spotbugs-maven-plugin</artifactId>
	<version>${spotbugs.version}</version>
	<configuration>
		<effort>Max</effort>
		<threshold>Low</threshold>
		<xmlOutput>true</xmlOutput>
		<failOnError>true</failOnError>
		<excludeFilterFile>spotbugs-exclude.xml</excludeFilterFile>
	</configuration>
		<executions>
			<execution>
				<phase>compile</phase>
				<goals>
					<goal>check</goal>
				</goals>
			</execution>
		</executions>
	</plugin>
```

Here setting `failsOnError`  attribute `true` causes the build to fail if violations are fail.

There might be certain bugs, which you do not want SpotBugs to alert on. They can be configured in an exclusion file. As shown in the above example, it is configured in `spotbugs-exclude.xml`.

The exclusions can be configured at class level or even method level. Below XML is an example of exclusion file.

```xml
<!-- This file specifies a spotbugs filter for excluding reports that
     should not be considered errors.

     The format of this file is documented at:

       https://spotbugs.readthedocs.io/en/latest/filter.html

     When possible, please specify the full names of the bug codes,
     using the pattern attribute, to make it clearer what reports are
     being suppressed.  You can find a listing of codes at:

       https://spotbugs.readthedocs.io/en/latest/bugDescriptions.html
  -->

<FindBugsFilter>

    <Match>
        <Or>
            <!-- Ignore checking for generated parser classes -->
            <Class name="io.undertow.client.http.HttpResponseParser$$generated"/>
            <Class name="io.undertow.server.protocol.http.HttpRequestParser$$generated"/>
            <!-- Ignore checking for generated JMH benchmarking classes -->
            <Package name="io.undertow.benchmarks.generated"/>
        </Or>
    </Match>

    <!-- Ignore spotbugs reports from incomplete detectors -->
    <Match>
        <Bug pattern="TESTING"/>
    </Match>

    <!-- We don't mind having redundant checks for null, it is more error prone to later changes -->
    <Match>
        <Bug pattern="RCN_REDUNDANT_NULLCHECK_OF_NONNULL_VALUE"/>
    </Match>

    <!-- Ignore negating result of compareTo -->
    <Match>
        <Bug pattern="RV_NEGATING_RESULT_OF_COMPARETO"/>
    </Match>

    <!-- Ignore class naming convention issues -->
    <Match>
        <Bug pattern="NM_CLASS_NAMING_CONVENTION"/>
    </Match>

    <!-- Ignore unread public and protected fields as someone may depend on Undertow and use them in their app -->
    <Match>
        <Bug pattern="URF_UNREAD_PUBLIC_OR_PROTECTED_FIELD"/>
    </Match>

    <!-- False positives => ignoring, the field is read in tests -->
    <Match>
        <Bug pattern="URF_UNREAD_FIELD"/>
        <Or>
            <And>
                <Class name="io.undertow.server.protocol.ajp.AjpRequestParseState"/>
                <Field name="dataSize"/>
            </And>
        </Or>
    </Match>

    <!-- False positives => ignoring, the field is regular boolean, no complex bitwise operation is in place here -->
    <Match>
        <Bug pattern="BIT_IOR"/>
        <Or>
            <And>
                <Class name="io.undertow.conduits.AbstractFixedLengthStreamSinkConduit"/>
            </And>
        </Or>
    </Match>

    <!-- field is always incremented/decremented inside synchronized blocks using the same lock -->
    <Match>
        <Bug pattern="VO_VOLATILE_INCREMENT"/>
        <Or>
            <And>
                <Class name="io.undertow.server.protocol.framed.AbstractFramedStreamSinkChannel"/>
                <Field name="waiterCount"/>
            </And>
            <And>
                <Class name="io.undertow.server.handlers.proxy.mod_cluster.NodeLbStatus"/>
                <Field name="elected"/>
            </And>
            <And>
                <Class name="io.undertow.websockets.jsr.SessionContainer"/>
                <Field name="waiterCount"/>
            </And>
        </Or>
    </Match>

    <!--Stream id in HTTP/2 is always unsigned int per spec -->
    <Match>
        <Bug pattern="IM_BAD_CHECK_FOR_ODD"/>
        <Class name="io.undertow.protocols.http2.Http2Channel"/>
        <Method name="isClient"/>
    </Match>

    <!-- Even per javadoc of Object.wait(), this should be always used in loop. It is on purpose -->
    <Match>
        <Bug pattern="WA_NOT_IN_LOOP"/>
        <Or>
            <And>
                <Class name="io.undertow.protocols.ssl.SslConduit"/>
                <Method name="~await.*"/>
            </And>
            <And>
                <Class name="io.undertow.server.protocol.framed.AbstractFramedStreamSourceChannel"/>
                <Method name="awaitReadable"/>
            </And>
            <And>
                <Class name="io.undertow.server.protocol.framed.AbstractFramedStreamSinkChannel"/>
                <Method name="awaitWritable"/>
            </And>
        </Or>
    </Match>

    <!-- Ignore returning references to internal representations of objects -->
    <Match>
        <Bug pattern="EI_EXPOSE_REP"/>
    </Match>

    <!-- Ignoring when internal representation stores reference to external representation -->
    <Match>
        <Bug pattern="EI_EXPOSE_REP2"/>
    </Match>

    <!-- Intentional switch case follow through -->
    <Match>
        <Bug pattern="SF_SWITCH_FALLTHROUGH"/>
        <Or>
            <And>
                <Class name="io.undertow.protocols.ajp.AjpResponseParser"/>
                <Method name="parse" params="java.nio.ByteBuffer" returns="void"/>
            </And>
            <And>
                <Class name="io.undertow.server.protocol.ajp.AjpRequestParser"/>
                <Method name="parse"/>
            </And>
            <And>
                <Class name="io.undertow.util.Cookies"/>
                <Method name="parseCookie"/>
            </And>
            <And>
                <Class name="io.undertow.util.PathTemplate"/>
                <Method name="create"/>
            </And>
        </Or>
    </Match>

    <!-- Path has always some elements in our cases => ignoring -->
    <Match>
        <Bug pattern="NP_NULL_ON_SOME_PATH_FROM_RETURN_VALUE"/>
        <Class name="io.undertow.server.handlers.resource.PathResource"/>
    </Match>

    <!-- The PathTemplate equivalent always exist, checked already by the contains method -->
    <Match>
        <Bug pattern="NP_NULL_ON_SOME_PATH"/>
        <Class name="io.undertow.util.PathTemplateMatcher"/>
    </Match>

    <!-- Ignoring switch cases with no default, all cases which can occur are covered -->
    <!-- TODO: Discuss with developer, whether not to add there some exception being thrown in such cases -->
    <Match>
        <Bug pattern="SF_SWITCH_NO_DEFAULT"/>
    </Match>


    <!-- Intentional throwing RuntimeException instead of checked exception -->
    <Match>
        <Bug pattern="REC_CATCH_EXCEPTION"/>
        <Or>
            <!-- Intentional throwing RuntimeException instead of checked exception -->
            <And>
                <Class name="io.undertow.Undertow"/>
                <Method name="start"/>
            </And>

            <!-- Intentional throwing RuntimeException instead of checked exception -->
            <And>
                <Class name="io.undertow.server.handlers.proxy.mod_cluster.MCMPHandler"/>
                <Method name="processConfig"/>
            </And>

            <!-- Intentional not throwing exception -->
            <And>
                <Class name="io.undertow.util.FlexBase64$Encoder"/>
                <Method name="encodeString"/>
            </And>

            <!-- Intentional not throwing exception -->
            <And>
                <Class name="io.undertow.protocols.alpn.JDK9AlpnProvider$1"/>
                <Method name="run"/>
            </And>
        </Or>
    </Match>

    <!-- The SQL is created based on configuration of the Handler => when proper configuration is created,
    then the risk of SQL injection is evaded -->
    <Match>
        <Bug pattern="SQL_PREPARED_STATEMENT_GENERATED_FROM_NONCONSTANT_STRING"/>
        <Class name="io.undertow.server.handlers.JDBCLogHandler"/>
        <Method name="prepareStatement"/>
    </Match>

    <!--Some inner subclasses of the AjpClientChannel class require to be non static, we want all of the same type inner -->
    <!--classes to be the same -->
    <Match>
        <Bug pattern="SIC_INNER_SHOULD_BE_STATIC"/>
        <Class name="~io\.undertow\.protocols\.ajp\.AjpClientChannel\$.*"/>
    </Match>

    <!-- Is done actually only once, no harm in it -->
    <Match>
        <Bug pattern="DMI_RANDOM_USED_ONLY_ONCE"/>
        <Class name="io.undertow.util.HttpString"/>
    </Match>

    <Match>
        <Bug pattern="EQ_COMPARETO_USE_OBJECT_EQUALS"/>
        <Or>
            <Class name="io.undertow.server.handlers.encoding.EncodingMapping"/>
            <Class name="~.*AlpnOpenListener\$ListenerEntry"/>
        </Or>
    </Match>

    <!-- MCMPAdvertiseTask is used only as single background thread for doing advertising -->
    <Match>
        <Bug pattern="STCAL_INVOKE_ON_STATIC_DATE_FORMAT_INSTANCE"/>
        <Class name="io.undertow.server.handlers.proxy.mod_cluster.MCMPAdvertiseTask"/>
    </Match>


    <!--We don't care whether it is Runtime or checked exception-->
    <Match>
        <Bug pattern="REC_CATCH_EXCEPTION"/>
        <Class name="io.undertow.servlet.handlers.security.SSLInformationAssociationHandler"/>
        <Method name="getCerts"/>
    </Match>

    <!--Ignoring checking for examples-->
    <Match>
        <Package name="~io\.undertow\.examples.*"/>
    </Match>

    <!-- The proper class type returned is handled by createInstance() method being overridden for each subclass => ignoring -->
    <Match>

        <Bug pattern="CN_IDIOM_NO_SUPER_CALL"/>
        <Or>
            <Class name="io.undertow.servlet.api.SecurityInfo"/>
            <Class name="io.undertow.servlet.api.AuthMethodConfig"/>
            <Class name="io.undertow.servlet.api.DeploymentInfo"/>
            <Class name="io.undertow.servlet.api.LoginConfig"/>
            <Class name="io.undertow.servlet.api.FilterInfo"/>
            <Class name="io.undertow.servlet.api.ServletInfo"/>
            <Class name="io.undertow.websockets.jsr.WebSocketDeploymentInfo"/>
        </Or>
    </Match>

    <!-- intentional -->
    <Match>
        <Bug pattern="DM_DEFAULT_ENCODING"/>
        <Or>
            <Class name="io.undertow.servlet.spec.ServletPrintWriterDelegate"/>
        </Or>
    </Match>

    <Match>
        <Bug pattern="UG_SYNC_SET_UNSYNC_GET"/>
        <Class name="io.undertow.servlet.spec.AsyncContextImpl"/>
    </Match>

    <Match>
        <Bug pattern="RV_RETURN_VALUE_IGNORED_NO_SIDE_EFFECT"/>
    </Match>

    <Match>
        <Bug pattern="DLS_DEAD_LOCAL_STORE"/>
        <Class name="io.undertow.predicate.PredicatesHandler$RestartHandlerBuilder$1$1"/>
        <Method name="handleRequest"/>
    </Match>

    <!-- Method is actually fine-->
    <Match>
        <Bug pattern="NP_NONNULL_PARAM_VIOLATION"/>
        <Class name="io.undertow.server.protocol.http.AlpnOpenListener$AlpnConnectionListener"/>
    </Match>
    <!-- Field can be modified by code between the first check-->
    <Match>
        <Bug pattern="RCN_REDUNDANT_NULLCHECK_WOULD_HAVE_BEEN_A_NPE"/>
        <Class name="io.undertow.client.http.HttpClientConnection$ClientReadListener" />
    </Match>
    <!-- Comparison of cookies path and domain with == before invoking equals is necessary because
         both could be null; only if the == fails we check for one of them != null && equals the other -->
    <Match>
        <Bug pattern="ES_COMPARING_STRINGS_WITH_EQ"/>
        <Class name="io.undertow.servlet.spec.HttpServletResponseImpl"/>
        <Method name="addCookie"/>
    </Match>
</FindBugsFilter>
```


