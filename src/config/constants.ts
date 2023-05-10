const livisConfig:any = {
    "demo_config":{
        IMAGE_URL:["http://127.0.0.1:8000/livis/operators/get_redis_image/frame/"],
        CAMERA_SECTION:1,
        CAMERA_PARTITION:12,
        API_URL:"http://0.0.0.0:8000/livis/",
        API_CALLBACK_DURATION:1000,
    },
    "development": {
        BASE_URL:"http://localhost:8000/livis/v1/",
        W_BASE_URL:"http://127.0.0.1:8000/livis/",

    },
    "testing": {
        BASE_URL:"http://demo.livis.ai:8000/",
    },
    "staging": {
        BASE_URL:"http://demo.livis.ai:8000/",
    },
    "production": {
        BASE_URL:"http://127.0.0.1:8000/",
    }
}
export {livisConfig};