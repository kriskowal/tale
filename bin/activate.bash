
if [ -z "${BASH_ARGV[0]}" ]; then

    # as a last recourse, use the present working directory
    PACKAGE_HOME=$(pwd)

else

    # get the absolute path of the executable
    SELF_PATH=$(
        cd -P -- "$(dirname -- "${BASH_ARGV[0]}")" \
        && pwd -P
    ) && SELF_PATH=$SELF_PATH/$(basename -- "${BASH_ARGV[0]}")

    # resolve symlinks
    while [ -h "$SELF_PATH" ]; do
        DIR=$(dirname -- "$SELF_PATH")
        SYM=$(readlink -- "$SELF_PATH")
        SELF_PATH=$(cd -- "$DIR" && cd -- $(dirname -- "$SYM") && pwd)/$(basename -- "$SYM")
    done

    PACKAGE_HOME=$(dirname -- "$(dirname -- "$SELF_PATH")")

fi

export PACKAGE_HOME

NODE_PATH="${PACKAGE_HOME}"/lib/js
NODE_PATH="${PACKAGE_HOME}"/packages/chiron/lib:"${NODE_PATH}"
NODE_PATH="${PACKAGE_HOME}"/packages/jaque/lib:"${NODE_PATH}"
NODE_PATH="${PACKAGE_HOME}"/packages/jack/lib:"${NODE_PATH}"
NODE_PATH="${PACKAGE_HOME}"/packages/narwhal-lib/lib:"${NODE_PATH}"
NODE_PATH="${PACKAGE_HOME}"/packages/node-narwhal/lib:"${NODE_PATH}"
export NODE_PATH

PATH="${PACKAGE_HOME}"/bin:"${PATH}"
export PATH

