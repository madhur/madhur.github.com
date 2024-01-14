---
layout: blog-post
title: "The validation data provided must contain class"
excerpt: "The validation data provided must contain class"
disqus_id: /2020/06/28/validation-data-provided-must-contain-class/
tags:
    - Swift
    - ML
---

I have been playing with Apple's [CreateML](https://developer.apple.com/documentation/createml).  Specifically, I have been following Apple's tutorial on [creating text classification models](https://developer.apple.com/documentation/createml/creating_a_text_classifier_model)

The exact code as described in article doesn't work, at least on OSX 10.14 Mojave.

The snippet I have been using is:

```swift
import Cocoa
import CreateML
import NaturalLanguage

let data = try MLDataTable(contentsOf: URL(fileURLWithPath: "/Users/madhur/Desktop/iOS/ML/twitter-sanders-apple3.csv"))
let (trainingData, testingData) = data.randomSplit(by: 0.8, seed: 5)
let sentimentClassifier = try MLTextClassifier(trainingData: trainingData, textColumn: "text", labelColumn: "class")
```

The last line throws the error: `The validation data provided must contain class`

Googling it doesn't help much since this is a very new API. Then, I stumbled upon some of the API's which Apple has marked deprecated, such as several `init()` methods in [MLTextClassifier.ModelParameters](https://developer.apple.com/documentation/createml/mltextclassifier/modelparameters)

Usingi those deprecated methods, somehow resolved the issue:

```swift
import Cocoa
import CreateML
import NaturalLanguage

let data = try MLDataTable(contentsOf: URL(fileURLWithPath: "/Users/madhur/Desktop/iOS/ML/twitter-sanders-apple3.csv"))
let (trainingData, testingData) = data.randomSplit(by: 0.8, seed: 5)
let parameters = MLTextClassifier.ModelParameters.init(validationData: trainingData, algorithm: MLTextClassifier.ModelAlgorithmType.maxEnt(revision: 1), language: NLLanguage.english, textColumnValidationData: "text", labelColumnValidationData: "class")
let sentimentClassifier = try MLTextClassifier(trainingData: trainingData, textColumn: "text", labelColumn: "class", parameters: parameters)
```

Hope this helps anyone encountering this issue. Just for sake of completeness, the complete sample code to generate a text classification model is given below. The generated `mlmodel` can then be imported in an iOS or MacOS App.

```swift
import Cocoa
import CreateML
import NaturalLanguage

let data = try MLDataTable(contentsOf: URL(fileURLWithPath: "/Users/madhur/Desktop/iOS/ML/twitter-sanders-apple3.csv"))
let (trainingData, testingData) = data.randomSplit(by: 0.8, seed: 5)
let parameters = MLTextClassifier.ModelParameters.init(validationData: trainingData, algorithm: MLTextClassifier.ModelAlgorithmType.maxEnt(revision: 1), language: NLLanguage.english, textColumnValidationData: "text", labelColumnValidationData: "class")
let sentimentClassifier = try MLTextClassifier(trainingData: trainingData, textColumn: "text", labelColumn: "class", parameters: parameters)

let evaluationMetrics = sentimentClassifier.evaluation(on: testingData, textColumn: "text", labelColumn: "class") //Training accuracy as a percentage

let evaluationAccuracy = (1.0 - evaluationMetrics.classificationError) * 100
print(evaluationAccuracy)

let metadata = MLModelMetadata(author: "Madhur Ahuja", shortDescription: "A model trained to classify movie review sentiment", version: "1.0")
try sentimentClassifier.write(to: URL(fileURLWithPath: "/Users/madhur/Desktop/iOS/ML/sentiment.mlmodel"), metadata: metadata)
```