const fs = require('fs');
const request = require('request');
const curl = require('curl');

const func = async () => {
    const param = {
      'query': 'machine_learning&',
      'community': '6451cb04d299148c0dc9ca10'
    };
    const headers = {
      'authorization': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjYzY2RhOTA2MWNhMmY5MTIzZGY2ZTgyOSJ9.kbroNq3ioSUPaX_1r_Is-R9Q9ka3fsrmtrCA6AyQs8U',
      'authority': 'textdata.org',
      'origin': 'chrome-extension://bldpjacibfnempiocmnloilpbeliejcl'
    };
    const options = {
      url: 'https://textdata.org/api/search?' + 'query=' + param['query'] + '&community=' + param['community'],
      headers: headers,
    };
    const response = await req(options);
    console.log("for machine_learning " + " with status code " + JSON.stringify(response.body))
  }

function req(options) {
    return new Promise(function(resolve, reject) {
      request.get(options, function(err, resp, body) {
        if (err) { reject(err); }
        else { resolve({resp: resp, body: body}); }
      })
    })
  };


func();