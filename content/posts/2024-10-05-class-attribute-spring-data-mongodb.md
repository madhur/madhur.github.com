---
slug: "class-attribute-spring-data-mongodb"
title: _class attribute in Spring data MongoDB_
date: '2024-10-05'
description: _class attribute in Spring data MongoDB
tags:
  - Spring
  - MongoDB
draft: false
params:
  disqus_id: /2024/10/05/class-attribute-spring-data-mongodb/
---

Spring data MongoDB adds a `_class` attribute to every document written to [MongoDB](https://www.mongodb.com/)

If we want to prvent adding Spring Data MongoDB from adding `_class` attribute, we can configure this behaviour through:


```java
@Configuration
public class MongoConfig extends AbstractMongoClientConfiguration {
    @Override
    protected boolean autoIndexCreation() {
        return true;
    }
    
    @Bean
    public MappingMongoConverter mappingMongoConverter(MongoDatabaseFactory databaseFactory, MongoMappingContext mappingContext) {
        DbRefResolver dbRefResolver = new DefaultDbRefResolver(databaseFactory);
        MappingMongoConverter converter = new MappingMongoConverter(dbRefResolver, mappingContext);
        converter.setTypeMapper(new DefaultMongoTypeMapper(null));
        return converter;
    }
}
```


