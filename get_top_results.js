const data = require('./job_desc.json')
const fs = require('fs');
const request = require('request');

const func = async () => {
  const final_data = [];
  for (let i = 0; i < data.length; i++) {
    const entry = data[i];
    const param = {
      'content': entry.content
    };
    const options = {
      url: 'http://127.0.0.1:8080/',
      json: param
    };
    const response = await req(options);
    console.log("Completed entry " + i + " with status code " + response.resp.statusCode)
    entry['suggested_urls'] = response.body['scores']
    final_data.push(entry)
  }
    fs.writeFileSync('suggested_jobs.json', JSON.stringify(final_data))
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