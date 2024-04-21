const express = require('express');
const redis = require('redis');
const app = express()
const { v4: uuidv4 } = require('uuid');
const cookieParser = require('cookie-parser');
const path = require('path');
const nunjucks = require('nunjucks');
const PORT = 3000;
const client = redis.createClient({
    'url': process.env.REDIS_URL
})

client.on('error', err => console.log('Redis Client Error', err));
client.connect();

app.engine('html', nunjucks.render);
app.set('view engine', 'html');
app.use(cookieParser());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.set('etag', false);

nunjucks.configure(path.resolve('/app/views'), {
    autoescape: true,
    express: app
});

async function authReq(req, res, next) {
    const UID = req.cookies.uid ? req.cookies.uid : undefined;
    if (UID) {
        const uid_exists = await client.exists(UID);
        if (uid_exists) {
            req.user = UID;
            res.set("X-Cache-UID", UID);
        }
    }
    next();
}

app.use(authReq)

app.use(express.static(path.join(__dirname, 'public'), {
    etag: false
}));

app.get('/', (req, res) => {
    if (req.user) {
        return res.render('index', { uid: req.user });
    }
    const UID = uuidv4();
    res.set("X-Cache-UID", UID);
    res.cookie("uid", UID);
    return res.render('index', { uid: UID });
})

app.post('/debug', async (req, res) => {
    const IPS = req.headers['x-forwarded-for']
        .split(',')
        .map(ip => ip.trim());
    // Developers will be forwarded from
    // the krusty krab proxy otherwise 
    // nginx will be the client ip
    const clientIP = IPS.pop();
    if (clientIP == '127.0.0.1') {
        console.log(req.body)
        const UID = req.body.uid ? req.body.uid : undefined;
        const DATA = req.body.data ? req.body.data : undefined;
        if (UID && DATA) {
            const uid_exists = await client.exists(UID);
            if (uid_exists) {
                await client.set(UID, DATA);
                return res.json({ 'success': `Set the entry for ${UID} to "${DATA}"` });
            }
        }
        return res.json({ 'error': `Expected valid uid and data but got ${UID} and ${DATA}` })
    }
    res.status(403).json({ 'error': 'This is only reachable from within the network!' });
})

app.listen(PORT, () => {
    console.log(`Money making app (made by Patrick Star) listening on port ${PORT}`)
})