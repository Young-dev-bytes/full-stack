"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.dispose = exports.ensureVSCodeLoaded = exports.wsRouter = exports.router = void 0;
const logger_1 = require("@coder/logger");
const crypto = __importStar(require("crypto"));
const express = __importStar(require("express"));
const fs_1 = require("fs");
const path = __importStar(require("path"));
const util_1 = require("../../common/util");
const cli_1 = require("../cli");
const constants_1 = require("../constants");
const http_1 = require("../http");
const socket_1 = require("../socket");
const util_2 = require("../util");
const wsRouter_1 = require("../wsRouter");
exports.router = express.Router();
exports.wsRouter = (0, wsRouter_1.Router)();
// The VS Code server is dynamically loaded in when a request is made to this
// router by `ensureCodeServerLoaded`.
let vscodeServer;
/**
 * Ensure the VS Code server is loaded.
 */
const ensureVSCodeLoaded = (req, _, next) => __awaiter(void 0, void 0, void 0, function* () {
    if (vscodeServer) {
        return next();
    }
    // See ../../../lib/vscode/src/vs/server/node/server.main.ts:72.
    const createVSServer = yield (0, util_2.loadAMDModule)("vs/server/node/server.main", "createServer");
    try {
        vscodeServer = yield createVSServer(null, Object.assign(Object.assign({}, (yield (0, cli_1.toCodeArgs)(req.args))), { "accept-server-license-terms": true, 
            // This seems to be used to make the connection token flags optional (when
            // set to 1.63) but we have always included them.
            compatibility: "1.64", "without-connection-token": true }));
    }
    catch (error) {
        (0, util_1.logError)(logger_1.logger, "CodeServerRouteWrapper", error);
        if (constants_1.isDevMode) {
            return next(new Error((error instanceof Error ? error.message : error) + " (VS Code may still be compiling)"));
        }
        return next(error);
    }
    return next();
});
exports.ensureVSCodeLoaded = ensureVSCodeLoaded;
exports.router.get("/", exports.ensureVSCodeLoaded, (req, res, next) => __awaiter(void 0, void 0, void 0, function* () {
    const isAuthenticated = yield (0, http_1.authenticated)(req);
    const NO_FOLDER_OR_WORKSPACE_QUERY = !req.query.folder && !req.query.workspace;
    // Ew means the workspace was closed so clear the last folder/workspace.
    const FOLDER_OR_WORKSPACE_WAS_CLOSED = req.query.ew;
    if (!isAuthenticated) {
        const to = (0, http_1.self)(req);
        return (0, http_1.redirect)(req, res, "login", {
            to: to !== "/" ? to : undefined,
        });
    }
    if (NO_FOLDER_OR_WORKSPACE_QUERY && !FOLDER_OR_WORKSPACE_WAS_CLOSED) {
        const settings = yield req.settings.read();
        const lastOpened = settings.query || {};
        // This flag disables the last opened behavior
        const IGNORE_LAST_OPENED = req.args["ignore-last-opened"];
        const HAS_LAST_OPENED_FOLDER_OR_WORKSPACE = lastOpened.folder || lastOpened.workspace;
        const HAS_FOLDER_OR_WORKSPACE_FROM_CLI = req.args._.length > 0;
        const to = (0, http_1.self)(req);
        let folder = undefined;
        let workspace = undefined;
        // Redirect to the last folder/workspace if nothing else is opened.
        if (HAS_LAST_OPENED_FOLDER_OR_WORKSPACE && !IGNORE_LAST_OPENED) {
            folder = lastOpened.folder;
            workspace = lastOpened.workspace;
        }
        else if (HAS_FOLDER_OR_WORKSPACE_FROM_CLI) {
            const lastEntry = path.resolve(req.args._[req.args._.length - 1]);
            const entryIsFile = yield (0, util_2.isFile)(lastEntry);
            const IS_WORKSPACE_FILE = entryIsFile && path.extname(lastEntry) === ".code-workspace";
            if (IS_WORKSPACE_FILE) {
                workspace = lastEntry;
            }
            else if (!entryIsFile) {
                folder = lastEntry;
            }
        }
        if (folder || workspace) {
            return (0, http_1.redirect)(req, res, to, {
                folder,
                workspace,
            });
        }
    }
    // Store the query parameters so we can use them on the next load.  This
    // also allows users to create functionality around query parameters.
    yield req.settings.write({ query: req.query });
    next();
}));
exports.router.get("/manifest.json", (req, res) => __awaiter(void 0, void 0, void 0, function* () {
    const appName = req.args["app-name"] || "code-server";
    res.writeHead(200, { "Content-Type": "application/manifest+json" });
    return res.end((0, http_1.replaceTemplates)(req, JSON.stringify({
        name: appName,
        short_name: appName,
        start_url: ".",
        display: "fullscreen",
        display_override: ["window-controls-overlay"],
        description: "Run Code on a remote server.",
        icons: [192, 512].map((size) => ({
            src: `{{BASE}}/_static/src/browser/media/pwa-icon-${size}.png`,
            type: "image/png",
            sizes: `${size}x${size}`,
        })),
    }, null, 2)));
}));
let mintKeyPromise;
exports.router.post("/mint-key", (req, res) => __awaiter(void 0, void 0, void 0, function* () {
    if (!mintKeyPromise) {
        mintKeyPromise = new Promise((resolve) => __awaiter(void 0, void 0, void 0, function* () {
            const keyPath = path.join(req.args["user-data-dir"], "serve-web-key-half");
            logger_1.logger.debug(`Reading server web key half from ${keyPath}`);
            try {
                resolve(yield fs_1.promises.readFile(keyPath));
                return;
            }
            catch (error) {
                if (error.code !== "ENOENT") {
                    (0, util_1.logError)(logger_1.logger, `read ${keyPath}`, error);
                }
            }
            // VS Code wants 256 bits.
            const key = crypto.randomBytes(32);
            try {
                yield fs_1.promises.writeFile(keyPath, key);
            }
            catch (error) {
                (0, util_1.logError)(logger_1.logger, `write ${keyPath}`, error);
            }
            resolve(key);
        }));
    }
    const key = yield mintKeyPromise;
    res.end(key);
}));
exports.router.all(/.*/, http_1.ensureAuthenticated, exports.ensureVSCodeLoaded, (req, res) => __awaiter(void 0, void 0, void 0, function* () {
    vscodeServer.handleRequest(req, res);
}));
const socketProxyProvider = new socket_1.SocketProxyProvider();
exports.wsRouter.ws(/.*/, http_1.ensureOrigin, http_1.ensureAuthenticated, exports.ensureVSCodeLoaded, (req) => __awaiter(void 0, void 0, void 0, function* () {
    const wrappedSocket = yield socketProxyProvider.createProxy(req.ws);
    // This should actually accept a duplex stream but it seems Code has not
    // been updated to match the Node 16 types so cast for now.  There does not
    // appear to be any code specific to sockets so this should be fine.
    vscodeServer.handleUpgrade(req, wrappedSocket);
    req.ws.resume();
}));
function dispose() {
    vscodeServer === null || vscodeServer === void 0 ? void 0 : vscodeServer.dispose();
    socketProxyProvider.stop();
}
exports.dispose = dispose;
//# sourceMappingURL=vscode.js.map