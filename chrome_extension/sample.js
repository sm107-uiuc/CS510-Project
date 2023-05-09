// Copyright 2023 Google LLC
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     https://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.


chrome.runtime.onInstalled.addListener(function () {
  // Create one test item for each context type.
  let contexts = [
    'selection'
  ];
  for (let i = 0; i < contexts.length; i++) {
    let context = contexts[i];
    let title = "Send the selected job description to TextData.org";
    chrome.contextMenus.create({
      title: title,
      contexts: [context],
      id: context
    });
  }

  chrome.contextMenus.onClicked.addListener(async function (info, tab) {
    console.log("info: " + JSON.stringify(info));
    //job_description = "Programming Skills – knowledge of statistical programming languages like R, Python, and database query languages like SQL, Hive, Pig is desirable. Familiarity with Scala, Java, or C++ is an added advantage.,Statistics – Good applied statistical skills, including knowledge of statistical tests, distributions, regression, maximum likelihood estimators, etc. Proficiency in statistics is essential for data-driven companies. ,Machine Learning – good knowledge of machine learning methods like k-Nearest Neighbors, Naive Bayes, SVM, Decision Forests. ,Strong Math Skills (Multivariable Calculus and Linear Algebra) - understanding the fundamentals of Multivariable Calculus and Linear Algebra is important as they form the basis of a lot of predictive performance or algorithm optimization techniques. ,Data Wrangling – proficiency in handling imperfections in data is an important aspect of a data scientist job description. ,Experience with Data Visualization Tools like matplotlib, ggplot, d3.js., Tableau that help to visually encode data,Excellent Communication Skills – it is incredibly important to describe findings to a technical and non-technical audience.,Strong Software Engineering Background,Hands-on experience with data science tools,Problem-solving aptitude,Analytical mind and great business sense,Degree in Computer Science, Engineering or relevant field is preferred,Proven Experience as Data Analyst or Data Scientist"
    job_description = info.selectionText;
    console.log("job_description: " + job_description);
    const param = {
      'content': job_description
    };

    console.log("param: " + JSON.stringify(param));

    const headers = {
      'origin': 'chrome-extension://gkcdcpgfcfpoibajaakckbdnapfblgej'
    }; 

    const options = {
      url: 'http://161.35.6.154:8080/',
      formData: param,
      headers: headers,
    };

    //make http request using fetch with body containing job description
    const response = await fetch(options.url, {
      method: 'POST',
      body: JSON.stringify(options.formData),
      headers: {
        'Content-Type': 'application/json'
      }
    });

    //log response only after it is received
    const data = await response.json();
    console.log("response: " + JSON.stringify(data));

    requested_keywords = data['keywords'];

    //convert requested_keywords to comma separated list
    requested_keywords = requested_keywords.join(",");
    //replace ' ' with '_' in requested_keywords

    requested_keywords = requested_keywords.replace(/ /g, "_");
    console.log("requested_keywords: " + requested_keywords);

    const new_param = {
      'query': 'machine_learning&',
      'community': '6451cb04d299148c0dc9ca10'
    };

    const new_headers = {
      'authorization': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjYzY2RhOTA2MWNhMmY5MTIzZGY2ZTgyOSJ9.kbroNq3ioSUPaX_1r_Is-R9Q9ka3fsrmtrCA6AyQs8U',
      'authority': 'textdata.org',
      'origin': 'chrome-extension://bldpjacibfnempiocmnloilpbeliejcl'
    };

    const request_url = 'https://textdata.org/api/search?' + 'query=' + requested_keywords + '&community=' + new_param['community'];

    console.log("request_url: " + request_url);

    const new_options = {
      url: request_url,
      headers: headers,
    };

    //make http request using fetch for the request url
    const new_response = await fetch(new_options.url, {
      method: 'GET',
      headers: new_headers
    });


    const new_data = await new_response.json();
    console.log("final resp: " + JSON.stringify(new_data));



  }
  );
});
