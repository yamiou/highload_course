# frontend-app

> A Vue.js project

## Build Setup

``` bash
# install dependencies
npm install

# serve with hot reload at localhost:8080
npm run dev

# build for production with minification
npm run build

# build for production and view the bundle analyzer report
npm run build --report

# run unit tests
npm run unit

# run e2e tests
npm run e2e

# run all tests
npm test
```

For detailed explanation on how things work, checkout the [guide](http://vuejs-templates.github.io/webpack/) and [docs for vue-loader](http://vuejs.github.io/vue-loader).

## Nginx site config
```
        # it assumes that content from dist/ after build placed into /var/nginx-www/highload
        # and htpasswd file is /etc/nginx/.htpasswd
        root   /var/nginx-www/highload;
        index  index.html index.htm;
        auth_basic "Auth needed";
        auth_basic_user_file /etc/nginx/.htpasswd;

        location / {
            try_files $uri $uri/ /index.html;
        }
```
