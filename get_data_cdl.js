const fs = require('fs');
const request = require('request');

const func = async (queries,page, searchId) => {
    
    const param = {
      'query': queries.join(','),
      'community': '6451cb04d299148c0dc9ca10',
      'page': page,
      'search_id':searchId
    };
    const headers = {
      'authorization': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjYzY2RhOTA2MWNhMmY5MTIzZGY2ZTgyOSJ9.kbroNq3ioSUPaX_1r_Is-R9Q9ka3fsrmtrCA6AyQs8U',
      'authority': 'textdata.org',
      'origin': 'chrome-extension://bldpjacibfnempiocmnloilpbeliejcl'
    };
    const options = {
      url: 'https://textdata.org/api/search?' + (searchId ? 'search_id=' + param['search_id'] : 'query=' + param['query'] + '&community=' + param['community']) + '&page=' + param['page'],
      headers: headers,
    };
    const response = await req(options);
    const responseBody = JSON.parse(response.body);
    return responseBody;
  }

function req(options) {
    return new Promise(function(resolve, reject) {
      request.get(options, function(err, resp, body) {
        if (err) { reject(err); }
        else { resolve({resp: resp, body: body}); }
      })
    })
  };

const queries = process.argv.slice(2)
const startPage = 0;
const allResponses = [];

(async () => {
  const firstResponse = await func(queries, startPage, null)
  const searchId = firstResponse.search_id;
  const pageCount=Math.ceil(firstResponse.total_num_results/10)

  allResponses.push(firstResponse);

  for (let page = startPage + 1; page < pageCount; page++) {
    const response = await func(queries, page, searchId);
    allResponses.push(response);
  }

  const search_results_page = allResponses.map(response => response.search_results_page);
  console.log(JSON.stringify(search_results_page));
  // console.log("Responses from" + pageCount + "pages in Array form : ", JSON.stringify(search_results_page));
})();