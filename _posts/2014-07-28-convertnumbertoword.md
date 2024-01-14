---
layout: blog-post
title: "Algorithm: Convert number to word"
excerpt: "Algorithm: Convert number to word"
disqus_id: /2014/07/28/convertnumbertoword/
location: New Delhi, India
time: 9:00 PM
js: angular.js
tags:
- Algorithms

---


This time another algorithm, converting a number to word. Try typing in a number below:

<script type="text/javascript">
	

	 function myController($scope)
		{
			$scope.problem={myWord: "madhur", myNum: 55};
		

			$scope.NumberToWords= function(number)
			{
				
			    if (number == 0)
			        return "zero";

			    if (number < 0)
			        return "minus " + $scope.NumberToWords(Math.abs(number));

			    var words = "";

			    if (Math.floor(number / 1000000) > 0)
			    {
			        words += $scope.NumberToWords(Math.floor(number / 1000000)) + " million ";
			        number %= 1000000;
			    }

			    if (Math.floor(number / 1000) > 0)
			    {
			        words += $scope.NumberToWords(Math.floor(number / 1000)) + " thousand ";
			        number %= 1000;
			    }

			    if (Math.floor(number / 100) > 0)
			    {
			        words += $scope.NumberToWords(Math.floor(number / 100)) + " hundred ";
			        number %= 100;
			    }

			    if (number > 0)
			    {
			        if (words != "")
			            words += "and ";

			        var unitsMap = [ "zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen" ];
			        var tensMap = ["zero", "ten", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety" ];

			        if (number < 20)
			            words += unitsMap[number];
			        else
			        {
			            words += tensMap[Math.floor(number / 10)];
			            if ((number % 10) > 0)
			                words += "-" + unitsMap[number % 10];
			        }
			    }

				
				
			    return words;
			}

			$scope.change=function(number)
			{
				$scope.problem.myWord=$scope.NumberToWords(number);				
			}


			$scope.problem.myWord=$scope.NumberToWords($scope.problem.myNum);

		}


</script>

<div ng-app ng-controller="myController">

	<div class="form-group">
		<input type="number" ng-change="change(problem.myNum)" ng-model="problem.myNum"  />
	</div>
	<p/>
	<br/>

    <div   class="alert alert-success" ng-bind="problem.myWord"></div>

</div>

The algorithm in Javascript below. [Click here](https://gist.github.com/madhur/5f4f49149e9ce68f619e) for C# gist.

```js
NumberToWords= function(number)
			{
				
			    if (number == 0)
			        return "zero";

			    if (number < 0)
			        return "minus " + $scope.NumberToWords(Math.abs(number));

			    var words = "";

			    if (Math.floor(number / 1000000) > 0)
			    {
			        words += $scope.NumberToWords(Math.floor(number / 1000000)) + " million ";
			        number %= 1000000;
			    }

			    if (Math.floor(number / 1000) > 0)
			    {
			        words += $scope.NumberToWords(Math.floor(number / 1000)) + " thousand ";
			        number %= 1000;
			    }

			    if (Math.floor(number / 100) > 0)
			    {
			        words += $scope.NumberToWords(Math.floor(number / 100)) + " hundred ";
			        number %= 100;
			    }

			    if (number > 0)
			    {
			        if (words != "")
			            words += "and ";

			        var unitsMap = [ "zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen" ];
			        var tensMap = ["zero", "ten", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety" ];

			        if (number < 20)
			            words += unitsMap[number];
			        else
			        {
			            words += tensMap[Math.floor(number / 10)];
			            if ((number % 10) > 0)
			                words += "-" + unitsMap[number % 10];
			        }
			    }

				
				
			    return words;
			}

```


