#!/usr/bin/env bash
#
# Copyright (c) Microsoft Corporation. All rights reserved.
#
realdir() {
	SOURCE=$1
	while [ -h "$SOURCE" ]; do
		DIR=$(dirname "$SOURCE")
		SOURCE=$(readlink "$SOURCE")
		[[ $SOURCE != /* ]] && SOURCE=$DIR/$SOURCE
	done
	echo "$( cd -P "$(dirname "$SOURCE")" >/dev/null 2>&1 && pwd )"
}

VSROOT="$(dirname "$(dirname "$(realdir "$0")")")"
ROOT="$(dirname "$(dirname "$VSROOT")")"

APP_NAME="code-server"
VERSION="1.89.0"
COMMIT="0f4791b816c184b612df3bdcfc4e1f9f1a13daca"
EXEC_NAME="code-server"
CLI_SCRIPT="$VSROOT/out/server-cli.js"
"${NODE_EXEC_PATH:-$ROOT/lib/node}" "$CLI_SCRIPT" "$APP_NAME" "$VERSION" "$COMMIT" "$EXEC_NAME" "$@"
