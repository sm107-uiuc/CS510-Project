const fs = require('fs');
const request = require('request');
const curl = require('curl');

const func = async () => {
  const data = JSON.parse(fs.readFileSync('final_out4.json'));
  for (let i = 10; i < data.length; i++) {
    const entry = data[i];
    entry['keywords'] = entry['keywords'].map(keyword => keyword.split(' ').join('_'));
    const param = {
      'highlighted_text': '',
      'source_url': entry['url'],
      'community': '6451cb04d299148c0dc9ca10',
      'explanation': entry['title'] + ' #' + entry['keywords'].join(' #'),
    };
    const headers = {
      'authorization': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjYzYzc0YzdmYTc4Njg3YTQ2ZWRhODQ5NCJ9.U9AKCQgBeZMOj9Ww-8F4THsFLNiqMf_d6kXaJFtlYp8',
      'authority': 'textdata.org',
      'origin': 'chrome-extension://gkcdcpgfcfpoibajaakckbdnapfblgej'
    };
    const options = {
      url: 'https://textdata.org/api/submission/',
      formData: param,
      headers: headers,
    };
    const response = await req(options);
    console.log("Completed entry " + i + " with status code " + response.resp.statusCode)
  }
}

function req(options) {
    return new Promise(function(resolve, reject) {
      request.post(options, function(err, resp, body) {
        if (err) { reject(err); }
        else { resolve({resp: resp, body: body}); }
      })
    })
  };


func();