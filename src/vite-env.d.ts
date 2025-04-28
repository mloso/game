interface ImportMetaEnv {
    VITE_HTTP_URL: string;
    VITE_WEBSOCKET_URL: string;
}

interface ImportMeta {
    readonly env: ImportMetaEnv;
}
