#!/bin/bash

mkdir -p $HOME/.config/code-server
echo >$HOME/.config/code-server/config.yaml
cat >> $HOME/.config/code-server/config.yaml <<EOF
auth: none
password: 123
cert: false
EOF

/var/young/code-server/bin/code-server --host=0.0.0.0 --port=${CODE_SERVER_PORT}
